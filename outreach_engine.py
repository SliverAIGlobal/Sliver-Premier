#!/usr/bin/env python3
"""
SliverVerse Edge Veritas // Automated Outreach Engine (SOREN-V2)
----------------------------------------------------------------
Generates, formats, and automates multi-channel sales outreach campaigns,
personalized direct messaging, and 60-second Airplane Mode proof packets.
"""

import argparse
import json
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class OutreachContact:
    name: str
    email: str
    vertical: str  # 'edtech', 'healthtech', 'wasm_dev', 'flash_seed'
    organization: Optional[str] = None
    custom_note: Optional[str] = None


class AutomatedOutreachEngine:
    def __init__(self, demo_url: str = "https://sliververse.edge/flower-learn", checkout_url: str = "https://gumroad.com/l/flower-learn-studio"):
        self.demo_url = demo_url
        self.checkout_url = checkout_url

    def generate_edtech_email(self, contact: OutreachContact) -> Dict[str, str]:
        """K-12 STEAM / District IT Director zero-DPA compliance pitch."""
        org_text = f" for {contact.organization}" if contact.organization else ""
        subject = f"0-Day IT Clearance: Offline Bio-Kinetic Coloring Studio{org_text}"
        body = f"""Hi {contact.name},

Most classroom digital tools require a 6-to-12-month IT security review and multi-page Data Processing Agreements (DPAs).

Flower Learn Studio (SOREN-V2) bypasses that bottleneck completely:
1. Turn on Airplane Mode ✈️ (disable Wi-Fi / cellular).
2. Open the self-contained app: {self.demo_url}
3. Convert any textbook diagram, plant specimen, or photo into a high-contrast line-art worksheet in <50ms locally via client-side WebAssembly (WASM).

Zero student data or personal identifiers ever leave the device (E_out = 0 Bytes), guaranteeing instant COPPA and FERPA compliance out of the box.

We are issuing 1-Page Zero-DPA Certifications alongside flat $49 individual teacher passes and $499 district-wide site licenses.

Would you be open to a 10-minute briefing this Thursday?

Best regards,
SliverVerse Edge Veritas Growth Team
""".strip()
        return {"subject": subject, "body": body, "contact": contact.email, "vertical": "edtech"}

    def generate_healthtech_email(self, contact: OutreachContact) -> Dict[str, str]:
        """Occupational Therapy & Senior Care somatic wellness pitch."""
        subject = f"Somatic Tremor Smoothing & Cortisol Reduction in Digital Art Therapy"
        body = f"""Hi {contact.name},

Digital screens often trigger ocular refixation strain, cognitive fatigue, and motor frustration for individuals with fine-motor tremors or senior care residents.

Flower Learn Studio is a 100% offline bio-kinetic canvas engineered specifically for therapeutic calm:
• Somatic Tremor Filter (alpha = 0.25): Real-time exponential low-pass filter suppressing 6–12 Hz motor jitter under an 8ms latency budget.
• 528 Hz Solfeggio Acoustic Fields: On-device dual-oscillator audio entrainment paired with 3.0 Hz Theta washes to actively lower systemic cortisol.
• CareState Micro-Grounding: Automatically transitions to soothing Chlorophyll Green (#2E7D32) and expands touch hitboxes when stress jitter is detected.

You can test the full therapeutic studio in Airplane Mode with zero cloud latency:
👉 Test Link: {self.demo_url}

Individual practitioner passes are $49 (covering up to 5 devices).

May I send you our clinical positioning whitepaper?

Warm regards,
SliverVerse HealthTech Team
""".strip()
        return {"subject": subject, "body": body, "contact": contact.email, "vertical": "healthtech"}

    def generate_wasm_dev_dm(self, contact: OutreachContact) -> Dict[str, str]:
        """Showcase for engineers, local-first builders, and Hacker News audience."""
        subject = f"Zero-cloud WASM 3x3 Sobel edge extraction in Airplane Mode"
        body = f"""Hey {contact.name} — saw your work in the local-first/WASM space.

We just launched Flower Learn Studio: a zero-dependency, single-file SPA (index.html) running image processing, procedural vector compilation, and audio synthesis 100% client-side.

Tech highlights:
• Sub-50ms 3x3 Sobel matrix convolutions (Gx & Gy) directly over WebAssembly.Memory.
• Zero-copy memory pointer coercion into Canvas ImageData buffers (no JS-to-C++ serialization overhead).
• Web Worker thread isolation locking 120 FPS UI physics.
• $0/user marginal compute cost.

Test it with your Wi-Fi turned OFF: {self.demo_url}

Lifetime individual developer passes (up to 5 devices) are available here: {self.checkout_url}

Would love your thoughts on the memory buffer layout!
""".strip()
        return {"subject": subject, "body": body, "contact": contact.email, "vertical": "wasm_dev"}

    def generate_flash_seed_pitch(self, contact: OutreachContact) -> Dict[str, str]:
        """60-Minute Scarcity Flash Seed Pitch ($50 / $49 Target)."""
        subject = f"⚡ 60-Minute Early Seed Pass: Flower Learn Studio ($49 Lifetime)"
        body = f"""Hi {contact.name},

Quick update: We just opened 10 Early Seed Lifetime Licenses for Flower Learn Studio (SOREN-V2) for $49 (Regular $149).

• Runs 100% offline in Airplane Mode.
• Upload ANY photo to extract detailed line art in <50ms.
• 100+ Curated Nature Specimen Library & 12+ real-world biological pigments per specimen.
• Valid for up to 5 personal devices with zero recurring subscription fees.

Claim your seed slot before the window closes:
👉 Live Airplane Mode Demo: {self.demo_url}
💳 Instant $49 License Checkout: {self.checkout_url}

Best regards,
Sliver AI Tech
""".strip()
        return {"subject": subject, "body": body, "contact": contact.email, "vertical": "flash_seed"}

    def dispatch_campaign(self, contacts: List[OutreachContact]) -> List[Dict[str, str]]:
        results = []
        for c in contacts:
            if c.vertical == "edtech":
                msg = self.generate_edtech_email(c)
            elif c.vertical == "healthtech":
                msg = self.generate_healthtech_email(c)
            elif c.vertical == "wasm_dev":
                msg = self.generate_wasm_dev_dm(c)
            else:
                msg = self.generate_flash_seed_pitch(c)
            results.append(msg)
        return results


def main():
    parser = argparse.ArgumentParser(description="Automated Outreach Engine for Flower Learn Studio")
    parser.add_argument("--vertical", choices=["edtech", "healthtech", "wasm_dev", "flash_seed", "all"], default="all")
    parser.add_argument("--demo-url", default="https://sliververse.edge/flower-learn")
    parser.add_argument("--checkout-url", default="https://gumroad.com/l/flower-learn-studio")
    parser.add_argument("--export-json", help="Path to export outreach campaign JSON")
    args = parser.parse_args()

    engine = AutomatedOutreachEngine(demo_url=args.demo_url, checkout_url=args.checkout_url)

    sample_contacts = [
        OutreachContact(name="Sarah Jenkins", email="sjenkins@district42.edu", vertical="edtech", organization="District 42 STEAM"),
        OutreachContact(name="Dr. Marcus Vance", email="vance@rehabhealth.org", vertical="healthtech", organization="Coastal OT Clinic"),
        OutreachContact(name="Alex Rivera", email="alex@kerneldev.io", vertical="wasm_dev"),
        OutreachContact(name="Taylor Smith", email="taylor@creativecreator.com", vertical="flash_seed"),
    ]

    selected = sample_contacts if args.vertical == "all" else [c for c in sample_contacts if c.vertical == args.vertical]
    campaign = engine.dispatch_campaign(selected)

    if args.export_json:
        with open(args.export_json, "w") as f:
            json.dump(campaign, f, indent=2)
        print(f"Exported {len(campaign)} outreach messages to {args.export_json}")
    else:
        for idx, item in enumerate(campaign, 1):
            print(f"=== [MESSAGE {idx} | {item['vertical'].upper()} | {item['contact']}] ===")
            print(f"Subject: {item['subject']}")
            print("-" * 50)
            print(item["body"])
            print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
