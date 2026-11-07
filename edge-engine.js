/* ==========================================================================
   COLORWORLD MASTERS STUDIO — Consolidated Engine (edge-engine.js)
   Modules:
     1. SOURCE        - Photo upload, Sobel de-colorer (offline 3x3 kernel)
     2. TOOLS         - Canvas tools, paper textures, somatic tremor low-pass filter
     3. PRECISION     - Coverage & accuracy scoring engine, >=85% gate
     4. JOURNEY       - 10 Masterpiece compositions, ink-bleed reveal animation
     5. KALEIDOSCOPE  - Faceted mirror reflection (6/8/12), vignette eyepiece, rotation
     6. AUDIO         - WebAudio player graph, Focus Ambience binaural beat
     7. EXPORT        - MediaRecorder MIME negotiation, Ken Burns wallpaper, time-lapse, 2x PNG
     8. EDGE-AI       - WebGPU Gemma WebLLM (Tier 1) -> Ollama / FLUX (Tier 2A) -> Procedural (Tier 2B)
     9. I18N & A11Y   - Translations (EN/ES/FR), Read Aloud (speechSynthesis), keyboard nav
    10. GUMROAD       - Opt-in creator publishing flow, CC license block, rate limiting & mock mode
    11. DIAGNOSTICS   - window.runDiagnostics() covering all requirements & BUG regressions
   ========================================================================== */

(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.Colorworld = factory();
  }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  /* ==========================================================================
     SHARED STATE OBJECT
     Shared state between Coloring Studio and Journey Masterpieces.
     Switching modes never resets this state.
     ========================================================================== */
  const state = {
    mode: 'coloring', // 'coloring' | 'journey'
    lang: 'en',

    // Canvas & Image State
    canvas: null,
    ctx: null,
    width: 820,
    height: 820,
    baseLine: null,
    lineMask: null,
    ops: [],
    undoStack: [],
    replaying: false, // BUG-4 fix: guard to suppress recording during replay

    // Tooling State
    tool: 'brush', // brush | marker | pencil | spray | fill | stamp | eraser
    color: '#6d4aff',
    size: 12,
    opacity: 100,
    stampChar: '🌸',
    tremorFilterEnabled: true,
    filterAlpha: 0.25, // Exponential low-pass filter smoothing hand jitter (Part 4)
    smoothPos: null,
    drawing: false,
    lastPos: null,

    // Zoom & Pan
    zoom: 1.0,
    panX: 0,
    panY: 0,
    paperMode: 0, // 0: Warm White, 1: Vintage Cream, 2: Midnight Ink

    // Journey State
    curPieceKey: 'blooming_skull',
    journeyStrokes: [],
    journeyAnimFn: () => {},
    journeyPlaying: false,
    journeyPlayT: 0,
    journeyDur: 4.5,
    journeyBleed: 1.4,
    journeySelectedPalette: 0,
    journeyFidelity: 0,
    journeyPassed: false,

    // Kaleidoscope State
    kaleidoActive: false,
    kaleidoFacets: parseInt(typeof localStorage !== 'undefined' ? (localStorage.getItem('prism_kaleido_facets') || '8') : '8', 10),
    kaleidoAutoSpin: true,
    kaleidoAngle: 0,
    kaleidoSpeed: 0.008, // 2-4 RPM

    // Audio State
    playlist: [],
    trackIdx: -1,
    audioCtx: null,
    audioDest: null,
    srcNode: null,
    audioElement: null,
    focusAmbienceActive: false,
    focusAmbienceGain: null,
    focusOsc1: null,
    focusOsc2: null,

    // Precision & Gate
    precisionScore: 0,
    gateUnlocked: false,

    // Edge AI State
    aiTier: 'Tier 2B (Procedural Fallback)',
    lastPrompt: '',
    lastGrammar: null,

    // Gumroad Module State
    gumroadEnabled: false,
    gumroadToken: '',
    gumroadLicense: 'CC BY-NC-SA 4.0',
    gumroadInstantPublish: false,
    gumroadAttestationChecked: false,
    gumroadAttestationTimestamp: null,
    gumroadProductsCountToday: 0
  };

  /* ==========================================================================
     PAPERS & PALETTES CONSTANTS
     ========================================================================== */
  const PAPERS = [
    { name: 'Warm White', bg: [250, 250, 252], hex: '#fafafc', defaultInk: '#141414' },
    { name: 'Vintage Cream', bg: [244, 240, 230], hex: '#f4f0e6', defaultInk: '#2a1a08' },
    { name: 'Midnight Ink', bg: [18, 18, 28], hex: '#12121c', defaultInk: '#e2e8f0' }
  ];

  const BASIC_PALETTE = [
    '#111111', '#ffffff', '#e63946', '#f4a261', '#e9c46a', '#2a9d8f',
    '#264653', '#6d4aff', '#b8a1ff', '#ff7ab6', '#00d4c8', '#3a86ff'
  ];

  // Biochemical Pigment Swatches (Part 4)
  const BIOCHEMICAL_PIGMENTS = [
    { name: 'Chlorophyll A', hex: '#2d6a4f' },
    { name: 'Chlorophyll B', hex: '#52b788' },
    { name: 'Carotenoid Gold', hex: '#e09f3e' },
    { name: 'Scute Amber', hex: '#9e2a2b' },
    { name: 'Luciferin Glow', hex: '#90be6d' },
    { name: 'Iridophore Cyan', hex: '#48cae4' },
    { name: 'Anthocyanin', hex: '#5c0099' },
    { name: 'Melanin Black', hex: '#1c1917' }
  ];

  const JOURNEY_PALETTES = [
    { name: 'Obsidian', main: '#141414', accent: '#444444', glow: 'rgba(160,60,180,0.2)' },
    { name: 'Crimson Ink', main: '#800f2f', accent: '#a4133c', glow: 'rgba(255,77,109,0.25)' },
    { name: 'Cyber Neon', main: '#03045e', accent: '#0077b6', glow: 'rgba(0,180,216,0.3)' },
    { name: 'Emerald Sage', main: '#1b4332', accent: '#2d6a4f', glow: 'rgba(82,183,136,0.3)' }
  ];

  /* ==========================================================================
     MODULE 1: SOURCE (Photo Upload & Sobel De-colorer)
     ========================================================================== */
  const SourceEngine = {
    sobelConvert(ctx, width, height, threshold, thickness) {
      const src = ctx.getImageData(0, 0, width, height);
      const d = src.data;
      const gray = new Float32Array(width * height);

      // Grayscale luminance pass
      for (let i = 0; i < gray.length; i++) {
        gray[i] = 0.299 * d[i * 4] + 0.587 * d[i * 4 + 1] + 0.114 * d[i * 4 + 2];
      }

      const out = ctx.createImageData(width, height);
      const mag = new Float32Array(gray.length);
      const W = width, H = height;

      // 3x3 Sobel convolution
      for (let y = 1; y < H - 1; y++) {
        const row = y * W;
        const rowPrev = (y - 1) * W;
        const rowNext = (y + 1) * W;
        for (let x = 1; x < W - 1; x++) {
          const i = row + x;
          const gx = -gray[rowPrev + x - 1] - 2 * gray[row + x - 1] - gray[rowNext + x - 1]
                     + gray[rowPrev + x + 1] + 2 * gray[row + x + 1] + gray[rowNext + x + 1];
          const gy = -gray[rowPrev + x - 1] - 2 * gray[rowPrev + x] - gray[rowPrev + x + 1]
                     + gray[rowNext + x - 1] + 2 * gray[rowNext + x] + gray[rowNext + x + 1];
          mag[i] = Math.sqrt(gx * gx + gy * gy);
        }
      }

      let lineMask = new Uint8Array(gray.length);
      for (let y = 0; y < H; y++) {
        const row = y * W;
        for (let x = 0; x < W; x++) {
          const i = row + x;
          const edge = mag[i] > threshold;
          lineMask[i] = edge ? 1 : 0;
          const v = edge ? 20 : 255;
          const o = i * 4;
          out.data[o] = v;
          out.data[o + 1] = v;
          out.data[o + 2] = v;
          out.data[o + 3] = 255;
        }
      }

      // Morphological dilation for line thickness
      if (thickness > 1.0) {
        const m2 = new Uint8Array(lineMask);
        const r = Math.round(thickness / 2);
        for (let y = r; y < H - r; y++) {
          for (let x = r; x < W - r; x++) {
            let hit = 0;
            for (let dy = -r; dy <= r && !hit; dy++) {
              for (let dx = -r; dx <= r; dx++) {
                if (lineMask[(y + dy) * W + (x + dx)]) {
                  hit = 1;
                  break;
                }
              }
            }
            m2[y * W + x] = Math.max(m2[y * W + x], hit);
          }
        }
        lineMask = m2;
        for (let i = 0; i < lineMask.length; i++) {
          const o = i * 4;
          const v = lineMask[i] ? 20 : 255;
          out.data[o] = v;
          out.data[o + 1] = v;
          out.data[o + 2] = v;
        }
      }

      return { imageData: out, lineMask };
    }
  };

  /* ==========================================================================
     MODULE 2: TOOLS (Drawing Engine & Somatic Filter)
     ========================================================================== */
  const ToolsEngine = {
    hexToRgb(hex) {
      let c = hex.replace('#', '');
      if (c.length === 3) c = c.split('').map(x => x + x).join('');
      const num = parseInt(c, 16);
      return { r: (num >> 16) & 255, g: (num >> 8) & 255, b: num & 255 };
    },

    // Somatic low-pass filter (Part 4) to dampen hand tremors
    filterPointer(newPt, prevPt, alpha = 0.25) {
      if (!prevPt) return { ...newPt };
      return {
        x: prevPt.x + alpha * (newPt.x - prevPt.x),
        y: prevPt.y + alpha * (newPt.y - prevPt.y)
      };
    },

    paint(ctx, a, b, opts, isReplay = false) {
      ctx.save();
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';

      const { tool, color, size, opacity } = opts;
      const alpha = (opacity / 100) * (tool === 'marker' ? 0.45 : 1.0);
      ctx.globalAlpha = alpha;

      if (tool === 'eraser') {
        // BUG-5: eraser stroke uses destination-out
        ctx.globalCompositeOperation = 'destination-out';
        ctx.strokeStyle = '#ffffff';
      } else {
        ctx.globalCompositeOperation = 'source-over';
        ctx.strokeStyle = color;
      }

      const strokeW = tool === 'pencil' ? Math.max(1, size / 3) : size;
      ctx.lineWidth = strokeW;

      if (tool === 'spray') {
        ctx.fillStyle = color;
        const count = 14;
        for (let i = 0; i < count; i++) {
          const ang = Math.random() * Math.PI * 2;
          const rr = Math.random() * size;
          ctx.fillRect(b.x + Math.cos(ang) * rr, b.y + Math.sin(ang) * rr, 1.8, 1.8);
        }
      } else {
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.stroke();
      }
      ctx.restore();

      // BUG-4 fix: only push to ops array if not currently replaying
      if (!isReplay && !state.replaying) {
        state.ops.push({
          t: 'paint',
          a: [a.x, a.y],
          b: [b.x, b.y],
          c: tool === 'eraser' ? 'erase' : color,
          w: strokeW,
          alpha,
          tool
        });
      }
    },

    stamp(ctx, pt, emojiChar, isReplay = false) {
      ctx.save();
      ctx.font = '48px serif';
      ctx.textBaseline = 'middle';
      ctx.textAlign = 'center';
      ctx.fillText(emojiChar, pt.x, pt.y);
      ctx.restore();

      if (!isReplay && !state.replaying) {
        state.ops.push({ t: 'stamp', e: emojiChar, x: pt.x, y: pt.y });
      }
    },

    floodFill(ctx, width, height, sx, sy, hex, isReplay = false) {
      const img = ctx.getImageData(0, 0, width, height);
      const d = img.data;
      const idx = (x, y) => (y * width + x) * 4;
      const tc = ToolsEngine.hexToRgb(hex);
      const si = idx(sx, sy);
      const sr = d[si], sg = d[si + 1], sb = d[si + 2];

      // If already target color, noop
      if (sr === tc.r && sg === tc.g && sb === tc.b) return;

      const tol = 42;
      const stack = [[sx, sy]];
      const seen = new Uint8Array(width * height);

      while (stack.length > 0) {
        const [x, y] = stack.pop();
        if (x < 0 || y < 0 || x >= width || y >= height) continue;
        const i = y * width + x;
        if (seen[i]) continue;
        seen[i] = 1;

        const o = i * 4;
        if (Math.abs(d[o] - sr) > tol || Math.abs(d[o + 1] - sg) > tol || Math.abs(d[o + 2] - sb) > tol) {
          continue;
        }

        d[o] = tc.r;
        d[o + 1] = tc.g;
        d[o + 2] = tc.b;
        d[o + 3] = 255;

        stack.push([x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]);
      }

      ctx.putImageData(img, 0, 0);

      if (!isReplay && !state.replaying) {
        state.ops.push({ t: 'fill', x: sx, y: sy, c: hex });
      }
    },

    saveUndoSnapshot(ctx, width, height) {
      state.undoStack.push(ctx.getImageData(0, 0, width, height));
      if (state.undoStack.length > 16) {
        state.undoStack.shift();
      }
    },

    undo(ctx) {
      if (state.undoStack.length > 0) {
        const snap = state.undoStack.pop();
        ctx.putImageData(snap, 0, 0);
        return true;
      }
      return false;
    }
  };

  /* ==========================================================================
     MODULE 3: PRECISION ENGINE (Part 5 & BUG-5 Fix)
     Score = coverage * (0.45 + 0.55 * accuracy)
     coverage = colored / estimated colorable (cap 1.0)
     accuracy = colored pixels inside line mask / all colored pixels
     BUG-5 fix: skip pixels with alpha < 128 (destination-out pixels)
     ========================================================================== */
  const PrecisionEngine = {
    computePrecision(ctx, baseLine, lineMask, width, height) {
      if (!baseLine) {
        return { score: 0, coverage: 0, accuracy: 0, passed: false, empty: true };
      }

      const curData = ctx.getImageData(0, 0, width, height).data;
      const baseData = baseLine.data;

      let colorable = 0;
      let colored = 0;
      let insideColored = 0;
      let outside = 0;

      // Sample every 4th pixel (stride = 16 bytes)
      for (let i = 0; i < baseData.length; i += 16) {
        const alpha = curData[i + 3];
        // BUG-5 fix: Skip erased/transparent pixels entirely
        if (alpha < 128) {
          continue;
        }

        const pxIndex = i / 4;
        const isLine = lineMask ? lineMask[pxIndex] : 0;

        const diff = Math.abs(curData[i] - baseData[i]) +
                     Math.abs(curData[i + 1] - baseData[i + 1]) +
                     Math.abs(curData[i + 2] - baseData[i + 2]);

        if (diff > 36) {
          colored++;
          if (isLine) {
            outside++;
          } else {
            insideColored++;
          }
        }
        if (!isLine) {
          colorable++;
        }
      }

      // Empty canvas or less than 40 colored pixels
      if (colored < 40) {
        return { score: 0, coverage: 0, accuracy: 0, passed: false, empty: true };
      }

      const accuracy = insideColored / Math.max(1, insideColored + outside);
      const coverage = Math.min(1.0, colored / Math.max(1, colorable * 0.55));
      const score = Math.round(100 * coverage * (0.45 + 0.55 * accuracy));

      return {
        score,
        coverage: Math.round(coverage * 100),
        accuracy: Math.round(accuracy * 100),
        passed: score >= 85,
        empty: false
      };
    },

    // Marketplace Listing Payload Generator (Part 5)
    generateMarketplacePayload(meta = {}) {
      return {
        schema: 'colorworld-masters-listing-v1',
        title: meta.title || 'Untitled Masterpiece — COLORWORKS Journey',
        description: meta.description || 'Masterpiece created and precision-scored with COLORWORLD MASTERS STUDIO.',
        precisionScore: meta.score || state.precisionScore,
        theme: meta.theme || (state.lastGrammar ? state.lastGrammar.theme : 'gothic'),
        tags: meta.tags || ['coloring-book', 'fine-art', 'animated-wallpaper', 'digital-art', 'pro-journey', 'masters'],
        suggestedPriceUSD: meta.price || 499, // Gumroad in cents ($4.99)
        license: meta.license || 'CC BY-NC-SA 4.0',
        exportFiles: meta.exportFiles || [],
        createdAt: new Date().toISOString()
      };
    }
  };

  /* ==========================================================================
     MODULE 4: JOURNEY ENGINE (10 Pieces Library & BUG-2, BUG-3 Fixes)
     ========================================================================== */
  const JourneyEngine = {
    PIECES: {
      blooming_skull: { name: 'Blooming Skull', tag: 'Floral Gothic' },
      ribcage_garden: { name: 'Ribcage Garden', tag: 'Bioluminescent Organic' },
      digital_realm: { name: 'Digital Realm', tag: 'Cyber Spire' },
      shadow_wraith: { name: 'Shadow Wraith', tag: 'Dark Fantasy' },
      gothic_dragon: { name: 'Gothic Dragon', tag: 'Mythic Beast' },
      spirit_stag: { name: 'Spirit Stag', tag: 'Ethereal Forest' },
      vr_goddess: { name: 'VR Goddess', tag: 'Sci-Fi Portrait' },
      haunted_forest: { name: 'Haunted Forest', tag: 'Atmospheric Arch' },
      phoenix_skull: { name: 'Phoenix Skull', tag: 'Fiery Rebirth' },
      cyber_serpent: { name: 'Cyber Serpent', tag: 'Futuristic Spiral' }
    },

    lerp(a, b, t) {
      return a + (b - a) * t;
    },

    drawPoly(ctx, pts, p) {
      if (p <= 0 || !pts || !pts.length) return;
      const totalSegs = pts.length - 1;
      const curLen = totalSegs * p;
      const count = Math.floor(curLen);
      const frac = curLen - count;

      ctx.beginPath();
      ctx.moveTo(pts[0][0], pts[0][1]);
      for (let i = 1; i <= count && i < pts.length; i++) {
        ctx.lineTo(pts[i][0], pts[i][1]);
      }
      if (count < pts.length - 1 && frac > 0) {
        const p1 = pts[count];
        const p2 = pts[count + 1];
        ctx.lineTo(JourneyEngine.lerp(p1[0], p2[0], frac), JourneyEngine.lerp(p1[1], p2[1], frac));
      }
      ctx.stroke();
    },

    drawSeg(ctx, x1, y1, x2, y2, p) {
      if (p <= 0) return;
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.lineTo(JourneyEngine.lerp(x1, x2, p), JourneyEngine.lerp(y1, y2, p));
      ctx.stroke();
    },

    drawRect(ctx, x, y, w, h, p) {
      JourneyEngine.drawPoly(ctx, [[x, y], [x + w, y], [x + w, y + h], [x, y + h], [x, y]], p);
    },

    drawCurve(ctx, pts, p) {
      const samples = [];
      for (let i = 0; i < pts.length - 1; i++) {
        for (let t = 0; t < 1; t += 0.05) {
          samples.push([
            JourneyEngine.lerp(pts[i][0], pts[i + 1][0], t),
            JourneyEngine.lerp(pts[i][1], pts[i + 1][1], t)
          ]);
        }
      }
      samples.push(pts[pts.length - 1]);
      JourneyEngine.drawPoly(ctx, samples, p);
    },

    drawRaven(ctx, x, y, s, p) {
      JourneyEngine.drawPoly(ctx, [
        [x - s, y],
        [x + s * 0.4, y - s * 0.5],
        [x + s, y - s * 0.2],
        [x + s * 0.3, y + s * 0.2],
        [x - s, y]
      ], p);
      JourneyEngine.drawSeg(ctx, x - s * 0.6, y + s * 0.1, x - s * 0.9, y + s * 0.5, p);
    },

    drawFlame(ctx, x, y, p, dx = 0) {
      const pts = [];
      for (let i = 0; i <= 8; i++) {
        const tt = i / 8;
        pts.push([x + dx * tt * 10 + 18 * (1 - tt) * Math.sin(tt * 10), y - tt * 90]);
      }
      JourneyEngine.drawPoly(ctx, pts, p);
    },

    buildPiece(name, palette) {
      const strokes = [];
      let animFn = () => {};
      const pal = palette || JOURNEY_PALETTES[0];
      const mainCol = pal.main;
      const shadowCol = pal.accent;

      const add = (fn, t, w = 3, col = mainCol) => {
        strokes.push({ fn, t, w, col, done: 0 });
      };

      if (name === 'blooming_skull') {
        // BUG-2 fix: The phantom noop loop `for(let a=0;a<=360;a+=6){ add(..., 0) }` has been completely removed!
        const contour = [];
        for (let a = -90; a <= 270; a += 5) {
          contour.push([410 + 170 * Math.cos(a * Math.PI / 180), 380 + 200 * Math.sin(a * Math.PI / 180)]);
        }
        add(ctx => JourneyEngine.drawPoly(ctx, contour, 1.0), 0.02, 5.5);

        const jaw = [];
        for (let i = 0; i <= 12; i++) jaw.push([310 + i * 16, 560 + Math.abs(i - 6) * 7]);
        add(ctx => JourneyEngine.drawPoly(ctx, jaw, 1.0), 0.09, 5);

        [[320, 360], [500, 360]].forEach(([cx, cy], si) => {
          const soc = [];
          for (let a = 0; a <= 360; a += 8) soc.push([cx + 54 * Math.cos(a * Math.PI / 180), cy + 64 * Math.sin(a * Math.PI / 180)]);
          add(ctx => JourneyEngine.drawPoly(ctx, soc, 1.0), 0.14 + si * 0.04, 4);
          for (let i = 0; i < 8; i++) {
            add(ctx => JourneyEngine.drawSeg(ctx, cx - 38, cy - 30 + i * 9, cx + 38, cy - 24 + i * 9, 1.0), 0.18 + si * 0.04 + i * 0.012, 2.2, shadowCol);
          }
        });

        const nose = [[410, 390], [390, 470], [430, 470]];
        add(ctx => JourneyEngine.drawPoly(ctx, nose.concat([nose[0]]), 1.0), 0.24, 4);

        for (let i = 0; i < 9; i++) {
          add(ctx => JourneyEngine.drawSeg(ctx, 322 + i * 20, 560, 322 + i * 20, 608, 1.0), 0.28 + i * 0.01, 2.5);
        }

        const spots = [[250, 240], [410, 165], [570, 240], [160, 330], [660, 330]];
        spots.forEach(([cx, cy], i) => {
          for (let pt = 0; pt < 4; pt++) {
            const pet = [];
            for (let a = 0; a <= 360; a += 10) {
              pet.push([cx + (28 + pt * 13) * Math.cos(a * Math.PI / 180), cy + (22 + pt * 11) * Math.sin(a * Math.PI / 180)]);
            }
            add(ctx => JourneyEngine.drawPoly(ctx, pet, 1.0), 0.35 + i * 0.05 + pt * 0.02, 2.8);
          }
        });

        spots.forEach(([cx, cy], i) => {
          add(ctx => JourneyEngine.drawSeg(ctx, cx, cy + 34, cx + (i - 2) * 22, cy + 130, 1.0), 0.55 + i * 0.03, 3);
        });

        for (let i = 0; i < 10; i++) {
          add(ctx => JourneyEngine.drawSeg(ctx, 300 + i * 12, 430 + i * 4, 360 + i * 12, 500 + i * 4, 1.0), 0.72 + i * 0.015, 1.6, shadowCol);
        }

        animFn = (ctx, t) => {
          ctx.save();
          ctx.strokeStyle = 'rgba(160, 60, 180, 0.4)';
          ctx.lineWidth = 2;
          spots.forEach(([cx, cy], i) => {
            ctx.beginPath();
            ctx.ellipse(cx, cy, 75 + 10 * Math.sin(t * 2 + i), 65 + 10 * Math.cos(t * 2 + i), 0, 0, Math.PI * 2);
            ctx.stroke();
          });
          ctx.restore();
        };

      } else if (name === 'ribcage_garden') {
        for (let i = 0; i < 9; i++) {
          const arc = [];
          for (let a = 0; a <= 180; a += 8) {
            arc.push([410 - (240 - i * 16) * Math.cos(a * Math.PI / 180), 260 + i * 45 + (75 - i * 6) * Math.sin(a * Math.PI / 180)]);
          }
          add(ctx => JourneyEngine.drawPoly(ctx, arc, 1.0), 0.03 + i * 0.05, 5);
        }
        const spine = [];
        for (let i = 0; i <= 14; i++) spine.push([410, 150 + i * 42]);
        add(ctx => JourneyEngine.drawPoly(ctx, spine, 1.0), 0.02, 6);

        const blooms = [[280, 300], [540, 300], [260, 420], [560, 420], [290, 540], [530, 540]];
        blooms.forEach(([cx, cy], i) => {
          for (let pt = 0; pt < 3; pt++) {
            const pet = [];
            for (let a = 0; a <= 360; a += 12) {
              pet.push([cx + (16 + pt * 11) * Math.cos(a * Math.PI / 180), cy + (16 + pt * 11) * Math.sin(a * Math.PI / 180)]);
            }
            add(ctx => JourneyEngine.drawPoly(ctx, pet, 1.0), 0.45 + i * 0.04 + pt * 0.015, 2.4);
          }
        });

        for (let i = 0; i < 6; i++) {
          add(ctx => JourneyEngine.drawSeg(ctx, 410, 740, 410 + (i - 2.5) * 55, 800, 1.0), 0.78 + i * 0.02, 3);
        }

        animFn = (ctx, t) => {
          ctx.save();
          ctx.strokeStyle = 'rgba(120, 220, 180, 0.4)';
          blooms.forEach(([cx, cy], i) => {
            ctx.beginPath();
            ctx.ellipse(cx, cy, 45 + 8 * Math.sin(t * 3 + i * 1.3), 45 + 8 * Math.sin(t * 3 + i * 1.3), 0, 0, Math.PI * 2);
            ctx.stroke();
          });
          ctx.restore();
        };

      } else if (name === 'digital_realm') {
        for (let i = 0; i < 12; i++) {
          add(ctx => JourneyEngine.drawSeg(ctx, 60, 700 + i * 10, 760, 700 + i * 10, 1.0), 0.02 + i * 0.008, 1.6, shadowCol);
        }
        const towers = [[70, 390, 65], [150, 280, 75], [240, 440, 60], [330, 200, 80], [420, 130, 88], [520, 300, 72], [600, 390, 65], [670, 260, 78]];
        towers.forEach(([x, top, w], i) => {
          add(ctx => JourneyEngine.drawRect(ctx, x, top, w, 700 - top, 1.0), 0.08 + i * 0.04, 4.4);
          for (let wy = top + 20; wy < 690; wy += 24) {
            add(ctx => JourneyEngine.drawSeg(ctx, x + 8, wy, x + w - 8, wy, 1.0), 0.12 + i * 0.04 + (wy - top) * 0.0004, 1.4, shadowCol);
          }
        });

        add(ctx => JourneyEngine.drawSeg(ctx, 410, 40, 410, 700, 1.0), 0.5, 6);
        add(ctx => JourneyEngine.drawSeg(ctx, 370, 700, 410, 40, 1.0), 0.54, 3);
        add(ctx => JourneyEngine.drawSeg(ctx, 450, 700, 410, 40, 1.0), 0.58, 3);

        for (let i = 0; i < 8; i++) {
          add(ctx => JourneyEngine.drawSeg(ctx, 410, 460, 120 + i * 80, 130 + ((i * 53) % 60), 1.0), 0.62 + i * 0.025, 2);
        }

        animFn = (ctx, t) => {
          ctx.save();
          ctx.lineWidth = 2;
          for (let i = 0; i < 8; i++) {
            ctx.strokeStyle = `rgba(90, 140, 255, ${0.4 + 0.3 * Math.abs(Math.sin(t * 2.2 + i))})`;
            ctx.beginPath();
            ctx.moveTo(410, 460);
            ctx.lineTo(120 + i * 80, 130 + ((i * 53) % 60) + 10 * Math.sin(t * 2 + i));
            ctx.stroke();
          }
          ctx.restore();
        };

      } else if (name === 'shadow_wraith') {
        const robe = [];
        for (let a = -60; a <= 60; a += 6) robe.push([410 + 180 * Math.sin(a * Math.PI / 180), 390 + 300 * Math.cos(a * Math.PI / 180)]);
        add(ctx => JourneyEngine.drawPoly(ctx, robe, 1.0), 0.03, 5);

        const hood = [];
        for (let a = 0; a <= 360; a += 8) hood.push([410 + 85 * Math.cos(a * Math.PI / 180), 240 + 100 * Math.sin(a * Math.PI / 180)]);
        add(ctx => JourneyEngine.drawPoly(ctx, hood, 1.0), 0.10, 5);

        for (let i = 0; i < 9; i++) add(ctx => JourneyEngine.drawSeg(ctx, 370, 210 + i * 8, 450, 210 + i * 8, 1.0), 0.15 + i * 0.012, 3);
        for (let i = 0; i < 9; i++) add(ctx => JourneyEngine.drawSeg(ctx, 330 + i * 20, 380, 300 + i * 25, 700 - ((i * 37) % 70), 1.0), 0.28 + i * 0.02, 2, shadowCol);

        const moon = [];
        for (let a = 0; a <= 360; a += 8) moon.push([640 + 65 * Math.cos(a * Math.PI / 180), 150 + 65 * Math.sin(a * Math.PI / 180)]);
        add(ctx => JourneyEngine.drawPoly(ctx, moon, 1.0), 0.45, 4);

        for (let i = 0; i < 5; i++) {
          const rx = 120 + (i * 150) % 580, ry = 150 + (i * 90) % 380;
          add(ctx => JourneyEngine.drawRaven(ctx, rx, ry, 30 + (i % 2) * 10, 1.0), 0.55 + i * 0.05, 3);
        }

        animFn = (ctx, t) => {
          ctx.save();
          ctx.strokeStyle = `rgba(200, 190, 255, ${0.4 + 0.2 * Math.sin(t * 2.5)})`;
          ctx.beginPath();
          ctx.arc(640, 150, 80 + 8 * Math.sin(t * 2.5), 0, Math.PI * 2);
          ctx.stroke();
          ctx.restore();
        };

      } else if (name === 'gothic_dragon') {
        const tw = [[350, 310], [470, 310], [490, 750], [330, 750]];
        add(ctx => JourneyEngine.drawPoly(ctx, tw.concat([tw[0]]), 1.0), 0.03, 5);
        add(ctx => JourneyEngine.drawRect(ctx, 340, 290, 140, 20, 1.0), 0.07, 4.4);

        [[390, 390], [390, 490], [390, 590]].forEach(([x, y], i) => {
          add(ctx => JourneyEngine.drawRect(ctx, x, y, 36, 64, 1.0), 0.10 + i * 0.03, 3.4, shadowCol);
        });

        for (let c = 0; c < 3; c++) {
          const coil = [];
          for (let a = 0; a <= 660; a += 8) {
            const rr = 150 + c * 42;
            coil.push([410 + rr * Math.cos(a * Math.PI / 180), 510 + rr * 0.42 * Math.sin(a * Math.PI / 180)]);
          }
          add(ctx => JourneyEngine.drawPoly(ctx, coil, 1.0), 0.16 + c * 0.12, 4.4);
        }

        add(ctx => JourneyEngine.drawCurve(ctx, [[410, 510], [390, 350], [430, 230], [480, 170]], 1.0), 0.52, 6);
        add(ctx => JourneyEngine.drawPoly(ctx, [[480, 170], [560, 150], [580, 185], [495, 200], [480, 170]], 1.0), 0.58, 4.4);

        [[-1], [1]].forEach(([s]) => {
          add(ctx => JourneyEngine.drawCurve(ctx, [[420, 270], [420 + s * 200, 120], [420 + s * 270, 270], [420 + s * 180, 330]], 1.0), 0.64, 4.4);
          for (let i = 1; i < 4; i++) {
            add(ctx => JourneyEngine.drawSeg(ctx, 420 + s * 35, 290, 420 + s * (110 + i * 50), 160 + i * 65, 1.0), 0.70 + i * 0.015, 2.4, shadowCol);
          }
        });

        for (let i = 0; i < 8; i++) {
          add(ctx => JourneyEngine.drawSeg(ctx, 410 + i * 8, 480 - i * 14, 425 + i * 8, 465 - i * 14, 1.0), 0.76 + i * 0.012, 2.4, shadowCol);
        }

        animFn = (ctx, t) => {
          ctx.save();
          ctx.strokeStyle = `rgba(255, 170, 60, ${0.4 + 0.3 * Math.sin(t * 3.2)})`;
          ctx.lineWidth = 3;
          [[390, 422], [390, 522], [390, 622]].forEach(([x, y], i) => {
            ctx.beginPath();
            ctx.arc(x + 18, y + 32, 25 + 6 * Math.sin(t * 3.2 + i), 0, Math.PI * 2);
            ctx.stroke();
          });
          ctx.restore();
        };

      } else if (name === 'spirit_stag') {
        const skull = [];
        for (let a = 0; a <= 360; a += 8) skull.push([410 + 55 * Math.cos(a * Math.PI / 180), 510 + 75 * Math.sin(a * Math.PI / 180)]);
        add(ctx => JourneyEngine.drawPoly(ctx, skull, 1.0), 0.03, 5);
        add(ctx => JourneyEngine.drawSeg(ctx, 390, 580, 390, 640, 1.0), 0.08, 4);
        add(ctx => JourneyEngine.drawSeg(ctx, 430, 580, 430, 640, 1.0), 0.08, 4);

        [[-1, 270], [1, 550]].forEach(([s, bx]) => {
          add(ctx => JourneyEngine.drawCurve(ctx, [[390 + s * 35, 460], [350 + s * 70, 350], [bx, 250], [bx + s * 18, 140]], 1.0), 0.12, 5);
          for (let b = 0; b < 5; b++) {
            const yy = 400 - b * 52;
            add(ctx => JourneyEngine.drawCurve(ctx, [
              [JourneyEngine.lerp(bx, 390 + s * 35, b * 0.2) + s * 9, yy],
              [bx + s * (55 + b * 13), yy - 35],
              [bx + s * (85 + b * 18), yy - 85]
            ], 1.0), 0.2 + b * 0.03, 3, shadowCol);
          }
        });

        for (let i = 0; i < 7; i++) {
          const cx = 220 + i * 60, cy = 160 + (i % 3) * 55;
          const pet = [];
          for (let a = 0; a <= 360; a += 12) pet.push([cx + 16 * Math.cos(a * Math.PI / 180), cy + 16 * Math.sin(a * Math.PI / 180)]);
          add(ctx => JourneyEngine.drawPoly(ctx, pet, 1.0), 0.45 + i * 0.035, 2.4);
        }

        add(ctx => JourneyEngine.drawCurve(ctx, [[360, 580], [300, 640], [300, 730], [380, 750], [490, 730], [510, 640], [460, 580]], 1.0), 0.68, 4.4);

        animFn = (ctx, t) => {
          ctx.save();
          ctx.strokeStyle = `rgba(140, 220, 160, ${0.4 + 0.2 * Math.sin(t * 2.4)})`;
          for (let i = 0; i < 7; i++) {
            ctx.beginPath();
            ctx.arc(220 + i * 60, 160 + (i % 3) * 55, 20 + 5 * Math.sin(t * 2.4 + i), 0, Math.PI * 2);
            ctx.stroke();
          }
          ctx.restore();
        };

      } else if (name === 'vr_goddess') {
        const head = [];
        for (let a = -140; a <= 140; a += 8) head.push([410 + 70 * Math.cos(a * Math.PI / 180), 300 + 82 * Math.sin(a * Math.PI / 180)]);
        add(ctx => JourneyEngine.drawPoly(ctx, head, 1.0), 0.03, 4.4);
        add(ctx => JourneyEngine.drawRect(ctx, 330, 260, 160, 58, 1.0), 0.08, 4.4);
        add(ctx => JourneyEngine.drawCurve(ctx, [[350, 380], [330, 500], [350, 690]], 1.0), 0.12, 5);
        add(ctx => JourneyEngine.drawCurve(ctx, [[470, 380], [490, 500], [475, 690]], 1.0), 0.14, 5);

        for (let s = 0; s < 7; s++) {
          const rb = [];
          for (let a = 0; a <= 340; a += 12) {
            rb.push([410 + s * 14 * Math.cos(a * Math.PI / 180) * 1.4, 300 + 110 * a / 340 + s * 27 * Math.sin(a * Math.PI / 180)]);
          }
          add(ctx => JourneyEngine.drawPoly(ctx, rb, 1.0), 0.18 + s * 0.045, 2.6, shadowCol);
        }

        for (let i = 0; i < 8; i++) {
          add(ctx => JourneyEngine.drawSeg(ctx, 355 + i * 15, 430, 370 + i * 15, 660, 1.0), 0.42 + i * 0.02, 2, shadowCol);
        }
        for (let i = 0; i < 5; i++) {
          add(ctx => JourneyEngine.drawSeg(ctx, 340, 460 + i * 45, 480, 460 + i * 45, 1.0), 0.5 + i * 0.02, 2, shadowCol);
        }

        for (let i = 0; i < 3; i++) {
          const ring = [];
          for (let a = 0; a <= 360; a += 8) {
            ring.push([410 + (135 + i * 62) * Math.cos(a * Math.PI / 180), 450 + (46 + i * 23) * Math.sin(a * Math.PI / 180)]);
          }
          add(ctx => JourneyEngine.drawPoly(ctx, ring, 1.0), 0.6 + i * 0.08, 3);
        }

        animFn = (ctx, t) => {
          ctx.save();
          ctx.strokeStyle = `rgba(120, 220, 255, ${0.4 + 0.3 * Math.sin(t * 2.8)})`;
          for (let i = 0; i < 3; i++) {
            ctx.beginPath();
            ctx.ellipse(410, 450, 135 + i * 62 + 7 * Math.sin(t * 2.8 + i), 46 + i * 23 + 5 * Math.cos(t * 2.8 + i), 0, 0, Math.PI * 2);
            ctx.stroke();
          }
          ctx.restore();
        };

      } else if (name === 'haunted_forest') {
        const arch = [];
        for (let a = 180; a <= 360; a += 6) arch.push([410 + 270 * Math.cos(a * Math.PI / 180), 580 + 250 * Math.sin(a * Math.PI / 180)]);
        add(ctx => JourneyEngine.drawPoly(ctx, arch, 1.0), 0.03, 6);

        for (let i = 0; i < 9; i++) {
          const a = (195 + i * 15) * (Math.PI / 180);
          add(ctx => JourneyEngine.drawSeg(ctx, 410 + 270 * Math.cos(a), 580 + 250 * Math.sin(a), 410 + 310 * Math.cos(a + 0.2), 580 + 270 * Math.sin(a + 0.2) - 35, 1.0), 0.1 + i * 0.02, 2.4, shadowCol);
        }

        add(ctx => JourneyEngine.drawPoly(ctx, [[350, 800], [470, 800], [440, 630], [380, 630], [350, 800]], 1.0), 0.26, 4);

        [[110], [710]].forEach(([tx], ti) => {
          add(ctx => JourneyEngine.drawSeg(ctx, tx, 790, tx, 230, 1.0), 0.32 + ti * 0.05, 6);
          add(ctx => JourneyEngine.drawSeg(ctx, tx, 360, tx - 60, 270, 1.0), 0.36 + ti * 0.05, 3.4);
          add(ctx => JourneyEngine.drawSeg(ctx, tx, 300, tx + 60, 210, 1.0), 0.40 + ti * 0.05, 3.4);
          for (let b = 0; b < 3; b++) {
            add(ctx => JourneyEngine.drawSeg(ctx, tx, 420 + b * 50, tx + (ti === 0 ? 40 : -40), 380 + b * 50, 1.0), 0.44 + ti * 0.05 + b * 0.02, 2.5, shadowCol);
          }
        });

        add(ctx => JourneyEngine.drawSeg(ctx, 410, 270, 410, 320, 1.0), 0.55, 3);
        add(ctx => JourneyEngine.drawRect(ctx, 385, 320, 50, 58, 1.0), 0.57, 4);

        animFn = (ctx, t) => {
          ctx.save();
          ctx.strokeStyle = `rgba(255, 220, 120, ${0.5 + 0.3 * Math.abs(Math.sin(t * 2.6))})`;
          ctx.lineWidth = 3;
          ctx.beginPath();
          ctx.arc(410, 350, 30 + 6 * Math.sin(t * 2.6), 0, Math.PI * 2);
          ctx.stroke();
          ctx.restore();
        };

      } else if (name === 'phoenix_skull') {
        [[250, 650], [570, 650]].forEach(([sx, sy], si) => {
          const sk = [];
          for (let a = 0; a <= 360; a += 8) sk.push([sx + 70 * Math.cos(a * Math.PI / 180), sy + 80 * Math.sin(a * Math.PI / 180)]);
          add(ctx => JourneyEngine.drawPoly(ctx, sk, 1.0), 0.03 + si * 0.08, 4.4);
          for (let i = 0; i < 3; i++) {
            add(ctx => JourneyEngine.drawSeg(ctx, sx - 25 + i * 25, sy - 10, sx - 25 + i * 25, sy + 20, 1.0), 0.06 + si * 0.08 + i * 0.015, 2.4, shadowCol);
          }
        });

        add(ctx => JourneyEngine.drawCurve(ctx, [[410, 630], [400, 470], [430, 360], [410, 270]], 1.0), 0.2, 5);
        const head = [];
        for (let a = 0; a <= 360; a += 8) head.push([410 + 47 * Math.cos(a * Math.PI / 180), 240 + 50 * Math.sin(a * Math.PI / 180)]);
        add(ctx => JourneyEngine.drawPoly(ctx, head, 1.0), 0.26, 4.4);

        for (let i = 0; i < 5; i++) {
          add(ctx => JourneyEngine.drawCurve(ctx, [[410, 200], [390 + i * 10, 150 - i * 10], [410 + i * 12, 100 - i * 14]], 1.0), 0.3 + i * 0.02, 3, shadowCol);
        }

        [[-1], [1]].forEach(([sIdx]) => {
          for (let f = 0; f < 6; f++) {
            const fx = 410 + sIdx * (65 + f * 34), fy = 340 - f * 8;
            add(ctx => JourneyEngine.drawCurve(ctx, [[410 + sIdx * 35, 360], [fx, fy - 80 - f * 12], [fx + sIdx * 35, fy - 25 - f * 9]], 1.0), 0.4 + f * 0.03 * sIdx + Math.abs(sIdx - 1) * 0.01, 3, shadowCol);
          }
        });

        for (let i = 0; i < 8; i++) {
          add(ctx => JourneyEngine.drawFlame(ctx, 410 + (i - 3.5) * 36, 680, 1.0), 0.66 + i * 0.02, 2.6);
        }

        animFn = (ctx, t) => {
          ctx.save();
          for (let i = 0; i < 8; i++) {
            ctx.strokeStyle = `rgba(255, 140, 50, ${0.4 + 0.3 * Math.sin(t * 4 + i)})`;
            ctx.lineWidth = 2.6;
            JourneyEngine.drawFlame(ctx, 410 + (i - 3.5) * 36, 680, 1.0, 6 * Math.sin(t * 4 + i));
          }
          ctx.restore();
        };

      } else if (name === 'cyber_serpent') {
        for (let c = 0; c < 9; c++) add(ctx => JourneyEngine.drawSeg(ctx, 80 + c * 80, 70, 80 + c * 80, 270, 1.0), 0.02 + c * 0.012, 2, shadowCol);
        for (let i = 0; i < 6; i++) add(ctx => JourneyEngine.drawSeg(ctx, 70, 200 + i * 13, 750, 200 + i * 13, 1.0), 0.04 + i * 0.012, 1.8, shadowCol);

        const body = [];
        for (let a = 0; a <= 760; a += 7) {
          const rr = 55 + a * 0.31;
          body.push([410 + rr * Math.cos(a * Math.PI / 180), 420 + rr * 0.72 * Math.sin(a * Math.PI / 180)]);
        }
        add(ctx => JourneyEngine.drawPoly(ctx, body, 1.0), 0.14, 6);

        for (let a = 30; a < 760; a += 26) {
          const rr = 55 + a * 0.31;
          add(ctx => JourneyEngine.drawSeg(ctx,
            410 + rr * Math.cos(a * Math.PI / 180),
            420 + rr * 0.72 * Math.sin(a * Math.PI / 180),
            410 + (rr + 15) * Math.cos(a * Math.PI / 180),
            420 + (rr + 15) * 0.72 * Math.sin(a * Math.PI / 180), 1.0), 0.28 + a * 0.0005, 1.8, shadowCol);
        }

        add(ctx => JourneyEngine.drawRect(ctx, 490, 160, 100, 76, 1.0), 0.5, 4.4);

        animFn = (ctx, t) => {
          ctx.save();
          ctx.strokeStyle = `rgba(120, 255, 220, ${0.4 + 0.3 * Math.abs(Math.sin(t * 3.4))})`;
          ctx.beginPath();
          ctx.ellipse(540, 198, 70 + 7 * Math.sin(t * 2.8), 40, 0, 0, Math.PI * 2);
          ctx.stroke();
          ctx.restore();
        };
      }

      strokes.sort((a, b) => a.t - b.t);
      return { strokes, animFn };
    },

    // Render single frame of ink-bleed reveal (Part 4)
    renderFrame(ctx, strokes, playT, dur, bleedScale, paper, animFn) {
      ctx.save();
      ctx.fillStyle = paper.hex || '#fafafc';
      ctx.fillRect(0, 0, state.width, state.height);

      const jt = Math.min(1.0, Math.max(0.0, playT / dur));
      const jtl = jt * dur;

      let strokeActive = 0;
      let strokeDone = 0;

      strokes.forEach(s => {
        const start = s.t * dur * 0.70;
        const duration = 0.8;
        const local = Math.min(1.0, Math.max(0.0, (jtl - start) / duration));

        if (local > 0) {
          strokeActive++;

          // 1. Wet-Ink Bleed Aura Pass
          ctx.save();
          ctx.lineCap = 'round';
          ctx.lineJoin = 'round';
          ctx.globalAlpha = 0.12 * (1.0 - local) * bleedScale;
          ctx.lineWidth = s.w * 2.8 * bleedScale;
          ctx.strokeStyle = s.col;
          s.fn(ctx, local);
          ctx.restore();

          // 2. Core Solid Ink Line with Dynamic Pressure Swell
          ctx.save();
          ctx.lineCap = 'round';
          ctx.lineJoin = 'round';
          ctx.globalAlpha = Math.min(1.0, local * 1.8);
          ctx.lineWidth = s.w * (0.8 + 0.45 * Math.sin(local * Math.PI));
          ctx.strokeStyle = s.col;
          s.fn(ctx, local);
          ctx.restore();

          if (local >= 1.0) {
            s.done = 1;
            strokeDone++;
          }
        }
      });

      // Dynamic element animation pass after partial composition reveal
      if (jt > 0.4 && animFn) {
        animFn(ctx, playT);
      }
      ctx.restore();

      return { strokeActive, strokeDone, jt };
    },

    // BUG-3 fix: Accurate stroke fidelity formula
    // Final fidelity = (strokes fully rendered at journey end / total strokes)
    computeFinalFidelity(strokes) {
      if (!strokes || strokes.length === 0) return 0;
      const fullyRendered = strokes.filter(s => s.done === 1).length;
      return Math.round((fullyRendered / strokes.length) * 100);
    }
  };

  /* ==========================================================================
     MODULE 5: KALEIDOSCOPE FINALE (Part 4)
     Mirrored facets (6/8/12), vignette eyepiece overlay, rotation & exports
     ========================================================================== */
  const KaleidoscopeEngine = {
    renderKaleidoscope(targetCtx, sourceCanvas, facets = 8, angle = 0, width = 820, height = 820) {
      targetCtx.save();
      targetCtx.fillStyle = '#08080e';
      targetCtx.fillRect(0, 0, width, height);

      const cx = width / 2;
      const cy = height / 2;
      const step = (Math.PI * 2) / facets;

      for (let i = 0; i < facets; i++) {
        targetCtx.save();
        targetCtx.translate(cx, cy);
        targetCtx.rotate(i * step + angle);
        if (i % 2 === 1) {
          targetCtx.scale(1, -1);
        }

        // Clip to pie slice
        targetCtx.beginPath();
        targetCtx.moveTo(0, 0);
        targetCtx.arc(0, 0, Math.max(width, height), -step / 2, step / 2);
        targetCtx.closePath();
        targetCtx.clip();

        // Draw mirrored quadrant of artwork
        targetCtx.drawImage(sourceCanvas, -cx, -cy, width, height);
        targetCtx.restore();
      }

      // Vignette Eyepiece overlay
      KaleidoscopeEngine.drawVignette(targetCtx, width, height);
      targetCtx.restore();
    },

    drawVignette(ctx, width, height) {
      ctx.save();
      const cx = width / 2;
      const cy = height / 2;
      const r = Math.min(cx, cy);
      const grad = ctx.createRadialGradient(cx, cy, r * 0.55, cx, cy, r);
      grad.addColorStop(0, 'rgba(0, 0, 0, 0)');
      grad.addColorStop(0.75, 'rgba(0, 0, 0, 0.65)');
      grad.addColorStop(1, 'rgba(0, 0, 0, 0.96)');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, width, height);
      ctx.restore();
    }
  };

  /* ==========================================================================
     MODULE 6: AUDIO ENGINE (WebAudio User Playlist & Focus Ambience)
     No licensed music bundled. Focus Ambience: 528 Hz + 3 Hz binaural beat.
     ========================================================================== */
  const AudioEngine = {
    ensureAudioGraph() {
      if (state.audioCtx) return state.audioCtx;
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtx) return null;

      state.audioCtx = new AudioCtx();
      state.audioDest = state.audioCtx.createMediaStreamDestination();

      if (!state.audioElement) {
        state.audioElement = new Audio();
        state.audioElement.crossOrigin = 'anonymous';
      }

      try {
        state.srcNode = state.audioCtx.createMediaElementSource(state.audioElement);
        state.srcNode.connect(state.audioCtx.destination);
        state.srcNode.connect(state.audioDest);
      } catch (e) {
        // Source already connected
      }
      return state.audioCtx;
    },

    toggleFocusAmbience() {
      const actx = AudioEngine.ensureAudioGraph();
      if (!actx) return false;

      if (state.focusAmbienceActive) {
        // Turn off
        try {
          if (state.focusOsc1) state.focusOsc1.stop();
          if (state.focusOsc2) state.focusOsc2.stop();
        } catch (e) {}
        state.focusAmbienceActive = false;
        return false;
      }

      // Turn on: 528 Hz base + 531 Hz (3.0 Hz theta difference)
      if (actx.state === 'suspended') actx.resume();

      const gain = actx.createGain();
      gain.gain.value = 0.08;

      const osc1 = actx.createOscillator();
      osc1.type = 'sine';
      osc1.frequency.value = 528.0;

      const osc2 = actx.createOscillator();
      osc2.type = 'sine';
      osc2.frequency.value = 531.0; // 3.0 Hz sub-bass theta difference

      osc1.connect(gain);
      osc2.connect(gain);
      gain.connect(actx.destination);
      if (state.audioDest) gain.connect(state.audioDest);

      osc1.start();
      osc2.start();

      state.focusOsc1 = osc1;
      state.focusOsc2 = osc2;
      state.focusAmbienceGain = gain;
      state.focusAmbienceActive = true;
      return true;
    }
  };

  /* ==========================================================================
     MODULE 7: EXPORT ENGINE (MediaRecorder & High-Res PNG)
     MIME negotiation: MP4 -> WebM. Wallpapers, time-lapse, composite.
     ========================================================================== */
  const ExportEngine = {
    pickMimeType() {
      if (typeof MediaRecorder === 'undefined') return null;
      const types = [
        'video/mp4;codecs=avc1.42E01E',
        'video/mp4',
        'video/webm;codecs=vp9',
        'video/webm'
      ];
      return types.find(t => MediaRecorder.isTypeSupported && MediaRecorder.isTypeSupported(t)) || null;
    },

    recordCanvasStream(canvas, seconds, withAudio, onComplete) {
      const mime = ExportEngine.pickMimeType();
      if (!mime) {
        throw new Error('MediaRecorder video recording is not supported in this browser.');
      }

      const stream = canvas.captureStream ? canvas.captureStream(60) : null;
      if (!stream) {
        throw new Error('Canvas.captureStream is not supported.');
      }

      // If user music is playing or Focus Ambience is on, bake in audio
      if (withAudio && state.audioDest) {
        const audioTracks = state.audioDest.stream.getAudioTracks();
        if (audioTracks.length > 0) {
          stream.addTrack(audioTracks[0]);
        }
      }

      const rec = new MediaRecorder(stream, {
        mimeType: mime,
        videoBitsPerSecond: 10_000_000 // 10 Mbps HD
      });

      const chunks = [];
      rec.ondataavailable = e => {
        if (e.data && e.data.size > 0) chunks.push(e.data);
      };

      rec.onstop = () => {
        const isMp4 = mime.includes('mp4');
        const ext = isMp4 ? 'mp4' : 'webm';
        const blob = new Blob(chunks, { type: mime });
        if (onComplete) onComplete(blob, ext, mime);
      };

      rec.start();
      setTimeout(() => {
        if (rec.state !== 'inactive') rec.stop();
      }, seconds * 1000);

      return rec;
    },

    // 2x High-Res PNG export for printing (Part 7)
    export2xPNG(sourceCanvas) {
      const off = document.createElement('canvas');
      off.width = sourceCanvas.width * 2;
      off.height = sourceCanvas.height * 2;
      const offCtx = off.getContext('2d');
      offCtx.imageSmoothingEnabled = true;
      offCtx.imageSmoothingQuality = 'high';
      offCtx.drawImage(sourceCanvas, 0, 0, off.width, off.height);
      return off.toDataURL('image/png');
    }
  };

  /* ==========================================================================
     MODULE 8: EDGE AI (Progressive Fallback Ladder & BUG-6 Fix)
     Tier 1: WebGPU WebLLM Gemma-2-2B-it ->
     Tier 2A: Ollama localhost:11434 / FLUX.1 localhost:7860 ->
     Tier 2B: Deterministic seed-pinned mulberry32 symmetric generator
     ========================================================================== */
  const EdgeEngine = (() => {
    let llmEngine = null;
    let engineStatus = 'idle';

    // Mulberry32 deterministic PRNG
    function mulberry32(seed) {
      let a = seed >>> 0;
      return function () {
        a |= 0;
        a = (a + 0x6D2B79F5) | 0;
        let t = Math.imul(a ^ (a >>> 15), 1 | a);
        t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
        return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
      };
    }

    function hashStringToSeed(str) {
      let s = 0;
      for (let i = 0; i < str.length; i++) {
        s = ((s << 5) - s + str.charCodeAt(i)) | 0;
      }
      return Math.abs(s);
    }

    function fallbackGrammar(prompt) {
      const p = (prompt || 'mandala').toLowerCase();
      const theme = /skull|ghost|dragon|haunt|wraith/.test(p) ? 'gothic'
        : /flower|garden|rose|forest|petal/.test(p) ? 'botanical'
        : /cyber|neon|circuit|robot|spire/.test(p) ? 'cyber'
        : /star|cosmos|space|moon|orbit/.test(p) ? 'cosmic'
        : 'hygge';
      const motifs = prompt.trim().split(/\s+/).slice(0, 5);
      return {
        motifs: motifs.length ? motifs : ['bloom', 'petal', 'spiral'],
        symmetry: 8,
        density: 0.7,
        theme
      };
    }

    async function probeOllama() {
      try {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 1500);
        const r = await fetch('http://localhost:11434/api/tags', { signal: controller.signal });
        clearTimeout(timeout);
        return r.ok;
      } catch (e) {
        return false;
      }
    }

    async function probeFlux() {
      try {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 1500);
        const r = await fetch('http://localhost:7860/sdapi/v1/txt2img', {
          method: 'HEAD',
          signal: controller.signal
        });
        clearTimeout(timeout);
        return r.ok;
      } catch (e) {
        return false;
      }
    }

    function renderProceduralGrammar(grammar, canvas) {
      const ctx = canvas.getContext('2d');
      const seedStr = (grammar.motifs || []).join('') + (grammar.theme || 'gothic');
      const seed = hashStringToSeed(seedStr);
      const rnd = mulberry32(seed);

      const n = Math.max(4, Math.min(16, grammar.symmetry || 8));
      const dense = Math.max(0.2, Math.min(1.0, grammar.density || 0.6));

      ctx.fillStyle = '#ffffff';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.strokeStyle = '#141414';
      ctx.lineWidth = 3;

      const C = canvas.width / 2;
      const themes = {
        gothic: ['arch', 'skull', 'vine'],
        botanical: ['petal', 'leaf', 'stem'],
        cosmic: ['ring', 'star', 'orbit'],
        cyber: ['grid', 'chip', 'trace'],
        hygge: ['cup', 'knit', 'flake']
      };

      const motifs = themes[grammar.theme] || themes.botanical;
      motifs.forEach((motif, m) => {
        for (let i = 0; i < n; i++) {
          ctx.save();
          ctx.translate(C, C);
          ctx.rotate(((Math.PI * 2) / n) * i);
          const r0 = 60 + m * 90 + rnd() * 30;
          ctx.beginPath();
          if (motif === 'petal' || motif === 'leaf' || motif === 'flake') {
            ctx.ellipse(r0 * 0.6, 0, r0 * 0.45 * dense + 10, 16 + m * 6, 0, 0, Math.PI * 2);
          } else if (motif === 'ring' || motif === 'grid' || motif === 'orbit') {
            ctx.arc(0, 0, r0 * (0.4 + dense * 0.4), 0, Math.PI * 1.8);
          } else {
            ctx.moveTo(r0 * 0.3, 0);
            ctx.lineTo(r0 * 0.8, -18);
            ctx.lineTo(r0 * 1.1, 0);
          }
          ctx.stroke();
          ctx.restore();
        }
      });
      return { seed, motifs: grammar.motifs };
    }

    return {
      mulberry32,
      hashStringToSeed,
      fallbackGrammar,
      renderProceduralGrammar,
      getStatus: () => engineStatus,

      // Progressive Generation Pipeline with BUG-6 Guard
      async generateLineArt(prompt, canvas, onStatus) {
        state.lastPrompt = prompt;

        // BUG-6 fix: Short-circuit when offline or race with 1s timeout
        if (typeof navigator !== 'undefined' && navigator.onLine !== false) {
          try {
            const controller = new AbortController();
            const timeout = setTimeout(() => controller.abort(), 1000);
            const r = await fetch('/api/generate-lineart', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ prompt }),
              signal: controller.signal
            });
            clearTimeout(timeout);
            if (r.ok) {
              const j = await r.json();
              if (j && j.image) {
                await new Promise((res, rej) => {
                  const img = new Image();
                  img.onload = () => {
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                    res();
                  };
                  img.onerror = rej;
                  img.src = j.image;
                });
                state.aiTier = 'Remote Lineart Hook';
                if (onStatus) onStatus('Remote line art loaded successfully');
                return { tier: 'remote', grammar: fallbackGrammar(prompt) };
              }
            }
          } catch (e) {
            // Silently fall through to local Edge tiers
          }
        }

        // Tier 1: In-browser WebGPU LLM (Gemma-2-2b-it via @mlc-ai/web-llm)
        if (typeof navigator !== 'undefined' && navigator.gpu) {
          try {
            if (!llmEngine) {
              if (onStatus) onStatus('Initializing WebGPU Edge LLM…');
              const webllm = await import('https://esm.run/@mlc-ai/web-llm');
              llmEngine = await webllm.CreateMLCEngine('gemma-2-2b-it-q4f16_1', {
                initProgressCallback: r => onStatus && onStatus(`Model loading ${Math.round(r.progress * 100)}%`)
              });
            }
            if (llmEngine) {
              const sysPrompt = 'You output ONLY JSON: {"motifs":[string],"symmetry":number,"density":number,"theme":"gothic"|"botanical"|"cosmic"|"cyber"|"hygge"}';
              const res = await llmEngine.chat.completions.create({
                messages: [{ role: 'system', content: sysPrompt }, { role: 'user', content: prompt }],
                temperature: 0.3,
                max_tokens: 120
              });
              const raw = res.choices[0].message.content;
              const match = raw.match(/\{[\s\S]*\}/);
              if (match) {
                const grammar = JSON.parse(match[0]);
                state.aiTier = 'Tier 1 (In-Browser WebGPU LLM)';
                state.lastGrammar = grammar;
                renderProceduralGrammar(grammar, canvas);
                if (onStatus) onStatus('Rendered with Tier 1 WebGPU Edge LLM');
                return { tier: 'tier1', grammar };
              }
            }
          } catch (e) {
            // WebGPU not available or failed -> proceed to Tier 2
          }
        }

        // Tier 2A: Local Companion (Ollama / FLUX.1)
        const hasOllama = await probeOllama();
        if (hasOllama) {
          try {
            const r = await fetch('http://localhost:11434/api/generate', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                model: 'gemma2:2b',
                prompt: `You output ONLY JSON matching {"motifs":[string],"symmetry":num,"density":num,"theme":string}.\n${prompt}`,
                stream: false,
                format: 'json',
                options: { temperature: 0.3 }
              })
            });
            const j = await r.json();
            const grammar = JSON.parse(j.response);
            state.aiTier = 'Tier 2A (Local Companion Ollama)';
            state.lastGrammar = grammar;
            renderProceduralGrammar(grammar, canvas);
            if (onStatus) onStatus('Rendered with Tier 2A Local Ollama');
            return { tier: 'tier2a', grammar };
          } catch (e) {}
        }

        // Tier 2B: Seed-pinned Procedural Fallback (always succeeds deterministically)
        const grammar = fallbackGrammar(prompt);
        state.aiTier = 'Tier 2B (Procedural Fallback)';
        state.lastGrammar = grammar;
        const res = renderProceduralGrammar(grammar, canvas);
        if (onStatus) onStatus('Rendered with Tier 2B Seed-Pinned Procedural Engine');
        return { tier: 'tier2b', grammar, seed: res.seed };
      }
    };
  })();

  /* ==========================================================================
     MODULE 9: I18N & A11Y (Translations & Read Aloud)
     ========================================================================== */
  const I18N = {
    dict: {
      en: {
        appTitle: "COLORWORKS MASTERS STUDIO",
        appSubtitle: "Pro Ink-Bleed Art Journey Generator · Motion & Fidelity Engine v2.5",
        modeColoring: "🎨 Coloring Studio",
        modeJourney: "✒️ Journey Masterpieces",
        sourceTitle: "1 · Source Artwork",
        uploadBtn: "📷 Upload Photo / Diagram",
        generateBtn: "✨ Generate from Prompt (AI)",
        promptPlaceholder: "e.g. haunted forest gateway",
        sobelTitle: "Sobel De-Colorer",
        edgeSensitivity: "Edge Sensitivity",
        lineThickness: "Line Thickness",
        convertBtn: "Convert to Line Art",
        toolsTitle: "2 · Create",
        brush: "🖌 Brush",
        marker: "🖊 Marker",
        pencil: "✏ Pencil",
        spray: "💨 Spray",
        floodFill: "🪣 Ink Bleed Fill",
        eraser: "🧽 Eraser",
        stampPlaceholder: "Emoji stamp e.g. 🌸",
        sizeLabel: "Size",
        opacityLabel: "Opacity",
        undoBtn: "↩ Undo",
        paletteTitle: "Color Palette",
        bioPigmentsTitle: "Biochemical Pigments",
        musicTitle: "🎵 Your Music",
        addSongsBtn: "＋ Add Songs",
        noSongs: "No songs loaded.",
        playBtn: "▶ Play",
        pauseBtn: "⏸ Pause",
        focusAmbience: "🎧 Focus Ambience",
        precisionTitle: "Precision Score",
        gateUnlockedText: "🔓 Marketplace Unlocked (≥85%)",
        gateLockedText: "🔒 Locked: Reach ≥85% Precision",
        sellWallpaperBtn: "🎬 Sell Animated Wallpaper",
        timelapseBtn: "⏱ Export Time-Lapse (5s)",
        mirrorFinaleBtn: "🪞 Mirror Finale",
        printBtn: "🖨 Print 2x PNG",
        galleryTitle: "Masterpiece Gallery",
        engineControls: "Engine Controls",
        durationLabel: "Export Duration",
        bleedLabel: "Ink Bleed Diffusion",
        fidelityMetric: "Fidelity Metric",
        replayJourneyBtn: "Replay Journey",
        recordVideoBtn: "Record & Export Video",
        readAloudBtn: "🔊 Read Aloud",
        creatorPublishing: "⚙️ Creator Publishing",
        readyStatus: "Ready. Select an art piece or draw to begin.",
        convertedStatus: "De-colored locally ✓ (820×820)",
        gatePassedStatus: "✓ Precision gate passed — marketplace unlocked!",
        keepColoringStatus: "Keep coloring to reach ≥85% precision."
      },
      es: {
        appTitle: "ESTUDIO MAESTRO COLORWORKS",
        appSubtitle: "Generador de Viaje de Arte con Tinta · Motor de Fidelidad v2.5",
        modeColoring: "🎨 Estudio de Colorear",
        modeJourney: "✒️ Obras Maestras",
        sourceTitle: "1 · Obra de Origen",
        uploadBtn: "📷 Subir Foto / Diagrama",
        generateBtn: "✨ Generar con IA",
        promptPlaceholder: "ej. puerta del bosque embrujado",
        sobelTitle: "Decolorador Sobel",
        edgeSensitivity: "Sensibilidad de Bordes",
        lineThickness: "Grosor de Línea",
        convertBtn: "Convertir a Dibujo de Líneas",
        toolsTitle: "2 · Crear",
        brush: "🖌 Pincel",
        marker: "🖊 Marcador",
        pencil: "✏ Lápiz",
        spray: "💨 Aerosol",
        floodFill: "🪣 Relleno de Tinta",
        eraser: "🧽 Borrador",
        stampPlaceholder: "Sello de emoji ej. 🌸",
        sizeLabel: "Tamaño",
        opacityLabel: "Opacidad",
        undoBtn: "↩ Deshacer",
        paletteTitle: "Paleta de Colores",
        bioPigmentsTitle: "Pigmentos Bioquímicos",
        musicTitle: "🎵 Tu Música",
        addSongsBtn: "＋ Añadir Canciones",
        noSongs: "No hay canciones cargadas.",
        playBtn: "▶ Reproducir",
        pauseBtn: "⏸ Pausar",
        focusAmbience: "🎧 Ambiente de Concentración",
        precisionTitle: "Puntuación de Precisión",
        gateUnlockedText: "🔓 Mercado Desbloqueado (≥85%)",
        gateLockedText: "🔒 Bloqueado: Alcanza ≥85% de Precisión",
        sellWallpaperBtn: "🎬 Vender Fondo Animado",
        timelapseBtn: "⏱ Exportar Intervalo (5s)",
        mirrorFinaleBtn: "🪞 Final de Espejo",
        printBtn: "🖨 Imprimir PNG 2x",
        galleryTitle: "Galería de Obras Maestras",
        engineControls: "Controles del Motor",
        durationLabel: "Duración de Exportación",
        bleedLabel: "Difusión de Tinta",
        fidelityMetric: "Métrica de Fidelidad",
        replayJourneyBtn: "Repetir Viaje",
        recordVideoBtn: "Grabar y Exportar Video",
        readAloudBtn: "🔊 Leer en Voz Alta",
        creatorPublishing: "⚙️ Publicación de Creador",
        readyStatus: "Listo. Selecciona una obra o dibuja para comenzar.",
        convertedStatus: "Decolorado localmente ✓ (820×820)",
        gatePassedStatus: "✓ ¡Umbral de precisión superado — mercado desbloqueado!",
        keepColoringStatus: "Sigue coloreando para alcanzar ≥85% de precisión."
      },
      fr: {
        appTitle: "STUDIO DES MAÎTRES COLORWORKS",
        appSubtitle: "Générateur de Trajets Artistiques à l'Encre · Moteur v2.5",
        modeColoring: "🎨 Studio de Coloriage",
        modeJourney: "✒️ Chefs-d'Œuvre",
        sourceTitle: "1 · Œuvre Source",
        uploadBtn: "📷 Télécharger Photo / Diagramme",
        generateBtn: "✨ Générer par IA",
        promptPlaceholder: "ex. porte de forêt hantée",
        sobelTitle: "Décoloriseur Sobel",
        edgeSensitivity: "Sensibilité des Bords",
        lineThickness: "Épaisseur de Ligne",
        convertBtn: "Convertir en Dessin au Trait",
        toolsTitle: "2 · Créer",
        brush: "🖌 Pinceau",
        marker: "🖊 Marqueur",
        pencil: "✏ Crayon",
        spray: "💨 Aérosol",
        floodFill: "🪣 Remplissage d'Encre",
        eraser: "🧽 Gomme",
        stampPlaceholder: "Tampon émoji ex. 🌸",
        sizeLabel: "Taille",
        opacityLabel: "Opacité",
        undoBtn: "↩ Annuler",
        paletteTitle: "Palette de Couleurs",
        bioPigmentsTitle: "Pigments Biochimiques",
        musicTitle: "🎵 Votre Musique",
        addSongsBtn: "＋ Ajouter Morceaux",
        noSongs: "Aucun morceau chargé.",
        playBtn: "▶ Lire",
        pauseBtn: "⏸ Pause",
        focusAmbience: "🎧 Ambiance de Concentration",
        precisionTitle: "Score de Précision",
        gateUnlockedText: "🔓 Marché Débloqué (≥85%)",
        gateLockedText: "🔒 Verrouillé: Atteindre ≥85% de Précision",
        sellWallpaperBtn: "🎬 Vendre Fond Animé",
        timelapseBtn: "⏱ Exporter Timelapse (5s)",
        mirrorFinaleBtn: "🪞 Finale Miroir",
        printBtn: "🖨 Imprimer PNG 2x",
        galleryTitle: "Galerie des Chefs-d'Œuvre",
        engineControls: "Contrôles du Moteur",
        durationLabel: "Durée d'Exportation",
        bleedLabel: "Diffusion d'Encre",
        fidelityMetric: "Métrique de Fidélité",
        replayJourneyBtn: "Rejouer le Parcours",
        recordVideoBtn: "Enregistrer et Exporter Vidéo",
        readAloudBtn: "🔊 Lecture à Voix Haute",
        creatorPublishing: "⚙️ Publication Créateur",
        readyStatus: "Prêt. Choisissez une œuvre ou dessinez pour commencer.",
        convertedStatus: "Décoloré localement ✓ (820×820)",
        gatePassedStatus: "✓ Seuil de précision validé — marché débloqué !",
        keepColoringStatus: "Continuez à colorier pour atteindre ≥85% de précision."
      }
    },

    t(key) {
      const lang = state.lang || 'en';
      const bundle = I18N.dict[lang] || I18N.dict.en;
      return bundle[key] || I18N.dict.en[key] || key;
    },

    setLang(lang) {
      if (['en', 'es', 'fr'].includes(lang)) {
        state.lang = lang;
        if (typeof document !== 'undefined') {
          document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (key) {
              if (el.tagName === 'INPUT' && el.type === 'text') {
                el.placeholder = I18N.t(key);
              } else {
                el.textContent = I18N.t(key);
              }
            }
          });
        }
      }
    },

    readAloud(text) {
      if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance(text);
        u.lang = state.lang === 'es' ? 'es-ES' : state.lang === 'fr' ? 'fr-FR' : 'en-US';
        window.speechSynthesis.speak(u);
      }
    }
  };

  /* ==========================================================================
     MODULE 10: GUMROAD PUBLISHING (Part 10 - Opt-in with Mock Support)
     ========================================================================== */
  const GumroadPublisher = {
    // Curated tag dictionary mapping theme + top motifs to exactly 6 tags
    deriveTags(grammar) {
      const theme = (grammar && grammar.theme) || 'gothic';
      const motifs = (grammar && grammar.motifs) || ['bloom', 'art', 'vector'];
      const themeTags = {
        gothic: ['gothic', 'dark-fantasy', 'fine-art'],
        botanical: ['botanical', 'floral', 'nature'],
        cyber: ['cyberpunk', 'futuristic', 'neon'],
        cosmic: ['celestial', 'cosmic', 'astral'],
        hygge: ['hygge', 'cozy', 'minimalist']
      };
      const base = themeTags[theme] || themeTags.gothic;
      const cleanMotifs = motifs.map(m => m.toLowerCase().replace(/[^a-z0-9]/g, '')).filter(Boolean);

      const tagSet = new Set([...base, ...cleanMotifs, 'coloring', 'wallpaper', 'studio']);
      return Array.from(tagSet).slice(0, 6);
    },

    formatLicenseBlock(artistName, license) {
      return `\n\n© 2026 ${artistName || 'Anonymous Creator'} · Created with COLORWORKS MASTERS STUDIO · Licensed under Creative Commons ${license}\nOriginal work by the creator; all rights in the artwork vest in the artist upon creation.`;
    },

    // Pre-flight validation (Part 10.4 & Part 10.6)
    validatePreflight(payload) {
      const errors = [];
      if (!payload.title || typeof payload.title !== 'string') errors.push('Title is required');
      if (!payload.tags || payload.tags.length !== 6) errors.push('Tags count must be exactly 6');
      if (!payload.license) errors.push('Creative Commons license must be selected');
      if (!payload.attestationChecked) errors.push('Creator attestation checkbox must be confirmed');
      return { ok: errors.length === 0, errors };
    },

    // Publish flow with ?publishMock=1 support for testing without network risk
    async publishListing(productData, useMock = false) {
      const isMock = useMock || (typeof location !== 'undefined' && location.search.includes('publishMock=1'));

      const preflight = GumroadPublisher.validatePreflight(productData);
      if (!preflight.ok) {
        return { success: false, message: preflight.errors.join(', ') };
      }

      // Account limit check (10 products/day)
      if (state.gumroadProductsCountToday >= 10) {
        return { success: false, message: 'Account limit reached: maximum 10 products per day on Gumroad.' };
      }

      if (isMock) {
        state.gumroadProductsCountToday++;
        return {
          success: true,
          mock: true,
          product: {
            id: 'mock_prod_' + Date.now(),
            name: productData.title,
            short_url: 'https://gumroad.com/l/mock-' + Date.now(),
            published: productData.published || false
          }
        };
      }

      // Real API call if token provided
      const token = productData.token || state.gumroadToken;
      if (!token) {
        return { success: false, message: 'Gumroad personal access token or OAuth connection required.' };
      }

      try {
        const res = await fetch('https://api.gumroad.com/v2/products', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            access_token: token,
            name: productData.title,
            price: productData.priceCents || 499,
            published: productData.instantPublish || false,
            description: productData.description + GumroadPublisher.formatLicenseBlock(productData.artistName, productData.license),
            tags: productData.tags
          })
        });
        const data = await res.json();
        if (data && data.success) {
          state.gumroadProductsCountToday++;
          return { success: true, product: data.product };
        }
        return { success: false, message: (data && data.message) || 'Gumroad returned failure.' };
      } catch (e) {
        return { success: false, message: e.message };
      }
    }
  };

  /* ==========================================================================
     MODULE 11: DIAGNOSTICS HARNESS (Part 8 & Delivery Contract)
     Covers:
       1. Untainted Canvas & getImageData
       2. MediaRecorder MIME negotiation
       3. Sobel Smoke Test (synthetic square -> interior white, edges dark)
       4. Flood Fill (stack/boundary safety)
       5. Precision Engine (empty canvas + BUG-5 fully erased canvas locked)
       6. Time-Lapse Ops Immutability (BUG-4 regression)
       7. Journey Stroke-Count Boundaries (BUG-2 regression: >20 strokes, 0 at t=0)
       8. Grammar Pipeline (valid schema & deterministic repeatability)
       9. i18n Dictionary completeness & SpeechSynthesis availability
      10. Gumroad Local Pre-flight validation
     ========================================================================== */
  const Diagnostics = {
    async runDiagnostics() {
      const results = [];
      const log = (name, passed, details) => {
        results.push({ check: name, status: passed ? 'PASS' : 'FAIL', details });
      };

      // 1. Untainted Canvas check
      try {
        const testCnv = document.createElement('canvas');
        testCnv.width = 100;
        testCnv.height = 100;
        const tCtx = testCnv.getContext('2d');
        tCtx.fillStyle = '#ff0000';
        tCtx.fillRect(0, 0, 100, 100);
        const data = tCtx.getImageData(0, 0, 10, 10);
        log('Untainted Canvas Context', data && data.data.length > 0, 'Canvas and getImageData untainted');
      } catch (e) {
        log('Untainted Canvas Context', false, e.message);
      }

      // 2. MediaRecorder MIME negotiation
      const mime = ExportEngine.pickMimeType();
      log('MediaRecorder MIME Negotiation', !!mime, `Negotiated MIME: ${mime || 'none'}`);

      // 3. Sobel Smoke Test
      try {
        const testCnv = document.createElement('canvas');
        testCnv.width = 100;
        testCnv.height = 100;
        const tCtx = testCnv.getContext('2d');
        tCtx.fillStyle = '#ffffff';
        tCtx.fillRect(0, 0, 100, 100);
        tCtx.fillStyle = '#000000';
        tCtx.fillRect(25, 25, 50, 50); // synthetic square

        const res = SourceEngine.sobelConvert(tCtx, 100, 100, 60, 1.0);
        const out = res.imageData.data;
        // Check interior of square (x=50, y=50) -> should be white (255)
        const interiorIdx = (50 * 100 + 50) * 4;
        const isInteriorWhite = out[interiorIdx] === 255;
        // Check edge (x=25, y=50) -> should be dark (20)
        const edgeIdx = (50 * 100 + 25) * 4;
        const isEdgeDark = out[edgeIdx] === 20;
        log('Sobel Smoke Test', isInteriorWhite && isEdgeDark, 'Interior white, edge boundary detected');
      } catch (e) {
        log('Sobel Smoke Test', false, e.message);
      }

      // 4. Flood Fill Correctness
      try {
        const testCnv = document.createElement('canvas');
        testCnv.width = 60;
        testCnv.height = 60;
        const tCtx = testCnv.getContext('2d');
        tCtx.fillStyle = '#ffffff';
        tCtx.fillRect(0, 0, 60, 60);
        ToolsEngine.floodFill(tCtx, 60, 60, 10, 10, '#6d4aff');
        const pix = tCtx.getImageData(10, 10, 1, 1).data;
        const rgb = ToolsEngine.hexToRgb('#6d4aff');
        const isFilled = pix[0] === rgb.r && pix[1] === rgb.g && pix[2] === rgb.b;
        log('Flood Fill Correctness', isFilled, 'Flood fill pixel color updated correctly');
      } catch (e) {
        log('Flood Fill Correctness', false, e.message);
      }

      // 5. Precision Engine & BUG-5 Regression Test
      try {
        const testCnv = document.createElement('canvas');
        testCnv.width = 100;
        testCnv.height = 100;
        const tCtx = testCnv.getContext('2d');
        tCtx.fillStyle = '#ffffff';
        tCtx.fillRect(0, 0, 100, 100);
        const baseLine = tCtx.getImageData(0, 0, 100, 100);
        const lineMask = new Uint8Array(100 * 100);

        // (a) Empty canvas returns empty / 0 score
        const emptyScore = PrecisionEngine.computePrecision(tCtx, baseLine, lineMask, 100, 100);
        const p1 = emptyScore.empty === true && emptyScore.score === 0;

        // (b) Fully erased canvas with destination-out produces alpha 0.
        // BUG-5 regression: Erasing 100% of canvas must NOT pass gate!
        tCtx.save();
        tCtx.globalCompositeOperation = 'destination-out';
        tCtx.fillStyle = '#ffffff';
        tCtx.fillRect(0, 0, 100, 100);
        tCtx.restore();

        const erasedScore = PrecisionEngine.computePrecision(tCtx, baseLine, lineMask, 100, 100);
        const p2 = erasedScore.passed === false && erasedScore.score === 0;
        log('Precision Engine (BUG-5 Regression)', p1 && p2, 'Empty canvas returns 0, erased canvas stays locked');
      } catch (e) {
        log('Precision Engine (BUG-5 Regression)', false, e.message);
      }

      // 6. Time-Lapse Ops Immutability (BUG-4 Regression)
      try {
        const testCnv = document.createElement('canvas');
        testCnv.width = 100;
        testCnv.height = 100;
        const tCtx = testCnv.getContext('2d');
        state.ops = [
          { t: 'paint', a: [10, 10], b: [20, 20], c: '#6d4aff', w: 2, alpha: 1, tool: 'brush' },
          { t: 'paint', a: [20, 20], b: [30, 30], c: '#6d4aff', w: 2, alpha: 1, tool: 'brush' }
        ];
        const initialLen = state.ops.length;

        // Replay run 1
        state.replaying = true;
        const replay1 = [...state.ops];
        replay1.forEach(o => ToolsEngine.paint(tCtx, { x: o.a[0], y: o.a[1] }, { x: o.b[0], y: o.b[1] }, { tool: 'brush', color: '#6d4aff', size: 2, opacity: 100 }, true));
        state.replaying = false;

        // Replay run 2
        state.replaying = true;
        const replay2 = [...state.ops];
        replay2.forEach(o => ToolsEngine.paint(tCtx, { x: o.a[0], y: o.a[1] }, { x: o.b[0], y: o.b[1] }, { tool: 'brush', color: '#6d4aff', size: 2, opacity: 100 }, true));
        state.replaying = false;

        const unchanged = state.ops.length === initialLen;
        log('Time-Lapse Immutability (BUG-4 Regression)', unchanged, `Ops count before: ${initialLen}, after: ${state.ops.length}`);
      } catch (e) {
        log('Time-Lapse Immutability (BUG-4 Regression)', false, e.message);
      }

      // 7. Journey Stroke-Count Boundaries (BUG-2 Regression)
      try {
        let allPiecesOk = true;
        const pieceKeys = Object.keys(JourneyEngine.PIECES);
        for (const k of pieceKeys) {
          const res = JourneyEngine.buildPiece(k);
          const hasEnoughStrokes = res.strokes.length > 20;
          // Verify no phantom strokes at t=0 with empty functions
          const phantomStrokes = res.strokes.filter(s => s.t === 0 && (!s.fn || s.fn.toString().includes('{}')));
          if (!hasEnoughStrokes || phantomStrokes.length > 0) {
            allPiecesOk = false;
            break;
          }
        }
        log('Journey Stroke Boundaries (BUG-2 Regression)', allPiecesOk, 'All 10 pieces build >20 strokes with 0 phantom strokes at t=0');
      } catch (e) {
        log('Journey Stroke Boundaries (BUG-2 Regression)', false, e.message);
      }

      // 8. Grammar Pipeline & Determinism
      try {
        const prompt = 'gothic skull garden';
        const g1 = EdgeEngine.fallbackGrammar(prompt);
        const g2 = EdgeEngine.fallbackGrammar(prompt);
        const validSchema = Array.isArray(g1.motifs) && typeof g1.symmetry === 'number' && typeof g1.density === 'number' && !!g1.theme;

        const testCnv1 = document.createElement('canvas');
        testCnv1.width = 100;
        testCnv1.height = 100;
        const res1 = EdgeEngine.renderProceduralGrammar(g1, testCnv1);

        const testCnv2 = document.createElement('canvas');
        testCnv2.width = 100;
        testCnv2.height = 100;
        const res2 = EdgeEngine.renderProceduralGrammar(g2, testCnv2);

        const deterministic = res1.seed === res2.seed;
        log('Grammar Pipeline & Determinism', validSchema && deterministic, `Valid JSON schema, seed pinned (${res1.seed})`);
      } catch (e) {
        log('Grammar Pipeline & Determinism', false, e.message);
      }

      // 9. i18n & Speech Synthesis
      const langs = ['en', 'es', 'fr'];
      let dictComplete = true;
      langs.forEach(l => {
        if (!I18N.dict[l] || Object.keys(I18N.dict[l]).length < 20) dictComplete = false;
      });
      const hasSpeech = typeof window !== 'undefined' && 'speechSynthesis' in window;
      log('i18n & Speech Synthesis', dictComplete, `Dictionaries EN/ES/FR complete; SpeechSynthesis available: ${hasSpeech}`);

      // 10. Gumroad Local Pre-flight
      const testPayload = {
        title: 'Gothic Skull Wallpaper',
        tags: ['gothic', 'dark-fantasy', 'fine-art', 'skull', 'coloring', 'wallpaper'],
        license: 'CC BY-NC-SA 4.0',
        attestationChecked: true
      };
      const pf = GumroadPublisher.validatePreflight(testPayload);
      log('Gumroad Local Pre-flight', pf.ok, 'Payload schema, 6 tags, CC license, and attestation verified');

      if (typeof console !== 'undefined' && console.table) {
        console.table(results);
      }

      const failures = results.filter(r => r.status === 'FAIL').length;
      if (typeof window !== 'undefined') {
        window.dispatchEvent(new CustomEvent('diagnostics:complete', { detail: { results, failures } }));
      }
      return failures;
    }
  };

  // Expose window.runDiagnostics globally per Part 8 contract
  if (typeof window !== 'undefined') {
    window.runDiagnostics = Diagnostics.runDiagnostics;
  }

  /* Return public API */
  return {
    state,
    PAPERS,
    BASIC_PALETTE,
    BIOCHEMICAL_PIGMENTS,
    JOURNEY_PALETTES,
    SourceEngine,
    ToolsEngine,
    PrecisionEngine,
    JourneyEngine,
    KaleidoscopeEngine,
    AudioEngine,
    ExportEngine,
    EdgeEngine,
    I18N,
    GumroadPublisher,
    Diagnostics
  };
});
