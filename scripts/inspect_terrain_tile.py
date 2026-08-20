"""
HiddenYatra — Developer Inspection Utility for .hyelev Terrain Tiles (Phase G4B-1)
Decodes a binary .hyelev file and displays header metadata, corner/center elevations,
sample dimensions, and edge profiles.
"""
import os
import sys

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.preprocess_dem_tiles import decode_hyelev_file, TERRAIN_DIR


def inspect_tile(tile_rel_path: str = "z11/1507/878.hyelev"):
    full_path = os.path.join(TERRAIN_DIR, tile_rel_path)
    if not os.path.exists(full_path):
        print(f"Error: Tile not found at {full_path}")
        return

    with open(full_path, 'rb') as f:
        data = f.read()

    header, samples = decode_hyelev_file(data)

    gw = header["gridWidth"]
    gh = header["gridHeight"]
    center_idx = (gh // 2) * gw + (gw // 2)
    nw_val = samples[0]
    ne_val = samples[gw - 1]
    sw_val = samples[(gh - 1) * gw]
    se_val = samples[gh * gw - 1]
    center_val = samples[center_idx]

    print("==================================================")
    print(f"HYELEV TILE INSPECTION: {tile_rel_path}")
    print("==================================================")
    print(f"Tile Key: Z={header['z']}, X={header['x']}, Y={header['y']}")
    print(f"Grid Dimensions: {gw} x {gh} ({header['sampleCount']} vertices)")
    print(f"Min Elevation: {header['minElevation']:.2f} m")
    print(f"Max Elevation: {header['maxElevation']:.2f} m")
    print(f"Offset: {header['offset']:.4f} m | Scale: {header['scale']:.6f} m/unit")
    print("--------------------------------------------------")
    print(f"NW Corner [0, 0]:     {nw_val:.2f} m")
    print(f"NE Corner [0, 64]:    {ne_val:.2f} m")
    print(f"Center Point [32, 32]:{center_val:.2f} m")
    print(f"SW Corner [64, 0]:    {sw_val:.2f} m")
    print(f"SE Corner [64, 64]:   {se_val:.2f} m")
    print("==================================================")


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else "z11/1507/878.hyelev"
    inspect_tile(path)
