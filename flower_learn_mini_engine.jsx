import React, { useState, useEffect, useRef } from 'react';

/**
 * FLOWER LEARN (SOREN-V2) <MINI VERSION> ENGINE
 * -------------------------------------------------------------
 * Dynamic Sensory Coloring Page Studio & Local Edge WASM De-Color Engine
 * Zero API Dependencies | 100% Local Canvas Computation
 */

// Biological Pigment Database
const BIOLOGICAL_PIGMENTS = [
  {
    id: 'chlorophyll_a',
    name: 'Chlorophyll A',
    hex: '#1E5631',
    bio: 'Primary Photosynthetic Core (P680/P700)',
    unlocked: true,
    texture: 'Granular Cell Matrix',
    category: 'Botanical'
  },
  {
    id: 'chlorophyll_b',
    name: 'Chlorophyll B',
    hex: '#4C9A2A',
    bio: 'Accessory Light-Harvesting Antenna',
    unlocked: true,
    texture: 'Velvet Micro-Fibril',
    category: 'Botanical'
  },
  {
    id: 'carotenoid_gold',
    name: 'Carotenoid Gold',
    hex: '#FFB300',
    bio: 'Photoprotective Xanthophyll Shield',
    unlocked: false,
    unlockCondition: 'Reach 80% Skill Precision',
    texture: 'Luminous Satin',
    category: 'Botanical'
  },
  {
    id: 'anthocyanin_purple',
    name: 'Anthocyanin Purple',
    hex: '#7E22CE',
    bio: 'Vacuolar Osmotic & UV Shield',
    unlocked: false,
    unlockCondition: 'Complete Guard Cell Quiz',
    texture: 'Silky Sheen',
    category: 'Botanical'
  },
  {
    id: 'keratin_amber',
    name: 'Keratin Scute Amber',
    hex: '#D97706',
    bio: 'Chelonian Epidermal Armor Layer',
    unlocked: true,
    texture: 'Tactile Scaley Scute',
    category: 'Marine Bio'
  },
  {
    id: 'structural_iridophore',
    name: 'Structural Iridophore',
    hex: '#06B6D4',
    bio: 'Guanine Nanocrystal Optical Reflection',
    unlocked: false,
    unlockCondition: '★ SECRET REVEAL: Precision > 90%',
    texture: 'Holographic Refraction',
    category: 'Marine Bio'
  },
  {
    id: 'bioluminescent_luciferin',
    name: 'Bioluminescent Luciferin',
    hex: '#10B981',
    bio: 'Enzymatic Oxygenation Photon Emission',
    unlocked: false,
    unlockCondition: '★ Sovereign Architect Level',
    texture: 'Radiant Phosphor Glow',
    category: 'Bioluminescence'
  }
];

// Topic Presets
const TOPICS = [
  {
    id: 'sea_turtle',
    title: 'Chelonia Mydas (Sea Turtle)',
    subtitle: 'Epidermal Scute Patterns & Iridophore Optics',
    ageRecommended: 'Scholar / Sovereign',
    defaultDetail: 'High',
    bioFact: 'Sea turtle shells consist of keratin scutes over bony carapace matrix. Iridophore cells reflect cyan light via guanine crystals.'
  },
  {
    id: 'guard_cells',
    title: 'Leaf Guard Cells & Stomata',
    subtitle: 'Stomatal Gas Exchange & Chloroplast Architecture',
    ageRecommended: 'Scholar',
    defaultDetail: 'Medium',
    bioFact: 'Guard cells inflate with water via potassium influx to open stomatal pores for CO2 uptake and transpiration.'
  },
  {
    id: 'xylem_transport',
    title: 'Xylem Vessels & Micro-Capillaries',
    subtitle: 'Lignified Tracheids & Cohesion-Tension Flow',
    ageRecommended: 'Sovereign',
    defaultDetail: 'High',
    bioFact: 'Xylem tracheids feature ring-like lignin reinforcements that withstand negative pressure during sap ascent.'
  }
];

export default function FlowerLearnMiniEngine() {
  // Engine Controls State
  const [ageGroup, setAgeGroup] = useState('Scholar'); // 'Botanist' (4-8), 'Scholar' (9-14), 'Sovereign' (15+)
  const [selectedTopic, setSelectedTopic] = useState(TOPICS[0]);
  const [detailLevel, setDetailLevel] = useState('High'); // 'Low', 'Medium', 'High'

  // Studio & Canvas State
  const [activePigment, setActivePigment] = useState(BIOLOGICAL_PIGMENTS[0]);
  const [brushSize, setBrushSize] = useState(12);
  const [activeTexture, setActiveTexture] = useState('Granular Cell Matrix');
  const [skillPrecision, setSkillPrecision] = useState(78); // %
  const [pigments, setPigments] = useState(BIOLOGICAL_PIGMENTS);
  const [unlockedSecret, setUnlockedSecret] = useState(false);
  const [activeTab, setActiveTab] = useState('studio'); // 'studio', 'decolor_wasm', 'learn'
  const [customImageLoaded, setCustomImageLoaded] = useState(false);

  // Canvas Refs
  const canvasRef = useRef(null);
  const isDrawing = useRef(false);

  // Initialize Line Art on Canvas
  useEffect(() => {
    drawPresetLineArt();
  }, [selectedTopic, detailLevel, ageGroup]);

  // Handle Local Line Art Drawing (Canvas)
  const drawPresetLineArt = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Background
    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.strokeStyle = '#1E293B';
    ctx.lineWidth = detailLevel === 'Low' ? 4 : detailLevel === 'Medium' ? 3 : 2;
    ctx.lineCap = 'round';

    if (selectedTopic.id === 'sea_turtle') {
      // Draw Sea Turtle Shell Outline
      ctx.beginPath();
      ctx.ellipse(300, 250, 180, 140, 0, 0, 2 * Math.PI);
      ctx.stroke();

      // Scutes
      ctx.beginPath();
      ctx.moveTo(180, 250);
      ctx.lineTo(240, 200);
      ctx.lineTo(300, 200);
      ctx.lineTo(360, 200);
      ctx.lineTo(420, 250);
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(180, 250);
      ctx.lineTo(240, 300);
      ctx.lineTo(300, 300);
      ctx.lineTo(360, 300);
      ctx.lineTo(420, 250);
      ctx.stroke();

      // Turtle Head
      ctx.beginPath();
      ctx.arc(520, 250, 45, -Math.PI / 2, Math.PI / 2);
      ctx.stroke();
      ctx.beginPath();
      ctx.arc(535, 235, 8, 0, 2 * Math.PI);
      ctx.fillStyle = '#1E293B';
      ctx.fill();

      // Flippers
      ctx.beginPath();
      ctx.moveTo(380, 140);
      ctx.quadraticCurveTo(460, 40, 500, 20);
      ctx.quadraticCurveTo(430, 80, 320, 120);
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(380, 360);
      ctx.quadraticCurveTo(460, 460, 500, 480);
      ctx.quadraticCurveTo(430, 420, 320, 380);
      ctx.stroke();

      // Labels if Scholar/Sovereign
      if (ageGroup !== 'Botanist') {
        ctx.font = '12px Inter, sans-serif';
        ctx.fillStyle = '#64748B';
        ctx.fillText('★ [Secret Reveal: Iridophore Layer]', 220, 180);
        ctx.fillText('[Keratin Scute Matrix]', 240, 255);
      }
    } else {
      // Guard Cells & Stoma
      ctx.beginPath();
      ctx.ellipse(230, 250, 60, 130, 0, 0, 2 * Math.PI);
      ctx.stroke();

      ctx.beginPath();
      ctx.ellipse(370, 250, 60, 130, 0, 0, 2 * Math.PI);
      ctx.stroke();

      // Stoma Pore
      ctx.beginPath();
      ctx.ellipse(300, 250, 20, 90, 0, 0, 2 * Math.PI);
      ctx.setLineDash([4, 4]);
      ctx.stroke();
      ctx.setLineDash([]);

      // Chloroplasts
      const chloroplasts = [[210, 180], [210, 250], [210, 320], [390, 180], [390, 250], [390, 320]];
      chloroplasts.forEach(([cx, cy]) => {
        ctx.beginPath();
        ctx.arc(cx, cy, 14, 0, 2 * Math.PI);
        ctx.stroke();
      });

      ctx.font = '12px Inter, sans-serif';
      ctx.fillStyle = '#64748B';
      ctx.fillText('STOMATAL PORE (CO2 Intake)', 215, 110);
    }
  };

  // Local Sobel De-Coloring Filter (Pure JS Canvas Edge WASM Simulation)
  const applyEdgeDeColor = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const img = new Image();
    img.onload = () => {
      const canvas = canvasRef.current;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

      // Get Image Data for Local Sobel Edge Detection
      const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
      const data = imgData.data;
      const w = canvas.width;
      const h = canvas.height;

      const grayscale = new Uint8Array(w * h);
      for (let i = 0; i < data.length; i += 4) {
        grayscale[i / 4] = 0.299 * data[i] + 0.587 * data[i + 1] + 0.114 * data[i + 2];
      }

      const output = ctx.createImageData(w, h);
      const outData = output.data;

      // Sobel Kernels
      for (let y = 1; y < h - 1; y++) {
        for (let x = 1; x < w - 1; x++) {
          const idx = y * w + x;
          const gx =
            -1 * grayscale[(y - 1) * w + (x - 1)] + 1 * grayscale[(y - 1) * w + (x + 1)] +
            -2 * grayscale[y * w + (x - 1)]       + 2 * grayscale[y * w + (x + 1)] +
            -1 * grayscale[(y + 1) * w + (x - 1)] + 1 * grayscale[(y + 1) * w + (x + 1)];

          const gy =
            -1 * grayscale[(y - 1) * w + (x - 1)] - 2 * grayscale[(y - 1) * w + x] - 1 * grayscale[(y - 1) * w + (x + 1)] +
             1 * grayscale[(y + 1) * w + (x - 1)] + 2 * grayscale[(y + 1) * w + x] + 1 * grayscale[(y + 1) * w + (x + 1)];

          const magnitude = Math.sqrt(gx * gx + gy * gy);
          const edge = magnitude > 50 ? 0 : 255; // Inverse line art (black outline on white)

          const outIdx = idx * 4;
          outData[outIdx] = edge;
          outData[outIdx + 1] = edge;
          outData[outIdx + 2] = edge;
          outData[outIdx + 3] = 255;
        }
      }

      ctx.putImageData(output, 0, 0);
      setCustomImageLoaded(true);
    };
    img.src = URL.createObjectURL(file);
  };

  // Drawing Handlers
  const startDrawing = (e) => {
    isDrawing.current = true;
    draw(e);
  };

  const stopDrawing = () => {
    isDrawing.current = false;
    // Simulate Precision Increment
    const newPrec = Math.min(100, skillPrecision + 2);
    setSkillPrecision(newPrec);
    if (newPrec >= 90 && !unlockedSecret) {
      setUnlockedSecret(true);
      setPigments(prev => prev.map(p => p.id === 'structural_iridophore' ? { ...p, unlocked: true } : p));
    }
  };

  const draw = (e) => {
    if (!isDrawing.current) return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    ctx.fillStyle = activePigment.hex;
    ctx.beginPath();
    ctx.arc(x, y, brushSize / 2, 0, 2 * Math.PI);
    ctx.fill();
  };

  // Export Canvas Handler
  const downloadColoringPage = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const link = document.createElement('a');
    link.download = `flower_learn_${selectedTopic.id}_${ageGroup}.png`;
    link.href = canvas.toDataURL('image/png');
    link.click();
  };

  return (
    <div style={{
      fontFamily: 'Inter, system-ui, sans-serif',
      backgroundColor: '#0F172A',
      color: '#F8FAFC',
      padding: '24px',
      borderRadius: '16px',
      maxWidth: '1100px',
      margin: '0 auto',
      boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.5)'
    }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', borderBottom: '1px solid #334155', paddingBottom: '16px' }}>
        <div>
          <div style={{ fontSize: '11px', fontWeight: '700', color: '#38BDF8', letterSpacing: '1px', textTransform: 'uppercase' }}>
            SOREN-V2 ENGINE • EDGE WASM COLOR STUDIO
          </div>
          <h1 style={{ fontSize: '24px', fontWeight: '800', margin: '4px 0 0 0', color: '#FFFFFF' }}>
            Flower Learn <span style={{ fontSize: '16px', color: '#10B981', fontWeight: '600' }}>&lt;mini version&gt;</span>
          </h1>
        </div>

        {/* Skill Precision Gauge */}
        <div style={{ backgroundColor: '#1E293B', padding: '10px 16px', borderRadius: '12px', border: '1px solid #334155', textAlign: 'right' }}>
          <div style={{ fontSize: '10px', color: '#94A3B8', fontWeight: '600' }}>SKILL PRECISION</div>
          <div style={{ fontSize: '18px', fontWeight: '800', color: skillPrecision >= 90 ? '#10B981' : '#F59E0B' }}>
            {skillPrecision}% {unlockedSecret && '★ REVEAL UNLOCKED'}
          </div>
        </div>
      </div>

      {/* Engine Controls Bar */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '16px', backgroundColor: '#1E293B', padding: '16px', borderRadius: '12px', marginBottom: '20px' }}>
        {/* Age Choice */}
        <div>
          <label style={{ fontSize: '11px', color: '#94A3B8', fontWeight: '700', display: 'block', marginBottom: '6px' }}>
            AGE / COGNITIVE LEVEL
          </label>
          <select
            value={ageGroup}
            onChange={(e) => setAgeGroup(e.target.value)}
            style={{ width: '100%', padding: '8px 12px', borderRadius: '8px', backgroundColor: '#0F172A', color: '#F8FAFC', border: '1px solid #334155', fontWeight: '600' }}
          >
            <option value="Botanist">Little Botanist (Age 4-8) - Bold Lines</option>
            <option value="Scholar">Young Scholar (Age 9-14) - Micro-Anatomy</option>
            <option value="Sovereign">Sovereign Architect (Age 15+) - Full Spectra</option>
          </select>
        </div>

        {/* Topic Choice */}
        <div>
          <label style={{ fontSize: '11px', color: '#94A3B8', fontWeight: '700', display: 'block', marginBottom: '6px' }}>
            BIOLOGICAL TOPIC LIBRARY
          </label>
          <select
            value={selectedTopic.id}
            onChange={(e) => setSelectedTopic(TOPICS.find(t => t.id === e.target.value))}
            style={{ width: '100%', padding: '8px 12px', borderRadius: '8px', backgroundColor: '#0F172A', color: '#F8FAFC', border: '1px solid #334155', fontWeight: '600' }}
          >
            {TOPICS.map(t => (
              <option key={t.id} value={t.id}>{t.title}</option>
            ))}
          </select>
        </div>

        {/* Detail Level Choice */}
        <div>
          <label style={{ fontSize: '11px', color: '#94A3B8', fontWeight: '700', display: 'block', marginBottom: '6px' }}>
            LINE ART DETAIL LEVEL
          </label>
          <div style={{ display: 'flex', gap: '8px' }}>
            {['Low', 'Medium', 'High'].map(lvl => (
              <button
                key={lvl}
                onClick={() => setDetailLevel(lvl)}
                style={{
                  flex: 1,
                  padding: '8px',
                  borderRadius: '8px',
                  border: 'none',
                  backgroundColor: detailLevel === lvl ? '#0EA5E9' : '#0F172A',
                  color: '#FFFFFF',
                  fontWeight: '700',
                  fontSize: '12px',
                  cursor: 'pointer'
                }}
              >
                {lvl}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Main Workspace: Canvas + Sensory Palette */}
      <div style={{ display: 'grid', gridTemplateColumns: '620px 1fr', gap: '20px' }}>
        {/* Canvas Area */}
        <div style={{ backgroundColor: '#1E293B', padding: '16px', borderRadius: '12px', textAlign: 'center' }}>
          <canvas
            ref={canvasRef}
            width={580}
            height={500}
            onMouseDown={startDrawing}
            onMouseUp={stopDrawing}
            onMouseMove={draw}
            style={{
              borderRadius: '8px',
              backgroundColor: '#FFFFFF',
              cursor: 'crosshair',
              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.3)',
              maxWidth: '100%'
            }}
          />

          {/* Local De-Color & Export Controls */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '14px' }}>
            <label style={{
              backgroundColor: '#334155',
              padding: '8px 14px',
              borderRadius: '8px',
              fontSize: '12px',
              fontWeight: '600',
              cursor: 'pointer',
              color: '#38BDF8'
            }}>
              📷 Local Edge WASM De-Color Picture
              <input type="file" accept="image/*" onChange={applyEdgeDeColor} style={{ display: 'none' }} />
            </label>

            <button
              onClick={downloadColoringPage}
              style={{
                backgroundColor: '#10B981',
                color: '#FFFFFF',
                padding: '8px 18px',
                borderRadius: '8px',
                border: 'none',
                fontWeight: '700',
                fontSize: '12px',
                cursor: 'pointer'
              }}
            >
              ↓ Export to Color Studio (PNG)
            </button>
          </div>
        </div>

        {/* Sensory Pigment & Texture Studio */}
        <div style={{ backgroundColor: '#1E293B', padding: '16px', borderRadius: '12px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div>
            <h3 style={{ fontSize: '14px', fontWeight: '800', margin: '0 0 12px 0', color: '#F8FAFC' }}>
              🎨 BIOLOGICAL PIGMENT FORMULAS
            </h3>

            <div style={{ display: 'grid', gap: '10px', maxHeight: '320px', overflowY: 'auto' }}>
              {pigments.map(pig => (
                <div
                  key={pig.id}
                  onClick={() => pig.unlocked && setActivePigment(pig)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px',
                    padding: '10px',
                    borderRadius: '8px',
                    backgroundColor: activePigment.id === pig.id ? '#0F172A' : '#1E293B',
                    border: activePigment.id === pig.id ? '2px solid #38BDF8' : '1px solid #334155',
                    opacity: pig.unlocked ? 1 : 0.5,
                    cursor: pig.unlocked ? 'pointer' : 'not-allowed'
                  }}
                >
                  <div style={{ width: '28px', height: '28px', borderRadius: '50%', backgroundColor: pig.hex, border: '2px solid #FFFFFF' }} />
                  <div style={{ flex: 1 }}>
                    <div style={{ fontSize: '12px', fontWeight: '700', color: '#FFFFFF' }}>
                      {pig.name} {!pig.unlocked && '🔒'}
                    </div>
                    <div style={{ fontSize: '10px', color: '#94A3B8' }}>{pig.bio}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Active Biological Fact Box */}
          <div style={{ backgroundColor: '#0F172A', padding: '12px', borderRadius: '8px', borderLeft: '4px solid #10B981', marginTop: '12px' }}>
            <div style={{ fontSize: '10px', fontWeight: '700', color: '#10B981', textTransform: 'uppercase' }}>
              BIOLOGICAL INSIGHT ({selectedTopic.title})
            </div>
            <p style={{ fontSize: '11px', color: '#CBD5E1', margin: '4px 0 0 0', lineHeight: '1.4' }}>
              {selectedTopic.bioFact}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
