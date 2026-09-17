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

print(f"Starting Project Structure Audit for {ROOT_DIR}...")

all_files = []

for root, dirs, files in os.walk(ROOT_DIR):
    # filter out ignored directories
    dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.endswith('.egg-info')]
    
    for f in files:
        if f in IGNORE_FILES or f.endswith('.pyc'):
            continue
        full_p = Path(root) / f
        try:
            rel_p = full_p.relative_to(ROOT_DIR)
        except ValueError:
            rel_p = full_p
        size = full_p.stat().st_size
        ext = full_p.suffix.lower()
        all_files.append({
            'full_path': str(full_p),
            'rel_path': str(rel_p).replace('\\', '/'),
            'filename': f,
            'ext': ext,
            'size': size,
            'dir': str(rel_p.parent).replace('\\', '/') if str(rel_p.parent) != '.' else ''
        })

print(f"Total relevant files collected: {len(all_files)}")

# Group by directory to see high-level distribution
dir_counts = {}
for f in all_files:
    top_dir = f['rel_path'].split('/')[0] if '/' in f['rel_path'] else '[ROOT]'
    dir_counts[top_dir] = dir_counts.get(top_dir, 0) + 1

for d, cnt in sorted(dir_counts.items(), key=lambda x: -x[1]):
    print(f"  {d:35s}: {cnt} files")
