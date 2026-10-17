use wasm_bindgen::prelude::*;
use serde::{Deserialize, Serialize};
use sha2::{Sha256, Digest};

#[derive(Serialize, Deserialize, Clone)]
pub struct Concept {
    pub title: String,
    pub description: String,
    pub layer: String,
}

#[derive(Serialize, Deserialize, Clone)]
pub struct Monetizable {
    pub strategy: String,
    pub value: String,
}

#[derive(Serialize, Deserialize)]
pub struct SiftedOutput {
    pub concepts: Vec<Concept>,
    pub highlights: Vec<String>,
    pub entropy_score: f32,
    pub monetizables: Vec<Monetizable>,
}

#[wasm_bindgen]
pub struct CognitiveEngine {
    memory_pool: Vec<u8>,
}

#[wasm_bindgen]
impl CognitiveEngine {
    #[wasm_bindgen(constructor)]
    pub fn new() -> CognitiveEngine {
        console_error_panic_hook::set_once();
        CognitiveEngine {
            memory_pool: Vec::with_capacity(1024 * 1024),
        }
    }

    #[wasm_bindgen]
    pub fn sift_text(&mut self, input: &str) -> Result<String, JsValue> {
        let lines: Vec<&str> = input.lines().collect();
        let mut concepts = Vec::new();
        let mut highlights = Vec::new();
        let mut total_entropy = 0.0f32;

        for line in &lines {
            if line.contains("Protocol") || line.contains("Module") || line.contains("Matrix") || line.contains("Substrate") {
                let end_idx = line.len().min(60);
                concepts.push(Concept {
                    title: line[..end_idx].trim().to_string(),
                    description: "Extracted structural pillar".to_string(),
                    layer: "D1-D9".to_string(),
                });
            }

            if line.contains("!") || line.contains("✓") || (!line.is_empty() && line.len() > 80) {
                highlights.push(line.trim().to_string());
            }

            let char_freq = Self::compute_char_frequency(line);
            let line_ent = Self::calculate_shannon_entropy(&char_freq);
            total_entropy += line_ent;
        }

        let line_count = lines.len().max(1) as f32;
        let normalized_entropy = (total_entropy / line_count).min(10.0);

        let output = SiftedOutput {
            concepts,
            highlights,
            entropy_score: normalized_entropy,
            monetizables: vec![
                Monetizable {
                    strategy: "Direct License Gateway".to_string(),
                    value: "$499/mo".to_string(),
                },
                Monetizable {
                    strategy: "Enterprise Compliance Node".to_string(),
                    value: "$12,500/yr".to_string(),
                },
            ],
        };

        serde_json::to_string(&output)
            .map_err(|e| JsValue::from_str(&e.to_string()))
    }

    fn calculate_shannon_entropy(frequencies: &[u32; 256]) -> f32 {
        let total: u32 = frequencies.iter().sum();
        if total == 0 {
            return 0.0;
        }

        let mut ent = 0.0f32;
        for &freq in frequencies.iter() {
            if freq > 0 {
                let p = freq as f32 / total as f32;
                ent -= p * p.ln();
            }
        }
        ent
    }

    fn compute_char_frequency(s: &str) -> [u32; 256] {
        let mut freq = [0u32; 256];
        for byte in s.bytes() {
            freq[byte as usize] += 1;
        }
        freq
    }

    #[wasm_bindgen]
    pub fn hash_document(&self, content: &str) -> String {
        generate_veridical_hash(content)
    }

    #[wasm_bindgen]
    pub fn garbage_collect(&mut self) {
        self.memory_pool.clear();
    }

    #[wasm_bindgen]
    pub fn get_info(&self) -> String {
        format!(
            r#"{{"engine": "PRISM9-WASM v1.0", "simd_enabled": false, "multithreaded": false, "memory_pool_size": {}}}"#,
            self.memory_pool.capacity()
        )
    }
}

#[wasm_bindgen]
pub fn generate_veridical_hash(data: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(data.as_bytes());
    hex::encode(hasher.finalize())
}

#[wasm_bindgen]
pub fn verify_integrity(data: &str, expected_hash: &str) -> bool {
    generate_veridical_hash(data) == expected_hash
}
