from models.database import get_db
db = get_db()
with db.cursor() as cur:
    # Check Jamui district
    cur.execute("SELECT * FROM districts WHERE name LIKE %s", ("%Jamui%",))
    jamui = cur.fetchone()
    print("Jamui district:", jamui)
    print()
    
    # Check existing places for Jamui
    if jamui:
        cur.execute("SELECT id, name, slug, category FROM places WHERE district_id = %s AND deleted_at IS NULL", (jamui["id"],))
        places = cur.fetchall()
        print("Existing places in Jamui (" + str(len(places)) + "):")
        for p in places:
            print("  - " + p["name"] + " (slug: " + p["slug"] + ", cat: " + p["category"] + ")")
    
    # Get state_id for Bihar
    cur.execute("SELECT DISTINCT state_id FROM districts LIMIT 1")
    state = cur.fetchone()
    print("State ID:", state)
    
    # Check existing categories used
    cur.execute("SELECT DISTINCT category FROM places")
    cats = cur.fetchall()
    print("Existing categories:", [c["category"] for c in cats])
    
    # Check nearby_services table schema
    cur.execute("DESCRIBE nearby_services")
    print("\nNearby Services table schema:")
    for row in cur.fetchall():
        print("  ", row)
    
    # Check a sample existing place for data format reference
    cur.execute("SELECT * FROM places WHERE deleted_at IS NULL LIMIT 1")
    sample = cur.fetchone()
    print("\nSample place fields:")
    for k, v in sample.items():
        val_str = str(v)[:80] if v else "NULL"
        print("  " + k + ": " + val_str)
