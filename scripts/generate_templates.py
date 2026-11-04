#!/usr/bin/env python3
"""Build script for single-file self-contained index.html."""

import os
import base64

def get_wasm_b64():
    with open('wasm_base64.txt', 'r') as f:
        return f.read().strip()

# Template library SVGs:
TEMPLATES = {
    "botanical_junior": {
        "title": "Sunflower Bloom (Junior)",
        "theme": "botanical",
        "difficulty": "junior",
        "description": "Bold petals, friendly center, and large leaves for easy coloring.",
        "svg": """<svg viewBox="0 0 800 800" xmlns="http://www.w3.org/2000/svg">
  <rect width="800" height="800" fill="#ffffff"/>
  <!-- Petals -->
  <path d="M400,340 C360,180 440,180 400,340 Z" fill="#ffffff" stroke="#000000" stroke-width="8" stroke-linejoin="round"/>
  <path d="M400,460 C360,620 440,620 400,460 Z" fill="#ffffff" stroke="#000000" stroke-width="8" stroke-linejoin="round"/>
  <path d="M340,400 C180,360 180,440 340,400 Z" fill="#ffffff" stroke="#000000" stroke-width="8" stroke-linejoin="round"/>
  <path d="M460,400 C620,360 620,440 460,400 Z" fill="#ffffff" stroke="#000000" stroke-width="8" stroke-linejoin="round"/>
  <path d="M358,358 C240,240 300,180 358,358 Z" fill="#ffffff" stroke="#000000" stroke-width="8" stroke-linejoin="round"/>
  <path d="M442,358 C560,240 500,180 442,358 Z" fill="#ffffff" stroke="#000000" stroke-width="8" stroke-linejoin="round"/>
  <path d="M358,442 C240,560 300,620 358,442 Z" fill="#ffffff" stroke="#000000" stroke-width="8" stroke-linejoin="round"/>
  <path d="M442,442 C560,560 500,620 442,442 Z" fill="#ffffff" stroke="#000000" stroke-width="8" stroke-linejoin="round"/>
  <!-- Center disk -->
  <circle cx="400" cy="400" r="90" fill="#ffffff" stroke="#000000" stroke-width="8"/>
  <circle cx="400" cy="400" r="60" fill="#ffffff" stroke="#000000" stroke-width="6"/>
  <circle cx="400" cy="400" r="30" fill="#ffffff" stroke="#000000" stroke-width="6"/>
  <!-- Stem & Leaves -->
  <path d="M400,490 Q420,640 380,780" fill="none" stroke="#000000" stroke-width="12" stroke-linecap="round"/>
  <path d="M410,580 C500,530 550,610 408,630 Z" fill="#ffffff" stroke="#000000" stroke-width="8"/>
  <path d="M392,660 C300,610 250,690 394,710 Z" fill="#ffffff" stroke="#000000" stroke-width="8"/>
</svg>"""
    },
    "botanical_adult": {
        "title": "Wild Rose & Foliage (Adult)",
        "theme": "botanical",
        "difficulty": "adult",
        "description": "Multi-layered organic petals, pistils, and delicate leaf veins.",
        "svg": """<svg viewBox="0 0 800 800" xmlns="http://www.w3.org/2000/svg">
  <rect width="800" height="800" fill="#ffffff"/>
  <!-- Outer Foliage -->
  <path d="M200,200 C250,120 380,180 320,280 C270,300 210,270 200,200 Z" fill="#ffffff" stroke="#000000" stroke-width="4"/>
  <path d="M200,200 Q260,240 320,280" fill="none" stroke="#000000" stroke-width="3"/>
  <path d="M600,200 C650,280 590,380 500,320 C480,270 520,210 600,200 Z" fill="#ffffff" stroke="#000000" stroke-width="4"/>
  <path d="M600,200 Q550,260 500,320" fill="none" stroke="#000000" stroke-width="3"/>
  <path d="M600,600 C520,670 420,610 460,510 C520,490 580,530 600,600 Z" fill="#ffffff" stroke="#000000" stroke-width="4"/>
  <path d="M600,600 Q530,550 460,510" fill="none" stroke="#000000" stroke-width="3"/>
  <path d="M200,600 C150,520 210,420 300,480 C320,530 280,590 200,600 Z" fill="#ffffff" stroke="#000000" stroke-width="4"/>
  <path d="M200,600 Q250,540 300,480" fill="none" stroke="#000000" stroke-width="3"/>
  <!-- Outer Petals -->
  <path d="M400,200 C340,120 280,220 310,290 C360,330 380,300 400,200 Z" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <path d="M400,200 C460,120 520,220 490,290 C440,330 420,300 400,200 Z" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <path d="M600,400 C680,340 580,280 510,310 C470,360 500,380 600,400 Z" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <path d="M600,400 C680,460 580,520 510,490 C470,440 500,420 600,400 Z" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <path d="M400,600 C460,680 520,580 490,510 C440,470 420,500 400,600 Z" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <path d="M400,600 C340,680 280,580 310,510 C360,470 380,500 400,600 Z" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <path d="M200,400 C120,460 220,520 290,490 C330,440 300,420 200,400 Z" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <path d="M200,400 C120,340 220,280 290,310 C330,360 300,380 200,400 Z" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <!-- Middle Tier -->
  <circle cx="400" cy="400" r="130" fill="#ffffff" stroke="#000000" stroke-width="4"/>
  <path d="M400,270 C360,330 360,370 400,400 C440,370 440,330 400,270 Z" fill="#ffffff" stroke="#000000" stroke-width="4"/>
  <path d="M400,530 C360,470 360,430 400,400 C440,430 440,470 400,530 Z" fill="#ffffff" stroke="#000000" stroke-width="4"/>
  <path d="M270,400 C330,360 370,360 400,400 C370,440 330,440 270,400 Z" fill="#ffffff" stroke="#000000" stroke-width="4"/>
  <path d="M530,400 C470,360 430,360 400,400 C430,440 470,440 530,400 Z" fill="#ffffff" stroke="#000000" stroke-width="4"/>
  <!-- Center Filigree -->
  <circle cx="400" cy="400" r="70" fill="#ffffff" stroke="#000000" stroke-width="4"/>
  <circle cx="400" cy="400" r="30" fill="#ffffff" stroke="#000000" stroke-width="4"/>
  <circle cx="400" cy="350" r="10" fill="#ffffff" stroke="#000000" stroke-width="3"/>
  <circle cx="450" cy="400" r="10" fill="#ffffff" stroke="#000000" stroke-width="3"/>
  <circle cx="400" cy="450" r="10" fill="#ffffff" stroke="#000000" stroke-width="3"/>
  <circle cx="350" cy="400" r="10" fill="#ffffff" stroke="#000000" stroke-width="3"/>
</svg>"""
    },
    "nature_junior": {
        "title": "Mountain Sunrise (Junior)",
        "theme": "nature",
        "difficulty": "junior",
        "description": "Clear sun, rolling peaks, and pine tree silhouettes.",
        "svg": """<svg viewBox="0 0 800 800" xmlns="http://www.w3.org/2000/svg">
  <rect width="800" height="800" fill="#ffffff"/>
  <!-- Sun & Rays -->
  <circle cx="400" cy="300" r="110" fill="#ffffff" stroke="#000000" stroke-width="8"/>
  <line x1="400" y1="120" x2="400" y2="160" stroke="#000000" stroke-width="8" stroke-linecap="round"/>
  <line x1="260" y1="170" x2="290" y2="200" stroke="#000000" stroke-width="8" stroke-linecap="round"/>
  <line x1="540" y1="170" x2="510" y2="200" stroke="#000000" stroke-width="8" stroke-linecap="round"/>
  <line x1="200" y1="300" x2="250" y2="300" stroke="#000000" stroke-width="8" stroke-linecap="round"/>
  <line x1="600" y1="300" x2="550" y2="300" stroke="#000000" stroke-width="8" stroke-linecap="round"/>
  <!-- Mountain Peaks -->
  <polygon points="400,260 220,560 580,560" fill="#ffffff" stroke="#000000" stroke-width="8" stroke-linejoin="round"/>
  <polygon points="400,260 360,350 430,350" fill="#ffffff" stroke="#000000" stroke-width="6"/>
  <polygon points="210,380 80,620 340,620" fill="#ffffff" stroke="#000000" stroke-width="8" stroke-linejoin="round"/>
  <polygon points="590,360 440,620 740,620" fill="#ffffff" stroke="#000000" stroke-width="8" stroke-linejoin="round"/>
  <!-- Rolling Hills Forefront -->
  <path d="M0,640 Q250,560 500,640 T800,600 L800,800 L0,800 Z" fill="#ffffff" stroke="#000000" stroke-width="8"/>
  <!-- Evergreen Trees -->
  <polygon points="200,580 160,650 240,650" fill="#ffffff" stroke="#000000" stroke-width="7"/>
  <polygon points="200,630 150,710 250,710" fill="#ffffff" stroke="#000000" stroke-width="7"/>
  <rect x="190" y="710" width="20" height="30" fill="#ffffff" stroke="#000000" stroke-width="6"/>
  <polygon points="620,560 580,630 660,630" fill="#ffffff" stroke="#000000" stroke-width="7"/>
  <polygon points="620,610 570,690 670,690" fill="#ffffff" stroke="#000000" stroke-width="7"/>
  <rect x="610" y="690" width="20" height="30" fill="#ffffff" stroke="#000000" stroke-width="6"/>
</svg>"""
    },
    "nature_adult": {
        "title": "Zen Garden Stream (Adult)",
        "theme": "nature",
        "difficulty": "adult",
        "description": "Flowing water contours, smooth river stones, and delicate bamboo stems.",
        "svg": """<svg viewBox="0 0 800 800" xmlns="http://www.w3.org/2000/svg">
  <rect width="800" height="800" fill="#ffffff"/>
  <!-- Bamboo Stalks -->
  <rect x="120" y="50" width="35" height="180" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <rect x="120" y="240" width="35" height="200" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <rect x="120" y="450" width="35" height="250" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <rect x="180" y="80" width="30" height="150" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <rect x="180" y="240" width="30" height="220" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <!-- Bamboo Leaves -->
  <path d="M155,140 C220,130 260,170 280,210 C230,200 180,180 155,140 Z" fill="#ffffff" stroke="#000000" stroke-width="4"/>
  <path d="M120,340 C60,330 20,370 0,420 C50,400 100,380 120,340 Z" fill="#ffffff" stroke="#000000" stroke-width="4"/>
  <!-- Flowing Waves / Current -->
  <path d="M250,150 C400,100 500,250 750,200" fill="none" stroke="#000000" stroke-width="5"/>
  <path d="M240,210 C410,160 490,310 770,260" fill="none" stroke="#000000" stroke-width="4"/>
  <path d="M230,270 C390,230 480,370 790,320" fill="none" stroke="#000000" stroke-width="5"/>
  <path d="M220,340 C380,310 450,450 780,410" fill="none" stroke="#000000" stroke-width="4"/>
  <path d="M210,410 C360,390 440,530 790,490" fill="none" stroke="#000000" stroke-width="5"/>
  <!-- River Stones -->
  <ellipse cx="450" cy="580" rx="90" ry="50" fill="#ffffff" stroke="#000000" stroke-width="6"/>
  <ellipse cx="440" cy="570" rx="65" ry="32" fill="#ffffff" stroke="#000000" stroke-width="4"/>
  <ellipse cx="330" cy="660" rx="110" ry="60" fill="#ffffff" stroke="#000000" stroke-width="6"/>
  <ellipse cx="320" cy="650" rx="75" ry="38" fill="#ffffff" stroke="#000000" stroke-width="4"/>
  <ellipse cx="580" cy="670" rx="100" ry="55" fill="#ffffff" stroke="#000000" stroke-width="6"/>
  <ellipse cx="570" cy="660" rx="70" ry="35" fill="#ffffff" stroke="#000000" stroke-width="4"/>
  <!-- Water ripples around stones -->
  <path d="M200,680 C230,730 430,730 470,680" fill="none" stroke="#000000" stroke-width="4"/>
  <path d="M450,710 C480,750 680,750 720,700" fill="none" stroke="#000000" stroke-width="4"/>
</svg>"""
    },
    "mandala_junior": {
        "title": "Harmony Mandala (Junior)",
        "theme": "mandala",
        "difficulty": "junior",
        "description": "Geometric radial symmetry with wide spaces and concentric rings.",
        "svg": """<svg viewBox="0 0 800 800" xmlns="http://www.w3.org/2000/svg">
  <rect width="800" height="800" fill="#ffffff"/>
  <!-- Rings -->
  <circle cx="400" cy="400" r="360" fill="#ffffff" stroke="#000000" stroke-width="8"/>
  <circle cx="400" cy="400" r="300" fill="#ffffff" stroke="#000000" stroke-width="8"/>
  <circle cx="400" cy="400" r="220" fill="#ffffff" stroke="#000000" stroke-width="8"/>
  <circle cx="400" cy="400" r="140" fill="#ffffff" stroke="#000000" stroke-width="8"/>
  <circle cx="400" cy="400" r="60" fill="#ffffff" stroke="#000000" stroke-width="8"/>
  <!-- 8 Petal Rays -->
  <polygon points="400,100 440,180 400,260 360,180" fill="#ffffff" stroke="#000000" stroke-width="7"/>
  <polygon points="400,700 440,620 400,540 360,620" fill="#ffffff" stroke="#000000" stroke-width="7"/>
  <polygon points="100,400 180,440 260,400 180,360" fill="#ffffff" stroke="#000000" stroke-width="7"/>
  <polygon points="700,400 620,440 540,400 620,360" fill="#ffffff" stroke="#000000" stroke-width="7"/>
  <!-- Diagonal Petals -->
  <polygon points="190,190 270,220 290,290 220,270" fill="#ffffff" stroke="#000000" stroke-width="7"/>
  <polygon points="610,190 530,220 510,290 580,270" fill="#ffffff" stroke="#000000" stroke-width="7"/>
  <polygon points="190,610 270,580 290,510 220,530" fill="#ffffff" stroke="#000000" stroke-width="7"/>
  <polygon points="610,610 530,580 510,510 580,530" fill="#ffffff" stroke="#000000" stroke-width="7"/>
  <!-- Accents -->
  <circle cx="400" cy="180" r="20" fill="#ffffff" stroke="#000000" stroke-width="6"/>
  <circle cx="400" cy="620" r="20" fill="#ffffff" stroke="#000000" stroke-width="6"/>
  <circle cx="180" cy="400" r="20" fill="#ffffff" stroke="#000000" stroke-width="6"/>
  <circle cx="620" cy="400" r="20" fill="#ffffff" stroke="#000000" stroke-width="6"/>
</svg>"""
    },
    "mandala_adult": {
        "title": "Cosmic Lotus Mandala (Adult)",
        "theme": "mandala",
        "difficulty": "adult",
        "description": "High-density radial lattice with 16-fold symmetry, repeating arches and stars.",
        "svg": """<svg viewBox="0 0 800 800" xmlns="http://www.w3.org/2000/svg">
  <rect width="800" height="800" fill="#ffffff"/>
  <!-- Outer Rim Frame -->
  <circle cx="400" cy="400" r="380" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <circle cx="400" cy="400" r="350" fill="#ffffff" stroke="#000000" stroke-width="4"/>
  <circle cx="400" cy="400" r="300" fill="#ffffff" stroke="#000000" stroke-width="4"/>
  <circle cx="400" cy="400" r="240" fill="#ffffff" stroke="#000000" stroke-width="4"/>
  <circle cx="400" cy="400" r="180" fill="#ffffff" stroke="#000000" stroke-width="4"/>
  <circle cx="400" cy="400" r="120" fill="#ffffff" stroke="#000000" stroke-width="4"/>
  <circle cx="400" cy="400" r="60" fill="#ffffff" stroke="#000000" stroke-width="4"/>
  <!-- 12 Radiating Rays and Scallops -->
  <g stroke="#000000" stroke-width="3" fill="#ffffff">
    <!-- Star Points -->
    <polygon points="400,20 425,120 400,100 375,120"/>
    <polygon points="400,780 425,680 400,700 375,680"/>
    <polygon points="20,400 120,425 100,400 120,375"/>
    <polygon points="780,400 680,425 700,400 680,375"/>
    <polygon points="131,131 223,178 206,194 178,223"/>
    <polygon points="669,131 577,178 594,194 622,223"/>
    <polygon points="131,669 223,622 206,606 178,577"/>
    <polygon points="669,669 577,622 594,606 622,577"/>
  </g>
  <!-- Intricate Petal Lattice -->
  <g stroke="#000000" stroke-width="3" fill="#ffffff">
    <path d="M400,180 C440,240 440,280 400,340 C360,280 360,240 400,180 Z"/>
    <path d="M400,620 C440,560 440,520 400,460 C360,520 360,560 400,620 Z"/>
    <path d="M180,400 C240,440 280,440 340,400 C280,360 240,360 180,400 Z"/>
    <path d="M620,400 C560,440 520,440 460,400 C520,360 560,360 620,400 Z"/>
    <path d="M244,244 C310,270 340,300 358,358 C300,340 270,310 244,244 Z"/>
    <path d="M556,244 C490,270 460,300 442,358 C500,340 530,310 556,244 Z"/>
    <path d="M244,556 C310,530 340,500 358,442 C300,460 270,490 244,556 Z"/>
    <path d="M556,556 C490,530 460,500 442,442 C500,460 530,490 556,556 Z"/>
  </g>
  <!-- Inner Rosette -->
  <circle cx="400" cy="400" r="30" fill="#ffffff" stroke="#000000" stroke-width="4"/>
  <circle cx="400" cy="400" r="10" fill="#000000"/>
</svg>"""
    },
    "geometric_junior": {
        "title": "Prism Mosaic (Junior)",
        "theme": "geometric",
        "difficulty": "junior",
        "description": "Bold interlocking triangles and polygons for clean color blocking.",
        "svg": """<svg viewBox="0 0 800 800" xmlns="http://www.w3.org/2000/svg">
  <rect width="800" height="800" fill="#ffffff"/>
  <!-- Outer Diamond Border -->
  <polygon points="400,50 750,400 400,750 50,400" fill="#ffffff" stroke="#000000" stroke-width="8"/>
  <polygon points="400,150 650,400 400,650 150,400" fill="#ffffff" stroke="#000000" stroke-width="8"/>
  <!-- Central Diamond -->
  <polygon points="400,270 530,400 400,530 270,400" fill="#ffffff" stroke="#000000" stroke-width="8"/>
  <!-- Cross Connectors -->
  <line x1="50" y1="400" x2="270" y2="400" stroke="#000000" stroke-width="8"/>
  <line x1="530" y1="400" x2="750" y2="400" stroke="#000000" stroke-width="8"/>
  <line x1="400" y1="50" x2="400" y2="270" stroke="#000000" stroke-width="8"/>
  <line x1="400" y1="530" x2="400" y2="750" stroke="#000000" stroke-width="8"/>
  <!-- Corner Triangles -->
  <polygon points="50,50 250,50 50,250" fill="#ffffff" stroke="#000000" stroke-width="8"/>
  <polygon points="750,50 550,50 750,250" fill="#ffffff" stroke="#000000" stroke-width="8"/>
  <polygon points="50,750 250,750 50,550" fill="#ffffff" stroke="#000000" stroke-width="8"/>
  <polygon points="750,750 550,750 750,550" fill="#ffffff" stroke="#000000" stroke-width="8"/>
</svg>"""
    },
    "geometric_adult": {
        "title": "Isometric Cubes & Hexagons (Adult)",
        "theme": "geometric",
        "difficulty": "adult",
        "description": "Tessellated 3D cube illusion with multiple shading facets.",
        "svg": """<svg viewBox="0 0 800 800" xmlns="http://www.w3.org/2000/svg">
  <rect width="800" height="800" fill="#ffffff"/>
  <!-- Center Cube -->
  <!-- Top Face -->
  <polygon points="400,320 480,366 400,412 320,366" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <!-- Left Face -->
  <polygon points="320,366 400,412 400,504 320,458" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <!-- Right Face -->
  <polygon points="400,412 480,366 480,458 400,504" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <!-- Top Cube -->
  <polygon points="400,136 480,182 400,228 320,182" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <polygon points="320,182 400,228 400,320 320,274" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <polygon points="400,228 480,182 480,274 400,320" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <!-- Bottom Cube -->
  <polygon points="400,504 480,550 400,596 320,550" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <polygon points="320,550 400,596 400,688 320,642" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <polygon points="400,596 480,550 480,642 400,688" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <!-- Top-Right Cube -->
  <polygon points="560,228 640,274 560,320 480,274" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <polygon points="480,274 560,320 560,412 480,366" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <polygon points="560,320 640,274 640,366 560,412" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <!-- Bottom-Right Cube -->
  <polygon points="560,412 640,458 560,504 480,458" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <polygon points="480,458 560,504 560,596 480,550" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <polygon points="560,504 640,458 640,550 560,596" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <!-- Top-Left Cube -->
  <polygon points="240,228 320,274 240,320 160,274" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <polygon points="160,274 240,320 240,412 160,366" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <polygon points="240,320 320,274 320,366 240,412" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <!-- Bottom-Left Cube -->
  <polygon points="240,412 320,458 240,504 160,458" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <polygon points="160,458 240,504 240,596 160,550" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <polygon points="240,504 320,458 320,550 240,596" fill="#ffffff" stroke="#000000" stroke-width="5"/>
  <!-- Framing Hexagon -->
  <polygon points="400,60 700,233 700,580 400,753 100,580 100,233" fill="none" stroke="#000000" stroke-width="8"/>
</svg>"""
    }
}

import json
print(f"Generated {len(TEMPLATES)} templates successfully.")
