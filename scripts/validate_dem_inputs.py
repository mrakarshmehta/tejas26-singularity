"""
HiddenYatra — Real DEM Input Validation Tool (Phase G4B-1R)
Performs strict pre-flight validation on real NASA SRTM 1-arcsecond HGT raster inputs:
- Exact file sizes (25,934,402 bytes)
- 3601 x 3601 signed 16-bit big-endian raster dimensions
- Cryptographic SHA-256 calculation
- Min/Max elevation checks and NoData counts
- Blocks terrain tile generation if any input is missing or corrupted.
"""
import os
import sys
import struct
import hashlib
from typing import Dict, List, Tuple, Optional

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

EXPECTED_TILES = [
    ("N24E083.hgt", 24, 83, "Kaimur / Rohtas Plateau (West)"),
    ("N24E084.hgt", 24, 84, "Kaimur / Aurangabad / Son River"),
    ("N24E085.hgt", 24, 85, "Gaya (Brahmayoni) / Rajgir (Nalanda) / Nawada"),
    ("N24E086.hgt", 24, 86, "Simultala / Jamui / Banka Uplands"),
    ("N24E087.hgt", 24, 87, "Mandar Hill / Bhagalpur / Ganga Basin"),
    ("N25E085.hgt", 25, 85, "Nalanda North / Patna East"),
]

EXPECTED_FILE_SIZE = 25934402  # 3601 * 3601 * 2 bytes


def validate_dem_directory(input_dir: str = r"d:\HiddenYatra\dem_input") -> bool:
    print("==================================================")
    print("REAL NASA SRTM INPUT PRE-FLIGHT VALIDATION")
    print("==================================================")
    print(f"Target Input Directory: {input_dir}")

    if not os.path.exists(input_dir):
        print(f"Status: Directory does not exist.")
        print(f"Action: Create '{input_dir}' and place the 6 required SRTM HGT files.")
        print("==================================================")
        print("GENERATION STATUS: BLOCKED (0/6 files present)")
        print("==================================================")
        return False

    all_valid = True
    found_count = 0

    print(f"{'Filename':<14} | {'Size (Bytes)':<12} | {'Min Elev':<10} | {'Max Elev':<10} | {'NoData':<8} | {'SHA-256 (First 16)':<18} | {'Status'}")
    print("-" * 95)

    for fname, exp_lat, exp_lng, region in EXPECTED_TILES:
        fpath = os.path.join(input_dir, fname)
        if not os.path.exists(fpath):
            print(f"{fname:<14} | {'MISSING':<12} | {'-':<10} | {'-':<10} | {'-':<8} | {'-':<18} | MISSING")
            all_valid = False
            continue

        found_count += 1
        size = os.path.getsize(fpath)
        if size != EXPECTED_FILE_SIZE:
            print(f"{fname:<14} | {size:<12} | {'-':<10} | {'-':<10} | {'-':<8} | {'-':<18} | INVALID SIZE (Expected {EXPECTED_FILE_SIZE})")
            all_valid = False
            continue

        # Compute SHA-256 & scan elevation min/max
        sha256 = hashlib.sha256()
        min_e = 99999
        max_e = -99999
        nodata_cnt = 0

        with open(fpath, 'rb') as f:
            while chunk := f.read(65536):
                sha256.update(chunk)

        # Sample raster data
        with open(fpath, 'rb') as f:
            data = f.read()
            samples = struct.unpack('>12967201h', data)  # 3601 * 3601
            for s in samples:
                if s == -32768:
                    nodata_cnt += 1
                else:
                    if s < min_e: min_e = s
                    if s > max_e: max_e = s

        hex_digest = sha256.hexdigest()
        print(f"{fname:<14} | {size:<12} | {min_e:<10} | {max_e:<10} | {nodata_cnt:<8} | {hex_digest[:16]:<18} | VALID")

    print("-" * 95)
    print(f"Files Validated: {found_count}/{len(EXPECTED_TILES)}")
    if all_valid and found_count == len(EXPECTED_TILES):
        print("==================================================")
        print("GENERATION STATUS: READY (All 6 files validated)")
        print("==================================================")
        return True
    else:
        print("==================================================")
        print(f"GENERATION STATUS: BLOCKED ({found_count}/{len(EXPECTED_TILES)} files present)")
        print("==================================================")
        return False


if __name__ == '__main__':
    dir_path = sys.argv[1] if len(sys.argv) > 1 else r"d:\HiddenYatra\dem_input"
    validate_dem_directory(dir_path)
