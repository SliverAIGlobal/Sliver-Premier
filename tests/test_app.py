"""Comprehensive verification test suite for Sliver Kids WASM Coloring Studio v2 ULTRA."""

import os
import re
import json
import base64
import pytest
from pathlib import Path


def test_core_files_exist():
    required_files = [
        "index.html",
        "styles.css",
        "app.js",
        "audio-fx.js",
        "pages-data.js",
        "stickers-data.js",
        "wasm-engine.js",
        "sw.js",
        "manifest.json",
        "MARKETING_COPY.md",
        "package.sh",
        "netlify.toml",
        ".github/workflows/deploy.yml",
        "static/wasm/wasm_decolorizer.wasm",
    ]
    for rf in required_files:
        assert Path(rf).exists(), f"Missing required file: {rf}"


def test_120_vector_pages_dataset():
    with open("pages-data.js", "r", encoding="utf-8") as f:
        content = f.read()

    # Match JSON from window.COLORING_PAGES
    match = re.search(r"window\.COLORING_PAGES\s*=\s*(\[.*?\]);", content, re.DOTALL)
    assert match, "window.COLORING_PAGES definition not found"
    pages = json.loads(match.group(1))

    assert len(pages) == 120, f"Expected 120 coloring pages, found {len(pages)}"

    # Check 10 themed packs are represented with exactly 12 pages each
    pack_counts = {}
    for p in pages:
        assert "id" in p and p["id"]
        assert "title" in p and p["title"]
        assert "packId" in p and p["packId"]
        assert "difficulty" in p and p["difficulty"] in ("junior", "adult")
        assert "svg" in p and "<svg" in p["svg"]
        pack_counts[p["packId"]] = pack_counts.get(p["packId"], 0) + 1

    expected_packs = [
        "dinosaurs",
        "space",
        "ocean",
        "safari",
        "fairytales",
        "vehicles",
        "island",
        "robots",
        "sweets",
        "mandalas",
    ]
    assert len(pack_counts) == 10, f"Expected 10 packs, found {len(pack_counts)}"
    for ep in expected_packs:
        assert pack_counts.get(ep) == 12, f"Pack {ep} does not have 12 pages (has {pack_counts.get(ep)})"


def test_60_stickers_dataset():
    with open("stickers-data.js", "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(r"window\.STICKERS_DATA\s*=\s*(\[.*?\]);", content, re.DOTALL)
    assert match, "window.STICKERS_DATA definition not found"
    stickers = json.loads(match.group(1))

    assert len(stickers) == 60, f"Expected 60 stickers, found {len(stickers)}"

    # Check 6 categories with 10 stickers each
    cat_counts = {}
    for s in stickers:
        assert "id" in s and s["id"]
        assert "category" in s and s["category"]
        assert "name" in s and s["name"]
        assert "svg" in s and "<svg" in s["svg"]
        cat_counts[s["category"]] = cat_counts.get(s["category"], 0) + 1

    expected_cats = [
        "stars_magic",
        "cute_animals",
        "yummy_snacks",
        "toys_gadgets",
        "expressive_moods",
        "dinos_nature",
    ]
    assert len(cat_counts) == 6, f"Expected 6 categories, found {len(cat_counts)}"
    for ec in expected_cats:
        assert cat_counts.get(ec) == 10, f"Category {ec} does not have 10 stickers (has {cat_counts.get(ec)})"


def test_wasm_binary_and_base64_sync():
    wasm_path = Path("static/wasm/wasm_decolorizer.wasm")
    assert wasm_path.exists()
    binary_data = wasm_path.read_bytes()
    assert len(binary_data) > 10000, "WASM binary seems incomplete"

    # Magic header \0asm
    assert binary_data[:4] == b"\x00asm", "Invalid WASM magic header"

    with open("wasm_base64.txt", "r") as f:
        b64 = f.read().strip()

    decoded = base64.b64decode(b64)
    assert decoded == binary_data, "Base64 payload does not match binary wasm module"

    # Ensure index.html embeds the base64 string for file:// offline operation
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    assert b64 in html, "index.html does not embed current wasm base64 string"


def test_audio_fx_synthesizer():
    with open("audio-fx.js", "r", encoding="utf-8") as f:
        audio_js = f.read()

    assert "class SoundEngine" in audio_js
    assert "playBucketPop" in audio_js
    assert "playBrushSwoosh" in audio_js
    assert "playStickerChime" in audio_js
    assert "playFanfare" in audio_js
    assert "startBGM" in audio_js
    assert "stopBGM" in audio_js
    # Zero external audio assets
    assert ".mp3" not in audio_js
    assert ".wav" not in audio_js


def test_manifest_and_pwa_serviceworker():
    with open("manifest.json", "r", encoding="utf-8") as f:
        manifest = json.load(f)
    assert manifest["short_name"] == "ColoringStudio"
    assert manifest["display"] == "standalone"

    with open("sw.js", "r", encoding="utf-8") as f:
        sw = f.read()
    assert "caches.open" in sw
    assert "wasm_decolorizer.wasm" in sw


def test_package_script_execution():
    import subprocess
    res = subprocess.run(["./package.sh"], capture_output=True, text=True)
    assert res.returncode == 0, f"package.sh failed: {res.stderr}"

    zip_path = Path("release/sliver-kids-wasm-coloring-studio-v2.zip")
    assert zip_path.exists()
    assert zip_path.stat().st_size > 50000, "Release zip is smaller than expected"

    sha256_path = Path("release/SHA256SUMS.txt")
    md5_path = Path("release/MD5SUMS.txt")
    assert sha256_path.exists()
    assert md5_path.exists()
