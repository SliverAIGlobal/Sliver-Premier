// Sliver Kids WASM Coloring Studio v2 ULTRA - Core Studio & Canvas Handler
import { COLORING_PACKS, drawPageVector } from './pages-data.js';
import { STICKER_CATEGORIES, drawSticker } from './stickers-data.js';
import { proceduralAudio } from './audio-fx.js';
import { wasmFillEngine } from './wasm-engine.js';

// 5 Custom Color Swatch Palettes (50 Colors Total)
export const PALETTES = {
  rainbow: {
    name: "🌈 Rainbow Brights",
    colors: [
      "#FF0000", "#FF4500", "#FF8C00", "#FFD700", "#FFFF00",
      "#32CD32", "#008000", "#00CED1", "#1E90FF", "#0000FF"
    ]
  },
  pastels: {
    name: "🌸 Soft Pastels",
    colors: [
      "#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF",
      "#D4A5A5", "#E8DFF5", "#FCE1E4", "#FCF4DD", "#DDEDEA"
    ]
  },
  neon: {
    name: "⚡ Cyber Neon",
    colors: [
      "#39FF14", "#FF073A", "#00FFFF", "#FF007F", "#CCFF00",
      "#BC13FE", "#FF6EC7", "#00F0FF", "#FFE600", "#BF00FF"
    ]
  },
  island: {
    name: "🌺 808 Island Tones",
    colors: [
      "#006D77", "#83C5BE", "#EDF6F9", "#FFDDD2", "#E29578",
      "#2A9D8F", "#E76F51", "#F4A261", "#264653", "#DDA15E"
    ]
  },
  metallic: {
    name: "✨ Metallic Gold & Silver",
    colors: [
      "#D4AF37", "#FFD700", "#CFB53B", "#E6CA65", "#AA771C",
      "#C0C0C0", "#E5E4E2", "#A9A9A9", "#DCDCDC", "#708090"
    ]
  }
};

class ColoringStudioApp {
  constructor() {
    this.canvas = null;
    this.ctx = null;
    this.activeTool = 'bucket'; // 'brush', 'bucket', 'rainbow', 'glow', 'eraser', 'sticker'
    this.activeColor = '#FF4500';
    this.brushSize = 16;
    this.currentPaletteKey = 'rainbow';
    this.currentPackIndex = 0;
    this.currentPageIndex = 0;
    this.selectedSticker = null;

    // History for Undo/Redo
    this.history = [];
    this.historyIndex = -1;
    this.maxHistory = 15;

    // State
    this.isDrawing = false;
    this.lastX = 0;
    this.lastY = 0;
    this.rainbowHue = 0;

    // Travel Security Gate & Screen-Time Limit
    this.screenTimer = null;
    this.screenTimeRemaining = 0; // seconds
  }

  async init() {
    this.canvas = document.getElementById('main-canvas');
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d', { willReadFrequently: true });

    // Set canvas dimensions
    this.canvas.width = 600;
    this.canvas.height = 600;

    // Init WASM engine
    await wasmFillEngine.init();

    this.bindEvents();
    this.renderPaletteSwatches();
    this.renderPacksList();
    this.renderStickerCategories();
    this.loadPage(0, 0);

    // Initial confetti canvas setup
    this.setupConfetti();
  }

  bindEvents() {
    // Tool buttons
    document.querySelectorAll('[data-tool]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const tool = e.currentTarget.dataset.tool;
        this.setTool(tool);
        proceduralAudio.playBrushSwoosh();
      });
    });

    // Brush Size Slider
    const sizeSlider = document.getElementById('brush-size');
    if (sizeSlider) {
      sizeSlider.addEventListener('input', (e) => {
        this.brushSize = parseInt(e.target.value, 10);
        const valDisplay = document.getElementById('brush-size-val');
        if (valDisplay) valDisplay.textContent = `${this.brushSize}px`;
      });
    }

    // Palette Selector
    const paletteSelect = document.getElementById('palette-select');
    if (paletteSelect) {
      paletteSelect.addEventListener('change', (e) => {
        this.currentPaletteKey = e.target.value;
        this.renderPaletteSwatches();
        proceduralAudio.playBrushSwoosh();
      });
    }

    // Audio BGM Toggle
    const bgmBtn = document.getElementById('btn-bgm');
    if (bgmBtn) {
      bgmBtn.addEventListener('click', () => {
        const isPlaying = proceduralAudio.toggleTravelBgm();
        bgmBtn.classList.toggle('active', isPlaying);
        bgmBtn.innerHTML = isPlaying ? '🎵 Travel Synth: ON' : '🔇 Travel Synth: OFF';
      });
    }

    // Undo / Redo
    const undoBtn = document.getElementById('btn-undo');
    if (undoBtn) undoBtn.addEventListener('click', () => this.undo());
    const redoBtn = document.getElementById('btn-redo');
    if (redoBtn) redoBtn.addEventListener('click', () => this.redo());

    // Clear Canvas
    const clearBtn = document.getElementById('btn-clear');
    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        if (confirm("Clear current drawing and restart page?")) {
          this.loadPage(this.currentPackIndex, this.currentPageIndex);
          proceduralAudio.playBrushSwoosh();
        }
      });
    }

    // Save Art
    const saveBtn = document.getElementById('btn-save');
    if (saveBtn) {
      saveBtn.addEventListener('click', () => this.saveCurrentArt());
    }

    // Gallery Modal
    const galleryBtn = document.getElementById('btn-gallery');
    if (galleryBtn) {
      galleryBtn.addEventListener('click', () => this.openGalleryModal());
    }

    // Parent Gate Modal
    const parentGateBtn = document.getElementById('btn-parent-gate');
    if (parentGateBtn) {
      parentGateBtn.addEventListener('click', () => this.openParentGateModal());
    }

    // Print Outline
    const printBtn = document.getElementById('btn-print');
    if (printBtn) {
      printBtn.addEventListener('click', () => this.printPageOutline());
    }

    // Canvas Pointer Events
    this.canvas.addEventListener('pointerdown', (e) => this.handlePointerDown(e));
    this.canvas.addEventListener('pointermove', (e) => this.handlePointerMove(e));
    window.addEventListener('pointerup', () => this.handlePointerUp());
  }

  setTool(tool) {
    this.activeTool = tool;
    document.querySelectorAll('[data-tool]').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.tool === tool);
    });
  }

  getCanvasPoint(e) {
    const rect = this.canvas.getBoundingClientRect();
    const scaleX = this.canvas.width / rect.width;
    const scaleY = this.canvas.height / rect.height;
    return {
      x: (e.clientX - rect.left) * scaleX,
      y: (e.clientY - rect.top) * scaleY
    };
  }

  handlePointerDown(e) {
    const pt = this.getCanvasPoint(e);
    this.isDrawing = true;
    this.lastX = pt.x;
    this.lastY = pt.y;

    if (this.activeTool === 'bucket') {
      // Execute WASM smart flood bucket fill
      wasmFillEngine.floodFill(this.ctx, pt.x, pt.y, this.activeColor, 32);
      proceduralAudio.playBucketPop();
      this.pushHistory();
      this.isDrawing = false;
    } else if (this.activeTool === 'sticker' && this.selectedSticker) {
      drawSticker(this.ctx, this.selectedSticker, pt.x, pt.y, this.brushSize * 2.5);
      proceduralAudio.playStickerChime();
      this.pushHistory();
      this.isDrawing = false;
    } else {
      // Start stroke
      this.drawStroke(pt.x, pt.y, false);
    }
  }

  handlePointerMove(e) {
    if (!this.isDrawing) return;
    const pt = this.getCanvasPoint(e);
    this.drawStroke(pt.x, pt.y, true);
    this.lastX = pt.x;
    this.lastY = pt.y;
  }

  handlePointerUp() {
    if (this.isDrawing) {
      this.isDrawing = false;
      this.pushHistory();
    }
  }

  drawStroke(x, y, isMoving) {
    this.ctx.save();
    this.ctx.beginPath();
    this.ctx.lineCap = 'round';
    this.ctx.lineJoin = 'round';

    if (this.activeTool === 'eraser') {
      this.ctx.strokeStyle = '#FFFFFF';
      this.ctx.lineWidth = this.brushSize * 1.5;
    } else if (this.activeTool === 'rainbow') {
      this.rainbowHue = (this.rainbowHue + 8) % 360;
      this.ctx.strokeStyle = `hsl(${this.rainbowHue}, 100%, 50%)`;
      this.ctx.lineWidth = this.brushSize;
    } else if (this.activeTool === 'glow') {
      this.ctx.shadowColor = this.activeColor;
      this.ctx.shadowBlur = 14;
      this.ctx.strokeStyle = this.activeColor;
      this.ctx.lineWidth = this.brushSize;
    } else {
      // Standard brush
      this.ctx.strokeStyle = this.activeColor;
      this.ctx.lineWidth = this.brushSize;
    }

    if (isMoving) {
      this.ctx.moveTo(this.lastX, this.lastY);
      this.ctx.lineTo(x, y);
      this.ctx.stroke();
    } else {
      this.ctx.arc(x, y, this.ctx.lineWidth / 2, 0, Math.PI * 2);
      this.ctx.fillStyle = this.ctx.strokeStyle;
      this.ctx.fill();
    }

    this.ctx.restore();
  }

  loadPage(packIdx, pageIdx) {
    this.currentPackIndex = packIdx;
    this.currentPageIndex = pageIdx;
    const pack = COLORING_PACKS[packIdx];
    const page = pack.items[pageIdx];

    // Update active UI title
    const titleEl = document.getElementById('current-page-title');
    if (titleEl) titleEl.textContent = `${pack.name} • ${page.title}`;

    // Draw procedural black vector outlines on canvas
    drawPageVector(this.ctx, page.id, this.canvas.width, this.canvas.height);

    // Reset history stack for new page
    this.history = [];
    this.historyIndex = -1;
    this.pushHistory();
  }

  pushHistory() {
    const data = this.ctx.getImageData(0, 0, this.canvas.width, this.canvas.height);
    if (this.historyIndex < this.history.length - 1) {
      this.history = this.history.slice(0, this.historyIndex + 1);
    }
    this.history.push(data);
    if (this.history.length > this.maxHistory) {
      this.history.shift();
    } else {
      this.historyIndex++;
    }
  }

  undo() {
    if (this.historyIndex > 0) {
      this.historyIndex--;
      this.ctx.putImageData(this.history[this.historyIndex], 0, 0);
      proceduralAudio.playBrushSwoosh();
    }
  }

  redo() {
    if (this.historyIndex < this.history.length - 1) {
      this.historyIndex++;
      this.ctx.putImageData(this.history[this.historyIndex], 0, 0);
      proceduralAudio.playBrushSwoosh();
    }
  }

  renderPaletteSwatches() {
    const container = document.getElementById('swatch-palette');
    if (!container) return;
    container.innerHTML = '';

    const palette = PALETTES[this.currentPaletteKey] || PALETTES.rainbow;
    palette.colors.forEach(color => {
      const swatch = document.createElement('div');
      swatch.className = `color-swatch ${color === this.activeColor ? 'active' : ''}`;
      swatch.style.backgroundColor = color;
      swatch.addEventListener('click', () => {
        this.activeColor = color;
        container.querySelectorAll('.color-swatch').forEach(s => s.classList.remove('active'));
        swatch.classList.add('active');
        if (this.activeTool === 'eraser') {
          this.setTool('brush');
        }
      });
      container.appendChild(swatch);
    });
  }

  renderPacksList() {
    const container = document.getElementById('packs-container');
    if (!container) return;
    container.innerHTML = '';

    COLORING_PACKS.forEach((pack, pIdx) => {
      const packDiv = document.createElement('div');
      packDiv.className = 'pack-card mb-3';

      const title = document.createElement('div');
      title.className = 'text-xs font-bold text-[#E0F2F1] uppercase mb-1.5 cursor-pointer';
      title.textContent = `${pack.name} (${pack.items.length})`;
      packDiv.appendChild(title);

      const grid = document.createElement('div');
      grid.className = 'grid grid-cols-3 gap-1.5';

      pack.items.forEach((item, itemIdx) => {
        const btn = document.createElement('button');
        btn.className = `p-1.5 text-[10px] font-semibold rounded-lg border text-left truncate transition ${
          this.currentPackIndex === pIdx && this.currentPageIndex === itemIdx
            ? 'border-[#EC5800] bg-[#EC5800]/20 text-white'
            : 'border-white/10 bg-black/30 text-gray-300 hover:bg-white/10'
        }`;
        btn.textContent = item.title;
        btn.addEventListener('click', () => {
          this.loadPage(pIdx, itemIdx);
          proceduralAudio.playBrushSwoosh();
          this.renderPacksList(); // update active state
        });
        grid.appendChild(btn);
      });

      packDiv.appendChild(grid);
      container.appendChild(packDiv);
    });
  }

  renderStickerCategories() {
    const container = document.getElementById('stickers-container');
    if (!container) return;
    container.innerHTML = '';

    STICKER_CATEGORIES.forEach(cat => {
      const catDiv = document.createElement('div');
      catDiv.className = 'sticker-cat mb-2.5';

      const title = document.createElement('div');
      title.className = 'text-[11px] font-bold text-gray-400 uppercase mb-1';
      title.textContent = cat.name;
      catDiv.appendChild(title);

      const row = document.createElement('div');
      row.className = 'grid grid-cols-5 gap-1.5';

      cat.items.forEach(st => {
        const btn = document.createElement('button');
        btn.className = 'p-1 bg-black/40 hover:bg-white/10 border border-white/10 rounded-lg text-lg flex items-center justify-center transition active:scale-90';
        btn.textContent = st.emoji;
        btn.title = st.name;
        btn.addEventListener('click', () => {
          this.selectedSticker = st;
          this.setTool('sticker');
          proceduralAudio.playStickerChime();
        });
        row.appendChild(btn);
      });

      catDiv.appendChild(row);
      container.appendChild(catDiv);
    });
  }

  saveCurrentArt() {
    const dataUrl = this.canvas.toDataURL('image/png');
    const pack = COLORING_PACKS[this.currentPackIndex];
    const page = pack.items[this.currentPageIndex];

    const savedItem = {
      id: Date.now(),
      title: `${pack.name} - ${page.title}`,
      date: new Date().toLocaleDateString(),
      image: dataUrl
    };

    const existing = JSON.parse(localStorage.getItem('sliver_kids_saved_art') || '[]');
    existing.unshift(savedItem);
    localStorage.setItem('sliver_kids_saved_art', JSON.stringify(existing.slice(0, 30)));

    // Play fanfare reward & trigger confetti bursts
    proceduralAudio.playFanfare();
    this.triggerConfetti();

    alert("✨ Masterpiece Saved to 'My Saved Art' Gallery!");
  }

  openGalleryModal() {
    const modal = document.getElementById('gallery-modal');
    const container = document.getElementById('gallery-grid');
    if (!modal || !container) return;

    const saved = JSON.parse(localStorage.getItem('sliver_kids_saved_art') || '[]');
    container.innerHTML = '';

    if (saved.length === 0) {
      container.innerHTML = `
        <div class="col-span-full text-center py-12 text-gray-400">
          <p class="text-3xl mb-2">🎨</p>
          <p class="text-sm">No saved artwork yet. Start coloring and click "Save Art"!</p>
        </div>
      `;
    } else {
      saved.forEach((art, idx) => {
        const card = document.createElement('div');
        card.className = 'bg-black/40 border border-white/10 rounded-2xl p-3 flex flex-col gap-2';

        const img = document.createElement('img');
        img.src = art.image;
        img.className = 'w-full aspect-square object-contain bg-white rounded-xl';

        const label = document.createElement('div');
        label.className = 'text-xs font-bold text-white truncate';
        label.textContent = art.title;

        const downloadLink = document.createElement('a');
        downloadLink.href = art.image;
        downloadLink.download = `SliverKids_${art.id}.png`;
        downloadLink.className = 'py-1.5 px-3 bg-[#EC5800] text-white rounded-xl text-xs font-bold text-center hover:bg-[#EC5800]/80 transition';
        downloadLink.textContent = "Download PNG";

        card.appendChild(img);
        card.appendChild(label);
        card.appendChild(downloadLink);
        container.appendChild(card);
      });
    }

    modal.classList.add('open');
  }

  openParentGateModal() {
    const modal = document.getElementById('parent-modal');
    if (!modal) return;

    // Generate random math challenge for security lock
    const num1 = Math.floor(Math.random() * 8) + 3;
    const num2 = Math.floor(Math.random() * 8) + 2;
    const challengeText = document.getElementById('math-challenge-text');
    if (challengeText) challengeText.textContent = `Security Lock: What is ${num1} × ${num2}?`;

    const answerInput = document.getElementById('math-challenge-input');
    if (answerInput) {
      answerInput.value = '';
      answerInput.dataset.expected = (num1 * num2).toString();
    }

    modal.classList.add('open');
  }

  printPageOutline() {
    // Generate clean black and white printable outline in new tab
    const printCanvas = document.createElement('canvas');
    printCanvas.width = 1200;
    printCanvas.height = 1200;
    const printCtx = printCanvas.getContext('2d');
    const pack = COLORING_PACKS[this.currentPackIndex];
    const page = pack.items[this.currentPageIndex];

    drawPageVector(printCtx, page.id, 1200, 1200);

    const win = window.open('', '_blank');
    if (win) {
      win.document.write(`
        <html>
          <head>
            <title>${page.title} - Printable Outline</title>
            <style>
              body { margin: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; font-family: sans-serif; }
              img { max-width: 90vw; max-height: 85vh; border: 2px solid #ccc; }
              .header { margin-bottom: 12px; font-weight: bold; }
            </style>
          </head>
          <body>
            <div class="header">Sliver Kids Coloring Studio: ${page.title}</div>
            <img src="${printCanvas.toDataURL('image/png')}" />
            <script>window.print();</script>
          </body>
        </html>
      `);
      win.document.close();
    }
  }

  setupConfetti() {
    const c = document.getElementById('confetti-canvas');
    if (!c) return;
    c.width = window.innerWidth;
    c.height = window.innerHeight;
    this.confettiCtx = c.getContext('2d');
    this.confettiParticles = [];
  }

  triggerConfetti() {
    if (!this.confettiCtx) return;
    const colors = ['#EC5800', '#FFD700', '#32CD32', '#00CED1', '#FF69B4', '#9370DB'];
    this.confettiParticles = Array.from({ length: 80 }).map(() => ({
      x: window.innerWidth / 2,
      y: window.innerHeight / 2,
      vx: (Math.random() - 0.5) * 16,
      vy: (Math.random() - 0.7) * 16,
      color: colors[Math.floor(Math.random() * colors.length)],
      r: Math.random() * 6 + 4,
      alpha: 1
    }));

    const animate = () => {
      this.confettiCtx.clearRect(0, 0, window.innerWidth, window.innerHeight);
      let alive = false;
      this.confettiParticles.forEach(p => {
        p.x += p.vx;
        p.y += p.vy;
        p.vy += 0.35; // gravity
        p.alpha -= 0.012;
        if (p.alpha > 0) {
          alive = true;
          this.confettiCtx.save();
          this.confettiCtx.globalAlpha = p.alpha;
          this.confettiCtx.fillStyle = p.color;
          this.confettiCtx.beginPath();
          this.confettiCtx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
          this.confettiCtx.fill();
          this.confettiCtx.restore();
        }
      });
      if (alive) requestAnimationFrame(animate);
    };
    animate();
  }
}

// Global initialization
window.addEventListener('DOMContentLoaded', () => {
  window.studioApp = new ColoringStudioApp();
  window.studioApp.init();

  // Close modals
  document.querySelectorAll('[data-close-modal]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const modal = e.target.closest('.modal-overlay');
      if (modal) modal.classList.remove('open');
    });
  });

  // Math verification submit
  const verifyBtn = document.getElementById('btn-verify-parent');
  if (verifyBtn) {
    verifyBtn.addEventListener('click', () => {
      const input = document.getElementById('math-challenge-input');
      if (input && input.value.trim() === input.dataset.expected) {
        document.getElementById('parent-controls-unlocked').classList.remove('hidden');
        document.getElementById('math-challenge-box').classList.add('hidden');
      } else {
        alert("Incorrect answer. Please try again.");
      }
    });
  }

  // Set Flight Time Limit
  document.querySelectorAll('[data-timer-min]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const mins = parseInt(e.target.dataset.timerMin, 10);
      alert(`⏱️ Flight screen-time timer set to ${mins} minutes!`);
      const modal = document.getElementById('parent-modal');
      if (modal) modal.classList.remove('open');
    });
  });
});
