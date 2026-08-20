"""
Unit tests for helper utilities: image processing, CSRF protection, and session handling.
"""
import os
import unittest
from unittest.mock import MagicMock
from PIL import Image

from utils.image import process_and_save_image
from utils import csrf_required, login_required, get_session_id


class TestUtilsImage(unittest.TestCase):

    def setUp(self):
        self.test_dir = os.path.join(os.path.dirname(__file__), 'temp_test_uploads')
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            for f in os.listdir(self.test_dir):
                os.remove(os.path.join(self.test_dir, f))
            os.rmdir(self.test_dir)

    def test_process_and_save_image(self):
        """Test image resizing and conversion to RGB."""
        img_path = os.path.join(self.test_dir, 'source.png')
        img = Image.new('RGBA', (2000, 1000), color='red')
        img.save(img_path)

        with open(img_path, 'rb') as f:
            file_obj = MagicMock()
            file_obj.filename = 'test.png'
            file_obj.stream = f

            saved_name = process_and_save_image(file_obj, self.test_dir, prefix='unit', max_width=1000)
            self.assertIsNotNone(saved_name)
            self.assertTrue(saved_name.startswith('unit_'))

            saved_path = os.path.join(self.test_dir, saved_name)
            self.assertTrue(os.path.exists(saved_path))

            saved_img = Image.open(saved_path)
            self.assertEqual(saved_img.mode, 'RGB')
            self.assertLessEqual(saved_img.width, 1000)
            saved_img.close()

    def test_invalid_file_returns_none(self):
        """None or empty filename should return None."""
        self.assertIsNone(process_and_save_image(None, self.test_dir))

        file_obj = MagicMock()
        file_obj.filename = ''
        self.assertIsNone(process_and_save_image(file_obj, self.test_dir))


class TestDecoratorExits(unittest.TestCase):

    def test_decorators_callable(self):
        """Test that decorators are callable functions."""
        self.assertTrue(callable(csrf_required))
        self.assertTrue(callable(login_required))
        self.assertTrue(callable(get_session_id))


def test_image_dimension_validation(self):
        """Test validate_dimensions utility with in-memory test image."""
        import io
        from PIL import Image
        from utils.image import validate_dimensions, get_image_metadata

        img_buf = io.BytesIO()
        img = Image.new('RGB', (300, 200), color='red')
        img.save(img_buf, format='JPEG')
        img_buf.seek(0)

        is_valid, w, h = validate_dimensions(img_buf, min_w=100, min_h=100)
        self.assertTrue(is_valid)
        self.assertEqual(w, 300)
        self.assertEqual(h, 200)

        meta = get_image_metadata(img_buf)
        self.assertEqual(meta.get('format'), 'JPEG')
        self.assertEqual(meta.get('width'), 300)

if __name__ == '__main__':
    unittest.main()
