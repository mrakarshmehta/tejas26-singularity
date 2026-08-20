"""
HiddenYatra — Shared Image Processing Utility
Centralizes image upload processing (resize, convert, compress) used by:
  - Admin place/hero/district uploads
  - Community submission uploads
  - User photo uploads
"""
import os
import uuid
import logging
from PIL import Image, ImageOps

logger = logging.getLogger(__name__)


def process_and_save_image(file_obj, dest_folder, prefix='img',
                           max_width=1600, quality=85):
    """Process an uploaded image: validate, convert, resize, compress, save.

    Args:
        file_obj: Werkzeug FileStorage object.
        dest_folder: Absolute path to the destination directory.
        prefix: Filename prefix (e.g., 'place', 'user', 'sub').
        max_width: Maximum width; images wider than this are downscaled.
        quality: JPEG compression quality (1-100).

    Returns:
        Saved filename (str) on success, or None on failure.
    """
    if not file_obj or not file_obj.filename:
        return None

    ext = file_obj.filename.rsplit('.', 1)[-1].lower()
    filename = f"{prefix}_{uuid.uuid4().hex[:10]}.{ext}"
    filepath = os.path.join(dest_folder, filename)

    try:
        stream = getattr(file_obj, 'stream', file_obj)
        img = Image.open(stream)
        img = ImageOps.exif_transpose(img)

        # Convert RGBA/Palette to RGB for JPEG compatibility
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        # Resize if exceeds max width, preserving aspect ratio
        if img.width > max_width:
            ratio = max_width / img.width
            new_size = (max_width, int(img.height * ratio))
            img = img.resize(new_size, Image.LANCZOS)

        img.save(filepath, quality=quality, optimize=True)
    except Exception as e:
        logger.warning("Failed to process image %s: %s", filename, e)
        return None

    return filename if os.path.exists(filepath) else None
"""Shared image processing utility for HiddenYatra."""


def compress_image_to_webp(file_obj, dest_folder, prefix='img',
                           max_width=1600, quality=80):
    """Process and save image as optimized WebP with EXIF orientation correction.

    Args:
        file_obj: Werkzeug FileStorage or file-like object.
        dest_folder: Directory to save into.
        prefix: Filename prefix.
        max_width: Maximum width in pixels.
        quality: WebP quality (1-100).

    Returns:
        Saved filename (str) or None on failure.
    """
    if not file_obj or not getattr(file_obj, 'filename', None):
        return None

    filename = f"{prefix}_{uuid.uuid4().hex[:10]}.webp"
    filepath = os.path.join(dest_folder, filename)

    try:
        stream = getattr(file_obj, 'stream', file_obj)
        img = Image.open(stream)

        # Transpose based on EXIF orientation tag
        img = ImageOps.exif_transpose(img)

        # Convert palette/RGBA modes appropriately for WebP
        if img.mode in ('P', 'LA'):
            img = img.convert('RGBA')

        # Resize if exceeds max width
        if img.width > max_width:
            ratio = max_width / img.width
            new_size = (max_width, int(img.height * ratio))
            img = img.resize(new_size, Image.LANCZOS)

        img.save(filepath, format='WEBP', quality=quality, method=4)
    except Exception as e:
        logger.warning("Failed to compress image to WebP %s: %s", filename, e)
        return None

    return filename if os.path.exists(filepath) else None
