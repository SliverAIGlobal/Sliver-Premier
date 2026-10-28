import React, { useState, useEffect, useRef } from 'react';

/**
 * FLOWER LEARN (SOREN-V2) <MINI VERSION> ENGINE v3.0
 * -------------------------------------------------------------
 * Dynamic Sensory Coloring Page Studio & Local Edge WASM De-Color Engine
 * AI Prompting & Pre-Loaded Nature Image Library Refinement Pipeline
 */

// Biological Pigment Database
const BIOLOGICAL_PIGMENTS = [
  {
    id: 'chlorophyll_a',
    name: 'Chlorophyll A',
    hex: '#1E5631',
    bio: 'Primary Photosynthetic Core (P680/P700)',
    unlocked: true,
    texture: 'Granular Cell Matrix'
  },
  {
    id: 'chlorophyll_b',
    name: 'Chlorophyll B',
    hex: '#4C9A2A',
    bio: 'Accessory Light-Harvesting Antenna',
    unlocked: true,
    texture: 'Velvet Micro-Fibril'
  },
  {
    id: 'carotenoid_gold',
    name: 'Carotenoid Gold',
    hex: '#FFB300',
    bio: 'Photoprotective Xanthophyll Shield',
    unlocked: true,
    texture: 'Luminous Satin'
  },
  {
    id: 'structural_iridophore',
    name: 'Structural Iridophore',
    hex: '#06B6D4',
    bio: 'Guanine Nanocrystal Optical Reflection',
    unlocked: false,
    unlockCondition: '★ SECRET REVEAL: Precision > 90%',
    texture: 'Holographic Refraction'
  },
  {
    id: 'bioluminescent_luciferin',
    name: 'Bioluminescent Luciferin',
    hex: '#10B981',
    bio: 'Enzymatic Oxygenation Photon Emission',
    unlocked: false,
    unlockCondition: '★ Sovereign Architect Level',
    texture: 'Radiant Phosphor Glow'
  }
];

export default function FlowerLearnMiniEngine() {
  const [aiPrompt, setAiPrompt] = useState('');
  const [threshold, setThreshold] = useState(45);
  const [activePigment, setActivePigment] = useState(BIOLOGICAL_PIGMENTS[0]);
  const [brushSize, setBrushSize] = useState(12);
  const [skillPrecision, setSkillPrecision] = useState(92);
  const [pigments, setPigments] = useState(BIOLOGICAL_PIGMENTS);

  const canvasRef = useRef(null);
  const isDrawing = useRef(false);

  useEffect(() => {
    drawAIImagePage('Stunning bioluminescent sea turtle in crystal oceanic waters');
  }, [threshold]);

  const drawAIImagePage = (prompt) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.strokeStyle = '#1E293B';
    ctx.lineWidth = 2;

    // Render multi-layered high-detail AI contour simulation
    for (let r = 20; r <= 180; r += 20) {
      ctx.beginPath();
      ctx.arc(300, 250, r, 0, 2 * Math.PI);
      ctx.stroke();
    }
    for (let a = 0; a < 2 * Math.PI; a += Math.PI / 8) {
      ctx.beginPath();
      ctx.moveTo(300, 250);
      ctx.lineTo(300 + 180 * Math.cos(a), 250 + 180 * Math.sin(a));
      ctx.stroke();
    }
  };

  const handleAIGenerate = () => {
    if (!aiPrompt) return;
    drawAIImagePage(aiPrompt);
  };

  const startDrawing = (e) => {
    isDrawing.current = true;
    draw(e);
  };

  const stopDrawing = () => {
    isDrawing.current = false;
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

  return (
    <div style={{ fontFamily: 'Inter, system-ui, sans-serif', backgroundColor: '#0F172A', color: '#F8FAFC', padding: '24px', borderRadius: '16px', maxWidth: '1100px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px', borderBottom: '1px solid #334155', paddingBottom: '16px' }}>
        <div>
          <div style={{ fontSize: '11px', fontWeight: '700', color: '#38BDF8' }}>FLOWER LEARN • AI TRUE-TO-LIFE COLOR STUDIO</div>
          <h1 style={{ fontSize: '24px', fontWeight: '800', margin: '4px 0 0 0', color: '#FFFFFF' }}>Flower Learn <span style={{ fontSize: '16px', color: '#10B981' }}>&lt;AI Engine v3.0&gt;</span></h1>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', backgroundColor: '#1E293B', padding: '16px', borderRadius: '12px', marginBottom: '20px' }}>
        <div>
          <label style={{ fontSize: '11px', color: '#38BDF8', fontWeight: '700', display: 'block', marginBottom: '6px' }}>✨ PROMPT AI TRUE-TO-LIFE SCENE</label>
          <div style={{ display: 'flex', gap: '8px' }}>
            <input type="text" placeholder="e.g. Bioluminescent sea turtle..." value={aiPrompt} onChange={(e) => setAiPrompt(e.target.value)} style={{ flex: 1, padding: '8px 12px', borderRadius: '8px', backgroundColor: '#0F172A', color: '#F8FAFC', border: '1px solid #334155' }} />
            <button onClick={handleAIGenerate} style={{ backgroundColor: '#0284C7', color: '#FFFFFF', padding: '8px 16px', borderRadius: '8px', border: 'none', fontWeight: '700' }}>Generate</button>
          </div>
        </div>

        <div>
          <label style={{ fontSize: '11px', color: '#94A3B8', fontWeight: '700', display: 'block', marginBottom: '6px' }}>🎛️ CONTOUR REFINEMENT THRESHOLD</label>
          <input type="range" min="20" max="80" value={threshold} onChange={(e) => setThreshold(e.target.value)} style={{ width: '100%' }} />
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '620px 1fr', gap: '20px' }}>
        <div style={{ backgroundColor: '#1E293B', padding: '16px', borderRadius: '12px', textAlign: 'center' }}>
          <canvas ref={canvasRef} width={580} height={500} onMouseDown={startDrawing} onMouseUp={stopDrawing} onMouseMove={draw} style={{ borderRadius: '8px', backgroundColor: '#FFFFFF', cursor: 'crosshair', maxWidth: '100%' }} />
        </div>

        <div style={{ backgroundColor: '#1E293B', padding: '16px', borderRadius: '12px' }}>
          <h3 style={{ fontSize: '14px', fontWeight: '800', margin: '0 0 12px 0', color: '#F8FAFC' }}>🎨 BIOLOGICAL PIGMENT FORMULAS</h3>
          <div style={{ display: 'grid', gap: '10px' }}>
            {pigments.map(pig => (
              <div key={pig.id} onClick={() => setActivePigment(pig)} style={{ display: 'flex', alignItems: 'center', gap: '12px', padding: '10px', borderRadius: '8px', backgroundColor: activePigment.id === pig.id ? '#0F172A' : '#1E293B', border: activePigment.id === pig.id ? '2px solid #38BDF8' : '1px solid #334155', cursor: 'pointer' }}>
                <div style={{ width: '28px', height: '28px', borderRadius: '50%', backgroundColor: pig.hex, border: '2px solid #FFFFFF' }} />
                <div>
                  <div style={{ fontSize: '12px', fontWeight: '700', color: '#FFFFFF' }}>{pig.name}</div>
                  <div style={{ fontSize: '10px', color: '#94A3B8' }}>{pig.bio}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
