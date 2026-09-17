"""
Forensic Image & Slug Shift Map Generator
Inspect the original seed slug shift to trace every district_X_hash.png file to its true district identity.
"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.stdout.reconfigure(encoding='utf-8')

# Read original backup audit dump to get original district ID and slug when images were generated
with open(r"D:\HiddenYatra\scratch\audit_dump.json", "r", encoding="utf-8") as f:
    dump = json.load(f)

# When images were generated, they were named district_{id}_{hash}.png
# where {id} was the row ID that had that district's SLUG at the time!
# Let's map original row's slug -> original image file.

slug_to_image = {}
for d in dump['districts']:
    orig_slug = d['slug']
    orig_img = d['cover_image']
    if orig_slug and orig_img:
        slug_to_image[orig_slug] = orig_img

print("Original Slug -> Image File Map:")
for slug, img in sorted(slug_to_image.items()):
    print(f"  {slug:25s} -> {img}")

# Now, each canonical district currently has canonical slug = slugify(name).
# So canonical district with slug S should have cover_image = slug_to_image[S]!
