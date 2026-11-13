"""Read the binary RPH layout observed in the supplied Hoeganaes export.

RPH is not a renamed CSV. Validate every boundary before interpreting samples;
unknown layouts fail explicitly instead of producing plausible-looking charts.
Source bytes are never changed. Timestamps remain UTC internally.
"""
from dataclasses import dataclass
import struct
import numpy as np


@dataclass
class Recording:
    names: list[str]
    values: np.ndarray
    seconds: np.ndarray
    gaps: int


def read_rph(raw: bytes) -> Recording:
    if len(raw) < 27 or raw[:4] != b"\x81\x07\x0f\x2c":
        raise ValueError("Unrecognized RPH format. This reader supports the supplied Hoeganaes layout.")
    columns = struct.unpack_from("<H", raw, 21)[0]
    if not 1 <= columns <= 4096:
        raise ValueError("Invalid RPH signal count.")
    offset, names = 23, []
    for _ in range(columns):
        if offset >= len(raw):
            raise ValueError("RPH signal list is truncated.")
        size = raw[offset]
        offset += 1
        if not size or offset + size > len(raw):
            raise ValueError("Invalid RPH signal name length.")
        try:
            name = raw[offset:offset + size].decode("ascii")
        except UnicodeDecodeError as exc:
            raise ValueError("Unsupported RPH signal-name encoding.") from exc
        if any(ord(c) < 32 for c in name):
            raise ValueError("RPH signal name contains control characters.")
        names.append(name)
        offset += size
    if len(set(names)) != columns or offset + 4 > len(raw):
        raise ValueError("Duplicate signal names or incomplete RPH header.")
    rows = struct.unpack_from("<I", raw, offset)[0]
    offset += 4
    stride = 2 + 4 * columns
    end = offset + rows * stride
    expected = end + 2 + rows * 12 + 4
    if rows == 0 or rows > 65535 or expected != len(raw):
        raise ValueError("RPH length does not match its sample counts; file is incomplete or uses another layout.")
    widths = np.ndarray((rows,), dtype="<u2", buffer=raw, offset=offset, strides=(stride,))
    if np.any(widths != columns) or struct.unpack_from("<H", raw, end)[0] != rows:
        raise ValueError("RPH sample widths or timestamp count do not match.")
    if raw[-4:] != b"\0" * 4:
        raise ValueError("Unsupported RPH footer.")
    values = np.ndarray((rows, columns), dtype="<f4", buffer=raw,
                        offset=offset + 2, strides=(stride, 4)).copy()
    stamps = np.ndarray((rows,), dtype=np.dtype([("s", "<u4"), ("ms", "<u2"),
                         ("bias", "<u2"), ("reserved", "<u4")]), buffer=raw, offset=end + 2)
    if np.any(stamps["ms"] >= 1000) or np.any(stamps["reserved"] != 0):
        raise ValueError("Unsupported RPH timestamp record.")
    seconds = stamps["s"].astype(float) + stamps["ms"] / 1000
    if np.any(np.diff(seconds) <= 0):
        raise ValueError("RPH timestamps are duplicated or out of order.")
    return Recording(names, values, seconds, int(np.sum(np.diff(seconds) > 5)))
