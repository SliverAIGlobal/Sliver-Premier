"""
Unit Test Suite: Sobel 3x3 CV Edge Detection & Low-Pass Tremor Filter
"""

import math
import pytest

def perceptual_luminance(r: int, g: int, b: int) -> int:
    """BT.601 perceptual luminance formula Y = 0.299R + 0.587G + 0.114B"""
    return int(round(0.299 * r + 0.587 * g + 0.114 * b))

def apply_sobel_3x3_pixel(patch):
    """
    Applies 3x3 Sobel matrix operators Gx and Gy to a 3x3 luminance patch.
    Gx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    Gy = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
    """
    gx = (-1 * patch[0][0] + 1 * patch[0][2] +
          -2 * patch[1][0] + 2 * patch[1][2] +
          -1 * patch[2][0] + 1 * patch[2][2])

    gy = (-1 * patch[0][0] - 2 * patch[0][1] - 1 * patch[0][2] +
           1 * patch[2][0] + 2 * patch[2][1] + 1 * patch[2][2])

    magnitude = math.sqrt(gx * gx + gy * gy)
    return min(255, int(magnitude))

def low_pass_filter_step(current_x: float, prev_x: float, alpha: float = 0.25) -> float:
    """S_t = alpha * X_t + (1 - alpha) * S_{t-1}"""
    return alpha * current_x + (1.0 - alpha) * prev_x

def test_perceptual_luminance_bt601():
    assert perceptual_luminance(255, 255, 255) == 255
    assert perceptual_luminance(0, 0, 0) == 0
    # RGB(100, 200, 50) => 0.299*100 + 0.587*200 + 0.114*50 = 29.9 + 117.4 + 5.7 = 153.0
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
