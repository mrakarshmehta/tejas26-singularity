"""
HiddenYatra — Multi-Worker Rate Limiter
Provides Redis-backed sliding window rate limiter, MySQL database table fallback
(ate_limit_attempts), and resilient in-memory fallback for offline/testing environments.
"""
import time
import logging
from config import REDIS_URL, RATE_LIMIT_BACKEND

logger = logging.getLogger(__name__)

# Redis client singleton
_redis_client = None
_redis_initialized = False


def _get_redis_client():
    """Get or initialize Redis client if REDIS_URL is configured."""
    global _redis_client, _redis_initialized
    if not _redis_initialized:
        _redis_initialized = True
        if REDIS_URL:
            try:
                import redis
                _redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
                _redis_client.ping()
                logger.info("Connected to Redis for multi-worker rate limiting.")
            except Exception as e:
                logger.warning("Failed to connect to Redis (%s); falling back to DB/Memory rate limiter.", e)
                _redis_client = None
    return _redis_client


_db_table_checked = False


def _ensure_rate_limit_table(cur):
    """Ensure ate_limit_attempts table exists in MySQL."""
    global _db_table_checked
    if not _db_table_checked:
        try:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS rate_limit_attempts (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    store_name VARCHAR(64) NOT NULL,
                    client_ip VARCHAR(64) NOT NULL,
                    attempt_time DOUBLE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_rate_lookup (store_name, client_ip, attempt_time)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)
            _db_table_checked = True
        except Exception as e:
            logger.debug("Table check warning: %s", e)


class RateLimitStore:
    """Multi-worker rate limit store supporting dict-like operations and multi-backend synchronization."""

    def __init__(self, name):
        self.name = name
        self._local = {}

    def get(self, key, default=None):
        return self._local.get(key, default if default is not None else [])

    def pop(self, key, default=None):
        res = self._local.pop(key, default)
        # Clear from Redis if active
        r = _get_redis_client()
        if r:
            try:
                r.delete(f"rate_limit:{self.name}:{key}")
            except Exception:
                pass
        # Clear from DB if active
        try:
            from models.connection import get_cursor
            with get_cursor(commit=True) as cur:
                _ensure_rate_limit_table(cur)
                cur.execute(
                    "DELETE FROM rate_limit_attempts WHERE store_name = %s AND client_ip = %s",
                    (self.name, key)
                )
        except Exception:
            pass
        return res

    def clear(self):
        self._local.clear()

    def __getitem__(self, key):
        return self._local[key]

    def __setitem__(self, key, value):
        self._local[key] = value

    def __len__(self):
        return len(self._local)


def _rate_check(store, ip, max_attempts=5, window=60):
    """Returns True if rate limited (exceeded max_attempts within window seconds)."""
    store_name = getattr(store, 'name', 'default') if not isinstance(store, str) else store
    now = time.time()
    cutoff = now - window

    # 1. Try Redis Backend
    r = _get_redis_client()
    if r:
        try:
            key = f"rate_limit:{store_name}:{ip}"
            pipe = r.pipeline()
            pipe.zremrangebyscore(key, 0, cutoff)
            pipe.zcard(key)
            pipe.expire(key, window + 10)
            res = pipe.execute()
            count = res[1]
            return count >= max_attempts
        except Exception as e:
            logger.warning("Redis rate_check failed (%s), falling back to DB/Memory.", e)

    # 2. Try MySQL DB Table Backend
    try:
        from models.connection import get_cursor
        with get_cursor(commit=True) as cur:
            _ensure_rate_limit_table(cur)
            # Periodic prune of old attempts
            if int(now) % 50 == 0:
                cur.execute("DELETE FROM rate_limit_attempts WHERE attempt_time < %s", (now - 3600,))
            cur.execute(
                "SELECT COUNT(*) AS cnt FROM rate_limit_attempts WHERE store_name = %s AND client_ip = %s AND attempt_time > %s",
                (store_name, ip, cutoff)
            )
            row = cur.fetchone()
            if row and row['cnt'] >= max_attempts:
                return True
            return False
    except Exception:
        pass

    # 3. In-memory local fallback
    local_dict = store._local if hasattr(store, '_local') else store
    if isinstance(local_dict, dict):
        attempts = [t for t in local_dict.get(ip, []) if now - t < window]
        local_dict[ip] = attempts
        if len(local_dict) > 500:
            local_dict.clear()
            return False
        return len(attempts) >= max_attempts

    return False


def _rate_record(store, ip):
    """Record a new attempt for the given store and client IP."""
    store_name = getattr(store, 'name', 'default') if not isinstance(store, str) else store
    now = time.time()

    # 1. Try Redis Backend
    r = _get_redis_client()
    if r:
        try:
            key = f"rate_limit:{store_name}:{ip}"
            pipe = r.pipeline()
            pipe.zadd(key, {str(now): now})
            pipe.expire(key, 3600)
            pipe.execute()
        except Exception as e:
            logger.warning("Redis rate_record failed (%s), falling back to DB/Memory.", e)

    # 2. Try MySQL DB Table Backend
    try:
        from models.connection import get_cursor
        with get_cursor(commit=True) as cur:
            _ensure_rate_limit_table(cur)
            cur.execute(
                "INSERT INTO rate_limit_attempts (store_name, client_ip, attempt_time) VALUES (%s, %s, %s)",
                (store_name, ip, now)
            )
    except Exception:
        pass

    # 3. Update local dict for local consistency
    local_dict = store._local if hasattr(store, '_local') else store
    if isinstance(local_dict, dict):
        attempts = local_dict.get(ip, [])
        attempts.append(now)
        local_dict[ip] = attempts