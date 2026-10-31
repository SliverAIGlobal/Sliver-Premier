// Privacy-First WASM Decolorizer Core Engine
// zero dependencies, no_std friendly, pure safe computational buffers

#[no_mangle]
pub extern "C" fn alloc_buffer(size: usize) -> *mut u8 {
    let mut vec = Vec::with_capacity(size);
    let ptr = vec.as_mut_ptr();
    std::mem::forget(vec);
    ptr
}

#[no_mangle]
pub extern "C" fn free_buffer(ptr: *mut u8, size: usize) {
    if !ptr.is_null() {
        unsafe {
            let _ = Vec::from_raw_parts(ptr, 0, size);
        }
    }
}

/// Convert RGBA image to coloring outline (White background with black outlines).
///
/// Parameters:
/// - `input_ptr`: Pointer to raw RGBA8 input bytes (width * height * 4)
/// - `output_ptr`: Pointer to raw RGBA8 output bytes (width * height * 4)
/// - `width`: Image width in pixels
/// - `height`: Image height in pixels
/// - `threshold`: Line sensitivity threshold (1 to 255, default ~40)
/// - `thickness`: Outlines dilation radius (0 for 1px, 1 for ~3px, 2 for ~5px)
/// - `contrast`: Detail / contrast scale factor (1.0 to 5.0, scaled as integer fixed-point x100, e.g. 150 = 1.5x)
/// - `invert_mode`: 0 = black lines on white paper (standard coloring page), 1 = white lines on black
#[no_mangle]
pub extern "C" fn decolorize(
    input_ptr: *const u8,
    output_ptr: *mut u8,
    width: usize,
    height: usize,
    threshold: u8,
    thickness: u8,
    contrast: u16,
    invert_mode: u8,
) {
    if input_ptr.is_null() || output_ptr.is_null() || width == 0 || height == 0 {
        return;
    }

    let total_pixels = width * height;
    let input_slice = unsafe { std::slice::from_raw_parts(input_ptr, total_pixels * 4) };
    let output_slice = unsafe { std::slice::from_raw_parts_mut(output_ptr, total_pixels * 4) };

    // Step 1: Grayscale Luminance Conversion + Contrast Adjustment
    let mut gray = Vec::with_capacity(total_pixels);
    let contrast_factor = if contrast == 0 { 100 } else { contrast as i32 };

    for i in 0..total_pixels {
        let r = input_slice[i * 4] as i32;
        let g = input_slice[i * 4 + 1] as i32;
        let b = input_slice[i * 4 + 2] as i32;
        // ITU-R BT.601 standard luminance: 0.299 R + 0.587 G + 0.114 B
        let lum = (r * 299 + g * 587 + b * 114) / 1000;

        // Contrast scaling centered at mid-gray (128)
        let mut adjusted = ((lum - 128) * contrast_factor) / 100 + 128;
        if adjusted < 0 {
            adjusted = 0;
        } else if adjusted > 255 {
            adjusted = 255;
        }
        gray.push(adjusted as u8);
    }

    // Step 2: 3x3 Separable Gaussian Blur (Noise Reduction)
    // Kernel: [1, 2, 1] / 4 horizontally and vertically
    let mut blurred_h = vec![0u8; total_pixels];
    for y in 0..height {
        let row_offset = y * width;
        for x in 0..width {
            let left = if x > 0 { gray[row_offset + x - 1] as u32 } else { gray[row_offset + x] as u32 };
            let center = gray[row_offset + x] as u32;
            let right = if x + 1 < width { gray[row_offset + x + 1] as u32 } else { gray[row_offset + x] as u32 };
            blurred_h[row_offset + x] = ((left + center * 2 + right + 2) / 4) as u8;
        }
    }

    let mut blurred = vec![0u8; total_pixels];
    for y in 0..height {
        let up_offset = if y > 0 { (y - 1) * width } else { y * width };
        let cur_offset = y * width;
        let down_offset = if y + 1 < height { (y + 1) * width } else { y * width };
        for x in 0..width {
            let up = blurred_h[up_offset + x] as u32;
            let cur = blurred_h[cur_offset + x] as u32;
            let down = blurred_h[down_offset + x] as u32;
            blurred[cur_offset + x] = ((up + cur * 2 + down + 2) / 4) as u8;
        }
    }

    // Step 3: Sobel 3x3 Edge Detection + Laplacian Gradient
    // Sobel Gx:
    // [-1  0 +1]
    // [-2  0 +2]
    // [-1  0 +1]
    // Sobel Gy:
    // [-1 -2 -1]
    // [ 0  0  0]
    // [+1 +2 +1]
    let mut edges = vec![0u8; total_pixels];
    let thresh_val = threshold as i32;

    for y in 1..(height.saturating_sub(1)) {
        let y_prev = (y - 1) * width;
        let y_curr = y * width;
        let y_next = (y + 1) * width;

        for x in 1..(width.saturating_sub(1)) {
            let p00 = blurred[y_prev + x - 1] as i32;
            let p01 = blurred[y_prev + x] as i32;
            let p02 = blurred[y_prev + x + 1] as i32;

            let p10 = blurred[y_curr + x - 1] as i32;
            let p12 = blurred[y_curr + x + 1] as i32;

            let p20 = blurred[y_next + x - 1] as i32;
            let p21 = blurred[y_next + x] as i32;
            let p22 = blurred[y_next + x + 1] as i32;

            let gx = (p02 + 2 * p12 + p22) - (p00 + 2 * p10 + p20);
            let gy = (p20 + 2 * p21 + p22) - (p00 + 2 * p01 + p02);

            // Manhattan approximation or L1 norm for speed and sharp borders
            let magnitude = gx.abs() + gy.abs();

            if magnitude >= thresh_val {
                edges[y_curr + x] = 255;
            } else {
                edges[y_curr + x] = 0;
            }
        }
    }

    // Step 4: Morphological Dilation (Thickness Control)
    let final_edges = if thickness > 0 {
        let rad = thickness as isize;
        let mut dilated = vec![0u8; total_pixels];
        for y in 0..height {
            let y_isize = y as isize;
            for x in 0..width {
                let x_isize = x as isize;
                let mut is_edge = false;
                'radius_search: for dy in -rad..=rad {
                    let ny = y_isize + dy;
                    if ny < 0 || ny >= height as isize {
                        continue;
                    }
                    let ny_offset = (ny as usize) * width;
                    for dx in -rad..=rad {
                        let nx = x_isize + dx;
                        if nx < 0 || nx >= width as isize {
                            continue;
                        }
                        if edges[ny_offset + (nx as usize)] == 255 {
                            is_edge = true;
                            break 'radius_search;
                        }
                    }
                }
                dilated[y * width + x] = if is_edge { 255 } else { 0 };
            }
        }
        dilated
    } else {
        edges
    };

    // Step 5: Render to RGBA Output
    // Standard coloring book mode: White background (255, 255, 255, 255), Black lines (0, 0, 0, 255)
    // Invert mode: Black background, White lines
    let (line_val, bg_val) = if invert_mode == 0 {
        (0u8, 255u8) // Black on white
    } else {
        (255u8, 0u8) // White on black
    };

    for i in 0..total_pixels {
        let is_edge = final_edges[i] == 255;
        let color = if is_edge { line_val } else { bg_val };
        let offset = i * 4;
        output_slice[offset] = color;
        output_slice[offset + 1] = color;
        output_slice[offset + 2] = color;
        output_slice[offset + 3] = 255; // Full alpha opacity
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_alloc_and_free() {
        let size = 1024;
        let ptr = alloc_buffer(size);
        assert!(!ptr.is_null());
        unsafe {
            *ptr = 42;
            assert_eq!(*ptr, 42);
        }
        free_buffer(ptr, size);
    }

    #[test]
    fn test_decolorize_synthetic_pattern() {
        let width = 10;
        let height = 10;
        let mut input = vec![0u8; width * height * 4];
        let mut output = vec![0u8; width * height * 4];

        // Create a black square inside a white canvas
        for y in 0..height {
            for x in 0..width {
                let idx = (y * width + x) * 4;
                if x >= 3 && x <= 6 && y >= 3 && y <= 6 {
                    input[idx] = 0;
                    input[idx + 1] = 0;
                    input[idx + 2] = 0;
                    input[idx + 3] = 255;
                } else {
                    input[idx] = 255;
                    input[idx + 1] = 255;
                    input[idx + 2] = 255;
                    input[idx + 3] = 255;
                }
            }
        }

        decolorize(
            input.as_ptr(),
            output.as_mut_ptr(),
            width,
            height,
            30, // threshold
            0,  // thickness
            100, // 1.0x contrast
            0,  // standard coloring book (black lines on white)
        );

        // Check corners are white background
        assert_eq!(output[0], 255); // Top-left is white
        assert_eq!(output[1], 255);
        assert_eq!(output[2], 255);
        assert_eq!(output[3], 255);

        // Check that some edge pixels were detected (black, 0,0,0,255)
        let mut edge_detected = false;
        for i in 0..(width * height) {
            if output[i * 4] == 0 && output[i * 4 + 3] == 255 {
                edge_detected = true;
                break;
            }
        }
        assert!(edge_detected, "Sobel filter should have detected boundary edges of the square");
    }

    #[test]
    fn test_invert_mode() {
        let width = 8;
        let height = 8;
        let mut input = vec![255u8; width * height * 4];
        let mut output = vec![0u8; width * height * 4];

        // Diagonal line
        for i in 0..8 {
            let idx = (i * width + i) * 4;
            input[idx] = 0;
            input[idx + 1] = 0;
            input[idx + 2] = 0;
        }

        decolorize(
            input.as_ptr(),
            output.as_mut_ptr(),
            width,
            height,
            20,
            0,
            100,
            1, // Invert mode: white lines on black background
        );

        // Non-edge should be black (0)
        assert_eq!(output[0], 0);
    }
}
