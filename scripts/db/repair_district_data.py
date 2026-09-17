"""
HiddenYatra Data Integrity Repair Script
=========================================
- Runs inside a SINGLE MySQL transaction
- Fixes district slugs, place/block/food/service district_id foreign keys
- Rolls back on ANY error
- Verifies correctness before committing

READ THE PLAN BEFORE RUNNING:
  Step 1: Fix district slugs (temp rename → final rename to avoid unique constraint conflicts)
  Step 2: Fix places.district_id
  Step 3: Fix blocks.district_id
  Step 4: Fix district_foods.district_id
  Step 5: Fix nearby_services.district_id
  Step 6: Fix host_listings.district_id
  Step 7: Delete orphan place ID 44
  Step 8: Delete duplicate district ID 39
  Step 9: Verify all fixes
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.stdout.reconfigure(encoding='utf-8')
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'))
import pymysql

DB_CONFIG = {
    'host': os.getenv('DB_HOST', '127.0.0.1'),
    'port': int(os.getenv('DB_PORT', '3307')),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'hiddenyatra'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
    'autocommit': False,
}

# ═══════════════════════════════════════════════════════════════
# CANONICAL DISTRICT SLUG MAP (ID → correct slug based on name)
# ═══════════════════════════════════════════════════════════════
DISTRICT_SLUG_FIXES = {
    # ID: correct_slug (derived from slugify(current_name))
    3:  'nalanda',
    4:  'jamui',
    5:  'bhagalpur',
    6:  'munger',
    7:  'muzaffarpur',
    8:  'rohtas',
    9:  'west-champaran',
    10: 'east-champaran',
    11: 'araria',
    12: 'arwal',
    13: 'aurangabad',
    14: 'banka',
    15: 'begusarai',
    16: 'bhojpur',
    17: 'buxar',
    18: 'darbhanga',
    19: 'gopalganj',
    20: 'jhanjharpur-madhubani',
    21: 'jehanabad',
    22: 'kaimur',
    23: 'katihar',
    24: 'khagaria',
    25: 'kishanganj',
    26: 'lakhisarai',
    27: 'madhepura',
    28: 'purnia',
    29: 'saharsa',
    30: 'samastipur',
    31: 'saran',
    32: 'sheikhpura',
    33: 'sheohar',
    34: 'sitamarhi',
    35: 'siwan',
    36: 'supaul',
    37: 'vaishali',
    38: 'nawada',
}

# ═══════════════════════════════════════════════════════════════
# PLACE → CORRECT DISTRICT ID (by geographic identity)
# Key = place_id, Value = correct district_id
# ═══════════════════════════════════════════════════════════════
PLACE_DISTRICT_FIXES = {
    # Old seed_bihar.py places (IDs 1-28)
    2: 2,    # Mahabodhi Temple → Gaya
    3: 3,    # Nalanda University Ruins (old dup) → Nalanda
    4: 4,    # Simultala Waterfall → Jamui
    5: 2,    # Barabar Caves → Gaya
    6: 38,   # Kakolat Waterfall → Nawada
    7: 2,    # Great Buddha Statue, Bodh Gaya → Gaya
    8: 3,    # Nalanda University Ruins → Nalanda
    9: 3,    # Rajgir (Rajagriha) → Nalanda
    10: 37,  # Vaishali - Birthplace of Democracy → Vaishali
    11: 5,   # Vikramshila University Ruins → Bhagalpur
    12: 5,   # Mandar Hill → Bhagalpur (original seed intent)
    13: 20,  # Madhubani Art Village (Jitwarpur) → Jhanjharpur (Madhubani)
    14: 8,   # Sher Shah Suri Tomb, Sasaram → Rohtas
    15: 8,   # Rohtasgarh Fort → Rohtas
    16: 38,  # Kakolat Waterfall (dup) → Nawada
    17: 9,   # Valmiki National Park → West Champaran
    18: 10,  # Kesariya Stupa → East Champaran
    19: 6,   # Munger Fort → Munger
    20: 15,  # Kanwar Lake Bird Sanctuary → Begusarai
    21: 6,   # Bhimbandh Hot Springs → Munger
    22: 13,  # Deo Sun Temple → Aurangabad
    23: 17,  # Battle of Buxar Memorial → Buxar
    24: 22,  # Mundeshwari Temple → Kaimur
    25: 34,  # Janaki Sthan Temple → Sitamarhi
    26: 18,  # Darbhanga Raj (Laxmi Vilas Palace) → Darbhanga
    27: 7,   # Litchi Gardens & Jubba Sahni Park → Muzaffarpur
    28: 16,  # Veer Kunwar Singh Fort, Jagdishpur → Bhojpur

    # seed_jamui_places.py places (IDs 57-73) → ALL go to Jamui (4)
    57: 4, 58: 4, 59: 4, 60: 4, 61: 4, 62: 4, 63: 4, 64: 4,
    65: 4, 66: 4, 67: 4, 68: 4, 69: 4, 70: 4, 71: 4, 72: 4, 73: 4,

    # seed_bihar_complete.py Gaya/Bodh Gaya places (IDs 102-112) → Gaya (2)
    102: 2, 103: 2, 104: 2, 105: 2, 106: 2, 107: 2,
    108: 2, 109: 2, 110: 2, 111: 2, 112: 2,
}
# Places 1, 88-101 are at district_id=1 (Patna) already — no change needed.

# ═══════════════════════════════════════════════════════════════
# BLOCK → CORRECT DISTRICT ID
# ═══════════════════════════════════════════════════════════════
BLOCK_DISTRICT_FIXES = {}
# Nalanda blocks (Bihar Sharif, Rajgir, Silao...) currently at DID 4 → move to 3
for bid in range(20, 26):
    BLOCK_DISTRICT_FIXES[bid] = 3
# Bhagalpur blocks (Bhagalpur, Sultanganj...) currently at DID 7 → move to 5
for bid in range(26, 32):
    BLOCK_DISTRICT_FIXES[bid] = 5
# Vaishali blocks (Hajipur, Vaishali...) currently at DID 5 → move to 37
for bid in range(32, 38):
    BLOCK_DISTRICT_FIXES[bid] = 37
# Muzaffarpur blocks (Mushahari, Kanti...) currently at DID 6 → move to 7
for bid in range(38, 44):
    BLOCK_DISTRICT_FIXES[bid] = 7
# Madhubani blocks (Madhubani, Jainagar...) currently at DID 10 → move to 20
for bid in range(44, 50):
    BLOCK_DISTRICT_FIXES[bid] = 20
# Rohtas blocks (Sasaram, Dehri...) currently at DID 9 → move to 8
for bid in range(50, 57):
    BLOCK_DISTRICT_FIXES[bid] = 8
# Munger blocks (Munger, Jamalpur...) currently at DID 8 → move to 6
for bid in range(57, 61):
    BLOCK_DISTRICT_FIXES[bid] = 6
# Jamui blocks (Jamui Sadar, Gidhaur...) currently at DID 22 → move to 4
for bid in range(61, 71):
    BLOCK_DISTRICT_FIXES[bid] = 4
# Gaya blocks currently at DID 3 → move to 2 (we'll query for exact IDs)

# ═══════════════════════════════════════════════════════════════
# FOOD → CORRECT DISTRICT ID
# ═══════════════════════════════════════════════════════════════
FOOD_DISTRICT_FIXES = {
    9:  2,   # Tilkut → Gaya
    10: 2,   # Thekua → Gaya
    11: 3,   # Khaja → Nalanda (Silao, Nalanda)
    18: 37,  # Chura-Dahi → Vaishali
    12: 7,   # Shahi Litchi → Muzaffarpur
    13: 5,   # Katarni Chawal → Bhagalpur
    14: 5,   # Bhagalpuri Tussar Silk → Bhagalpur
    17: 8,   # Sattu Paratha → Rohtas
    15: 20,  # Makhana → Jhanjharpur (Madhubani)
    16: 20,  # Dahi Chura → Jhanjharpur (Madhubani)
    20: 18,  # Jhilli → Darbhanga
    21: 18,  # Bari-Kadhi → Darbhanga
    19: 9,   # Champaran Meat → West Champaran
}

# ═══════════════════════════════════════════════════════════════
# HOST LISTING → CORRECT DISTRICT ID
# ═══════════════════════════════════════════════════════════════
HOST_LISTING_FIXES = {
    10: 3,  # Free Village Stay (Near Rajgir) → Nalanda
}


def run_repair():
    conn = pymysql.connect(**DB_CONFIG)
    cur = conn.cursor()
    changes = {'districts': 0, 'places': 0, 'blocks': 0, 'foods': 0,
               'services': 0, 'host_listings': 0, 'orphan_deleted': 0, 'dup_deleted': 0}

    try:
        print("=" * 70)
        print("STARTING TRANSACTIONAL REPAIR")
        print("=" * 70)

        # ─── STEP 0: Delete duplicate district ID 39 first ─────
        # Must happen before slug fixes because ID 33 (Sheohar) needs slug='sheohar'
        # but ID 39 (duplicate Sheohar) already has slug='sheohar'
        print("\n── STEP 0: Deleting duplicate district (ID 39) ──")
        cur.execute("SELECT id, name, slug FROM districts WHERE id = 39")
        dup = cur.fetchone()
        if dup and dup['name'] == 'Sheohar':
            cur.execute("SELECT COUNT(*) AS c FROM places WHERE district_id = 39")
            places_39 = cur.fetchone()['c']
            cur.execute("SELECT COUNT(*) AS c FROM blocks WHERE district_id = 39")
            blocks_39 = cur.fetchone()['c']
            if places_39 == 0 and blocks_39 == 0:
                cur.execute("DELETE FROM districts WHERE id = 39")
                changes['dup_deleted'] = cur.rowcount
                print(f"  Deleted duplicate Sheohar district ID 39 (0 child records)")
            else:
                raise Exception(f"District 39 has {places_39} places and {blocks_39} blocks, cannot delete safely")
        else:
            print(f"  District 39 not found or not Sheohar, skipping")

        # ─── STEP 1: Fix District Slugs ──────────────────────────
        print("\n── STEP 1: Fixing district slugs (36 rows) ──")
        # Phase 1a: Set temporary slugs to avoid unique constraint conflicts
        for did, slug in DISTRICT_SLUG_FIXES.items():
            temp_slug = f"__temp_fix_{did}__"
            cur.execute("UPDATE districts SET slug = %s WHERE id = %s", (temp_slug, did))
        print(f"  Phase 1a: Set {len(DISTRICT_SLUG_FIXES)} temporary slugs")

        # Phase 1b: Set final correct slugs
        for did, slug in DISTRICT_SLUG_FIXES.items():
            cur.execute("UPDATE districts SET slug = %s WHERE id = %s", (slug, did))
            changes['districts'] += 1
        print(f"  Phase 1b: Set {changes['districts']} final slugs")

        # ─── STEP 2: Fix Place district_id ───────────────────────
        print("\n── STEP 2: Fixing places.district_id ──")
        for pid, correct_did in PLACE_DISTRICT_FIXES.items():
            cur.execute("SELECT id, district_id FROM places WHERE id = %s", (pid,))
            row = cur.fetchone()
            if row and row['district_id'] != correct_did:
                cur.execute("UPDATE places SET district_id = %s WHERE id = %s", (correct_did, pid))
                changes['places'] += 1
                # print(f"  Place {pid}: {row['district_id']} → {correct_did}")
        print(f"  Fixed {changes['places']} place district_id values")

        # ─── STEP 3: Fix Block district_id ───────────────────────
        print("\n── STEP 3: Fixing blocks.district_id ──")

        # First, find Gaya blocks currently at DID 3 (need their exact IDs)
        cur.execute("SELECT id, name FROM blocks WHERE district_id = 3")
        gaya_blocks_at_3 = cur.fetchall()
        for b in gaya_blocks_at_3:
            BLOCK_DISTRICT_FIXES[b['id']] = 2  # Move Gaya blocks to DID 2
        print(f"  Found {len(gaya_blocks_at_3)} Gaya blocks at DID 3 to move to DID 2")

        for bid, correct_did in BLOCK_DISTRICT_FIXES.items():
            cur.execute("SELECT id, district_id FROM blocks WHERE id = %s", (bid,))
            row = cur.fetchone()
            if row and row['district_id'] != correct_did:
                cur.execute("UPDATE blocks SET district_id = %s WHERE id = %s", (correct_did, bid))
                changes['blocks'] += 1
        print(f"  Fixed {changes['blocks']} block district_id values")

        # ─── STEP 4: Fix district_foods.district_id ──────────────
        print("\n── STEP 4: Fixing district_foods.district_id ──")
        for fid, correct_did in FOOD_DISTRICT_FIXES.items():
            cur.execute("SELECT id, district_id FROM district_foods WHERE id = %s", (fid,))
            row = cur.fetchone()
            if row and row['district_id'] != correct_did:
                cur.execute("UPDATE district_foods SET district_id = %s WHERE id = %s", (correct_did, fid))
                changes['foods'] += 1
        print(f"  Fixed {changes['foods']} food district_id values")

        # ─── STEP 5: Fix nearby_services.district_id ──────────────
        print("\n── STEP 5: Fixing nearby_services.district_id ──")
        # Services at DID 3 (27 Gaya services) → move to DID 2
        cur.execute("UPDATE nearby_services SET district_id = 2 WHERE district_id = 3")
        svc_gaya = cur.rowcount
        changes['services'] += svc_gaya
        print(f"  Moved {svc_gaya} Gaya services from DID 3 → DID 2")

        # Services at DID 22 (26 Jamui services) → move to DID 4
        cur.execute("UPDATE nearby_services SET district_id = 4 WHERE district_id = 22")
        svc_jamui = cur.rowcount
        changes['services'] += svc_jamui
        print(f"  Moved {svc_jamui} Jamui services from DID 22 → DID 4")

        # ─── STEP 6: Fix host_listings.district_id ────────────────
        print("\n── STEP 6: Fixing host_listings.district_id ──")
        for lid, correct_did in HOST_LISTING_FIXES.items():
            cur.execute("SELECT id, district_id FROM host_listings WHERE id = %s", (lid,))
            row = cur.fetchone()
            if row and row['district_id'] != correct_did:
                cur.execute("UPDATE host_listings SET district_id = %s WHERE id = %s", (correct_did, lid))
                changes['host_listings'] += 1
        print(f"  Fixed {changes['host_listings']} host listing district_id values")

        # ─── STEP 7: Delete orphan place ID 44 ───────────────────
        print("\n── STEP 7: Deleting orphan place (ID 44) ──")
        cur.execute("SELECT id, name FROM places WHERE id = 44")
        orphan = cur.fetchone()
        if orphan and (not orphan['name'] or orphan['name'].strip() == ''):
            cur.execute("DELETE FROM places WHERE id = 44")
            changes['orphan_deleted'] = cur.rowcount
            print(f"  Deleted orphan place ID 44 (empty name)")
        else:
            print(f"  Place 44 not found or has content, skipping")

        # ─── STEP 8: (Moved to Step 0 — duplicate district already deleted) ──
        print("\n── STEP 8: Duplicate district already deleted in Step 0 ──")

        # ─── STEP 9: Verification ────────────────────────────────
        print("\n" + "=" * 70)
        print("VERIFICATION CHECKS")
        print("=" * 70)

        errors = []

        # Check 1: Every district has slug = slugify(name)
        cur.execute("SELECT id, name, slug FROM districts WHERE id != 39 ORDER BY id")
        for d in cur.fetchall():
            import re
            expected = re.sub(r'[^a-z0-9]+', '-', d['name'].lower().strip()).strip('-')
            if d['slug'] != expected:
                errors.append(f"District {d['id']}: slug='{d['slug']}' != expected='{expected}'")
        print(f"\n✓ District slug check: {len(errors)} errors")

        # Check 2: No duplicate slugs within same state
        cur.execute("""
            SELECT state_id, slug, COUNT(*) AS c FROM districts
            GROUP BY state_id, slug HAVING c > 1
        """)
        dup_slugs = cur.fetchall()
        if dup_slugs:
            for ds in dup_slugs:
                errors.append(f"Duplicate slug: state={ds['state_id']}, slug='{ds['slug']}', count={ds['c']}")
        print(f"✓ Duplicate slug check: {len(dup_slugs)} duplicates")

        # Check 3: Jamui places are at DID 4
        cur.execute("SELECT COUNT(*) AS c FROM places WHERE district_id = 4 AND slug LIKE '%jamui%'")
        jamui_count = cur.fetchone()['c']
        if jamui_count < 10:
            errors.append(f"Expected 10+ Jamui places at DID 4, got {jamui_count}")
        print(f"✓ Jamui places at DID 4: {jamui_count}")

        # Check 4: Nalanda places (Nalanda Ruins, Rajgir) at DID 3
        cur.execute("SELECT COUNT(*) AS c FROM places WHERE district_id = 3 AND (name LIKE '%Nalanda%' OR name LIKE '%Rajgir%')")
        nalanda_count = cur.fetchone()['c']
        if nalanda_count < 2:
            errors.append(f"Expected 2+ Nalanda/Rajgir places at DID 3, got {nalanda_count}")
        print(f"✓ Nalanda/Rajgir places at DID 3: {nalanda_count}")

        # Check 5: Gaya places at DID 2
        cur.execute("SELECT COUNT(*) AS c FROM places WHERE district_id = 2 AND (name LIKE '%Bodh Gaya%' OR name LIKE '%Mahabodhi%' OR name LIKE '%Buddha%')")
        gaya_count = cur.fetchone()['c']
        print(f"✓ Gaya/Bodh Gaya places at DID 2: {gaya_count}")

        # Check 6: Jamui blocks at DID 4
        cur.execute("SELECT COUNT(*) AS c FROM blocks WHERE district_id = 4 AND (name LIKE '%Jamui%' OR name LIKE '%Gidhaur%' OR name LIKE '%Jhajha%' OR name LIKE '%Simultala%')")
        jamui_blocks = cur.fetchone()['c']
        print(f"✓ Jamui blocks at DID 4: {jamui_blocks}")

        # Check 7: Nalanda blocks at DID 3
        cur.execute("SELECT COUNT(*) AS c FROM blocks WHERE district_id = 3 AND (name LIKE '%Bihar Sharif%' OR name LIKE '%Rajgir%' OR name LIKE '%Silao%')")
        nalanda_blocks = cur.fetchone()['c']
        print(f"✓ Nalanda blocks at DID 3: {nalanda_blocks}")

        # Check 8: Gaya blocks at DID 2
        cur.execute("SELECT COUNT(*) AS c FROM blocks WHERE district_id = 2 AND (name LIKE '%Bodh Gaya%' OR name LIKE '%Gaya Town%')")
        gaya_blocks = cur.fetchone()['c']
        print(f"✓ Gaya blocks at DID 2: {gaya_blocks}")

        # Check 9: Jamui services at DID 4
        cur.execute("SELECT COUNT(*) AS c FROM nearby_services WHERE district_id = 4")
        jamui_svcs = cur.fetchone()['c']
        print(f"✓ Jamui services at DID 4: {jamui_svcs}")

        # Check 10: No orphan place 44
        cur.execute("SELECT COUNT(*) AS c FROM places WHERE id = 44")
        orphan_check = cur.fetchone()['c']
        print(f"✓ Orphan place 44 exists: {'NO ✅' if orphan_check == 0 else 'YES ❌'}")

        # Check 11: Per-district place counts
        print("\n── Post-fix Place Counts by District ──")
        cur.execute("""
            SELECT d.id, d.name, d.slug, COUNT(p.id) AS pc
            FROM districts d
            LEFT JOIN places p ON p.district_id = d.id AND p.deleted_at IS NULL
            GROUP BY d.id ORDER BY d.id
        """)
        for d in cur.fetchall():
            print(f"  DID={d['id']:2d} | {d['name']:25s} | slug={d['slug']:22s} | Places: {d['pc']}")

        # ─── DECISION: Commit or Rollback ────────────────────────
        if errors:
            print(f"\n❌ {len(errors)} VERIFICATION ERRORS FOUND:")
            for e in errors:
                print(f"  - {e}")
            print("\n⚠️  ROLLING BACK — no changes saved!")
            conn.rollback()
        else:
            print(f"\n✅ ALL VERIFICATION CHECKS PASSED!")
            print(f"\nChanges Summary:")
            print(f"  Districts fixed:      {changes['districts']}")
            print(f"  Places fixed:         {changes['places']}")
            print(f"  Blocks fixed:         {changes['blocks']}")
            print(f"  Foods fixed:          {changes['foods']}")
            print(f"  Services fixed:       {changes['services']}")
            print(f"  Host listings fixed:  {changes['host_listings']}")
            print(f"  Orphan deleted:       {changes['orphan_deleted']}")
            print(f"  Duplicate deleted:    {changes['dup_deleted']}")
            conn.commit()
            print("\n🎉 COMMITTED SUCCESSFULLY — all changes saved!")

    except Exception as e:
        print(f"\n💥 EXCEPTION: {e}")
        print("⚠️  ROLLING BACK — no changes saved!")
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()


if __name__ == '__main__':
    run_repair()
