"""
HiddenYatra — Quality Assurance Script: Real NASA SRTM vs Decoded .hyelev
Directly compares raw HGT sensor elevations against decoded .hyelev tiles at key topographic landmarks.
"""
import os
import sys
import math

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.preprocess_dem_tiles import (
    SRTM1RasterReader,
    decode_hyelev_file,
    lat_lng_to_tile_xy,
    TERRAIN_DIR
)

reader = SRTM1RasterReader(r"D:\HiddenYatra\dem_input")

checkpoints = [
    ("Rajgir Peak (Ratnagiri)", 25.006, 85.445, 11),
    ("Gaya (Brahmayoni Hill)", 24.782, 84.992, 11),
    ("Kaimur (Rohtas Escarpment)", 24.630, 83.650, 11),
    ("Mandar Hill (Banka)", 24.805, 87.026, 11),
    ("Simultala (Jamui)", 24.708, 86.533, 11),
]

print("=========================================================================================================")
print("REAL NASA SRTM SOURCE VS DECODED .HYELEV QUALITY COMPARISON")
print("=========================================================================================================")
print(f"{'Landmark Location':<28} | {'Coordinates':<18} | {'Raw SRTM HGT':<14} | {'Decoded .hyelev':<16} | {'Delta'}")
print("-" * 105)

for name, lat, lng, z in checkpoints:
    raw_elev = reader.sample_elevation(lat, lng)
    x, y = lat_lng_to_tile_xy(lat, lng, z)
    tile_file = os.path.join(TERRAIN_DIR, f"z{z}", str(x), f"{y}.hyelev")

    if os.path.exists(tile_file):
        with open(tile_file, 'rb') as f:
            header, samples = decode_hyelev_file(f.read())

        # Exact bilinear interpolation within tile
        n = 2.0 ** z
        x_norm = (lng + 180.0) / 360.0 * n - x
        lat_rad = math.radians(lat)
        y_norm = (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n - y
        c_f = x_norm * 64.0
        r_f = y_norm * 64.0
        r0 = max(0, min(63, int(math.floor(r_f))))
        r1 = r0 + 1
        c0 = max(0, min(63, int(math.floor(c_f))))
        c1 = c0 + 1
        dr = r_f - r0
        dc = c_f - c0

        h00 = samples[r0 * 65 + c0]
        h01 = samples[r0 * 65 + c1]
        h10 = samples[r1 * 65 + c0]
        h11 = samples[r1 * 65 + c1]

        top = (1.0 - dc) * h00 + dc * h01
        bot = (1.0 - dc) * h10 + dc * h11
        interp_elev = (1.0 - dr) * top + dr * bot
        delta = abs(raw_elev - interp_elev)

        print(f"{name:<28} | {lat:.3f}°N, {lng:.3f}°E    | {raw_elev:8.2f} m     | {interp_elev:10.2f} m      | {delta:8.4f} m")
    else:
        print(f"{name:<28} | {lat:.3f}°N, {lng:.3f}°E    | {raw_elev:8.2f} m     | TILE NOT FOUND   | -")

print("=========================================================================================================")
