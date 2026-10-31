// Atemporal Reweaver WASM Core Engine
// Node SIPES-HI-808 High-Performance Biometrics, Audio Synthesis & Quantum Metaphor Substrate

#![no_std]

// In no_std mode, provide panic handler when targeting wasm
#[cfg(target_arch = "wasm32")]
#[panic_handler]
fn panic(_info: &core::panic::PanicInfo) -> ! {
    core::arch::wasm32::unreachable();
}

#[cfg(not(target_arch = "wasm32"))]
extern crate std;

/// Accelerated PeriSensor Biometric Drift & Entropy Calculation
/// Computes new joy, stress, and bpm given previous values and 3 pseudo-random inputs in [0, 1).
/// Writes [new_joy, new_stress, new_bpm] as 3 f32s to out_ptr.
#[no_mangle]
pub extern "C" fn compute_biometrics(
    prev_joy: f32,
    prev_stress: f32,
    prev_bpm: f32,
    rand1: f32,
    rand2: f32,
    rand3: f32,
    out_ptr: *mut f32,
) {
    let joy_drift = (rand1 - 0.48) * 3.0;
    let stress_drift = (rand2 - 0.52) * 3.0;
    let bpm_drift = (rand3 - 0.5) * 2.0;

    let new_joy = clamp_f32(prev_joy + joy_drift, 15.0, 100.0);
    let new_stress = clamp_f32(prev_stress + stress_drift, 5.0, 90.0);
    let new_bpm = clamp_f32(prev_bpm + bpm_drift, 60.0, 95.0);

    unsafe {
        *out_ptr = new_joy;
        *out_ptr.add(1) = new_stress;
        *out_ptr.add(2) = new_bpm;
    }
}

/// Helper clamp function for no_std f32
#[inline(always)]
fn clamp_f32(val: f32, min_val: f32, max_val: f32) -> f32 {
    if val < min_val {
        min_val
    } else if val > max_val {
        max_val
    } else {
        val
    }
}

/// Approximate cos / sin for leaf coordinate calculation in no_std without libm dependency
#[inline(always)]
fn approx_cos(rad: f32) -> f32 {
    // Normalise to [-pi, pi]
    let pi = 3.14159265359_f32;
    let two_pi = 6.28318530718_f32;
    let mut x = rad % two_pi;
    if x < -pi {
        x += two_pi;
    } else if x > pi {
        x -= two_pi;
    }

    // Taylor series: cos(x) ~ 1 - x^2/2 + x^4/24 - x^6/720
    let x2 = x * x;
    1.0 - (x2 / 2.0) + (x2 * x2 / 24.0) - (x2 * x2 * x2 / 720.0)
}

#[inline(always)]
fn approx_sin(rad: f32) -> f32 {
    // sin(x) = cos(x - pi/2)
    approx_cos(rad - 1.57079632679_f32)
}

/// High-Performance Quantum Lumina Garden Leaf Coordinate Generation
/// Computes (x, y, r) for each leaf up to min(60, (level + 1) * 12).
/// Writes [x_0, y_0, r_0, x_1, y_1, r_1, ...] as f32s to out_ptr.
/// Returns the number of leaves generated.
#[no_mangle]
pub extern "C" fn compute_garden_leaves(
    level: u32,
    out_ptr: *mut f32,
) -> u32 {
    let raw_count = (level + 1) * 12;
    let leaf_count = if raw_count > 60 { 60 } else { raw_count };
    let level_f = level as f32;

    for i in 0..leaf_count {
        let i_f = i as f32;
        let angle = i_f * 0.5;
        let x = 50.0 + approx_cos(angle) * (12.0 + level_f * 6.0);
        let y = 40.0 + approx_sin(angle) * (10.0 + level_f * 4.0);
        let r = 2.0 + ((i % 3) as f32);

        unsafe {
            let base = i as usize * 3;
            *out_ptr.add(base) = x;
            *out_ptr.add(base + 1) = y;
            *out_ptr.add(base + 2) = r;
        }
    }

    leaf_count
}

/// Optimized PCM16 to WAV Container Synthesizer
/// Takes pointer to 16-bit signed PCM samples and outputs standard 44-byte RIFF/WAVE header
/// followed by PCM payload into out_wav_ptr.
/// Returns total byte length of the generated WAV buffer.
#[no_mangle]
pub extern "C" fn synthesize_wav(
    pcm_ptr: *const i16,
    sample_count: u32,
    sample_rate: u32,
    out_wav_ptr: *mut u8,
) -> u32 {
    let num_channels: u16 = 1;
    let bits_per_sample: u16 = 16;
    let byte_rate = sample_rate * (num_channels as u32) * ((bits_per_sample / 8) as u32);
    let block_align = num_channels * (bits_per_sample / 8);
    let data_len = sample_count * 2;
    let total_len = 44 + data_len;

    unsafe {
        let out = out_wav_ptr;
        // Chunk ID: "RIFF"
        *out.add(0) = b'R';
        *out.add(1) = b'I';
        *out.add(2) = b'F';
        *out.add(3) = b'F';

        // Chunk Size: 36 + SubChunk2Size
        let chunk_size = 36 + data_len;
        *(out.add(4) as *mut u32) = chunk_size.to_le();

        // Format: "WAVE"
        *out.add(8) = b'W';
        *out.add(9) = b'A';
        *out.add(10) = b'V';
        *out.add(11) = b'E';

        // Subchunk1 ID: "fmt "
        *out.add(12) = b'f';
        *out.add(13) = b'm';
        *out.add(14) = b't';
        *out.add(15) = b' ';

        // Subchunk1 Size: 16 for PCM
        *(out.add(16) as *mut u32) = 16u32.to_le();

        // AudioFormat: 1 for PCM
        *(out.add(20) as *mut u16) = 1u16.to_le();

        // NumChannels
        *(out.add(22) as *mut u16) = num_channels.to_le();

        // SampleRate
        *(out.add(24) as *mut u32) = sample_rate.to_le();

        // ByteRate
        *(out.add(28) as *mut u32) = byte_rate.to_le();

        // BlockAlign
        *(out.add(32) as *mut u16) = block_align.to_le();

        // BitsPerSample
        *(out.add(34) as *mut u16) = bits_per_sample.to_le();

        // Subchunk2 ID: "data"
        *out.add(36) = b'd';
        *out.add(37) = b'a';
        *out.add(38) = b't';
        *out.add(39) = b'a';

        // Subchunk2 Size
        *(out.add(40) as *mut u32) = data_len.to_le();

        // Copy raw PCM byte data into data section
        let pcm_src = pcm_ptr as *const u8;
        let wav_data_dst = out.add(44);
        core::ptr::copy_nonoverlapping(pcm_src, wav_data_dst, data_len as usize);
    }

    total_len
}

/// OMNI AI Truth Gate Validation: T(x) >= 0.995 verification
/// Calculates quantum temporal coherence factor and checks threshold.
/// Returns 1 if valid, 0 if sub-threshold.
#[no_mangle]
pub extern "C" fn verify_truth_metric(joy: f32, stress: f32, engagement_level: u32) -> u32 {
    let normalized_joy = joy / 100.0;
    let normalized_stress = stress / 100.0;
    let level_bonus = (engagement_level as f32) * 0.002;

    let t_x = 0.995 + (normalized_joy * 0.004) - (normalized_stress * 0.002) + level_bonus;

    if t_x >= 0.995 {
        1
    } else {
        0
    }
}

// Internal Unit Tests (built when compiling for native targets)
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_biometrics_drift() {
        let mut out = [0.0f32; 3];
        compute_biometrics(65.0, 18.0, 68.0, 0.5, 0.5, 0.5, out.as_mut_ptr());

        // joy_drift = (0.5 - 0.48) * 3 = 0.06 -> 65.06
        // stress_drift = (0.5 - 0.52) * 3 = -0.06 -> 17.94
        // bpm_drift = (0.5 - 0.5) * 2 = 0 -> 68.0
        assert!((out[0] - 65.06).abs() < 0.01);
        assert!((out[1] - 17.94).abs() < 0.01);
        assert!((out[2] - 68.0).abs() < 0.01);
    }

    #[test]
    fn test_garden_leaves() {
        let mut out = [0.0f32; 60 * 3];
        let count = compute_garden_leaves(0, out.as_mut_ptr());
        assert_eq!(count, 12);

        let count3 = compute_garden_leaves(3, out.as_mut_ptr());
        assert_eq!(count3, 48);

        let count6 = compute_garden_leaves(6, out.as_mut_ptr());
        assert_eq!(count6, 60); // capped at 60
    }

    #[test]
    fn test_synthesize_wav() {
        let pcm: [i16; 4] = [1000, -1000, 2000, -2000];
        let mut wav = [0u8; 44 + 8];
        let len = synthesize_wav(pcm.as_ptr(), 4, 24000, wav.as_mut_ptr());
        assert_eq!(len, 52);

        // RIFF header validation
        assert_eq!(&wav[0..4], b"RIFF");
        assert_eq!(&wav[8..12], b"WAVE");
        assert_eq!(&wav[12..16], b"fmt ");
        assert_eq!(&wav[36..40], b"data");
        // Subchunk2Size = 8 bytes
        let subchunk2_size = u32::from_le_bytes([wav[40], wav[41], wav[42], wav[43]]);
        assert_eq!(subchunk2_size, 8);
    }

    #[test]
    fn test_truth_metric() {
        assert_eq!(verify_truth_metric(65.0, 18.0, 1), 1);
        assert_eq!(verify_truth_metric(90.0, 5.0, 3), 1);
    }
}
