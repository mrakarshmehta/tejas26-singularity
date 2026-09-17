import sys
sys.path.insert(0, r'd:\HiddenYatra')
from dotenv import load_dotenv
load_dotenv()
from models.connection import get_cursor

with get_cursor(commit=True) as cur:
    # ID 1 photos
    cur.execute('DELETE FROM listing_photos WHERE listing_id = 1')
    cur.execute("""
        INSERT INTO listing_photos (listing_id, filename, caption, sort_order, uploaded_at) VALUES
        (1, 'bodh_gaya_homestay_cover.jpg', 'Heritage courtyard & facade', 0, NOW()),
        (1, 'stay_demo_gaya_bedroom.jpg', 'Airy bedroom with garden view', 1, NOW()),
        (1, 'stay_demo_gaya_terrace.jpg', 'Meditation terrace overlooking Bodh Gaya', 2, NOW()),
        (1, 'stay_demo_gaya_dining.jpg', 'Family dining table', 3, NOW())
    """)
    # ID 2 photos
    cur.execute('DELETE FROM listing_photos WHERE listing_id = 2')
    cur.execute("""
        INSERT INTO listing_photos (listing_id, filename, caption, sort_order, uploaded_at) VALUES
        (2, 'simultala_stay_cover.jpg', 'Eco cottage amidst pine trees', 0, NOW()),
        (2, 'stay_demo_simultala_bedroom.jpg', 'Peaceful forest guest bedroom', 1, NOW()),
        (2, 'stay_demo_simultala_veranda.jpg', 'Sunset veranda with mountain vista', 2, NOW()),
        (2, 'stay_demo_simultala_dining.jpg', 'Organic village kitchen & dining', 3, NOW())
    """)
    print('Populated gallery photos for ID 1 and ID 2 successfully.')
