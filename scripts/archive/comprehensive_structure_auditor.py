import os
import sys
import re
import csv
import json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = Path(r"D:\HiddenYatra")

IGNORE_DIRS = {
    '.git',
    'node_modules',
    '.venv',
    'venv',
    'env',
    '__pycache__',
    '.pytest_cache',
    'mysql_data',
    'mysql_data_BACKUP_20260808'
}

IGNORE_FILES = {
    'Thumbs.db',
    '.DS_Store'
}

print(f"Executing Comprehensive Structure Auditor on {ROOT_DIR}...")

# 1. Collect all files
files_db = []
for root, dirs, files in os.walk(ROOT_DIR):
    dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.endswith('.egg-info')]
    for f in files:
        if f in IGNORE_FILES or f.endswith('.pyc'):
            continue
        full_p = Path(root) / f
        try:
            rel_p = str(full_p.relative_to(ROOT_DIR)).replace('\\', '/')
        except ValueError:
            rel_p = str(full_p).replace('\\', '/')
        size = full_p.stat().st_size
        ext = full_p.suffix.lower()
        files_db.append({
            'full_path': str(full_p),
            'rel_path': rel_p,
            'filename': f,
            'ext': ext,
            'size': size,
            'dir': str(Path(rel_p).parent).replace('\\', '/') if str(Path(rel_p).parent) != '.' else ''
        })

print(f"Total files indexed: {len(files_db)}")

# 2. Build quick text index of all files for reference searching
# (For small-to-medium text files, load content to scan for references)
text_contents = {}
binary_exts = {'.png', '.jpg', '.jpeg', '.webp', '.svg', '.ico', '.pptx', '.bin', '.gz', '.tar', '.zip'}

for item in files_db:
    rel_p = item['rel_path']
    if item['ext'] not in binary_exts and item['size'] < 1_500_000:
        try:
            with open(item['full_path'], 'r', encoding='utf-8', errors='ignore') as fh:
                text_contents[rel_p] = fh.read()
        except Exception:
            pass

print(f"Indexed text contents of {len(text_contents)} files for reference scanning.")

# 3. Categorization logic
def categorize_file(item):
    rel = item['rel_path']
    f = item['filename']
    ext = item['ext']
    
    # Check directory and filename patterns
    if rel.startswith('static/css/'):
        return 'D. CSS', 'Client-side styling stylesheet'
    if rel.startswith('static/js/map/') or rel == 'static/js/map.js' or rel == 'static/js/map.min.js' or rel.startswith('static/data/terrain/') or rel.startswith('static/data/bihar/'):
        return 'F. MAP / GIS', 'GIS mapping engine, spatial layers, or terrain mesh'
    if rel.startswith('static/js/'):
        return 'E. JAVASCRIPT', 'Client-side JavaScript logic/bundle'
    if rel.startswith('static/uploads/') or rel.startswith('static/hero/') or ext in {'.png', '.jpg', '.jpeg', '.webp', '.svg', '.ico'} or 'screenshot' in f.lower() or 'evidence' in rel.lower():
        return 'G. IMAGES / MEDIA', 'Visual media, icon, screenshot, or banner asset'
    if rel.startswith('templates/'):
        return 'C. UI / TEMPLATES', 'Jinja2 HTML view template'
    if rel.startswith('routes/'):
        return 'B. BACKEND', 'Flask Blueprint route handler / API controller'
    if rel.startswith('models/'):
        return 'B. BACKEND', 'Backend data model, database schema, or business engine'
    if rel.startswith('utils/'):
        return 'B. BACKEND', 'Backend utility functions and helpers'
    if rel.startswith('tests/'):
        return 'J. TESTS', 'Automated unit, integration, or regression test'
    if rel.startswith('deploy/') or rel in {'Dockerfile', 'docker-compose.yml', 'render.yaml', 'gunicorn.conf.py', 'wsgi.py'}:
        return 'N. DEPLOYMENT', 'Production deployment, container, or server configuration'
    if rel in {'app.py', 'config.py', 'requirements.txt', '.env', '.env.example', '.env.production.example', '.gitignore', '.dockerignore', 'my.ini'}:
        return 'M. CONFIGURATION', 'Core application or environment configuration'
    if ext == '.sql':
        return 'H. DATABASE', 'SQL database schema, migration, or backup dump'
    if ext == '.csv':
        if 'audit' in f.lower() or 'preview' in f.lower() or 'status' in f.lower():
            return 'O. GENERATED REPORTS', 'Audit, fact-check, or candidate review CSV report'
        return 'I. DATA / SEED', 'Tabular data or candidate queue CSV'
    if rel.startswith('scripts/seed/') or 'seed' in f.lower():
        return 'I. DATA / SEED', 'Database seeding script or sample data generator'
    if rel.startswith('scripts/migrations/'):
        return 'H. DATABASE', 'Database migration or schema patch script'
    if rel.startswith('docs/') or f in {'README.md', 'CHANGELOG.md', 'INSTALL.md', 'API_DOCUMENTATION.md', 'DEPLOYMENT.md'}:
        return 'L. DOCUMENTATION', 'Project architecture, installation, or user documentation'
    if ext in {'.md', '.txt'}:
        if 'report' in f.lower() or 'audit' in f.lower() or 'log' in f.lower() or 'review' in f.lower() or 'preview' in f.lower() or 'analysis' in f.lower() or 'plan' in f.lower() or 'changelog' in f.lower() or 'smells' in f.lower():
            return 'O. GENERATED REPORTS', 'Historical audit, phase log, or regression report markdown'
        return 'L. DOCUMENTATION', 'Documentation or notes markdown'
    if rel.startswith('scratch/'):
        if f.startswith('test_') or 'tester' in f:
            return 'J. TESTS', 'Ad-hoc verification or scratch test script'
        if 'audit' in f or 'inspect' in f or 'check' in f:
            return 'K. DEVELOPMENT SCRIPTS', 'Development inspection or diagnostic script'
        if 'insert' in f or 'seed' in f or 'populate' in f or 'db' in f:
            return 'K. DEVELOPMENT SCRIPTS', 'Database insertion, repair, or migration helper'
        if ext == '.json':
            return 'P. TEMPORARY / DEBUG', 'Temporary diagnostic dump or test report JSON'
        return 'K. DEVELOPMENT SCRIPTS', 'Development script or scratch automation'
    if rel.startswith('scripts/'):
        return 'K. DEVELOPMENT SCRIPTS', 'Development tooling or operational maintenance script'
    if ext == '.pptx':
        return 'L. DOCUMENTATION', 'Project presentation pitch deck'
    return 'Q. UNKNOWN / MANUAL REVIEW', 'Unclassified file requiring manual inspection'

# 4. Safe to move logic
def evaluate_safe_to_move(item, category):
    rel = item['rel_path']
    f = item['filename']
    
    # Root critical files that MUST stay in place
    root_must_stay = {
        'app.py', 'config.py', 'requirements.txt', '.env', '.env.example',
        'Dockerfile', 'docker-compose.yml', 'render.yaml', 'gunicorn.conf.py',
        'wsgi.py', '.gitignore', '.dockerignore', 'README.md'
    }
    if rel in root_must_stay:
        return 'NO (MUST REMAIN IN ROOT)', 'Essential entry point, container, or environment config'
    
    # Core backend modules that Flask / routes import
    if rel.startswith('models/') or rel.startswith('routes/') or rel.startswith('utils/'):
        return 'REVIEW (HIGH-RISK)', 'Core Python module; moving requires updating all relative and absolute imports'
    
    # Templates
    if rel.startswith('templates/'):
        return 'REVIEW (MEDIUM-RISK)', 'Flask Jinja template; moving requires updating render_template() and {% extends %} paths'
    
    # Static CSS and JS
    if rel.startswith('static/css/') or rel.startswith('static/js/'):
        return 'REVIEW (MEDIUM-RISK)', 'Static asset; moving requires updating url_for("static") and template references'
    
    # GIS data
    if rel.startswith('static/data/'):
        return 'REVIEW (HIGH-RISK)', 'GIS GeoJSON or 3D terrain tile; hardcoded paths in map-google-terrain.js and map-layers.js'
    
    # Tests
    if rel.startswith('tests/'):
        return 'REVIEW (LOW-RISK)', 'Test suite file; safe if pytest discovery root is configured'
    
    # Deployment configs in deploy/
    if rel.startswith('deploy/'):
        return 'NO (KEEP IN deploy/)', 'Production Nginx/systemd configs reference fixed paths'
    
    # Batch artifacts in root
    if ('BATCH' in f or 'PHASE' in f or 'JEHANABAD' in f or 'BIHAR_' in f) and f.endswith(('.csv', '.md')):
        return 'YES (SAFE TO MOVE)', 'Historical research/batch report artifact; safe to move to docs/batches/ or data/research/'
    
    # Root documentation reports
    if rel.count('/') == 0 and f.endswith('.md'):
        return 'YES (SAFE TO MOVE)', 'Audit or documentation markdown; safe to move to docs/'
    
    # Root SQL dumps
    if rel.count('/') == 0 and f.endswith('.sql'):
        return 'YES (SAFE TO MOVE)', 'Database backup dump; safe to move to data/backups/ or archive/'
    
    # Scratch directory
    if rel.startswith('scratch/'):
        return 'YES (SAFE TO MOVE)', 'Scratch/debug script or test artifact; safe to move to scripts/ or archive/'
    
    # UIUX evidence
    if rel.startswith('uiux_'):
        return 'YES (SAFE TO MOVE)', 'UI/UX visual proof artifact; safe to move to docs/evidence/'
    
    return 'REVIEW', 'Manual review recommended'

# Apply categorization and safety analysis
for item in files_db:
    cat, purpose = categorize_file(item)
    item['category'] = cat
    item['purpose'] = purpose
    safe, move_reason = evaluate_safe_to_move(item, cat)
    item['safe_to_move'] = safe
    item['move_reason'] = move_reason
    item['is_temp'] = 'YES' if (cat in {'P. TEMPORARY / DEBUG', 'O. GENERATED REPORTS'} or 'scratch' in item['rel_path'] or 'backup' in item['filename'].lower() or item['filename'].endswith('.log')) else 'NO'

print("Categorization and safety analysis complete.")

# 5. Secret scanning (REPORT SECRET_PRESENT = YES / NO ONLY, NEVER PRINT SECRET)
secret_patterns = [
    re.compile(r'(password|passwd|secret|api_key|apikey|jwt_secret|private_key)\s*[:=]\s*["\']?([^"\'\s]{6,})["\']?', re.IGNORECASE)
]
secret_findings = {}
for rel, content in text_contents.items():
    has_sec = False
    for pat in secret_patterns:
        m = pat.search(content)
        if m:
            val = m.group(2).lower()
            # filter out placeholders
            if val not in {'root', 'password', 'your_secret_key', 'your-secret-key', 'none', 'false', 'true', 'test', 'dev', 'dummy'}:
                has_sec = True
                break
    if has_sec or rel == '.env':
        secret_findings[rel] = 'YES'
    else:
        secret_findings[rel] = 'NO'

print("Secret audit complete.")

# 6. Summary counts by Category
category_counts = {}
for item in files_db:
    c = item['category']
    category_counts[c] = category_counts.get(c, 0) + 1

print("\n--- Category Breakdown ---")
for c, cnt in sorted(category_counts.items()):
    print(f"  {c:30s}: {cnt} files")
