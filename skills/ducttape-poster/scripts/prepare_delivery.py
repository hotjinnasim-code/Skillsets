#!/usr/bin/env python3
"""Prepare a poster answer from explicit selections; never generate or alter images."""

import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import struct
import sys
from urllib.parse import urlsplit
import zlib


def positive(value):
    return type(value) is int and value > 0


def safe_ref(value):
    if not isinstance(value, str) or not value.strip() or value != value.strip():
        raise ValueError("references must be nonempty strings without outer whitespace")
    if len(value.splitlines()) != 1 or any(ord(c) < 32 or ord(c) == 127 for c in value) or any(c in value for c in "<>\\"):
        raise ValueError("references cannot contain control characters, HTML, or backslashes")
    scheme = urlsplit(value).scheme.lower()
    if scheme in {"data", "javascript", "vbscript", "file"}:
        raise ValueError("unsafe or unsupported reference scheme: " + scheme)
    if scheme in {"http", "https"} and not urlsplit(value).netloc:
        raise ValueError("HTTP references require a host")
    return value


def validate(manifest):
    if not isinstance(manifest, dict) or not positive(manifest.get("requested_count")):
        raise ValueError("requested_count must be a positive integer")
    if manifest.get("reference_mode") not in {"local", "dialog"}:
        raise ValueError("reference_mode must be local or dialog")
    items = manifest.get("items")
    if not isinstance(items, list) or len(items) != manifest["requested_count"]:
        raise ValueError("items must contain exactly requested_count roles")
    ids = set()
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("each item must be an object")
        for key in ("id", "label"):
            if not isinstance(item.get(key), str) or not item[key].strip():
                raise ValueError(key + " must be a nonempty string")
        if item["id"] in ids:
            raise ValueError("item ids must be unique")
        ids.add(item["id"])
        if item.get("selection") == "none":
            if not isinstance(item.get("reason"), str) or not item["reason"].strip():
                raise ValueError("NONE roles require a nonempty reason")
            if any(k in item for k in ("original_path", "display_ref", "download_ref", "width", "height")):
                raise ValueError("NONE roles cannot carry a completed image or card")
            continue
        if item.get("selection") != "selected":
            raise ValueError("selection must be selected or none")
        if "original_path" in item:
            path = item["original_path"]
            if not isinstance(path, str) or not Path(path).is_absolute():
                raise ValueError("original_path must be an absolute path")
            safe_ref(path)
        if manifest["reference_mode"] == "local" and "original_path" not in item:
            raise ValueError("local selected roles require original_path")
        for key in ("display_ref", "download_ref"):
            if key in item and item[key] is not None:
                safe_ref(item[key])
        if ("width" in item) != ("height" in item):
            raise ValueError("width and height must be supplied together")
        if "width" in item and not all(positive(item[k]) for k in ("width", "height")):
            raise ValueError("dimensions must be positive integers")
    return manifest


def png_size(data):
    offset, size, idat, ended = 8, None, False, False
    while offset + 12 <= len(data):
        length = struct.unpack_from(">I", data, offset)[0]
        kind = data[offset + 4:offset + 8]
        end = offset + 12 + length
        if end > len(data):
            raise ValueError("truncated PNG chunk")
        body = data[offset + 8:end - 4]
        if zlib.crc32(kind + body) & 0xffffffff != struct.unpack_from(">I", data, end - 4)[0]:
            raise ValueError("PNG checksum mismatch")
        if size is None:
            if kind != b"IHDR" or length != 13:
                raise ValueError("missing PNG header")
            w, h, depth, color, compression, filtering, interlace = struct.unpack(">IIBBBBB", body)
            depths = {0: {1, 2, 4, 8, 16}, 2: {8, 16}, 3: {1, 2, 4, 8}, 4: {8, 16}, 6: {8, 16}}
            if not w or not h or depth not in depths.get(color, set()) or compression or filtering or interlace > 1:
                raise ValueError("invalid PNG header")
            size = (w, h)
        elif kind == b"IHDR":
            raise ValueError("duplicate PNG header")
        if kind == b"IDAT" and body:
            idat = True
        if kind == b"IEND":
            ended = length == 0 and end == len(data)
            break
        offset = end
    if not size or not idat or not ended:
        raise ValueError("incomplete PNG image")
    return size


def jpeg_size(data):
    offset, size, scan = 2, None, False
    while offset < len(data):
        if data[offset] != 255:
            raise ValueError("invalid JPEG marker")
        while offset < len(data) and data[offset] == 255:
            offset += 1
        if offset >= len(data):
            break
        marker, offset = data[offset], offset + 1
        if marker == 0xd9:
            if size and scan and offset == len(data):
                return size
            break
        if marker in {0, 0xd8} or 0xd0 <= marker <= 0xd7:
            raise ValueError("unexpected JPEG marker")
        if marker == 1:
            continue
        if offset + 2 > len(data):
            break
        length = struct.unpack_from(">H", data, offset)[0]
        end = offset + length
        if length < 2 or end > len(data):
            raise ValueError("truncated JPEG segment")
        if marker in {0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf}:
            if length < 11 or length != 8 + 3 * data[offset + 7]:
                raise ValueError("invalid JPEG frame")
            h, w = struct.unpack_from(">HH", data, offset + 3)
            if not w or not h or size and size != (w, h):
                raise ValueError("invalid JPEG dimensions")
            size = (w, h)
        offset = end
        if marker == 0xda:
            if not size or length < 6:
                raise ValueError("invalid JPEG scan")
            scan, start = True, offset
            while offset < len(data):
                if data[offset] != 255:
                    offset += 1
                    continue
                next_byte = offset + 1
                while next_byte < len(data) and data[next_byte] == 255:
                    next_byte += 1
                if next_byte == len(data):
                    break
                if data[next_byte] == 0 or 0xd0 <= data[next_byte] <= 0xd7:
                    offset = next_byte + 1
                else:
                    break
            if offset == start:
                raise ValueError("empty JPEG scan")
    raise ValueError("incomplete JPEG image")


def webp_size(data):
    if len(data) < 20 or struct.unpack_from("<I", data, 4)[0] + 8 != len(data):
        raise ValueError("truncated or invalid WebP container")
    offset, canvas, size = 12, None, None
    while offset + 8 <= len(data):
        kind, length = data[offset:offset + 4], struct.unpack_from("<I", data, offset + 4)[0]
        end = offset + 8 + length
        if end + (length & 1) > len(data):
            raise ValueError("truncated WebP chunk")
        body = data[offset + 8:end]
        if kind == b"VP8X":
            if length != 10 or body[0] & 2:
                raise ValueError("invalid or unsupported animated WebP")
            canvas = tuple(int.from_bytes(body[i:i + 3], "little") + 1 for i in (4, 7))
        elif kind == b"VP8 ":
            if length <= 10 or body[0] & 1 or body[3:6] != b"\x9d\x01\x2a":
                raise ValueError("invalid WebP VP8 frame")
            size = tuple(v & 0x3fff for v in struct.unpack_from("<HH", body, 6))
        elif kind == b"VP8L":
            if length <= 5 or body[0] != 0x2f:
                raise ValueError("invalid WebP lossless frame")
            bits = int.from_bytes(body[1:5], "little")
            if bits >> 29:
                raise ValueError("invalid WebP lossless version")
            size = ((bits & 0x3fff) + 1, ((bits >> 14) & 0x3fff) + 1)
        offset = end + (length & 1)
    if offset != len(data) or not size or not all(size) or canvas and canvas != size:
        raise ValueError("incomplete or inconsistent WebP image")
    return size


def inspect_image(path):
    result = {"path": path, "availability": "unavailable"}
    try:
        data = Path(path).read_bytes()
    except OSError as exc:
        result["detail"] = "source check unavailable: " + str(exc)
        return result
    result.update(sha256=hashlib.sha256(data).hexdigest(), byte_count=len(data))
    try:
        if data.startswith(b"\x89PNG\r\n\x1a\n"):
            format_name, size = "PNG", png_size(data)
        elif data.startswith(b"\xff\xd8"):
            format_name, size = "JPEG", jpeg_size(data)
        elif data.startswith(b"RIFF") and data[8:12] == b"WEBP":
            format_name, size = "WebP", webp_size(data)
        else:
            raise ValueError("unsupported or invalid image; supported: PNG, JPEG, static WebP")
        result.update(availability="checked", format=format_name, width=size[0], height=size[1])
    except (ValueError, struct.error, IndexError) as exc:
        result.update(availability="rejected", detail=str(exc))
    return result


def text(value):
    value = html.escape(" ".join(value.split()), quote=False)
    return re.sub(r"([\\`*_{}\[\]()#+.!|\-])", r"\\\1", value)


def prepare(item, mode):
    row = {"id": item["id"], "label": item["label"], "selection": item["selection"]}
    title = text(item["label"]) + " (" + text(item["id"]) + ")"
    if item["selection"] == "none":
        row.update(status="unresolved", reason=item["reason"], source={"availability": "not_selected"},
                   display={"availability": "not_selected"}, download={"availability": "not_selected"})
        return row, title + ": 미해결 — " + text(item["reason"]) + "."
    source = inspect_image(item["original_path"]) if "original_path" in item else {"availability": "unavailable", "detail": "no original_path supplied"}
    row["source"], errors = source, []
    if source["availability"] == "rejected" or mode == "local" and source["availability"] != "checked":
        errors.append(source.get("detail", "original source unavailable"))
    actual = (source.get("width"), source.get("height"))
    declared = (item.get("width"), item.get("height"))
    if source["availability"] == "checked" and declared[0] and declared != actual:
        errors.append("declared dimensions do not match the selected original")
    size = actual if source["availability"] == "checked" else declared
    if not all(size):
        errors.append("original pixel dimensions unavailable; supply width and height")
    for key, role in (("display_ref", "display"), ("download_ref", "download")):
        ref = item.get(key, item.get("original_path") if mode == "local" else None)
        state = {"ref": ref, "availability": "unavailable"}
        if mode == "local" and ref and Path(ref).is_absolute():
            checked = inspect_image(ref)
            state.update(checked)
            if checked["availability"] != "checked":
                errors.append(role + " image unavailable: " + checked.get("detail", "check failed"))
            elif role == "download" and checked.get("sha256") != source.get("sha256"):
                state.update(availability="rejected", detail="download bytes do not match selected original")
                errors.append(state["detail"])
        elif mode == "dialog" and ref and urlsplit(ref).scheme:
            state.update(availability="supplied_unverified", detail="explicit dialog reference; remote accessibility not checked")
        else:
            errors.append(role + " reference unavailable for " + mode + " mode")
        row[role] = state
    row.update(status="blocked" if errors else "prepared", width=size[0], height=size[1], errors=errors)
    if errors:
        return row, title + ": 미해결 — 선택 원본의 파일·참조·크기를 확보해야 전달할 수 있습니다."
    return row, (title + "\n\n"
                 + f"![{text(item['label'])}](<{row['display']['ref']}>)\n\n"
                 + f"[원본 다운로드](<{row['download']['ref']}>) · {size[0]} × {size[1]} px")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    try:
        manifest = validate(json.loads(args.manifest.read_text(encoding="utf-8")))
        if args.output_dir.exists() or args.output_dir.is_symlink():
            raise ValueError("output directory must be fresh; refusing to overwrite")
        rows, cards = zip(*(prepare(item, manifest["reference_mode"]) for item in manifest["items"]))
        counts = {"requested": manifest["requested_count"], "selected": sum(r["selection"] == "selected" for r in rows),
                  "prepared": sum(r["status"] == "prepared" for r in rows),
                  "none": sum(r["status"] == "unresolved" for r in rows), "blocked": sum(r["status"] == "blocked" for r in rows)}
        status = "NOT_READY" if counts["blocked"] else "PARTIAL" if counts["none"] else "READY"
        report = {"status": status, "reference_mode": manifest["reference_mode"], "counts": counts,
                  "meaning": "Answer prepared only; display and download in the user conversation are not confirmed.",
                  "checks": "Local file bytes, SHA-256, container structure and header dimensions only; no full image decoding or visual review.",
                  "items": rows}
        response = "\n\n".join(cards) + "\n"
        args.output_dir.mkdir(parents=True, exist_ok=False)
        for name, content in (("response.md", response), ("delivery.json", json.dumps(report, ensure_ascii=False, indent=2) + "\n")):
            with (args.output_dir / name).open("x", encoding="utf-8") as handle:
                handle.write(content)
        print(response, end="")
        return 2 if status == "NOT_READY" else 0
    except (ValueError, OSError, TypeError) as exc:
        print("prepare_delivery: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
