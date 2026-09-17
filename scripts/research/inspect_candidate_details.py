import sys
import os
import csv
import math
sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv()
from models.connection import get_cursor

sys.stdout.reconfigure(encoding='utf-8')

# Let's inspect the remaining top candidates from PHASE6_TOP30_FACTCHECK.md
with open('PHASE6_TOP30_FACTCHECK.md', mode='r', encoding='utf-8') as f:
    factcheck_md = f.read()

# Let's search for candidate sections #16, #19, #21, #22, #27
for c_num in [16, 19, 21, 22, 27]:
    header = f"### Candidate #{c_num}"
    pos = factcheck_md.find(header)
    if pos != -1:
        end_pos = factcheck_md.find("### Candidate #", pos + len(header))
        if end_pos == -1:
            end_pos = factcheck_md.find("## 3.", pos)
        section = factcheck_md[pos:end_pos].strip()
        print(f"==================================================")
        print(section)
        print(f"==================================================\n")

