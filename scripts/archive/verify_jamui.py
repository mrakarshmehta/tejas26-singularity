from models.connection import get_cursor

with get_cursor() as cur:
    cur.execute("""
        SELECT id, name, slug, category, latitude, longitude, is_featured, is_hidden_gem
        FROM places
        WHERE district_id = 22 AND deleted_at IS NULL
        ORDER BY id
    """)
    rows = cur.fetchall()
    print("Jamui District Places in Database (" + str(len(rows)) + "):")
    print("-" * 80)
    for r in rows:
        print("  ID=" + str(r["id"]) + 
              " | " + r["name"] + 
              " | cat=" + r["category"] + 
              " | lat=" + str(r["latitude"]) + 
              " | lng=" + str(r["longitude"]) +
              " | feat=" + str(r["is_featured"]) +
              " | gem=" + str(r["is_hidden_gem"]))
    print("-" * 80)
