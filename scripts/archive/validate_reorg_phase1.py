import os
import sys
import re
import csv
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

print(f"Starting Reorganization Phase 1 Validation on {ROOT_DIR}...")

# 1. Collect all project text files
text_files = {}
all_files = []

for root, dirs, files in os.walk(ROOT_DIR):
    dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.endswith('.egg-info')]
    for f in files:
        if f in {'Thumbs.db', '.DS_Store'} or f.endswith('.pyc'):
            continue
        fp = Path(root) / f
        rel = str(fp.relative_to(ROOT_DIR)).replace('\\', '/')
        all_files.append(rel)
        if fp.stat().st_size < 2_000_000 and fp.suffix.lower() not in {'.png', '.jpg', '.jpeg', '.webp', '.svg', '.ico', '.pptx', '.bin', '.gz'}:
            try:
                with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                    text_files[rel] = fh.read()
            except Exception:
                pass

print(f"Indexed {len(all_files)} total files, {len(text_files)} text files loaded.")

# 2. Check for any cross-references to scratch/
print("\n=== Scanning for scratch references across codebase ===")
scratch_import_patterns = [
    re.compile(r'from\s+scratch(?:\.|\s+import)', re.IGNORECASE),
    re.compile(r'import\s+scratch(?:\.|\s+)', re.IGNORECASE),
    re.compile(r'scratch[/\\][\w\.-]+', re.IGNORECASE)
]

scratch_refs = {}
for rel, content in text_files.items():
    for pat in scratch_import_patterns:
        matches = pat.findall(content)
        if matches:
            scratch_refs.setdefault(rel, []).extend(matches)

print(f"Files referencing scratch/ ({len(scratch_refs)} files):")
for ref_file, m_list in sorted(scratch_refs.items()):
    # distinct matches
    distinct_m = list(set(m_list))[:5]
    print(f"  {ref_file:45s}: {distinct_m}")

# 3. Check for root CSV and Markdown references
print("\n=== Scanning for root CSV/MD references in python code ===")
root_csv_refs = {}
root_md_refs = {}

for rel, content in text_files.items():
    if rel.endswith('.py'):
        for m in re.findall(r'[\'"]([A-Za-z0-9_-]+\.(?:csv|md|sql))[\'"]', content):
            if m.endswith('.csv'):
                root_csv_refs.setdefault(m, []).append(rel)
            elif m.endswith('.md'):
                root_md_refs.setdefault(m, []).append(rel)

print(f"Root CSVs referenced in Python code ({len(root_csv_refs)}):")
for csv_name, callers in sorted(root_csv_refs.items()):
    print(f"  {csv_name:40s} referenced in: {callers[:3]}")

# 4. Check for root SQL references
root_sql_refs = {}
for rel, content in text_files.items():
    if rel.endswith(('.py', '.sh', '.bat', '.ps1', '.yml', '.yaml')):
        for m in re.findall(r'[\'"]?([A-Za-z0-9_-]+\.sql)[\'"]?', content):
            root_sql_refs.setdefault(m, []).append(rel)

print(f"\nRoot SQL files referenced ({len(root_sql_refs)}):")
for sql_name, callers in sorted(root_sql_refs.items()):
    print(f"  {sql_name:40s} referenced in: {callers[:3]}")
