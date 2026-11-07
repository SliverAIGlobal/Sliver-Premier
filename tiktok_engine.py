import io
import time
import base64
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

class TikTokAnimationEngine:
    """
    Engine for creating high-retention, seamless looping TikTok animation videos
    and animated GIFs from static artwork/coloring pages.
    """

    PRESETS = [
        "3d_parallax",
        "zoom_punch",
        "floating_jelly",
        "beat_pulse",
        "elastic_bounce",
        "reveal_glitch"
    ]

    ASPECT_RATIOS = {
        "9:16_hd": (720, 1280),
        "9:16_full": (1080, 1920),
        "1:1_square": (1080, 1080)
    }

    VIRAL_HOOKS = [
        "Wait for the end... 🤯",
        "Coloring therapy you didn't know you needed ✨",
        "Satisfying ink flow in 4K 🎨",
        "Drop a ❤️ if you love this vibe!",
        "Watch the colors come alive 💫"
    ]

    TRENDING_TAGS = [
        "#fyp", "#arttok", "#satisfying", "#coloring",
        "#aesthetic", "#creative", "#digitalart", "#relaxing"
    ]

    @staticmethod
    def isolate_subject_chroma(img_bgr: np.ndarray, tolerance: int = 240) -> np.ndarray:
        """
        Isolate non-white artwork / subject creating transparent BG RGBA image.
        """
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        # Check white background threshold
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        alpha = np.where(gray >= tolerance, 0, 255).astype(np.uint8)

        # Soften edges
        alpha = cv2.GaussianBlur(alpha, (3, 3), 0)
        rgba = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2RGBA)
        rgba[:, :, 3] = alpha
        return rgba

    @staticmethod
    def render_loop_frames(
        image_bytes: bytes,
        preset: str = "zoom_punch",
        duration_sec: float = 3.0,
        fps: int = 20,
        output_dim: tuple = (720, 1280),
        hook_text: str = "Wait for the end... 🤯",
        bg_style: str = "aurora"
    ) -> list[Image.Image]:
        """
        Render a list of PIL Images forming a mathematically perfect seamless loop.
        """
        nparr = np.frombuffer(image_bytes, np.uint8)
        img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img_bgr is None:
            # Fallback blank
            img_bgr = np.full((600, 600, 3), 255, dtype=np.uint8)

        # Subject isolation
        rgba_subject = TikTokAnimationEngine.isolate_subject_chroma(img_bgr)
        pil_subject = Image.fromarray(rgba_subject)

        width, height = output_dim
        total_frames = int(duration_sec * fps)
        frames = []

        # Color palettes for dynamic background gradient
        bg_gradients = {
            "aurora": ((15, 23, 42), (99, 102, 241), (236, 72, 153)),
            "neon_cyber": ((10, 10, 20), (168, 85, 247), (6, 182, 212)),
            "sunset": ((30, 10, 30), (244, 63, 94), (251, 146, 60)),
            "minimal_dark": ((18, 18, 24), (30, 30, 42), (40, 40, 56))
        }
        c1, c2, c3 = bg_gradients.get(bg_style, bg_gradients["aurora"])

        for f in range(total_frames):
            phase = (f / total_frames) * 2 * np.pi  # 0 to 2pi seamless
            t = f / total_frames

            # 1. Create dynamic moving background
            frame_bg = Image.new("RGBA", (width, height), c1)
            draw = ImageDraw.Draw(frame_bg)

            # Atmospheric glowing orbs in background
            orb_y = int(height * 0.45 + np.sin(phase) * 60)
            orb_r = int(width * 0.4 + np.cos(phase) * 30)
            orb_box = [width // 2 - orb_r, orb_y - orb_r, width // 2 + orb_r, orb_y + orb_r]
            draw.ellipse(orb_box, fill=(c2[0], c2[1], c2[2], 90))

            orb2_y = int(height * 0.65 - np.cos(phase) * 70)
            orb2_r = int(width * 0.35 + np.sin(phase) * 25)
            orb2_box = [width // 2 - orb2_r, orb2_y - orb2_r, width // 2 + orb2_r, orb2_y + orb2_r]
            draw.ellipse(orb2_box, fill=(c3[0], c3[1], c3[2], 75))

            # 2. Compute motion transformation based on preset
            scale = 1.0
            dx, dy = 0, 0
            angle = 0.0

            if preset == "zoom_punch":
                # Heartbeat pulse / zoom punch: sharp zoom-in then smooth settle
                scale = 1.0 + 0.14 * (np.sin(phase) ** 2)
            elif preset == "3d_parallax":
                # Simulated 3D tilt & gentle orbital float
                dx = int(np.sin(phase) * 35)
                dy = int(np.cos(phase) * 25)
                angle = np.sin(phase) * 3.5
            elif preset == "floating_jelly":
                # Organic undulating squish & float
                scale_x = 1.0 + 0.08 * np.sin(phase)
                scale_y = 1.0 + 0.08 * np.cos(phase)
                dy = int(np.sin(phase) * 30)
                scale = (scale_x + scale_y) / 2.0
            elif preset == "beat_pulse":
                # Double bounce rhythm
                beat = (np.sin(phase * 2) ** 4) * 0.18
                scale = 1.0 + beat
            elif preset == "elastic_bounce":
                dy = int(-abs(np.sin(phase)) * 70)
                scale = 1.0 + 0.06 * np.sin(phase)
            elif preset == "reveal_glitch":
                scale = 1.0 + 0.05 * np.sin(phase)
                if f % 7 == 0:
                    dx = np.random.randint(-12, 12)

            # Resize subject to fit canvas nicely (~70% width)
            base_w = int(width * 0.72 * scale)
            aspect = pil_subject.height / max(1, pil_subject.width)
            base_h = int(base_w * aspect)

            scaled_sub = pil_subject.resize((base_w, base_h), Image.Resampling.BILINEAR)
            if angle != 0:
                scaled_sub = scaled_sub.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)

            # Center position
            pos_x = (width - scaled_sub.width) // 2 + dx
            pos_y = int(height * 0.42) - (scaled_sub.height // 2) + dy

            # Shadow layer
            shadow = Image.new("RGBA", (scaled_sub.width, scaled_sub.height), (0, 0, 0, 80))
            frame_bg.paste(shadow, (pos_x + 8, pos_y + 14), mask=scaled_sub.split()[3])

            # Composite subject
            frame_bg.paste(scaled_sub, (pos_x, pos_y), mask=scaled_sub.split()[3])

            # 3. Add Engagement Overlays & Safe-zone friendly Hook Caption
            # Top hook banner (sits comfortably above TikTok captions)
            if hook_text:
                hook_w = int(width * 0.85)
                hook_h = 60
                hook_x = (width - hook_w) // 2
                hook_y = int(height * 0.16)

                # Pill backdrop
                draw.rounded_rectangle(
                    [hook_x, hook_y, hook_x + hook_w, hook_y + hook_h],
                    radius=25,
                    fill=(0, 0, 0, 180),
                    outline=(255, 255, 255, 120),
                    width=2
                )
                draw.text(
                    (width // 2, hook_y + hook_h // 2),
                    hook_text,
                    fill=(255, 255, 255, 255),
                    anchor="mm"
                )

            # Bottom Branding watermark (Safe from bottom caption zone)
            wm_text = "© 2026 Color World • sliverai.gumroad.com"
            draw.text((width // 2, int(height * 0.88)), wm_text, fill=(255, 255, 255, 180), anchor="mm")

            frames.append(frame_bg.convert("RGB"))

        return frames

    @staticmethod
    def export_animated_gif(frames: list[Image.Image], duration_ms: int = 50) -> bytes:
        """
        Export seamlessly looping GIF bytes.
        """
        if not frames:
            raise ValueError("No frames provided")

        out = io.BytesIO()
        frames[0].save(
            out,
            format="GIF",
            save_all=True,
            append_images=frames[1:],
            duration=duration_ms,
            loop=0,
            optimize=True
        )
        return out.getvalue()

    @staticmethod
    def export_animated_webp(frames: list[Image.Image], duration_ms: int = 50) -> bytes:
        """
        Export animated WebP bytes (high quality, lower file size).
        """
        if not frames:
            raise ValueError("No frames provided")

        out = io.BytesIO()
        frames[0].save(
            out,
            format="WEBP",
            save_all=True,
            append_images=frames[1:],
            duration=duration_ms,
            loop=0,
            quality=85
        )
        return out.getvalue()
