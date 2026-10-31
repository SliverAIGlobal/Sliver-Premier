import os
import zipfile
import pytest

def test_v2_files_exist():
    base_dir = "sliver-kids-wasm-coloring-studio-v2"
    assert os.path.exists(os.path.join(base_dir, "index.html"))
    assert os.path.exists(os.path.join(base_dir, "app.js"))
    assert os.path.exists(os.path.join(base_dir, "styles.css"))
    assert os.path.exists(os.path.join(base_dir, "wasm-engine.js"))
    assert os.path.exists(os.path.join(base_dir, "audio-fx.js"))
    assert os.path.exists(os.path.join(base_dir, "pages-data.js"))
    assert os.path.exists(os.path.join(base_dir, "stickers-data.js"))
    assert os.path.exists(os.path.join(base_dir, "manifest.json"))
    assert os.path.exists(os.path.join(base_dir, "sw.js"))

def test_v2_zip_archive():
    zip_path = "sliver-kids-wasm-coloring-studio-v2.zip"
    assert os.path.exists(zip_path)
    with zipfile.ZipFile(zip_path, "r") as z:
        namelist = z.namelist()
        assert "sliver-kids-wasm-coloring-studio-v2/index.html" in namelist
        assert "sliver-kids-wasm-coloring-studio-v2/pages-data.js" in namelist
        assert "sliver-kids-wasm-coloring-studio-v2/stickers-data.js" in namelist
        assert "sliver-kids-wasm-coloring-studio-v2/wasm-engine.js" in namelist

def test_vector_counts_in_files():
    with open("sliver-kids-wasm-coloring-studio-v2/pages-data.js", "r") as f:
        content = f.read()
        assert "COLORING_PACKS" in content
        for pack in ["dinos", "space", "ocean", "safari", "fantasy", "vehicles", "island", "robots", "sweets", "mandalas"]:
            assert f'"{pack}"' in content

    with open("sliver-kids-wasm-coloring-studio-v2/stickers-data.js", "r") as f:
        content = f.read()
        assert "STICKER_CATEGORIES" in content
        for cat in ["stars", "animals", "snacks", "toys", "moods", "nature"]:
            assert f'"{cat}"' in content
