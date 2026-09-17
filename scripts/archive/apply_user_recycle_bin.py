import sys
sys.path.insert(0, r'd:\HiddenYatra')
from dotenv import load_dotenv
load_dotenv()
from models.places import soft_delete_place, get_deleted_places

for pid in [65, 70, 71, 72, 73]:
    soft_delete_place(pid, 'admin')

print("Soft-deleted 5 Jamui places to Recycle Bin:")
for p in get_deleted_places():
    print(f"  - ID {p['id']}: {p['name']} (deleted_at: {p['deleted_at']})")
