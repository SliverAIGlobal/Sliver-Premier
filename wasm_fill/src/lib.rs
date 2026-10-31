#![no_std]

#[cfg(target_arch = "wasm32")]
#[panic_handler]
fn panic(_info: &core::panic::PanicInfo) -> ! {
    core::arch::wasm32::unreachable();
}

#[cfg(not(target_arch = "wasm32"))]
extern crate std;

/// Color distance tolerance helper
#[inline(always)]
fn color_match(c1: u32, c2: u32, tolerance: u32) -> bool {
    if c1 == c2 {
        return true;
    }
    if tolerance == 0 {
        return false;
    }

    let r1 = (c1 & 0xFF) as i32;
    let g1 = ((c1 >> 8) & 0xFF) as i32;
    let b1 = ((c1 >> 16) & 0xFF) as i32;
    let a1 = ((c1 >> 24) & 0xFF) as i32;

    let r2 = (c2 & 0xFF) as i32;
    let g2 = ((c2 >> 8) & 0xFF) as i32;
    let b2 = ((c2 >> 16) & 0xFF) as i32;
    let a2 = ((c2 >> 24) & 0xFF) as i32;

    let dr = (r1 - r2).abs() as u32;
    let dg = (g1 - g2).abs() as u32;
    let db = (b1 - b2).abs() as u32;
    let da = (a1 - a2).abs() as u32;

    (dr + dg + db + da) <= tolerance * 4
}

/// Span-based scanline flood fill in WASM memory
/// pixels_ptr points to an array of u32 (RGBA/ABGR values) with dimensions width * height.
/// Returns number of pixels modified.
#[no_mangle]
pub extern "C" fn flood_fill(
    pixels_ptr: *mut u32,
    width: u32,
    height: u32,
    start_x: u32,
    start_y: u32,
    fill_color: u32,
    tolerance: u32,
    stack_buffer_ptr: *mut u32,
    stack_max_capacity: u32,
) -> u32 {
    if start_x >= width || start_y >= height {
        return 0;
    }

    let total_pixels = (width * height) as usize;
    let target_color = unsafe { *pixels_ptr.add((start_y * width + start_x) as usize) };

    if color_match(target_color, fill_color, 2) {
        return 0; // Already matches target color
    }

    let mut modified_count: u32 = 0;
    let mut stack_len: usize = 0;

    // Push (x, y) encoded as (y * width + x)
    unsafe {
        *stack_buffer_ptr.add(stack_len) = start_y * width + start_x;
        stack_len += 1;
    }

    while stack_len > 0 {
        stack_len -= 1;
        let index = unsafe { *stack_buffer_ptr.add(stack_len) } as usize;
        let x = (index % width as usize) as u32;
        let y = (index / width as usize) as u32;

        let current_color = unsafe { *pixels_ptr.add(index) };
        if !color_match(current_color, target_color, tolerance) {
            continue;
        }

        // Find left boundary of span
        let mut left_x = x;
        while left_x > 0 {
            let left_idx = (y * width + (left_x - 1)) as usize;
            if !color_match(unsafe { *pixels_ptr.add(left_idx) }, target_color, tolerance) {
                break;
            }
            left_x -= 1;
        }

        // Find right boundary of span
        let mut right_x = x;
        while right_x + 1 < width {
            let right_idx = (y * width + (right_x + 1)) as usize;
            if !color_match(unsafe { *pixels_ptr.add(right_idx) }, target_color, tolerance) {
                break;
            }
            right_x += 1;
        }

        // Fill current span
        for cur_x in left_x..=right_x {
            let cur_idx = (y * width + cur_x) as usize;
            unsafe {
                *pixels_ptr.add(cur_idx) = fill_color;
            }
            modified_count += 1;
        }

        // Scan row above (y - 1)
        if y > 0 {
            let scan_y = y - 1;
            let mut scan_x = left_x;
            while scan_x <= right_x {
                let scan_idx = (scan_y * width + scan_x) as usize;
                if color_match(unsafe { *pixels_ptr.add(scan_idx) }, target_color, tolerance) {
                    if (stack_len as u32) < stack_max_capacity {
                        unsafe {
                            *stack_buffer_ptr.add(stack_len) = scan_idx as u32;
                            stack_len += 1;
                        }
                    }
                    // Skip over matching run
                    while scan_x <= right_x && color_match(unsafe { *pixels_ptr.add((scan_y * width + scan_x) as usize) }, target_color, tolerance) {
                        scan_x += 1;
                    }
                } else {
                    scan_x += 1;
                }
            }
        }

        // Scan row below (y + 1)
        if y + 1 < height {
            let scan_y = y + 1;
            let mut scan_x = left_x;
            while scan_x <= right_x {
                let scan_idx = (scan_y * width + scan_x) as usize;
                if color_match(unsafe { *pixels_ptr.add(scan_idx) }, target_color, tolerance) {
                    if (stack_len as u32) < stack_max_capacity {
                        unsafe {
                            *stack_buffer_ptr.add(stack_len) = scan_idx as u32;
                            stack_len += 1;
                        }
                    }
                    // Skip over matching run
                    while scan_x <= right_x && color_match(unsafe { *pixels_ptr.add((scan_y * width + scan_x) as usize) }, target_color, tolerance) {
                        scan_x += 1;
                    }
                } else {
                    scan_x += 1;
                }
            }
        }
    }

    modified_count
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_flood_fill() {
        let width = 10u32;
        let height = 10u32;
        let mut pixels = [0xFFFFFFFFu32; 100];
        let mut stack = [0u32; 256];

        // Draw a vertical wall down column 5
        for y in 0..height {
            pixels[(y * width + 5) as usize] = 0xFF000000;
        }

        let filled = flood_fill(
            pixels.as_mut_ptr(),
            width,
            height,
            0,
            0,
            0xFF00FF00,
            5,
            stack.as_mut_ptr(),
            256,
        );

        // Should fill the 5x10 region on the left side = 50 pixels
        assert_eq!(filled, 50);
        assert_eq!(pixels[0], 0xFF00FF00);
        assert_eq!(pixels[4], 0xFF00FF00);
        assert_eq!(pixels[5], 0xFF000000); // Wall intact
        assert_eq!(pixels[6], 0xFFFFFFFF); // Right side untouched
    }
}
