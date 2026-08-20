/**
 * HiddenYatra — Google Maps WebGL 3D Terrain Web Worker (Phase G4B-2)
 * Off-thread binary .hyelev fetcher and elevation decoder.
 * Decodes 40-byte HYEL header and Int16 elevation grid into Transferable Float32Array
 * and pre-indexes 64x64 cell triangle indices for zero-copy main-thread transfer.
 */
'use strict';

const HEADER_MAGIC_0 = 0x48; // 'H'
const HEADER_MAGIC_1 = 0x59; // 'Y'
const HEADER_MAGIC_2 = 0x45; // 'E'
const HEADER_MAGIC_3 = 0x4C; // 'L'
const EXPECTED_HEADER_SIZE = 40;
const VERTEX_GRID_SIZE = 65;
const CELL_GRID_SIZE = 64;
const TOTAL_SAMPLES = VERTEX_GRID_SIZE * VERTEX_GRID_SIZE; // 4225
const EXPECTED_FILE_SIZE = 8490; // 40 bytes header + 4225 * 2 bytes Int16
const NODATA_INT16 = -32768;

/**
 * Pre-computes 64x64 grid triangle index buffer (24,576 uint16 indices, 6 per cell).
 * Shared across all 65x65 tiles.
 */
function generateTileIndexBuffer() {
    const indices = new Uint16Array(CELL_GRID_SIZE * CELL_GRID_SIZE * 6);
    let ptr = 0;
    for (let r = 0; r < CELL_GRID_SIZE; r++) {
        for (let c = 0; c < CELL_GRID_SIZE; c++) {
            const topLeft = r * VERTEX_GRID_SIZE + c;
            const topRight = topLeft + 1;
            const bottomLeft = (r + 1) * VERTEX_GRID_SIZE + c;
            const bottomRight = bottomLeft + 1;

            // First triangle (top-left, bottom-left, top-right)
            indices[ptr++] = topLeft;
            indices[ptr++] = bottomLeft;
            indices[ptr++] = topRight;

            // Second triangle (top-right, bottom-left, bottom-right)
            indices[ptr++] = topRight;
            indices[ptr++] = bottomLeft;
            indices[ptr++] = bottomRight;
        }
    }
    return indices;
}

// Cached shared index buffer template
const SHARED_INDEX_TEMPLATE = generateTileIndexBuffer();

/**
 * Decodes raw ArrayBuffer of a .hyelev file into header metadata and Float32Array elevation grid.
 * @param {ArrayBuffer} arrayBuffer
 * @returns {Object} { header, elevations, indices }
 */
function decodeHyelevBinary(arrayBuffer) {
    if (!arrayBuffer || arrayBuffer.byteLength !== EXPECTED_FILE_SIZE) {
        throw new Error(`Invalid .hyelev file size: expected ${EXPECTED_FILE_SIZE} bytes, got ${arrayBuffer ? arrayBuffer.byteLength : 0}`);
    }

    const dataView = new DataView(arrayBuffer);

    // 1. Verify Magic 'HYEL'
    if (
        dataView.getUint8(0) !== HEADER_MAGIC_0 ||
        dataView.getUint8(1) !== HEADER_MAGIC_1 ||
        dataView.getUint8(2) !== HEADER_MAGIC_2 ||
        dataView.getUint8(3) !== HEADER_MAGIC_3
    ) {
        throw new Error("Invalid .hyelev binary header magic (expected 'HYEL')");
    }

    // 2. Parse 40-byte Header
    const version = dataView.getUint16(4, true);
    if (version !== 1) {
        throw new Error(`Unsupported .hyelev format version: ${version}`);
    }

    const z = dataView.getUint8(6);
    // byte 7 is padding
    const x = dataView.getUint32(8, true);
    const y = dataView.getUint32(12, true);
    const gridWidth = dataView.getUint16(16, true);
    const gridHeight = dataView.getUint16(18, true);
    const sampleCount = dataView.getUint32(20, true);
    const minElevation = dataView.getFloat32(24, true);
    const maxElevation = dataView.getFloat32(28, true);
    const offset = dataView.getFloat32(32, true);
    const scale = dataView.getFloat32(36, true);

    if (gridWidth !== VERTEX_GRID_SIZE || gridHeight !== VERTEX_GRID_SIZE || sampleCount !== TOTAL_SAMPLES) {
        throw new Error(`Unexpected grid dimensions: ${gridWidth}x${gridHeight} (${sampleCount} samples)`);
    }

    // 3. Decode Int16 Elevation Payload
    const elevations = new Float32Array(TOTAL_SAMPLES);
    let byteOffset = EXPECTED_HEADER_SIZE;

    for (let i = 0; i < TOTAL_SAMPLES; i++) {
        const qVal = dataView.getInt16(byteOffset, true);
        byteOffset += 2;

        if (qVal === NODATA_INT16) {
            elevations[i] = NaN;
        } else {
            elevations[i] = offset + qVal * scale;
        }
    }

    // 4. Create copy of index buffer for zero-copy transfer
    const indices = new Uint16Array(SHARED_INDEX_TEMPLATE);

    return {
        header: {
            z,
            x,
            y,
            gridWidth,
            gridHeight,
            sampleCount,
            minElevation,
            maxElevation,
            offset,
            scale,
            key: `${z}/${x}/${y}`,
        },
        elevations,
        indices,
    };
}

/**
 * Worker message dispatcher.
 */
if (typeof self !== 'undefined') {
    self.onmessage = async function (e) {
        const { msgId, action, url, tileKey } = e.data;

        if (action === 'FETCH_AND_DECODE') {
            try {
                const response = await fetch(url);
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status} fetching terrain tile ${tileKey}`);
                }
                const arrayBuffer = await response.arrayBuffer();
                const decoded = decodeHyelevBinary(arrayBuffer);

                // Transfer elevation and index buffers with zero copy
                self.postMessage(
                    {
                        msgId,
                        success: true,
                        tileKey,
                        header: decoded.header,
                        elevations: decoded.elevations,
                        indices: decoded.indices,
                    },
                    [decoded.elevations.buffer, decoded.indices.buffer]
                );
            } catch (err) {
                self.postMessage({
                    msgId,
                    success: false,
                    tileKey,
                    error: err.message || String(err),
                });
            }
        } else if (action === 'DECODE_BUFFER') {
            try {
                const arrayBuffer = e.data.buffer;
                const decoded = decodeHyelevBinary(arrayBuffer);

                self.postMessage(
                    {
                        msgId,
                        success: true,
                        tileKey,
                        header: decoded.header,
                        elevations: decoded.elevations,
                        indices: decoded.indices,
                    },
                    [decoded.elevations.buffer, decoded.indices.buffer]
                );
            } catch (err) {
                self.postMessage({
                    msgId,
                    success: false,
                    tileKey,
                    error: err.message || String(err),
                });
            }
        }
    };
}

// Export for Node/testing environment
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        decodeHyelevBinary,
        generateTileIndexBuffer,
        VERTEX_GRID_SIZE,
        CELL_GRID_SIZE,
        TOTAL_SAMPLES,
        EXPECTED_FILE_SIZE,
    };
}
