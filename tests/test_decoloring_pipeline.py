"""
Unit Test Suite: Sobel 3x3 CV Edge Detection, Low-Pass Tremor Filter, & Pigment Database
"""

import math
import pytest

BIOLOGICAL_PIGMENTS = {
    "chlorophyll_a": "#2E7D32",
    "chlorophyll_b": "#81C784",
    "carotenoid_gold": "#FFB300",
    "scute_amber": "#C67D0A",
    "luciferin_glow": "#76FF03",
    "iridophore_cyan": "#00F2FE",
    "anthocyanin_violet": "#7E22CE",
    "tannin_bark_rust": "#9A3412",
    "cellulose_white": "#F8FAFC",
    "pollen_ochre": "#F59E0B",
    "basalt_obsidian": "#0F172A",
    "xanthophyll_yellow": "#FDE047"
}

def perceptual_luminance(r: int, g: int, b: int) -> int:
    """BT.601 perceptual luminance formula Y = 0.299R + 0.587G + 0.114B"""
    return int(round(0.299 * r + 0.587 * g + 0.114 * b))

def apply_sobel_3x3_pixel(patch):
    gx = (-1 * patch[0][0] + 1 * patch[0][2] +
          -2 * patch[1][0] + 2 * patch[1][2] +
          -1 * patch[2][0] + 1 * patch[2][2])

    gy = (-1 * patch[0][0] - 2 * patch[0][1] - 1 * patch[0][2] +
           1 * patch[2][0] + 2 * patch[2][1] + 1 * patch[2][2])

    magnitude = math.sqrt(gx * gx + gy * gy)
    return min(255, int(magnitude))

def low_pass_filter_step(current_x: float, prev_x: float, alpha: float = 0.25) -> float:
    return alpha * current_x + (1.0 - alpha) * prev_x

def evaluate_precision_secret_unlock(drawn_pixels: int, target_pixels: int) -> bool:
    """Returns True if drawn precision reaches >= 90% threshold for Secret Bio-Glow upgrade."""
    ratio = drawn_pixels / max(1, target_pixels)
    return (ratio * 100) >= 90.0

def test_perceptual_luminance_bt601():
    assert perceptual_luminance(255, 255, 255) == 255
    assert perceptual_luminance(0, 0, 0) == 0
    assert perceptual_luminance(100, 200, 50) == 153

def test_sobel_3x3_gradient():
    patch_vertical_edge = [
        [0, 0, 255],
        [0, 0, 255],
        [0, 0, 255]
    ]
    mag = apply_sobel_3x3_pixel(patch_vertical_edge)
    assert mag > 100

def test_somatic_tremor_filter():
    smoothed = low_pass_filter_step(current_x=100.0, prev_x=0.0, alpha=0.25)
    assert smoothed == 25.0

def test_biological_pigments_database():
    assert len(BIOLOGICAL_PIGMENTS) >= 12
    assert "chlorophyll_a" in BIOLOGICAL_PIGMENTS
    assert BIOLOGICAL_PIGMENTS["iridophore_cyan"] == "#00F2FE"
    assert "xanthophyll_yellow" in BIOLOGICAL_PIGMENTS

def test_precision_secret_unlock_trigger():
    assert evaluate_precision_secret_unlock(95, 100) is True
    assert evaluate_precision_secret_unlock(50, 100) is False


def test_specimens_data_pure_biological_uniqueness():
    import json
    with open("specimens_data.json") as f:
        data = json.load(f)
    assert len(data) == 100
    titles = [x["title"] for x in data]
    assert len(titles) == len(set(titles)), "Specimens must have unique titles"
    # Verify no astronomy entries
    for x in data:
        assert x.get("category") != "Astronomy & Earth Systems", f"Non-biological category found: {x.get('category')}"
        assert not x.get("imageUrl", "").startswith("https://images.unsplash.com"), "No repeating external urls allowed"
