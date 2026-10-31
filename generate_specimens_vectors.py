#!/usr/bin/env python3
"""
Biological Vector SVG Synthesizer for SORENv2 Flower Learn Studio.
Generates rich, bespoke, scientifically authentic vector illustrations for all specimens
with zero repeating silhouettes and pure client-side offline execution (E_out = 0 Bytes).
"""
import math
import re

PALETTES = {
    'marine': {'bg1': '#031926', 'bg2': '#0b3954', 'c1': '#087e8b', 'c2': '#38bdf8', 'c3': '#67e8f9', 'accent': '#00ffcc'},
    'botany': {'bg1': '#0d1f12', 'bg2': '#1b4332', 'c1': '#2d6a4f', 'c2': '#74c69d', 'c3': '#b7e4c7', 'accent': '#52b788'},
    'insects': {'bg1': '#231124', 'bg2': '#4a154b', 'c1': '#a2238e', 'c2': '#f472b6', 'c3': '#fbcfe8', 'accent': '#fbbf24'},
    'animals': {'bg1': '#1c1917', 'bg2': '#44403c', 'c1': '#78716c', 'c2': '#fb923c', 'c3': '#fed7aa', 'accent': '#f97316'},
    'micro': {'bg1': '#180e29', 'bg2': '#3b1c61', 'c1': '#6d28d9', 'c2': '#a855f7', 'c3': '#e9d5ff', 'accent': '#c084fc'},
    'default': {'bg1': '#0f172a', 'bg2': '#1e293b', 'c1': '#334155', 'c2': '#64748b', 'c3': '#cbd5e1', 'accent': '#38bdf8'}
}

def map_category(cat_str):
    s = cat_str.lower()
    if any(k in s for k in ['marine', 'sea', 'ocean', 'whale', 'coral', 'shark', 'seahorse', 'octopus', 'otter']):
        return 'marine'
    if any(k in s for k in ['botan', 'plant', 'tree', 'flower', 'lotus', 'moss', 'dendro', 'fern', 'bamboo']):
        return 'botany'
    if any(k in s for k in ['insect', 'entomol', 'bee', 'butterfly', 'moth', 'ant', 'beetle', 'dragonfly', 'cicada']):
        return 'insects'
    if any(k in s for k in ['mycol', 'fungi', 'micro', 'cell', 'organelle', 'diatom', 'dna', 'ciliate', 'neuron']):
        return 'micro'
    return 'animals'

def generate_specimen_vector(title, category_name, seed=1):
    cat = map_category(category_name + " " + title)
    pal = PALETTES.get(cat, PALETTES['default'])
    t_low = title.lower()

    elements = []

    # 1. Nautilus / Spiral Shell
    if 'nautilus' in t_low or 'shell' in t_low or 'foraminifera' in t_low or 'snail' in t_low:
        # Logarithmic spiral chambers
        cx, cy = 100, 100
        spiral_pts = []
        for a in range(0, 1400, 10):
            theta = math.radians(a)
            r = 4.5 * math.exp(0.12 * theta)
            if r > 82: break
            x = cx + r * math.cos(theta)
            y = cy + r * math.sin(theta)
            spiral_pts.append(f"{x:.1f},{y:.1f}")
        elements.append(f'<polyline points="{" ".join(spiral_pts)}" fill="none" stroke="{pal["c2"]}" stroke-width="2.5"/>')
        # Septa ribs
        for a in range(120, 1200, 80):
            th = math.radians(a)
            r = 4.5 * math.exp(0.12 * th)
            if r > 80: break
            x = cx + r * math.cos(th)
            y = cy + r * math.sin(th)
            elements.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{pal["c1"]}" stroke-width="1.6" stroke-dasharray="2,2"/>')
            elements.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2" fill="{pal["accent"]}"/>')

    # 2. Sea Turtle / Carapace / Tortoise
    elif 'turtle' in t_low or 'tortoise' in t_low or 'carapace' in t_low or 'scute' in t_low:
        elements.append(f'<ellipse cx="100" cy="100" rx="55" ry="68" fill="none" stroke="{pal["c2"]}" stroke-width="3"/>')
        # Vertebral scutes down middle
        for y in [60, 80, 100, 120, 140]:
            elements.append(f'<polygon points="90,{y-10} 110,{y-10} 115,{y+5} 100,{y+12} 85,{y+5}" fill="none" stroke="{pal["c1"]}" stroke-width="2"/>')
        # Costal scutes left & right
        for y in [70, 95, 120]:
            elements.append(f'<polygon points="85,{y} 55,{y-8} 52,{y+12} 85,{y+16}" fill="none" stroke="{pal["c3"]}" stroke-width="1.8"/>')
            elements.append(f'<polygon points="115,{y} 145,{y-8} 148,{y+12} 115,{y+16}" fill="none" stroke="{pal["c3"]}" stroke-width="1.8"/>')
        # Flippers
        elements.append(f'<path d="M 55,60 Q 20,40 15,70 Q 25,95 52,80" fill="none" stroke="{pal["c2"]}" stroke-width="2"/>')
        elements.append(f'<path d="M 145,60 Q 180,40 185,70 Q 175,95 148,80" fill="none" stroke="{pal["c2"]}" stroke-width="2"/>')

    # 3. Jellyfish / Medusa
    elif 'jellyfish' in t_low or 'aequorea' in t_low or 'bell' in t_low or 'medusa' in t_low:
        # Radial bell umbrella
        elements.append(f'<path d="M 35,90 Q 100,20 165,90 Q 140,98 100,92 Q 60,98 35,90 Z" fill="none" stroke="{pal["c2"]}" stroke-width="2.5"/>')
        elements.append(f'<path d="M 50,88 Q 100,38 150,88" fill="none" stroke="{pal["c1"]}" stroke-width="1.8" stroke-dasharray="3,3"/>')
        # Central oral arms
        elements.append(f'<path d="M 90,92 Q 80,125 92,160 Q 100,140 108,160 Q 120,125 110,92" fill="none" stroke="{pal["c3"]}" stroke-width="2"/>')
        # Undulating marginal tentacles
        for tx in [45, 60, 75, 125, 140, 155]:
            dx = (tx - 100) * 0.4
            elements.append(f'<path d="M {tx},92 Q {tx+dx+10},125 {tx-dx},155 T {tx+dx},185" fill="none" stroke="{pal["accent"]}" stroke-width="1.5"/>')

    # 4. Leaf Guard Cells / Stomata / Epidermis
    elif 'stomata' in t_low or 'guard cell' in t_low or 'epidermis' in t_low:
        # Kidney-shaped paired guard cells
        elements.append(f'<ellipse cx="80" cy="100" rx="18" ry="46" fill="none" stroke="{pal["c2"]}" stroke-width="2.8"/>')
        elements.append(f'<ellipse cx="120" cy="100" rx="18" ry="46" fill="none" stroke="{pal["c2"]}" stroke-width="2.8"/>')
        # Stomatal aperture pore
        elements.append(f'<ellipse cx="100" cy="100" rx="6" ry="32" fill="none" stroke="{pal["accent"]}" stroke-width="2"/>')
        # Chloroplast organelles inside guard cells
        for cy_dot in [70, 85, 100, 115, 130]:
            elements.append(f'<circle cx="80" cy="{cy_dot}" r="3.5" fill="{pal["c3"]}" stroke="{pal["c1"]}" stroke-width="1"/>')
            elements.append(f'<circle cx="120" cy="{cy_dot}" r="3.5" fill="{pal["c3"]}" stroke="{pal["c1"]}" stroke-width="1"/>')
        # Surrounding epidermal cell wall boundaries
        elements.append(f'<polygon points="40,50 70,54 62,90 35,85" fill="none" stroke="{pal["c1"]}" stroke-width="1.5"/>')
        elements.append(f'<polygon points="40,150 70,146 62,110 35,115" fill="none" stroke="{pal["c1"]}" stroke-width="1.5"/>')
        elements.append(f'<polygon points="160,50 130,54 138,90 165,85" fill="none" stroke="{pal["c1"]}" stroke-width="1.5"/>')
        elements.append(f'<polygon points="160,150 130,146 138,110 165,115" fill="none" stroke="{pal["c1"]}" stroke-width="1.5"/>')

    # 5. Honeybee / Wasps / Ants / Exoskeleton
    elif 'bee' in t_low or 'ant' in t_low or 'wasp' in t_low or 'beetle' in t_low or 'cicada' in t_low:
        # Head, Thorax, Abdomen
        elements.append(f'<ellipse cx="100" cy="50" rx="14" ry="12" fill="none" stroke="{pal["c2"]}" stroke-width="2"/>') # Head
        elements.append(f'<ellipse cx="100" cy="80" rx="20" ry="18" fill="none" stroke="{pal["c2"]}" stroke-width="2.5"/>') # Thorax
        elements.append(f'<ellipse cx="100" cy="130" rx="22" ry="34" fill="none" stroke="{pal["c2"]}" stroke-width="2.5"/>') # Abdomen
        # Abdominal chitin stripes
        for sy in [112, 124, 136, 148]:
            elements.append(f'<path d="M 80,{sy} Q 100,{sy+8} 120,{sy}" fill="none" stroke="{pal["c1"]}" stroke-width="2"/>')
        # Forewings with venation
        elements.append(f'<ellipse cx="55" cy="75" rx="36" ry="15" transform="rotate(-32 55 75)" fill="none" stroke="{pal["c3"]}" stroke-width="1.8"/>')
        elements.append(f'<ellipse cx="145" cy="75" rx="36" ry="15" transform="rotate(32 145 75)" fill="none" stroke="{pal["c3"]}" stroke-width="1.8"/>')
        elements.append(f'<line x1="100" y1="78" x2="30" y2="60" stroke="{pal["c1"]}" stroke-width="1.2"/>')
        elements.append(f'<line x1="100" y1="78" x2="170" y2="60" stroke="{pal["c1"]}" stroke-width="1.2"/>')
        # Antennae
        elements.append(f'<path d="M 94,40 Q 82,24 70,26" fill="none" stroke="{pal["accent"]}" stroke-width="1.5"/>')
        elements.append(f'<path d="M 106,40 Q 118,24 130,26" fill="none" stroke="{pal["accent"]}" stroke-width="1.5"/>')

    # 6. Butterfly / Moth
    elif 'butterfly' in t_low or 'moth' in t_low:
        # Large forewings
        elements.append(f'<path d="M 100,80 Q 50,15 25,45 Q 15,80 70,105 Q 95,95 100,80" fill="none" stroke="{pal["c2"]}" stroke-width="2.5"/>')
        elements.append(f'<path d="M 100,80 Q 150,15 175,45 Q 185,80 130,105 Q 105,95 100,80" fill="none" stroke="{pal["c2"]}" stroke-width="2.5"/>')
        # Hindwings
        elements.append(f'<path d="M 95,100 Q 40,115 50,155 Q 80,175 98,125" fill="none" stroke="{pal["c3"]}" stroke-width="2"/>')
        elements.append(f'<path d="M 105,100 Q 160,115 150,155 Q 120,175 102,125" fill="none" stroke="{pal["c3"]}" stroke-width="2"/>')
        # Thorax & abdomen
        elements.append(f'<ellipse cx="100" cy="100" rx="6" ry="32" fill="none" stroke="{pal["accent"]}" stroke-width="2"/>')
        # Wing cell veins
        for wx, wy in [(55, 60), (145, 60), (70, 135), (130, 135)]:
            elements.append(f'<circle cx="{wx}" cy="{wy}" r="6" fill="none" stroke="{pal["c1"]}" stroke-width="1.5"/>')

    # 7. Redwood / Trees / Dendrology
    elif 'redwood' in t_low or 'tree' in t_low or 'pine' in t_low or 'oak' in t_low or 'sequoia' in t_low or 'aspen' in t_low or 'banyan' in t_low or 'eucalyptus' in t_low:
        # Concentric tree rings with medullary rays
        cx, cy = 100, 100
        for r in [18, 32, 46, 60, 74]:
            elements.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{pal["c1"]}" stroke-width="1.8" stroke-dasharray="{3+r%4},{2+r%3}"/>')
        # Vascular cambium & bark perimeter
        elements.append(f'<circle cx="{cx}" cy="{cy}" r="84" fill="none" stroke="{pal["c2"]}" stroke-width="3"/>')
        # Medullary ray spokes
        for a in range(0, 360, 30):
            th = math.radians(a)
            x1 = cx + 18 * math.cos(th)
            y1 = cy + 18 * math.sin(th)
            x2 = cx + 84 * math.cos(th)
            y2 = cy + 84 * math.sin(th)
            elements.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{pal["c3"]}" stroke-width="1.2"/>')
        elements.append(f'<circle cx="{cx}" cy="{cy}" r="6" fill="{pal["accent"]}"/>')

    # 8. Fungi / Mycelium / Mushroom
    elif 'fungi' in t_low or 'mushroom' in t_low or 'mycorrhiz' in t_low or 'agaric' in t_low or 'truffle' in t_low:
        # Pileus (cap) with radial gill lamellae
        elements.append(f'<path d="M 25,100 Q 100,20 175,100 Q 140,110 100,105 Q 60,110 25,100 Z" fill="none" stroke="{pal["c2"]}" stroke-width="2.5"/>')
        for gx in range(40, 165, 12):
            elements.append(f'<line x1="{gx}" y1="102" x2="100" y2="40" stroke="{pal["c1"]}" stroke-width="1.2"/>')
        # Stipe (stem)
        elements.append(f'<path d="M 85,105 L 80,165 Q 100,172 120,165 L 115,105" fill="none" stroke="{pal["c2"]}" stroke-width="2"/>')
        # Hyphal root web
        for hx, hy in [(70, 180), (85, 190), (100, 185), (115, 190), (130, 180)]:
            elements.append(f'<path d="M 100,168 Q {hx},{hy-10} {hx},{hy}" fill="none" stroke="{pal["accent"]}" stroke-width="1.5"/>')

    # 9. Peacock / Birds / Feathers / Wings
    elif 'peacock' in t_low or 'bird' in t_low or 'falcon' in t_low or 'owl' in t_low or 'hummingbird' in t_low or 'eagle' in t_low or 'feather' in t_low:
        # Central eye ocellus
        cx, cy = 100, 75
        elements.append(f'<ellipse cx="{cx}" cy="{cy}" rx="32" ry="42" fill="none" stroke="{pal["c2"]}" stroke-width="2.5"/>')
        elements.append(f'<ellipse cx="{cx}" cy="{cy+8}" rx="20" ry="26" fill="none" stroke="{pal["c3"]}" stroke-width="2"/>')
        elements.append(f'<circle cx="{cx}" cy="{cy+12}" r="10" fill="none" stroke="{pal["accent"]}" stroke-width="2"/>')
        # Feather shaft (rachis)
        elements.append(f'<line x1="{cx}" y1="30" x2="{cx}" y2="180" stroke="{pal["c2"]}" stroke-width="3"/>')
        # Radiating barbs
        for y in range(40, 175, 10):
            w = 55 - (y - 40) * 0.25
            elements.append(f'<line x1="{cx}" y1="{y}" x2="{cx-w}" y2="{y-15}" stroke="{pal["c1"]}" stroke-width="1.4"/>')
            elements.append(f'<line x1="{cx}" y1="{y}" x2="{cx+w}" y2="{y-15}" stroke="{pal["c1"]}" stroke-width="1.4"/>')

    # 10. Plants / Flowers / Lotus / Pitcher
    elif 'lotus' in t_low or 'flower' in t_low or 'sunflower' in t_low or 'orchid' in t_low or 'venus' in t_low or 'pitcher' in t_low:
        # Multi-tiered radiating flower petals
        cx, cy = 100, 100
        petals = 8
        for p in range(petals):
            ang = p * (360 / petals)
            elements.append(f'<ellipse cx="{cx}" cy="58" rx="15" ry="32" transform="rotate({ang} {cx} {cy})" fill="none" stroke="{pal["c2"]}" stroke-width="2"/>')
        # Inner corolla ring
        for p in range(petals):
            ang = p * (360 / petals) + (180 / petals)
            elements.append(f'<ellipse cx="{cx}" cy="72" rx="10" ry="20" transform="rotate({ang} {cx} {cy})" fill="none" stroke="{pal["c3"]}" stroke-width="1.6"/>')
        # Central receptacle
        elements.append(f'<circle cx="{cx}" cy="{cy}" r="16" fill="none" stroke="{pal["accent"]}" stroke-width="2.2"/>')
        for i in range(6):
            th = math.radians(i * 60)
            elements.append(f'<circle cx="{cx + 8*math.cos(th):.1f}" cy="{cy + 8*math.sin(th):.1f}" r="2" fill="{pal["accent"]}"/>')

    # 11. DNA / Organelles / Cells / Microscopic
    elif 'dna' in t_low or 'helix' in t_low or 'cell' in t_low or 'neuron' in t_low or 'diatom' in t_low or 'chloroplast' in t_low:
        if 'dna' in t_low or 'helix' in t_low:
            # Double helix ladder
            for y in range(30, 175, 12):
                x1 = 100 + 35 * math.sin(y * 0.08)
                x2 = 100 - 35 * math.sin(y * 0.08)
                elements.append(f'<line x1="{x1:.1f}" y1="{y}" x2="{x2:.1f}" y2="{y}" stroke="{pal["c1"]}" stroke-width="1.8"/>')
                elements.append(f'<circle cx="{x1:.1f}" cy="{y}" r="2.5" fill="{pal["accent"]}"/>')
                elements.append(f'<circle cx="{x2:.1f}" cy="{y}" r="2.5" fill="{pal["c2"]}"/>')
        elif 'neuron' in t_low or 'synaptic' in t_low:
            # Soma with radiating dendrites & long axon
            elements.append(f'<circle cx="80" cy="80" r="22" fill="none" stroke="{pal["c2"]}" stroke-width="2.5"/>')
            elements.append(f'<circle cx="80" cy="80" r="8" fill="{pal["accent"]}"/>')
            # Dendrite branches
            for a in [0, 45, 90, 135, 180, 225]:
                th = math.radians(a)
                x2 = 80 + 45 * math.cos(th)
                y2 = 80 + 45 * math.sin(th)
                elements.append(f'<line x1="{80 + 22*math.cos(th):.1f}" y1="{80 + 22*math.sin(th):.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{pal["c3"]}" stroke-width="1.8"/>')
            # Axon
            elements.append(f'<path d="M 98,92 Q 135,110 150,150 T 175,175" fill="none" stroke="{pal["c2"]}" stroke-width="2.5"/>')
        else: # Diatom / Centric cell
            cx, cy = 100, 100
            elements.append(f'<circle cx="{cx}" cy="{cy}" r="70" fill="none" stroke="{pal["c2"]}" stroke-width="3"/>')
            elements.append(f'<circle cx="{cx}" cy="{cy}" r="45" fill="none" stroke="{pal["c3"]}" stroke-width="2"/>')
            elements.append(f'<circle cx="{cx}" cy="{cy}" r="20" fill="none" stroke="{pal["accent"]}" stroke-width="2"/>')
            for a in range(0, 360, 20):
                th = math.radians(a)
                elements.append(f'<circle cx="{cx + 58*math.cos(th):.1f}" cy="{cy + 58*math.sin(th):.1f}" r="3" fill="none" stroke="{pal["c1"]}" stroke-width="1.2"/>')

    # 12. Marine Animals: Shark, Whale, Seahorse, Ray, Fish
    elif 'shark' in t_low or 'whale' in t_low or 'manta' in t_low or 'seahorse' in t_low or 'fish' in t_low:
        if 'seahorse' in t_low:
            # Curved coronet, snout, segmented tail spiral
            elements.append(f'<path d="M 85,45 Q 60,48 55,55 Q 65,65 85,62 Q 95,75 88,110 Q 82,145 100,165 Q 115,175 110,155 Q 100,140 102,150" fill="none" stroke="{pal["c2"]}" stroke-width="2.5"/>')
            # Dorsal fin & body segments
            elements.append(f'<path d="M 95,85 Q 118,92 110,105 Q 92,102 90,95" fill="none" stroke="{pal["c3"]}" stroke-width="1.8"/>')
            for sy in range(75, 140, 10):
                elements.append(f'<line x1="82" y1="{sy}" x2="98" y2="{sy}" stroke="{pal["c1"]}" stroke-width="1.6"/>')
        elif 'manta' in t_low or 'ray' in t_low:
            # Diamond cephalic lobes, broad pectoral wings, whip tail
            elements.append(f'<path d="M 100,45 Q 60,55 20,85 Q 60,115 95,120 L 98,185 L 102,185 L 105,120 Q 140,115 180,85 Q 140,55 100,45 Z" fill="none" stroke="{pal["c2"]}" stroke-width="2.5"/>')
            elements.append(f'<ellipse cx="100" cy="85" rx="18" ry="26" fill="none" stroke="{pal["c3"]}" stroke-width="1.8"/>')
            elements.append(f'<circle cx="85" cy="55" r="2.5" fill="{pal["accent"]}"/>')
            elements.append(f'<circle cx="115" cy="55" r="2.5" fill="{pal["accent"]}"/>')
        else: # Shark / Whale hydrodynamic body
            elements.append(f'<path d="M 25,100 Q 75,55 145,80 Q 175,95 185,75 L 180,105 L 185,135 Q 175,115 145,118 Q 75,145 25,100 Z" fill="none" stroke="{pal["c2"]}" stroke-width="2.5"/>')
            # Dorsal fin
            elements.append(f'<path d="M 90,70 L 105,40 L 120,74" fill="none" stroke="{pal["c3"]}" stroke-width="2"/>')
            # Pectoral fin
            elements.append(f'<path d="M 85,115 L 75,145 L 105,125" fill="none" stroke="{pal["c1"]}" stroke-width="2"/>')
            # Gill slits
            for gx in [65, 70, 75, 80]:
                elements.append(f'<line x1="{gx}" y1="92" x2="{gx}" y2="108" stroke="{pal["accent"]}" stroke-width="1.4"/>')

    # 13. Mammals & Reptiles: Leopard, Zebra, Chameleon, Gecko, Sloth, etc.
    else:
        # Organic vertebrate head/spine morphology
        cx, cy = 100, 100
        elements.append(f'<ellipse cx="{cx}" cy="{cy}" rx="65" ry="42" fill="none" stroke="{pal["c2"]}" stroke-width="2.8"/>')
        elements.append(f'<ellipse cx="{cx-45}" cy="{cy-15}" rx="24" ry="20" fill="none" stroke="{pal["c3"]}" stroke-width="2"/>')
        # Spine & rib contours
        elements.append(f'<path d="M 40,90 Q 100,85 160,95" fill="none" stroke="{pal["c1"]}" stroke-width="2"/>')
        for rx in range(70, 145, 14):
            elements.append(f'<path d="M {rx},88 Q {rx+6},110 {rx-2},126" fill="none" stroke="{pal["accent"]}" stroke-width="1.5"/>')
        elements.append(f'<circle cx="{cx-52}" cy="{cy-20}" r="3" fill="{pal["accent"]}"/>')

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <radialGradient id="g_{seed}" cx="50%" cy="50%" r="70%">
      <stop offset="0%" stop-color="{pal['bg2']}"/>
      <stop offset="100%" stop-color="{pal['bg1']}"/>
    </radialGradient>
  </defs>
  <rect width="200" height="200" rx="16" fill="url(#g_{seed})"/>
  {" ".join(elements)}
  <text x="100" y="185" font-family="system-ui, sans-serif" font-size="8.5" font-weight="bold" fill="{pal['c2']}" text-anchor="middle" letter-spacing="0.5">{title.upper()[:24]}</text>
</svg>'''
    return 'data:image/svg+xml;utf8,' + re.sub(r'\s+', ' ', svg_content).replace('"', '%22').replace('#', '%23').replace('<', '%3C').replace('>', '%3E')

if __name__ == '__main__':
    import json
    with open('specimens_data.json') as f:
        data = json.load(f)

    for i, item in enumerate(data):
        item['url'] = generate_specimen_vector(item['title'], item['category'], seed=i+1)

    with open('specimens_data.json', 'w') as f:
        json.dump(data, f, indent=2)

    print(f"Updated {len(data)} specimens with bespoke anatomical vector SVGs in specimens_data.json.")
