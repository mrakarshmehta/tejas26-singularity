"""
HiddenYatra — Ultimate AI Search Engine (Phase 2.5)
Production-grade intelligent search with:
  - Fuzzy matching (Levenshtein ≤ 2)
  - Phonetic matching (Soundex)
  - Hindi transliteration + Roman Hindi
  - Synonym expansion
  - Natural Language Intent parsing
  - Nearby/Geolocation search
  - Smart filters (category, district, family, fee, parking)
  - Multi-tier ranking (Exact > Prefix > Word > Partial > Synonym > Phonetic > Fuzzy > Popularity)
  - Search analytics tracking
  - LRU caching
  - Security hardening (query sanitization, length limits)

Zero external dependencies — pure Python implementation.
"""
import re
import math
import logging
import threading
import time
import unicodedata
from collections import OrderedDict, defaultdict
from datetime import datetime, timezone

from models.connection import get_db

logger = logging.getLogger(__name__)

# ════════════════════════════════════════════════════════════════
# 1. LEVENSHTEIN DISTANCE (Pure Python, optimized)
# ════════════════════════════════════════════════════════════════

def levenshtein_distance(s1, s2):
    """Compute Levenshtein edit distance between two strings.
    Optimized with early termination and single-row DP."""
    if s1 == s2:
        return 0
    len1, len2 = len(s1), len(s2)
    if len1 == 0:
        return len2
    if len2 == 0:
        return len1
    if abs(len1 - len2) > 3:
        return abs(len1 - len2)

    prev_row = list(range(len2 + 1))
    for i in range(len1):
        curr_row = [i + 1]
        c1 = s1[i]
        for j in range(len2):
            cost = 0 if c1 == s2[j] else 1
            curr_row.append(min(
                curr_row[j] + 1,
                prev_row[j + 1] + 1,
                prev_row[j] + cost
            ))
        prev_row = curr_row
    return prev_row[len2]


# ════════════════════════════════════════════════════════════════
# 2. PHONETIC MATCHING (Soundex — pure Python)
# ════════════════════════════════════════════════════════════════

_SOUNDEX_MAP = {
    'B': '1', 'F': '1', 'P': '1', 'V': '1',
    'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2', 'S': '2', 'X': '2', 'Z': '2',
    'D': '3', 'T': '3',
    'L': '4',
    'M': '5', 'N': '5',
    'R': '6',
}

def soundex(word):
    """Generate Soundex code for a word. Returns 4-char code like 'J500'."""
    if not word:
        return ''
    word = word.upper().strip()
    word = re.sub(r'[^A-Z]', '', word)
    if not word:
        return ''

    first = word[0]
    coded = [first]
    prev_code = _SOUNDEX_MAP.get(first, '0')

    for ch in word[1:]:
        code = _SOUNDEX_MAP.get(ch, '0')
        if code != '0' and code != prev_code:
            coded.append(code)
        prev_code = code if code != '0' else prev_code

    result = ''.join(coded)
    return (result + '0000')[:4]


# ════════════════════════════════════════════════════════════════
# 3. TEXT NORMALIZATION
# ════════════════════════════════════════════════════════════════

def normalize(text):
    """Normalize text for search matching."""
    if not text:
        return ''
    text = text.lower().strip()
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    text = text.replace('-', ' ').replace('_', ' ').replace('.', ' ')
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def normalize_compact(text):
    """Normalize and remove ALL spaces for tighter fuzzy matching."""
    return normalize(text).replace(' ', '')


def sanitize_query(query, max_len=200):
    """Sanitize user query for security. Strip dangerous chars, limit length."""
    if not query:
        return ''
    query = query.strip()[:max_len]
    # Remove null bytes and control characters
    query = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', query)
    # Remove SQL-like injection patterns (extra safety — we never use raw queries)
    query = re.sub(r'[;\'"\\]', '', query)
    return query.strip()


# ════════════════════════════════════════════════════════════════
# 4. HINDI TRANSLITERATION + ROMAN HINDI
# ════════════════════════════════════════════════════════════════

HINDI_TO_ENGLISH = {
    # Districts & Cities
    'जमुई': 'jamui', 'पटना': 'patna', 'गया': 'gaya',
    'नालंदा': 'nalanda', 'राजगीर': 'rajgir', 'वैशाली': 'vaishali',
    'मुजफ्फरपुर': 'muzaffarpur', 'भागलपुर': 'bhagalpur',
    'मुंगेर': 'munger', 'रोहतास': 'rohtas', 'मधुबनी': 'madhubani',
    'दरभंगा': 'darbhanga', 'सीतामढ़ी': 'sitamarhi',
    'पश्चिम चंपारण': 'west champaran', 'पूर्वी चंपारण': 'east champaran',
    'सारण': 'saran', 'सिवान': 'siwan', 'गोपालगंज': 'gopalganj',
    'नवादा': 'nawada', 'औरंगाबाद': 'aurangabad', 'जहानाबाद': 'jehanabad',
    'अरवल': 'arwal', 'लखीसराय': 'lakhisarai', 'शेखपुरा': 'sheikhpura',
    'बेगूसराय': 'begusarai', 'समस्तीपुर': 'samastipur',
    'खगड़िया': 'khagaria', 'कटिहार': 'katihar', 'पूर्णिया': 'purnia',
    'किशनगंज': 'kishanganj', 'अररिया': 'araria', 'सुपौल': 'supaul',
    'मधेपुरा': 'madhepura', 'सहरसा': 'saharsa', 'बांका': 'banka',
    'बक्सर': 'buxar', 'भोजपुर': 'bhojpur', 'कैमूर': 'kaimur',
    'शेओहर': 'sheohar', 'बिहार': 'bihar', 'बोधगया': 'bodh gaya',

    # Category words
    'मंदिर': 'temple', 'मस्जिद': 'mosque', 'गुरुद्वारा': 'gurudwara',
    'चर्च': 'church', 'मठ': 'monastery', 'पहाड़': 'hill',
    'पहाड़ी': 'hill', 'पर्वत': 'mountain', 'झरना': 'waterfall',
    'जलप्रपात': 'waterfall', 'झील': 'lake', 'तालाब': 'lake',
    'नदी': 'river', 'बांध': 'dam', 'जंगल': 'forest',
    'वन': 'forest', 'अभयारण्य': 'sanctuary', 'किला': 'fort',
    'गुफा': 'cave', 'बाग': 'garden', 'वाटिका': 'garden',
    'संग्रहालय': 'museum', 'पक्षी विहार': 'bird sanctuary',
    'चिड़ियाघर': 'zoo', 'ऐतिहासिक': 'historical',
    'प्राचीन': 'ancient', 'तीर्थ': 'pilgrimage', 'धाम': 'pilgrimage',

    # Place names
    'गिद्धेश्वर': 'giddheswar', 'पटनेश्वर': 'patneshwar',
    'गोलघर': 'golghar', 'महाबोधि': 'mahabodhi', 'विष्णुपद': 'vishnupad',
}

# Roman Hindi spelling variations → canonical English
ROMAN_HINDI_VARIANTS = {
    'gidheshwar': 'giddheswar', 'gidheshwar': 'giddheswar',
    'gidheswar': 'giddheswar', 'giddeshwar': 'giddheswar',
    'patneswar': 'patneshwar', 'patneshwer': 'patneshwar',
    'bodhgya': 'bodh gaya', 'bodhgaya': 'bodh gaya',
    'bodhgaia': 'bodh gaya', 'bodgaya': 'bodh gaya',
    'rajgirr': 'rajgir', 'rajgeer': 'rajgir', 'rajgr': 'rajgir',
    'jamuii': 'jamui', 'jamuih': 'jamui', 'jamue': 'jamui',
    'nalnda': 'nalanda', 'naalnda': 'nalanda',
    'golgar': 'golghar', 'golghaar': 'golghar',
    'vishunpad': 'vishnupad', 'vishnupaad': 'vishnupad',
    'mahabodi': 'mahabodhi', 'mahaboodhi': 'mahabodhi',
    'mandir': 'temple', 'masjid': 'mosque', 'jharna': 'waterfall',
    'pahar': 'hill', 'pahad': 'hill', 'parbat': 'mountain',
    'jheel': 'lake', 'talab': 'lake', 'jangal': 'forest',
    'kila': 'fort', 'qila': 'fort', 'gufa': 'cave',
    'bagh': 'garden', 'vatika': 'garden',
}

ENGLISH_TO_HINDI = {v: k for k, v in HINDI_TO_ENGLISH.items()}


def transliterate_hindi(text):
    """If text contains Hindi (Devanagari), convert to English equivalent."""
    if not text:
        return text, False
    has_hindi = any('\u0900' <= c <= '\u097F' for c in text)
    if not has_hindi:
        return text, False

    text_stripped = text.strip()
    if text_stripped in HINDI_TO_ENGLISH:
        return HINDI_TO_ENGLISH[text_stripped], True

    words = text_stripped.split()
    translated_words = []
    any_translated = False
    for word in words:
        if word in HINDI_TO_ENGLISH:
            translated_words.append(HINDI_TO_ENGLISH[word])
            any_translated = True
        else:
            translated_words.append(word)

    if any_translated:
        return ' '.join(translated_words), True
    return text, False


def resolve_roman_hindi(query_norm):
    """Check if query is a Roman Hindi variant and resolve to canonical form."""
    compact = query_norm.replace(' ', '')
    if compact in ROMAN_HINDI_VARIANTS:
        return ROMAN_HINDI_VARIANTS[compact]
    if query_norm in ROMAN_HINDI_VARIANTS:
        return ROMAN_HINDI_VARIANTS[query_norm]
    # Try word-level
    words = query_norm.split()
    resolved = []
    any_resolved = False
    for w in words:
        if w in ROMAN_HINDI_VARIANTS:
            resolved.append(ROMAN_HINDI_VARIANTS[w])
            any_resolved = True
        else:
            resolved.append(w)
    return ' '.join(resolved) if any_resolved else None


# ════════════════════════════════════════════════════════════════
# 5. SYNONYM DICTIONARY
# ════════════════════════════════════════════════════════════════

SYNONYM_GROUPS = [
    {'temple', 'mandir', 'devalaya'},
    {'mosque', 'masjid'},
    {'church', 'girja', 'cathedral'},
    {'gurudwara', 'gurdwara', 'sahib'},
    {'monastery', 'math', 'vihar', 'vihara'},
    {'waterfall', 'falls', 'jharna', 'jharana', 'jalprapat'},
    {'hill', 'mountain', 'pahar', 'pahad', 'parbat', 'parvat'},
    {'lake', 'talab', 'jheel', 'jhil', 'pond'},
    {'river', 'nadi'},
    {'dam', 'bandh', 'barrage', 'reservoir'},
    {'forest', 'jungle', 'van', 'ban'},
    {'sanctuary', 'abhayaranya', 'wildlife'},
    {'fort', 'kila', 'qila', 'garh', 'durg'},
    {'cave', 'gufa', 'gupha'},
    {'garden', 'bagh', 'vatika', 'park', 'udyan'},
    {'museum', 'sangrahalaya'},
    {'bird sanctuary', 'pakshi vihar'},
    {'zoo', 'chidiyaghar'},
    {'historical', 'heritage', 'aitihasik', 'ancient', 'prachin'},
    {'pilgrimage', 'tirth', 'dham', 'yatra'},
    {'tourist spot', 'tourist place', 'paryatan sthal'},
    {'picnic spot', 'picnic place'},
    {'viewpoint', 'view point', 'scenic point'},
    {'hotel', 'lodge', 'inn', 'dharamshala'},
    {'restaurant', 'dhaba', 'eatery', 'bhojanalaya'},
]

_SYNONYM_MAP = {}
for group in SYNONYM_GROUPS:
    for word in group:
        _SYNONYM_MAP[word] = group


def get_synonyms(word):
    """Get set of synonyms for a word (including the word itself)."""
    return _SYNONYM_MAP.get(word.lower(), {word.lower()})


def expand_query_with_synonyms(query):
    """Expand a query with synonym alternatives."""
    words = normalize(query).split()
    alternatives = {normalize(query)}
    for i, word in enumerate(words):
        syns = get_synonyms(word)
        for syn in syns:
            if syn != word:
                alt_words = words[:i] + [syn] + words[i+1:]
                alternatives.add(' '.join(alt_words))
    query_norm = normalize(query)
    for group in SYNONYM_GROUPS:
        for phrase in group:
            if phrase in query_norm:
                for replacement in group:
                    if replacement != phrase:
                        alternatives.add(query_norm.replace(phrase, replacement))
    return list(alternatives)


# ════════════════════════════════════════════════════════════════
# 6. NATURAL LANGUAGE INTENT PARSER
# ════════════════════════════════════════════════════════════════

# Patterns for NL queries like "best temple in jamui", "waterfall near me"
_NL_PATTERNS = [
    # "best/top/famous <category> in <location>"
    (r'(?:best|top|famous|popular)\s+(\w+)\s+(?:in|of|at|near)\s+(.+)', 'category_in_location'),
    # "<category> near me" / "near me <category>"
    (r'(.+?)\s+near\s+me$', 'near_me'),
    (r'^near\s+me\s+(.+)', 'near_me'),
    # "<category> in <location>"
    (r'(.+?)\s+(?:in|of|at)\s+(.+)', 'category_in_location'),
    # "<category> near <location>"
    (r'(.+?)\s+near\s+(.+)', 'near_location'),
    # "places to visit in <season>"
    (r'(?:places?|things?)\s+to\s+(?:visit|see|explore)\s+(?:in\s+)?(.+)', 'season_or_location'),
    # "family friendly" / "family picnic"
    (r'family\s+(?:friendly|picnic|outing|trip)', 'family_friendly'),
    # "free entry" / "no fee"
    (r'(?:free\s+entry|no\s+fee|free\s+places?)', 'free_entry'),
]
_NL_COMPILED = [(re.compile(p, re.IGNORECASE), intent) for p, intent in _NL_PATTERNS]

# Category keyword → place category code mapping
_CATEGORY_KEYWORDS = {
    'temple': 'temple', 'mandir': 'temple', 'religious': 'temple',
    'mosque': 'temple', 'gurudwara': 'temple', 'church': 'temple',
    'historical': 'historical', 'heritage': 'historical', 'monument': 'historical',
    'ancient': 'historical', 'fort': 'historical', 'museum': 'historical',
    'waterfall': 'waterfall', 'falls': 'waterfall', 'jharna': 'waterfall',
    'hill': 'mountain', 'mountain': 'mountain', 'pahar': 'mountain',
    'lake': 'lake', 'river': 'lake', 'pond': 'lake',
    'nature': 'nature', 'wildlife': 'nature', 'sanctuary': 'nature',
    'forest': 'nature', 'bird': 'nature', 'jungle': 'nature',
    'food': 'food_place', 'restaurant': 'food_place', 'dhaba': 'food_place',
    'market': 'market', 'shopping': 'market',
    'adventure': 'adventure', 'sport': 'adventure', 'trekking': 'adventure',
    'cultural': 'cultural', 'festival': 'cultural',
    'beach': 'beach',
    'hidden': 'hidden_gem', 'gem': 'hidden_gem', 'offbeat': 'hidden_gem',
    'picnic': 'tourist_spot', 'park': 'tourist_spot', 'garden': 'tourist_spot',
}

# Season keywords
_SEASON_KEYWORDS = {
    'winter': 'October to February',
    'summer': 'March to May',
    'monsoon': 'June to September',
    'rainy': 'June to September',
    'spring': 'February to April',
    'autumn': 'September to November',
}


class NLIntent:
    """Parsed natural language search intent."""
    __slots__ = ('raw_query', 'intent_type', 'category_filter', 'location_filter',
                 'near_me', 'family_friendly', 'free_entry', 'season',
                 'radius_km', 'effective_query')

    def __init__(self, raw_query):
        self.raw_query = raw_query
        self.intent_type = 'keyword'  # default
        self.category_filter = None
        self.location_filter = None
        self.near_me = False
        self.family_friendly = False
        self.free_entry = False
        self.season = None
        self.radius_km = None
        self.effective_query = raw_query

    def __repr__(self):
        return f'NLIntent({self.intent_type}, cat={self.category_filter}, loc={self.location_filter}, near={self.near_me})'


def parse_nl_intent(query):
    """Parse natural language query into structured intent."""
    intent = NLIntent(query)
    q_lower = query.lower().strip()

    # Check for "near me"
    if 'near me' in q_lower:
        intent.near_me = True
        intent.intent_type = 'near_me'
        clean = re.sub(r'\s*near\s+me\s*', ' ', q_lower).strip()
        # Check if the remaining part is a category keyword
        for word in clean.split():
            if word in _CATEGORY_KEYWORDS:
                intent.category_filter = _CATEGORY_KEYWORDS[word]
                break
        intent.effective_query = clean if clean else query

    # Check for "within X km"
    radius_match = re.search(r'within\s+(\d+)\s*(?:km|kilometer)', q_lower)
    if radius_match:
        intent.radius_km = int(radius_match.group(1))
        intent.near_me = True
        q_lower = re.sub(r'within\s+\d+\s*(?:km|kilometer)', '', q_lower).strip()
        intent.effective_query = q_lower

    # Check family friendly
    if re.search(r'family\s+(?:friendly|picnic|outing|trip)', q_lower):
        intent.family_friendly = True
        intent.intent_type = 'filter'

    # Check free entry
    if re.search(r'(?:free\s+entry|no\s+fee|free\s+places?)', q_lower):
        intent.free_entry = True
        intent.intent_type = 'filter'

    # Try NL patterns
    for pattern, intent_type in _NL_COMPILED:
        m = pattern.search(q_lower)
        if m:
            groups = m.groups()
            if intent_type == 'category_in_location' and len(groups) >= 2:
                cat_str = groups[0].strip()
                loc_str = groups[1].strip()
                for word in cat_str.split():
                    if word in _CATEGORY_KEYWORDS:
                        intent.category_filter = _CATEGORY_KEYWORDS[word]
                        break
                intent.location_filter = loc_str
                intent.intent_type = 'nl'
                intent.effective_query = f"{cat_str} {loc_str}"
            elif intent_type == 'near_location' and len(groups) >= 2:
                cat_str = groups[0].strip()
                loc_str = groups[1].strip()
                for word in cat_str.split():
                    if word in _CATEGORY_KEYWORDS:
                        intent.category_filter = _CATEGORY_KEYWORDS[word]
                        break
                intent.location_filter = loc_str
                intent.intent_type = 'nl'
                intent.effective_query = f"{cat_str} {loc_str}"
            elif intent_type == 'season_or_location' and len(groups) >= 1:
                val = groups[0].strip()
                if val in _SEASON_KEYWORDS:
                    intent.season = _SEASON_KEYWORDS[val]
                    intent.intent_type = 'season'
                else:
                    intent.location_filter = val
                    intent.intent_type = 'nl'
                intent.effective_query = val
            break

    # Check for season keywords in remaining query
    if not intent.season:
        for kw, season_val in _SEASON_KEYWORDS.items():
            if kw in q_lower:
                intent.season = season_val

    return intent


# ════════════════════════════════════════════════════════════════
# 7. GEOLOCATION UTILITIES
# ════════════════════════════════════════════════════════════════

def haversine_km(lat1, lon1, lat2, lon2):
    """Calculate distance in km between two lat/lng points using Haversine formula."""
    R = 6371.0  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# ════════════════════════════════════════════════════════════════
# 8. CATEGORY & EMOJI MAPPING
# ════════════════════════════════════════════════════════════════

CATEGORY_EMOJI = {
    'tourist_spot': '📸', 'temple': '🛕', 'food_place': '🍽️',
    'hidden_gem': '💎', 'nature': '🌿', 'historical': '🏛️',
    'beach': '🏖️', 'mountain': '⛰️', 'market': '🛍️',
    'adventure': '🧗', 'cultural': '🎭', 'waterfall': '💧',
    'lake': '🌊', 'other': '📌',
}

CATEGORY_LABELS = {
    'tourist_spot': 'Tourist Spot', 'temple': 'Temple / Religious',
    'food_place': 'Food Place', 'hidden_gem': 'Hidden Gem',
    'nature': 'Nature / Wildlife', 'historical': 'Historical Monument',
    'beach': 'Beach', 'mountain': 'Hills & Mountains',
    'market': 'Market / Shopping', 'adventure': 'Adventure / Sport',
    'cultural': 'Cultural Site', 'waterfall': 'Waterfall',
    'lake': 'Lake / River', 'other': 'Other',
}

TYPE_EMOJI = {
    'place': '📍', 'district': '🗺️', 'state': '🏛️',
    'block': '🏘️', 'service': '🏨', 'food': '🍛',
}


# ════════════════════════════════════════════════════════════════
# 9. SEARCH ANALYTICS TRACKER
# ════════════════════════════════════════════════════════════════

class SearchAnalytics:
    """Thread-safe in-memory search analytics tracker."""

    def __init__(self, max_entries=5000):
        self._lock = threading.RLock()
        self._queries = []          # [(timestamp, query, result_count, ms)]
        self._query_counts = defaultdict(int)   # query → count
        self._failed_queries = defaultdict(int)  # query → count (0 results)
        self._category_counts = defaultdict(int)  # category → click count
        self._max = max_entries

    def log_search(self, query, result_count, response_ms):
        """Log a search event."""
        with self._lock:
            now = datetime.now(timezone.utc)
            self._queries.append((now, query, result_count, response_ms))
            if len(self._queries) > self._max:
                self._queries = self._queries[-self._max:]
            q_norm = normalize(query)
            if q_norm:
                self._query_counts[q_norm] += 1
                if result_count == 0:
                    self._failed_queries[q_norm] += 1

    def log_category_click(self, category):
        """Log a category filter click."""
        with self._lock:
            self._category_counts[category] += 1

    def get_trending_queries(self, limit=10):
        """Return most searched queries."""
        with self._lock:
            sorted_q = sorted(self._query_counts.items(), key=lambda x: -x[1])
            return sorted_q[:limit]

    def get_failed_queries(self, limit=10):
        """Return queries with 0 results (for admin diagnostics)."""
        with self._lock:
            sorted_f = sorted(self._failed_queries.items(), key=lambda x: -x[1])
            return sorted_f[:limit]

    def get_popular_categories(self, limit=10):
        """Return most clicked categories."""
        with self._lock:
            sorted_c = sorted(self._category_counts.items(), key=lambda x: -x[1])
            return sorted_c[:limit]

    def get_stats(self):
        """Return summary stats for admin dashboard."""
        with self._lock:
            total = len(self._queries)
            failed = sum(1 for _, _, rc, _ in self._queries if rc == 0)
            avg_ms = sum(ms for _, _, _, ms in self._queries) / max(total, 1)
            return {
                'total_searches': total,
                'failed_searches': failed,
                'avg_response_ms': round(avg_ms, 2),
                'unique_queries': len(self._query_counts),
                'trending': self.get_trending_queries(5),
                'failed_top': self.get_failed_queries(5),
            }


# Global analytics singleton
_analytics = SearchAnalytics()

def get_search_analytics():
    """Get the global search analytics instance."""
    return _analytics


# ════════════════════════════════════════════════════════════════
# 10. SEARCH INDEX (Enhanced)
# ════════════════════════════════════════════════════════════════

class SearchEntry:
    """Single searchable entry in the index."""
    __slots__ = (
        'id', 'entry_type', 'name', 'slug', 'url', 'category',
        'district_name', 'state_name', 'cover_image', 'keywords',
        'name_norm', 'name_compact', 'name_soundex', 'is_featured',
        'view_count', 'extra', 'latitude', 'longitude',
        'family_friendly', 'entry_fee', 'parking_info',
        'best_time_to_visit', 'avg_rating', 'review_count',
    )

    def __init__(self, id, entry_type, name, slug, url, category='',
                 district_name='', state_name='', cover_image='',
                 keywords=None, is_featured=False, view_count=0, extra=None,
                 latitude=None, longitude=None, family_friendly=False,
                 entry_fee='', parking_info='', best_time_to_visit='',
                 avg_rating=0.0, review_count=0):
        self.id = id
        self.entry_type = entry_type
        self.name = name
        self.slug = slug
        self.url = url
        self.category = category
        self.district_name = district_name
        self.state_name = state_name
        self.cover_image = cover_image or ''
        self.keywords = keywords or []
        self.name_norm = normalize(name)
        self.name_compact = normalize_compact(name)
        # Generate Soundex codes for each word
        self.name_soundex = [soundex(w) for w in name.split() if w.isalpha()]
        self.is_featured = is_featured
        self.view_count = view_count or 0
        self.extra = extra or {}
        self.latitude = float(latitude) if latitude else None
        self.longitude = float(longitude) if longitude else None
        self.family_friendly = bool(family_friendly)
        self.entry_fee = entry_fee or ''
        self.parking_info = parking_info or ''
        self.best_time_to_visit = best_time_to_visit or ''
        self.avg_rating = float(avg_rating) if avg_rating else 0.0
        self.review_count = int(review_count) if review_count else 0

    @property
    def is_free(self):
        """Check if entry is free (no fee or 'Free')."""
        fee = self.entry_fee.lower().strip()
        return not fee or fee == 'free' or 'free' in fee

    @property
    def has_parking(self):
        """Check if parking info suggests parking is available."""
        p = self.parking_info.lower()
        return bool(p) and 'no parking' not in p and 'not available' not in p


class SearchIndex:
    """In-memory search index with NL parsing, fuzzy/phonetic matching,
    nearby search, smart filters, and multi-tier ranking."""

    def __init__(self):
        self._entries = []
        self._lock = threading.Lock()
        self._built = False
        self._cache = OrderedDict()
        self._cache_max = 512
        # Inverted indexes for fast filtered lookups
        self._by_category = defaultdict(list)
        self._by_district = defaultdict(list)
        self._districts_list = []  # unique district names
        self._categories_list = []  # unique category codes

    @property
    def size(self):
        return len(self._entries)

    def build(self):
        """Build the search index from MySQL database."""
        logger.info("Building search index...")
        entries = []
        conn = get_db()
        try:
            cur = conn.cursor()

            # ── PLACES ── (enhanced: lat/lng, family, fee, parking, ratings)
            cur.execute("""
                SELECT p.id, p.name, p.slug, p.category, p.cover_image,
                       p.is_featured, p.view_count, p.description,
                       p.nearest_railway, p.nearest_bus_stand,
                       p.latitude, p.longitude, p.family_friendly,
                       p.entry_fee, p.parking_info, p.best_time_to_visit,
                       s.name AS state_name, d.name AS district_name,
                       COALESCE(AVG(r.rating), 0) AS avg_rating,
                       COUNT(r.id) AS review_count
                FROM places p
                JOIN states s ON s.id = p.state_id
                LEFT JOIN districts d ON d.id = p.district_id
                LEFT JOIN reviews r ON r.place_id = p.id
                WHERE p.deleted_at IS NULL
                GROUP BY p.id
            """)
            for row in cur.fetchall():
                keywords = []
                if row['description']:
                    desc_words = set(normalize(row['description']).split())
                    keywords.extend(w for w in desc_words if len(w) >= 4)
                if row['category']:
                    keywords.append(row['category'].replace('_', ' '))
                    cat_syns = get_synonyms(row['category'].replace('_', ' '))
                    keywords.extend(cat_syns)

                entries.append(SearchEntry(
                    id=row['id'], entry_type='place',
                    name=row['name'], slug=row['slug'],
                    url=f"/place/{row['slug']}",
                    category=row['category'] or '',
                    district_name=row['district_name'] or '',
                    state_name=row['state_name'] or '',
                    cover_image=row['cover_image'] or '',
                    keywords=keywords,
                    is_featured=bool(row['is_featured']),
                    view_count=row['view_count'] or 0,
                    latitude=row['latitude'], longitude=row['longitude'],
                    family_friendly=row['family_friendly'],
                    entry_fee=row['entry_fee'] or '',
                    parking_info=row['parking_info'] or '',
                    best_time_to_visit=row['best_time_to_visit'] or '',
                    avg_rating=row['avg_rating'],
                    review_count=row['review_count'],
                ))

            # ── DISTRICTS ──
            cur.execute("""
                SELECT d.id, d.name, d.slug, d.cover_image, d.famous_for,
                       d.is_featured, s.name AS state_name, s.slug AS state_slug,
                       COUNT(DISTINCT p.id) AS place_count
                FROM districts d
                JOIN states s ON s.id = d.state_id
                LEFT JOIN places p ON p.district_id = d.id AND p.deleted_at IS NULL
                GROUP BY d.id
            """)
            for row in cur.fetchall():
                keywords = []
                if row['famous_for']:
                    keywords.extend(normalize(row['famous_for']).split())
                entries.append(SearchEntry(
                    id=row['id'], entry_type='district',
                    name=row['name'], slug=row['slug'],
                    url=f"/state/{row['state_slug']}/{row['slug']}",
                    category='district',
                    district_name=row['name'],
                    state_name=row['state_name'] or '',
                    cover_image=row['cover_image'] or '',
                    keywords=keywords,
                    is_featured=bool(row.get('is_featured', False)),
                    extra={'place_count': row.get('place_count', 0)},
                ))

            # ── STATES ──
            cur.execute("SELECT id, name, slug FROM states")
            for row in cur.fetchall():
                entries.append(SearchEntry(
                    id=row['id'], entry_type='state',
                    name=row['name'], slug=row['slug'],
                    url=f"/state/{row['slug']}",
                    category='state', state_name=row['name'],
                ))

            # ── BLOCKS ──
            cur.execute("""
                SELECT b.id, b.name, b.slug,
                       d.name AS district_name, d.slug AS district_slug,
                       s.name AS state_name, s.slug AS state_slug
                FROM blocks b
                JOIN districts d ON d.id = b.district_id
                JOIN states s ON s.id = d.state_id
            """)
            for row in cur.fetchall():
                entries.append(SearchEntry(
                    id=row['id'], entry_type='block',
                    name=row['name'], slug=row['slug'],
                    url=f"/state/{row['state_slug']}/{row['district_slug']}/{row['slug']}",
                    category='block',
                    district_name=row['district_name'] or '',
                    state_name=row['state_name'] or '',
                ))

            # ── NEARBY SERVICES ──
            cur.execute("""
                SELECT ns.id, ns.name, ns.service_type, ns.address,
                       ns.latitude, ns.longitude,
                       d.name AS district_name
                FROM nearby_services ns
                LEFT JOIN districts d ON d.id = ns.district_id
                WHERE ns.is_active = 1
            """)
            for row in cur.fetchall():
                entries.append(SearchEntry(
                    id=row['id'], entry_type='service',
                    name=row['name'], slug='', url='',
                    category=row['service_type'] or '',
                    district_name=row['district_name'] or '',
                    keywords=[row['service_type'] or '', row['address'] or ''],
                    latitude=row['latitude'], longitude=row['longitude'],
                ))

            # ── FOODS ──
            cur.execute("""
                SELECT df.id, df.name, df.description,
                       d.name AS district_name, d.slug AS district_slug,
                       s.slug AS state_slug
                FROM district_foods df
                JOIN districts d ON d.id = df.district_id
                JOIN states s ON s.id = d.state_id
            """)
            for row in cur.fetchall():
                entries.append(SearchEntry(
                    id=row['id'], entry_type='food',
                    name=row['name'], slug='',
                    url=f"/food-culture",
                    category='food',
                    district_name=row['district_name'] or '',
                    keywords=[normalize(row['description'] or '')[:200]],
                ))

            cur.close()
        finally:
            conn.close()

        # Build inverted indexes
        by_cat = defaultdict(list)
        by_dist = defaultdict(list)
        for entry in entries:
            if entry.category:
                by_cat[entry.category].append(entry)
            if entry.district_name:
                by_dist[normalize(entry.district_name)].append(entry)

        with self._lock:
            self._entries = entries
            self._by_category = by_cat
            self._by_district = by_dist
            self._districts_list = sorted(set(
                e.district_name for e in entries if e.district_name
            ))
            self._categories_list = sorted(set(
                e.category for e in entries if e.category and e.entry_type == 'place'
            ))
            self._cache.clear()
            self._built = True

        logger.info(f"Search index built: {len(entries)} entries "
                    f"({len(by_cat)} categories, {len(by_dist)} districts)")

    def _get_cached(self, key):
        if key in self._cache:
            self._cache.move_to_end(key)
            return self._cache[key]
        return None

    def _set_cached(self, key, value):
        self._cache[key] = value
        self._cache.move_to_end(key)
        while len(self._cache) > self._cache_max:
            self._cache.popitem(last=False)

    # ── MAIN SEARCH ──────────────────────────────────────────

    def search(self, query, limit=12, filters=None, user_lat=None, user_lng=None):
        """Main search function with NL parsing, filters, nearby, and multi-tier ranking.

        Args:
            query: Search text
            limit: Max results
            filters: dict with optional keys: category, district, family_friendly,
                     free_entry, has_parking, radius_km
            user_lat, user_lng: User's geolocation for nearby search
        """
        if not query or not query.strip():
            return []

        if not self._built:
            self.build()

        # Security: sanitize
        query = sanitize_query(query)
        if not query:
            return []

        # Parse NL intent
        intent = parse_nl_intent(query)

        # Merge intent filters with explicit filters
        filters = filters or {}
        if intent.category_filter and not filters.get('category'):
            filters['category'] = intent.category_filter
        if intent.location_filter and not filters.get('district'):
            filters['district'] = intent.location_filter
        if intent.family_friendly:
            filters['family_friendly'] = True
        if intent.free_entry:
            filters['free_entry'] = True
        if intent.near_me:
            filters['near_me'] = True
        if intent.radius_km and not filters.get('radius_km'):
            filters['radius_km'] = intent.radius_km

        # Transliterate Hindi
        query_original = intent.effective_query.strip()
        query_translated, was_hindi = transliterate_hindi(query_original)
        query_str = query_translated if was_hindi else query_original

        # Resolve Roman Hindi variants
        roman_resolved = resolve_roman_hindi(normalize(query_str))
        if roman_resolved:
            query_str = roman_resolved

        query_norm = normalize(query_str)
        query_compact = normalize_compact(query_str)
        query_soundex = [soundex(w) for w in query_str.split() if w.isalpha()]

        if not query_norm:
            return []

        # Check cache (include filters in cache key)
        filter_key = str(sorted(filters.items())) if filters else ''
        geo_key = f"{user_lat:.4f},{user_lng:.4f}" if user_lat and user_lng else ''
        cache_key = f"{query_norm}|{filter_key}|{geo_key}"
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached[:limit]

        # Expand with synonyms
        synonym_queries = expand_query_with_synonyms(query_str)

        scored_results = []

        for entry in self._entries:
            # ── APPLY FILTERS ──
            if not self._passes_filters(entry, filters, user_lat, user_lng):
                continue

            best_score = 0
            match_type = ''

            # ── TIER 1: Exact name match (100) ──
            if entry.name_norm == query_norm:
                best_score = 100
                match_type = 'exact'

            # ── TIER 2: Prefix match (90) ──
            elif entry.name_norm.startswith(query_norm):
                best_score = 90
                match_type = 'prefix'

            # ── TIER 3: Word-start match (75) ──
            elif not match_type:
                name_words = entry.name_norm.split()
                if any(w.startswith(query_norm) for w in name_words):
                    best_score = 75
                    match_type = 'word_start'

            # ── TIER 4: Contains match (60) ──
            if not match_type and query_norm in entry.name_norm:
                best_score = 60
                match_type = 'contains'

            # ── TIER 5: Compact contains (55) ──
            if not match_type and len(query_compact) >= 3 and query_compact in entry.name_compact:
                best_score = 55
                match_type = 'contains'

            # ── TIER 6: Synonym match (45) ──
            if not match_type:
                for alt_q in synonym_queries:
                    alt_norm = normalize(alt_q)
                    if alt_norm == query_norm:
                        continue
                    if alt_norm in entry.name_norm or entry.name_norm.startswith(alt_norm):
                        best_score = max(best_score, 45)
                        match_type = 'synonym'
                        break
                    for kw in entry.keywords:
                        kw_norm = normalize(kw)
                        if alt_norm in kw_norm or kw_norm.startswith(alt_norm):
                            best_score = max(best_score, 15)
                            match_type = 'keyword'
                            break
                    if match_type:
                        break

            # ── TIER 7: Phonetic / Soundex match (35) ──
            if not match_type and query_soundex:
                for qs in query_soundex:
                    if qs and qs in entry.name_soundex:
                        best_score = max(best_score, 35)
                        match_type = 'phonetic'
                        break

            # ── TIER 8: Fuzzy match (25-40) ──
            if not match_type and len(query_norm) >= 3:
                dist = levenshtein_distance(query_compact, entry.name_compact)
                max_dist = 1 if len(query_compact) <= 5 else 2
                if dist <= max_dist:
                    best_score = 40 if dist == 1 else 25
                    match_type = 'fuzzy'
                else:
                    for word in entry.name_norm.split():
                        word_c = word.replace(' ', '')
                        if len(word_c) >= 3:
                            wd = levenshtein_distance(query_compact, word_c)
                            if wd <= max_dist:
                                best_score = max(best_score, 35 if wd == 1 else 20)
                                match_type = 'fuzzy'
                                break

            # ── TIER 9: District/state name match (50) ──
            if not match_type:
                if entry.district_name and query_norm in normalize(entry.district_name):
                    best_score = 50
                    match_type = 'district'
                elif entry.state_name and query_norm in normalize(entry.state_name):
                    best_score = 45
                    match_type = 'state'

            # ── BONUS SCORING ──
            if best_score > 0:
                if entry.is_featured:
                    best_score += 5
                if entry.view_count > 100:
                    best_score += 3
                elif entry.view_count > 50:
                    best_score += 2
                elif entry.view_count > 10:
                    best_score += 1
                if entry.avg_rating >= 4.0:
                    best_score += 3
                elif entry.avg_rating >= 3.0:
                    best_score += 1

                type_bonus = {'place': 3, 'district': 2, 'state': 2, 'food': 1, 'block': 0, 'service': 0}
                best_score += type_bonus.get(entry.entry_type, 0)

                scored_results.append((best_score, match_type, entry))

        # Sort by score descending, then name
        scored_results.sort(key=lambda x: (-x[0], x[2].name))

        # Build result dicts
        results = []
        for score, match_type, entry in scored_results[:limit]:
            highlighted = highlight_match(entry.name, query_str)

            result = {
                'id': entry.id,
                'type': entry.entry_type,
                'name': entry.name,
                'slug': entry.slug,
                'url': entry.url,
                'category': entry.category,
                'category_label': CATEGORY_LABELS.get(
                    entry.category,
                    entry.category.replace('_', ' ').title() if entry.category else ''
                ),
                'category_emoji': CATEGORY_EMOJI.get(
                    entry.category, TYPE_EMOJI.get(entry.entry_type, '📍')
                ),
                'district_name': entry.district_name,
                'state_name': entry.state_name,
                'cover_image': entry.cover_image,
                'score': score,
                'match_type': match_type,
                'highlighted_name': highlighted,
                'extra': entry.extra,
                'latitude': entry.latitude,
                'longitude': entry.longitude,
                'family_friendly': entry.family_friendly,
                'entry_fee': entry.entry_fee,
                'avg_rating': entry.avg_rating,
                'review_count': entry.review_count,
            }

            # Add distance if user location provided
            if user_lat and user_lng and entry.latitude and entry.longitude:
                dist_km = haversine_km(user_lat, user_lng, entry.latitude, entry.longitude)
                result['distance_km'] = round(dist_km, 1)

            results.append(result)

        # If nearby search, re-sort by distance
        if filters.get('near_me') and user_lat and user_lng:
            results.sort(key=lambda r: r.get('distance_km', 99999))

        self._set_cached(cache_key, results)
        if seq_id is not None:
            for r in results:
                r['seq_id'] = seq_id
        return results[:limit]

    def _passes_filters(self, entry, filters, user_lat=None, user_lng=None):
        """Check if entry passes all active filters."""
        if not filters:
            return True

        # Category filter
        cat = filters.get('category')
        if cat:
            cat_norm = normalize(cat.replace('_', ' '))
            entry_cat_norm = normalize(entry.category)
            filter_syns = get_synonyms(cat_norm)
            if entry.category != cat and entry_cat_norm != cat_norm and entry_cat_norm not in filter_syns:
                return False

        # District filter
        dist = filters.get('district')
        if dist:
            dist_norm = normalize(dist)
            if dist_norm not in normalize(entry.district_name) and dist_norm not in normalize(entry.state_name):
                return False

        # Family friendly
        if filters.get('family_friendly') and not entry.family_friendly:
            return False

        # Free entry
        if filters.get('free_entry') and not entry.is_free:
            return False

        # Parking
        if filters.get('has_parking') and not entry.has_parking:
            return False

        # Radius (geofence)
        radius = filters.get('radius_km')
        if radius and user_lat and user_lng:
            if entry.latitude and entry.longitude:
                d = haversine_km(user_lat, user_lng, entry.latitude, entry.longitude)
                if d > radius:
                    return False
            else:
                return False  # No coordinates → can't determine distance

        return True

    def get_popular_searches(self, limit=6):
        """Return popular/trending places for empty search state."""
        if not self._built:
            self.build()
        popular = [e for e in self._entries
                   if e.entry_type == 'place' and (e.is_featured or e.view_count > 0)]
        popular.sort(key=lambda e: (-int(e.is_featured), -e.view_count))
        results = []
        for entry in popular[:limit]:
            results.append({
                'id': entry.id, 'type': entry.entry_type,
                'name': entry.name, 'slug': entry.slug, 'url': entry.url,
                'category': entry.category,
                'category_emoji': CATEGORY_EMOJI.get(entry.category, '📍'),
                'category_label': CATEGORY_LABELS.get(entry.category, ''),
                'district_name': entry.district_name,
                'cover_image': entry.cover_image,
            })
        return results

    def get_nearby(self, lat, lng, radius_km=25, limit=20, category=None):
        """Get places near a coordinate, sorted by distance."""
        if not self._built:
            self.build()
        nearby = []
        for e in self._entries:
            if not e.latitude or not e.longitude:
                continue
            if e.entry_type not in ('place', 'service'):
                continue
            if category and e.category != category:
                continue
            d = haversine_km(lat, lng, e.latitude, e.longitude)
            if d <= radius_km:
                nearby.append((d, e))
        nearby.sort(key=lambda x: x[0])
        results = []
        for dist_km, entry in nearby[:limit]:
            results.append({
                'id': entry.id, 'type': entry.entry_type,
                'name': entry.name, 'slug': entry.slug, 'url': entry.url,
                'category': entry.category,
                'category_emoji': CATEGORY_EMOJI.get(entry.category, TYPE_EMOJI.get(entry.entry_type, '📍')),
                'category_label': CATEGORY_LABELS.get(entry.category, ''),
                'district_name': entry.district_name,
                'cover_image': entry.cover_image,
                'distance_km': round(dist_km, 1),
                'latitude': entry.latitude, 'longitude': entry.longitude,
            })
        return results

    def get_filter_options(self):
        """Return available filter options for the UI."""
        return {
            'categories': [
                {'code': c, 'label': CATEGORY_LABELS.get(c, c), 'emoji': CATEGORY_EMOJI.get(c, '📌')}
                for c in self._categories_list if c in CATEGORY_LABELS
            ],
            'districts': self._districts_list,
        }


# ════════════════════════════════════════════════════════════════
# 11. HIGHLIGHT MATCH
# ════════════════════════════════════════════════════════════════

def highlight_match(name, query):
    """Highlight the matching portion with <mark> tags."""
    if not query or not name:
        return name
    query_norm = normalize(query)
    name_lower = name.lower()

    idx = name_lower.find(query_norm)
    if idx >= 0:
        return (name[:idx] + '<mark>' + name[idx:idx + len(query_norm)] + '</mark>' +
                name[idx + len(query_norm):])

    query_compact = query_norm.replace(' ', '').replace('-', '')
    name_compact_lower = name_lower.replace(' ', '').replace('-', '')
    idx_c = name_compact_lower.find(query_compact)
    if idx_c >= 0:
        orig_idx = 0
        compact_count = 0
        start_idx = None
        end_idx = None
        for i, ch in enumerate(name):
            if ch not in (' ', '-'):
                if compact_count == idx_c and start_idx is None:
                    start_idx = i
                compact_count += 1
                if compact_count == idx_c + len(query_compact):
                    end_idx = i + 1
                    break
        if start_idx is not None and end_idx is not None:
            return (name[:start_idx] + '<mark>' + name[start_idx:end_idx] + '</mark>' +
                    name[end_idx:])

    query_words = query_norm.split()
    result = name
    for qw in query_words:
        if len(qw) >= 2:
            pattern = re.compile(re.escape(qw), re.IGNORECASE)
            result = pattern.sub(lambda m: f'<mark>{m.group()}</mark>', result, count=1)
    return result


# ════════════════════════════════════════════════════════════════
# 12. GLOBAL SINGLETON & PUBLIC API
# ════════════════════════════════════════════════════════════════

_index = None
_index_lock = threading.Lock()


def get_search_index():
    """Get or create the global search index singleton."""
    global _index
    if _index is None:
        with _index_lock:
            if _index is None:
                _index = SearchIndex()
    return _index


def rebuild_search_index():
    """Rebuild the search index (call after CRUD operations)."""
    idx = get_search_index()
    idx.build()
    return idx.size


def instant_search(query, limit=12, filters=None, user_lat=None, user_lng=None):
    """Public API: perform instant search with optional filters and geolocation."""
    t0 = time.perf_counter()
    idx = get_search_index()
    results = idx.search(query, limit=limit, filters=filters,
                         user_lat=user_lat, user_lng=user_lng)
    elapsed_ms = (time.perf_counter() - t0) * 1000
    _analytics.log_search(query, len(results), elapsed_ms)
    return results


def get_search_suggestions(limit=6):
    """Public API: get popular/trending suggestions for empty search."""
    idx = get_search_index()
    return idx.get_popular_searches(limit=limit)


def nearby_search(lat, lng, radius_km=25, limit=20, category=None):
    """Public API: get places near a coordinate."""
    idx = get_search_index()
    return idx.get_nearby(lat, lng, radius_km=radius_km, limit=limit, category=category)


def get_filter_options():
    """Public API: get available filter options for UI."""
    idx = get_search_index()
    if not idx._built:
        idx.build()
    return idx.get_filter_options()
