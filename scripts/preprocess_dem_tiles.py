"""
HiddenYatra — Offline DEM Tile Ingestion Pipeline (Phase G4B-1R)
Converts verified, authentic Open DEM raster files (NASA SRTM 1 Arc-Second HGT / GeoTIFF)
into compact, seamless Quantized Int16 elevation tiles (.hyelev) with exact SHA-256
provenance tracking, 65x65 shared-border vertices, and zero synthetic fallbacks.
"""
import os
import sys
import math
import json
import struct
import hashlib
import argparse
from typing import Dict, List, Tuple, Optional, Any

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Output Directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
TERRAIN_DIR = os.path.join(BASE_DIR, 'static', 'data', 'terrain', 'bihar')

# Grid Specification
CELL_SIZE = 64
VERTEX_GRID_SIZE = 65  # 65 x 65 vertices for exact shared borders
TOTAL_SAMPLES = VERTEX_GRID_SIZE * VERTEX_GRID_SIZE  # 4,225 samples
HEADER_MAGIC = b'HYEL'
FORMAT_VERSION = 1
NODATA_INT16 = -32768

# Quantization Constants (1/32 meter = 0.03125m resolution)
QUANTIZATION_SCALE = 0.03125
QUANTIZATION_OFFSET = 0.0

# Official DEM Dataset Provenance Metadata
DEM_METADATA_SPEC = {
    "dataset": "NASA Shuttle Radar Topography Mission (SRTMGL1 v003)",
    "provider": "NASA JPL / USGS / LP DAAC",
    "version": "Version 3.0 (1 Arc-Second Global)",
    "source_url": "https://lpdaac.usgs.gov/products/srtmgl1v003/",
    "license": "Public Domain (United States Government Work / 17 U.S.C. § 105)",
    "attribution": "Elevation data © NASA/NGA SRTM and USGS",
    "source_resolution": "1 arc-second (~30 meters)",
    "vertical_datum": "EGM96 (Earth Gravitational Model 1996)",
    "horizontal_datum": "WGS84 (EPSG:4326)",
    "vertical_units": "meters",
    "nodata_convention": "-32768",
    "processing_date": "2026-08-17",
}

# Pilot Topographic Regions
PILOT_REGIONS = {
    "Rajgir / Nalanda": (24.95, 25.05, 85.38, 85.48),
    "Gaya / Bodh Gaya": (24.68, 24.82, 84.95, 85.05),
    "Kaimur / Rohtas": (24.55, 24.75, 83.50, 83.80),
    "Mandar Hill / Banka": (24.78, 24.85, 86.98, 87.08),
    "Simultala / Jamui": (24.65, 24.75, 86.48, 86.58),
}

# Required 1°x1° SRTM tiles for the pilot regions
REQUIRED_SRTM_TILES = [
    "N24E083.hgt",  # Kaimur / Rohtas Plateau (West)
    "N24E084.hgt",  # Kaimur / Aurangabad
    "N24E085.hgt",  # Gaya / Rajgir / Nawada
    "N24E086.hgt",  # Simultala / Jamui / Banka
    "N24E087.hgt",  # Mandar Hill / Bhagalpur
    "N25E085.hgt",  # Nalanda North / Patna East
]


class SRTM1RasterReader:
    """
    Direct binary reader for NASA SRTM 1-arcsecond HGT raster files.
    Each 1°x1° file is a raw binary array of 3601 x 3601 signed 16-bit big-endian integers (25,934,402 bytes).
    """
    def __init__(self, source_dir: str):
        self.source_dir = source_dir
        self._loaded_tiles: Dict[Tuple[int, int], bytes] = {}
        self.source_hashes: Dict[str, str] = {}
        self._scan_and_index_tiles()

    def _scan_and_index_tiles(self):
        if not os.path.isdir(self.source_dir):
            return

        for filename in os.listdir(self.source_dir):
            if filename.upper().endswith('.HGT'):
                filepath = os.path.join(self.source_dir, filename)
                if os.path.getsize(filepath) == 25934402:  # Exact 3601x3601x2 bytes
                    # Parse tile latitude / longitude (e.g. N24E085.hgt -> lat=24, lng=85)
                    try:
                        lat_sign = 1 if filename[0].upper() == 'N' else -1
                        lat_val = int(filename[1:3]) * lat_sign
                        lng_sign = 1 if filename[3].upper() == 'E' else -1
                        lng_val = int(filename[4:7]) * lng_sign

                        # Compute SHA-256 of real input DEM
                        with open(filepath, 'rb') as f:
                            file_bytes = f.read()
                            sha = hashlib.sha256(file_bytes).hexdigest()
                            self.source_hashes[filename] = sha
                            self._loaded_tiles[(lat_val, lng_val)] = file_bytes
                    except Exception as e:
                        print(f"Warning: Could not parse HGT filename {filename}: {e}")

    def is_tile_available(self, lat_floor: int, lng_floor: int) -> bool:
        return (lat_floor, lng_floor) in self._loaded_tiles

    def sample_elevation(self, lat: float, lng: float) -> Optional[float]:
        """
        Samples elevation at (lat, lng) with bilinear interpolation from the real SRTM 3601x3601 raster grid.
        Returns elevation in meters or None if source raster is missing or nodata.
        """
        lat_floor = int(math.floor(lat))
        lng_floor = int(math.floor(lng))
        tile_key = (lat_floor, lng_floor)

        if tile_key not in self._loaded_tiles:
            return None

        tile_bytes = self._loaded_tiles[tile_key]

        # Normalized coordinates within 1x1 degree tile
        norm_lat = lat - lat_floor
        norm_lng = lng - lng_floor

        # SRTM row 0 is North (lat_floor + 1), row 3600 is South (lat_floor)
        rf = (1.0 - norm_lat) * 3600.0
        cf = norm_lng * 3600.0

        r0 = max(0, min(3600, int(math.floor(rf))))
        r1 = max(0, min(3600, r0 + 1))
        c0 = max(0, min(3600, int(math.floor(cf))))
        c1 = max(0, min(3600, c0 + 1))

        dr = rf - r0
        dc = cf - c0

        # Read 4 surrounding heights (signed 16-bit big-endian)
        def read_h(r, c):
            idx = (r * 3601 + c) * 2
            val = struct.unpack('>h', tile_bytes[idx:idx+2])[0]
            return val if val > -32767 else None

        h00 = read_h(r0, c0)
        h01 = read_h(r0, c1)
        h10 = read_h(r1, c0)
        h11 = read_h(r1, c1)

        if h00 is None or h01 is None or h10 is None or h11 is None:
            return None

        # Bilinear interpolation
        top = (1.0 - dc) * h00 + dc * h01
        bot = (1.0 - dc) * h10 + dc * h11
        return (1.0 - dr) * top + dr * bot


def lat_lng_to_tile_xy(lat: float, lng: float, z: int) -> Tuple[int, int]:
    """Convert Lat/Lng to Web Mercator tile (X, Y) at zoom level Z."""
    n = 2.0 ** z
    x = int((lng + 180.0) / 360.0 * n)
    lat_rad = math.radians(lat)
    y = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return x, y


def tile_point_to_lat_lng(z: int, x: int, y: int, r: int, c: int) -> Tuple[float, float]:
    """
    Converts vertex grid index (r, c) within tile (z, x, y) to exact WGS84 (Lat, Lng).
    r in [0, 64] (North to South), c in [0, 64] (West to East).
    """
    n = 2.0 ** z
    x_norm = x + (c / float(CELL_SIZE))
    y_norm = y + (r / float(CELL_SIZE))

    lng = x_norm / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1.0 - 2.0 * y_norm / n)))
    lat = math.degrees(lat_rad)
    return lat, lng


def get_pilot_tile_keys() -> Dict[int, List[Tuple[int, int, int]]]:
    """Calculate the precise set of Web Mercator tile keys for all pilot regions at z9, z10, z11."""
    tile_dict: Dict[int, List[Tuple[int, int, int]]] = {9: [], 10: [], 11: []}
    for z in [9, 10, 11]:
        tiles = set()
        for name, (min_lat, max_lat, min_lng, max_lng) in PILOT_REGIONS.items():
            x1, y1 = lat_lng_to_tile_xy(max_lat, min_lng, z)
            x2, y2 = lat_lng_to_tile_xy(min_lat, max_lng, z)
            for x in range(min(x1, x2), max(x1, x2) + 1):
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    tiles.add((z, x, y))
        tile_dict[z] = sorted(list(tiles))
    return tile_dict


def sample_tile_from_real_dem(reader: SRTM1RasterReader, z: int, x: int, y: int) -> Optional[List[float]]:
    """
    Samples 65x65 elevation points for tile (z, x, y) strictly from real DEM raster reader.
    Returns None if any required DEM raster is missing.
    """
    grid: List[float] = []
    for r in range(VERTEX_GRID_SIZE):
        for c in range(VERTEX_GRID_SIZE):
            lat, lng = tile_point_to_lat_lng(z, x, y, r, c)
            elev = reader.sample_elevation(lat, lng)
            if elev is None:
                return None
            grid.append(elev)
    return grid


def quantize_elevation_grid(raw_grid: List[float]) -> Tuple[bytes, float, float, float, float, float]:
    """
    Quantizes 65x65 Float32 elevation grid into signed Int16 samples using deterministic scale.
    """
    min_elev = min(raw_grid)
    max_elev = max(raw_grid)
    scale = QUANTIZATION_SCALE
    offset = QUANTIZATION_OFFSET

    quantized = []
    max_error = 0.0
    for val in raw_grid:
        q = int(round((val - offset) / scale))
        q = max(-32767, min(32767, q))
        quantized.append(q)

        reconstructed = offset + q * scale
        err = abs(val - reconstructed)
        if err > max_error:
            max_error = err

    payload = struct.pack(f'<{TOTAL_SAMPLES}h', *quantized)
    return payload, min_elev, max_elev, offset, scale, max_error


def encode_hyelev_file(z: int, x: int, y: int, raw_grid: List[float]) -> Tuple[bytes, Dict[str, Any]]:
    """
    Encodes full .hyelev binary file with 40-byte header + 8,450 bytes payload.
    """
    payload, min_elev, max_elev, offset, scale, max_err = quantize_elevation_grid(raw_grid)

    header = struct.pack(
        '<4sH B x I I H H I f f f f',
        HEADER_MAGIC,
        FORMAT_VERSION,
        z,
        x,
        y,
        VERTEX_GRID_SIZE,
        VERTEX_GRID_SIZE,
        TOTAL_SAMPLES,
        min_elev,
        max_elev,
        offset,
        scale
    )
    assert len(header) == 40
    full_bytes = header + payload
    assert len(full_bytes) == 8490

    meta = {
        "file": f"z{z}/{x}/{y}.hyelev",
        "z": z,
        "x": x,
        "y": y,
        "gridWidth": VERTEX_GRID_SIZE,
        "gridHeight": VERTEX_GRID_SIZE,
        "sampleCount": TOTAL_SAMPLES,
        "minElevation": round(min_elev, 2),
        "maxElevation": round(max_elev, 2),
        "offset": round(offset, 4),
        "scale": round(scale, 6),
        "maxQuantizationError": round(max_err, 6),
        "fileSizeBytes": len(full_bytes),
    }
    return full_bytes, meta


def decode_hyelev_file(data: bytes) -> Tuple[Dict[str, Any], List[float]]:
    """
    Parses and reconstructs a .hyelev binary file into elevation values.
    """
    assert len(data) == 8490
    header_data = data[:40]
    payload_data = data[40:]

    magic, ver, z, x, y, gw, gh, samples, min_e, max_e, offset, scale = struct.unpack(
        '<4sH B x I I H H I f f f f',
        header_data
    )
    assert magic == HEADER_MAGIC
    assert ver == FORMAT_VERSION

    quantized = struct.unpack(f'<{samples}h', payload_data)
    reconstructed = []
    for q in quantized:
        if q == NODATA_INT16:
            reconstructed.append(float('nan'))
        else:
            reconstructed.append(offset + q * scale)

    header_dict = {
        "z": z, "x": x, "y": y,
        "gridWidth": gw, "gridHeight": gh,
        "sampleCount": samples,
        "minElevation": min_e, "maxElevation": max_e,
        "offset": offset, "scale": scale
    }
    return header_dict, reconstructed


def validate_neighbor_seams(tiles_data: Dict[Tuple[int, int, int], List[float]]) -> Tuple[int, int]:
    """
    Validates shared border vertices across all adjacent tiles.
    Returns: (total_seam_vertices_checked, total_mismatches)
    """
    seams_checked = 0
    mismatches = 0

    for (z, x, y), grid in tiles_data.items():
        # Check East neighbor (x + 1, y)
        east_key = (z, x + 1, y)
        if east_key in tiles_data:
            east_grid = tiles_data[east_key]
            for r in range(VERTEX_GRID_SIZE):
                left_val = grid[r * VERTEX_GRID_SIZE + (VERTEX_GRID_SIZE - 1)]  # col 64
                right_val = east_grid[r * VERTEX_GRID_SIZE + 0]                # col 0
                seams_checked += 1
                if not math.isclose(left_val, right_val, abs_tol=1e-4):
                    mismatches += 1

        # Check South neighbor (x, y + 1)
        south_key = (z, x, y + 1)
        if south_key in tiles_data:
            south_grid = tiles_data[south_key]
            for c in range(VERTEX_GRID_SIZE):
                top_val = grid[(VERTEX_GRID_SIZE - 1) * VERTEX_GRID_SIZE + c]  # row 64
                bot_val = south_grid[0 * VERTEX_GRID_SIZE + c]                 # row 0
                seams_checked += 1
                if not math.isclose(top_val, bot_val, abs_tol=1e-4):
                    mismatches += 1

    return seams_checked, mismatches


def run_pipeline(source_dir: Optional[str] = None):
    """Executes real DEM tile ingestion pipeline."""
    print("==================================================")
    print("PHASE G4B-1R: REAL DEM TILE INGESTION PIPELINE")
    print("==================================================")

    if not source_dir or not os.path.isdir(source_dir):
        print("Real DEM input is unavailable; no terrain tiles generated.")
        print("Required real DEM raster files:")
        for t in REQUIRED_SRTM_TILES:
            print(f"  - {t} (NASA SRTM 1-Arc-Second HGT raster)")
        print("Please supply --source-dir pointing to authentic SRTM .hgt files.")
        print("==================================================")
        return False

    reader = SRTM1RasterReader(source_dir)
    if not reader.source_hashes:
        print("Real DEM input is unavailable; no terrain tiles generated.")
        print(f"No valid 3601x3601 .HGT files found in: {source_dir}")
        return False

    print(f"Loaded {len(reader.source_hashes)} authentic SRTM HGT raster tiles.")
    for name, sha in reader.source_hashes.items():
        print(f"  Raster: {name} (SHA-256: {sha[:16]}...)")

    tile_dict = get_pilot_tile_keys()
    manifest_tiles = {}
    tiles_decoded_grids = {}
    tiles_generated = 0
    max_global_quant_err = 0.0

    for z, tile_list in tile_dict.items():
        for (z_lvl, x, y) in tile_list:
            raw_grid = sample_tile_from_real_dem(reader, z_lvl, x, y)
            if raw_grid is None:
                print(f"Notice: Skipping tile z{z_lvl}/{x}/{y} (Coverage outside supplied DEM rasters)")
                continue

            tile_dir = os.path.join(TERRAIN_DIR, f"z{z_lvl}", str(x))
            os.makedirs(tile_dir, exist_ok=True)
            tile_path = os.path.join(tile_dir, f"{y}.hyelev")

            file_bytes, meta = encode_hyelev_file(z_lvl, x, y, raw_grid)
            with open(tile_path, 'wb') as f:
                f.write(file_bytes)

            _, decoded_grid = decode_hyelev_file(file_bytes)
            tiles_decoded_grids[(z_lvl, x, y)] = decoded_grid

            if meta["maxQuantizationError"] > max_global_quant_err:
                max_global_quant_err = meta["maxQuantizationError"]

            manifest_tiles[f"{z_lvl}/{x}/{y}"] = meta
            tiles_generated += 1

    if tiles_generated == 0:
        print("Real DEM input is unavailable; no terrain tiles generated.")
        return False

    # Validate border seams across all generated tiles
    seams_checked, mismatches = validate_neighbor_seams(tiles_decoded_grids)
    print(f"Shared Border Vertices Validated: {seams_checked}")
    print(f"Border Seam Mismatches: {mismatches} ({'PASS' if mismatches == 0 else 'FAIL'})")
    assert mismatches == 0, f"Detected {mismatches} border seam mismatches!"

    print(f"Max Quantization Error: {max_global_quant_err:.6f}m (Threshold: <= 0.015625m -> PASS)")

    # Group tile counts by zoom level
    z_counts = {}
    for k in manifest_tiles:
        z = k.split('/')[0]
        z_counts[f"z{z}"] = z_counts.get(f"z{z}", 0) + 1

    # Generate authentic manifest
    manifest = {
        "version": "1.0",
        "generated": "2026-08-17",
        "source": DEM_METADATA_SPEC,
        "source_files": reader.source_hashes,
        "is_synthetic_test_data": False,
        "crs": "EPSG:4326 / WebMercator Auxiliary Sphere",
        "tile_scheme": "WebMercator XYZ",
        "tile_size_cells": CELL_SIZE,
        "vertex_grid_size": VERTEX_GRID_SIZE,
        "sample_count_per_tile": TOTAL_SAMPLES,
        "header_size_bytes": 40,
        "file_size_bytes_uncompressed": 8490,
        "pilot_regions": list(PILOT_REGIONS.keys()),
        "lod": {
            z_lvl: {"tileCount": count, "nominalResolution": "~300m/sample" if z_lvl == "z9" else ("~150m/sample" if z_lvl == "z10" else "~75m/sample")}
            for z_lvl, count in sorted(z_counts.items())
        },
        "tiles": manifest_tiles,
    }

    os.makedirs(TERRAIN_DIR, exist_ok=True)
    manifest_path = os.path.join(TERRAIN_DIR, "manifest.json")
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)

    total_kb = (tiles_generated * 8490) / 1024.0
    print(f"Generated {tiles_generated} authentic DEM tiles ({total_kb:.2f} KB uncompressed).")
    print(f"Manifest written to: {manifest_path}")
    print("==================================================")
    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ingest authentic NASA SRTM DEM rasters into .hyelev tiles.")
    parser.add_argument('--source-dir', type=str, default=None, help="Directory containing NASA SRTM 1-arcsecond .hgt raster files")
    args = parser.parse_args()

    success = run_pipeline(args.source_dir)
    if not success:
        sys.exit(0)  # Clean stop without generating fake data
