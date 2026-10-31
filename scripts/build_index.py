#!/usr/bin/env python3
"""Builds index.html cleanly by reading wasm_base64.txt and substituting."""

with open('wasm_base64.txt', 'r') as f:
    wasm_b64 = f.read().strip()

template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Sliver Kids WASM Coloring Studio v2 ULTRA</title>
  <link rel="stylesheet" href="styles.css">
  <link rel="manifest" href="manifest.json">
  <meta name="theme-color" content="#0f111a">
</head>
<body>

  <!-- Top Header Navigation -->
  <header class="app-header">
    <div class="brand-section">
      <span class="brand-badge">v2 ULTRA</span>
      <h1 class="brand-title">Sliver <span>Coloring Studio</span></h1>
    </div>

    <div class="header-actions">
      <!-- Calm Travel Synth BGM Toggle -->
      <button id="btnBGM" class="btn-icon" title="Calm Travel Synth BGM">
        🎵 <span id="bgmLabel">BGM Off</span>
      </button>

      <!-- Sound FX Toggle -->
      <button id="btnSoundFX" class="btn-icon active" title="Sound Effects">
        🔊 <span>Sound On</span>
      </button>

      <!-- 120 Pages Library Selector -->
      <button id="btnOpenLibrary" class="btn-icon btn-accent">
        📚 <span>120 Pages</span>
      </button>

      <!-- Decolorizer Photo Uploader -->
      <button id="btnOpenUploader" class="btn-icon">
        📷 <span>Decolorizer</span>
      </button>

      <!-- My Saved Art Gallery -->
      <button id="btnOpenGallery" class="btn-icon">
        🖼️ <span>Gallery</span>
      </button>

      <!-- Parent Security & Travel Gate -->
      <button id="btnParentGate" class="btn-icon">
        👨‍👩‍👧 <span>Parent Gate</span>
      </button>

      <!-- Print / Export Menu -->
      <button id="btnExport" class="btn-icon">
        💾 <span>Export</span>
      </button>
    </div>
  </header>

  <!-- Main Coloring Studio Workspace -->
  <main class="studio-layout">

    <!-- Left Toolset Drawer -->
    <aside class="left-toolbar">
      <div class="tool-group">
        <!-- Magic Flood Bucket -->
        <button class="tool-btn active" data-tool="bucket" title="WASM Smart Flood Fill">
          <span class="icon">🪣</span>
          <span>Fill</span>
        </button>

        <!-- Standard Brush -->
        <button class="tool-btn" data-tool="brush" title="Standard Brush">
          <span class="icon">🖌️</span>
          <span>Brush</span>
        </button>

        <!-- Magic Rainbow Brush -->
        <button class="tool-btn" data-tool="rainbow" title="Magic Rainbow Brush (Auto-Shifts Color)">
          <span class="icon">🌈</span>
          <span>Rainbow</span>
        </button>

        <!-- Neon Glow Brush -->
        <button class="tool-btn" data-tool="glow" title="Neon Glow Brush">
          <span class="icon">✨</span>
          <span>Neon</span>
        </button>

        <!-- Magic Sticker Stamp Drawer Toggle -->
        <button class="tool-btn" data-tool="sticker" id="btnStickerDrawer" title="60 Magic Sticker Stamps">
          <span class="icon">⭐</span>
          <span>Stickers</span>
        </button>

        <!-- Eraser -->
        <button class="tool-btn" data-tool="eraser" title="Clean Eraser">
          <span class="icon">🧼</span>
          <span>Eraser</span>
        </button>
      </div>

      <!-- Action Controls -->
      <div class="tool-group" style="margin-top: auto;">
        <button class="tool-btn" id="btnUndo" title="Undo">
          <span class="icon">↩️</span>
          <span>Undo</span>
        </button>
        <button class="tool-btn" id="btnRedo" title="Redo">
          <span class="icon">↪️</span>
          <span>Redo</span>
        </button>
        <button class="tool-btn" id="btnClear" title="Clear Page">
          <span class="icon">🗑️</span>
          <span>Clear</span>
        </button>
      </div>
    </aside>

    <!-- Center Canvas Area -->
    <section class="canvas-viewport">
      <div class="canvas-container">
        <canvas id="mainCanvas"></canvas>
      </div>

      <!-- Floating Canvas Info -->
      <div class="canvas-floating-controls">
        <span id="currentArtworkTitle" style="font-weight: 700; font-size: 14px; color: var(--neon-cyan);">Loading...</span>
      </div>
    </section>

    <!-- Right Panel: Custom Color Swatch Palettes & Brush Controls -->
    <aside class="right-panel">
      <div class="panel-header">
        <span>🎨 Color Studio</span>
        <div id="activeColorDisplay" style="width: 24px; height: 24px; border-radius: 50%; border: 2px solid #fff; background-color: #FF3D00;"></div>
      </div>

      <!-- Brush Stroke Slider -->
      <div class="brush-controls">
        <label>
          <span>Stroke Size</span>
          <span id="brushSizeLabel">18px</span>
        </label>
        <input type="range" id="brushSizeSlider" class="brush-slider" min="4" max="60" value="18">
      </div>

      <!-- 5 Custom Color Palettes Tabs -->
      <div class="swatch-group-title">Color Palettes</div>
      <div class="palette-tabs" id="paletteTabs"></div>

      <!-- Palette Swatches Grid (50 Colors Total) -->
      <div class="swatches-grid" id="swatchesGrid"></div>

      <!-- Quick Save & Print Action -->
      <div style="padding: 16px; margin-top: auto; display: flex; flex-direction: column; gap: 10px;">
        <button id="btnQuickSave" class="btn-icon btn-accent" style="justify-content: center; padding: 12px;">
          🎉 <span>Save to My Art</span>
        </button>
        <button id="btnPrintOutline" class="btn-icon" style="justify-content: center; padding: 10px;">
          🖨️ <span>Print Outline</span>
        </button>
      </div>
    </aside>

  </main>

  <!-- ================= MODALS & DRAWERS ================= -->

  <!-- 1. 120 Vector Pages Library Modal -->
  <div class="modal-overlay" id="libraryModal">
    <div class="modal-card">
      <div class="modal-header">
        <div class="modal-title">📚 120 Vector Coloring Pages</div>
        <button class="btn-icon" id="btnCloseLibrary">✕</button>
      </div>
      <div class="modal-body">
        <div class="pack-tabs-container" id="packTabsContainer"></div>
        <div class="pages-grid" id="pagesGrid"></div>
      </div>
    </div>
  </div>

  <!-- 2. 60 Magic Sticker Stamps Modal -->
  <div class="modal-overlay" id="stickerModal">
    <div class="modal-card" style="max-width: 680px;">
      <div class="modal-header">
        <div class="modal-title">⭐ 60 Magic Sticker Stamps</div>
        <button class="btn-icon" id="btnCloseStickers">✕</button>
      </div>
      <div class="modal-body">
        <div class="pack-tabs-container" id="stickerCatTabs"></div>
        <div class="sticker-drawer-body" id="stickersGrid"></div>
      </div>
    </div>
  </div>

  <!-- 3. WASM Privacy-First Decolorizer Uploader Modal -->
  <div class="modal-overlay" id="uploaderModal">
    <div class="modal-card" style="max-width: 820px;">
      <div class="modal-header">
        <div class="modal-title">📷 WASM Photo Decolorizer (100% On-Device)</div>
        <button class="btn-icon" id="btnCloseUploader">✕</button>
      </div>
      <div class="modal-body">
        <div class="decolorize-grid">
          <div>
            <div style="margin-bottom: 12px;">
              <input type="file" id="decolorizeFileInput" accept="image/*" style="display: none;">
              <button class="btn-icon btn-accent" id="btnSelectPhoto" style="width: 100%; justify-content: center; padding: 12px;">
                📁 <span>Select Photo from Device</span>
              </button>
            </div>

            <div class="slider-group">
              <label>Edge Sensitivity Cutoff: <span id="cutoffVal">40</span></label>
              <input type="range" id="edgeThresholdSlider" class="brush-slider" min="10" max="150" value="40">
            </div>

            <div class="slider-group">
              <label>Line Thickness / Weight: <span id="thickVal">1</span></label>
              <input type="range" id="thicknessSlider" class="brush-slider" min="0" max="3" value="1">
            </div>

            <div class="slider-group">
              <label>Contrast / Detail Boost: <span id="contrastVal">1.4x</span></label>
              <input type="range" id="contrastSlider" class="brush-slider" min="100" max="300" value="140">
            </div>

            <div style="display: flex; gap: 10px; margin-top: 16px;">
              <button class="btn-icon btn-accent" id="btnApplyDecolorize" style="flex: 1; justify-content: center;">
                🎨 Load into Studio
              </button>
              <button class="btn-icon" id="btnDownloadDecolorize" style="flex: 1; justify-content: center;">
                💾 Download Outline
              </button>
            </div>
          </div>

          <div class="decolorize-preview-box">
            <canvas id="decolorizePreviewCanvas" width="400" height="400"></canvas>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 4. "My Saved Art" Local Gallery Modal -->
  <div class="modal-overlay" id="galleryModal">
    <div class="modal-card">
      <div class="modal-header">
        <div class="modal-title">🖼️ My Saved Art Gallery</div>
        <button class="btn-icon" id="btnCloseGallery">✕</button>
      </div>
      <div class="modal-body">
        <div class="pages-grid" id="galleryGrid"></div>
      </div>
    </div>
  </div>

  <!-- 5. Parent Security & Travel Gate Modal -->
  <div class="modal-overlay" id="parentGateModal">
    <div class="modal-card" style="max-width: 500px;">
      <div class="modal-header">
        <div class="modal-title">👨‍👩‍👧 Parent Security & Travel Gate</div>
        <button class="btn-icon" id="btnCloseParentGate">✕</button>
      </div>
      <div class="modal-body">
        <div id="parentGateLockView">
          <p style="margin-bottom: 12px; color: var(--text-muted);">Please solve this math question to unlock parent controls:</p>
          <div style="font-size: 24px; font-weight: bold; margin-bottom: 16px; color: var(--neon-cyan);" id="parentMathPrompt">7 x 8 = ?</div>
          <input type="number" id="parentMathInput" class="btn-icon" style="width: 100%; font-size: 18px; padding: 12px; margin-bottom: 16px;" placeholder="Your Answer">
          <button class="btn-icon btn-accent" id="btnUnlockParentGate" style="width: 100%; justify-content: center; padding: 12px;">
            🔓 Unlock Settings
          </button>
        </div>

        <div id="parentSettingsView" style="display: none;">
          <h3 style="margin-bottom: 12px;">✈️ Flight Screen-Time Limiter</h3>
          <p style="font-size: 13px; color: var(--text-muted); margin-bottom: 16px;">Set a gentle rest reminder timer for long airplane flights.</p>

          <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 20px;">
            <button class="btn-icon screen-timer-btn" data-min="15">15 Minutes</button>
            <button class="btn-icon screen-timer-btn" data-min="30">30 Minutes</button>
            <button class="btn-icon screen-timer-btn" data-min="45">45 Minutes</button>
            <button class="btn-icon screen-timer-btn" data-min="60">60 Minutes</button>
          </div>

          <div style="margin-bottom: 20px;">
            <button class="btn-icon" id="btnCancelTimer" style="width: 100%; justify-content: center;">
              ❌ Disable Screen Timer
            </button>
          </div>

          <h3 style="margin-bottom: 12px;">🖨️ Batch Outline Printer</h3>
          <button class="btn-icon btn-accent" id="btnBatchPrint" style="width: 100%; justify-content: center; padding: 12px;">
            Print Current Page Outline (Clean Margins)
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- 6. Export Menu Modal -->
  <div class="modal-overlay" id="exportModal">
    <div class="modal-card" style="max-width: 520px;">
      <div class="modal-header">
        <div class="modal-title">💾 Download & Export</div>
        <button class="btn-icon" id="btnCloseExport">✕</button>
      </div>
      <div class="modal-body" style="display: flex; flex-direction: column; gap: 12px;">
        <button class="btn-icon btn-accent" id="btnDownloadColoredPNG" style="justify-content: center; padding: 14px;">
          🖼️ Download Colored Artwork (PNG)
        </button>
        <button class="btn-icon" id="btnDownloadOutlinePNG" style="justify-content: center; padding: 14px;">
          📄 Download Blank Line-Art (PNG)
        </button>
        <button class="btn-icon" id="btnPrintSheet" style="justify-content: center; padding: 14px;">
          🖨️ Print-Ready PDF / Sheet
        </button>
        <button class="btn-icon" id="btnSaveJSONProject" style="justify-content: center; padding: 14px;">
          📦 Save Project State (JSON)
        </button>
        <button class="btn-icon" id="btnLoadJSONProject" style="justify-content: center; padding: 14px;">
          📂 Load Project State (JSON)
        </button>
        <input type="file" id="jsonProjectInput" accept=".json" style="display: none;">
      </div>
    </div>
  </div>

  <!-- 7. Gentle Rest Screen Overlay (Screen-time limiter) -->
  <div class="rest-screen-overlay" id="restScreenOverlay" style="display: none;">
    <div style="font-size: 64px; margin-bottom: 16px;">🌙</div>
    <h2 class="rest-title">Time for a Gentle Rest!</h2>
    <p class="rest-desc">Great job creating art today! Look out the airplane window, stretch your hands, or take a little break.</p>
    <button class="btn-icon btn-accent" id="btnDismissRestScreen" style="font-size: 16px; padding: 14px 28px;">
      👨‍👩‍👧 Parent Unlock
    </button>
  </div>

  <!-- Confetti Canvas -->
  <canvas id="confettiCanvas"></canvas>

  <!-- Embedded WASM Payload for Offline file:// Support -->
  <script>
    window.WASM_BASE64_PAYLOAD = "%%WASM_BASE64%%";
  </script>

  <!-- Scripts -->
  <script src="audio-fx.js"></script>
  <script src="wasm-engine.js"></script>
  <script src="pages-data.js"></script>
  <script src="stickers-data.js"></script>
  <script src="app.js"></script>

  <!-- UI Glue & Interaction Wiring -->
  <script>
    document.addEventListener('DOMContentLoaded', () => {
      // Sound FX Toggle
      const soundBtn = document.getElementById('btnSoundFX');
      soundBtn.addEventListener('click', () => {
        const enabled = window.soundEngine.toggleSound();
        soundBtn.classList.toggle('active', enabled);
        soundBtn.querySelector('span').textContent = enabled ? 'Sound On' : 'Muted';
      });

      // Calm Travel Synth BGM Toggle
      const bgmBtn = document.getElementById('btnBGM');
      bgmBtn.addEventListener('click', () => {
        const enabled = window.soundEngine.toggleBGM();
        bgmBtn.classList.toggle('active', enabled);
        document.getElementById('bgmLabel').textContent = enabled ? 'BGM Playing' : 'BGM Off';
      });

      // Modal helpers
      const openModal = (id) => document.getElementById(id).classList.add('open');
      const closeModal = (id) => document.getElementById(id).classList.remove('open');

      // 120 Pages Library Modal
      const libraryModal = document.getElementById('libraryModal');
      document.getElementById('btnOpenLibrary').addEventListener('click', () => {
        populateLibrary();
        openModal('libraryModal');
      });
      document.getElementById('btnCloseLibrary').addEventListener('click', () => closeModal('libraryModal'));

      function populateLibrary() {
        const tabsContainer = document.getElementById('packTabsContainer');
        const grid = document.getElementById('pagesGrid');
        if (!tabsContainer || !grid) return;

        tabsContainer.innerHTML = '';
        let activePack = window.COLORING_PACKS[0].id;

        const renderPages = (packId) => {
          grid.innerHTML = '';
          const filtered = window.COLORING_PAGES.filter(p => p.packId === packId);
          filtered.forEach(page => {
            const card = document.createElement('div');
            card.className = 'page-card';
            card.innerHTML = `
              <div class="page-thumb">${page.svg}</div>
              <div class="page-info-title">${page.title}</div>
              <span class="page-badge">${page.difficulty}</span>
            `;
            card.addEventListener('click', () => {
              window.studio.loadPage(page);
              closeModal('libraryModal');
              if (window.soundEngine) window.soundEngine.playFanfare();
            });
            grid.appendChild(card);
          });
        };

        window.COLORING_PACKS.forEach((pack, idx) => {
          const tab = document.createElement('button');
          tab.className = `pack-tab ${idx === 0 ? 'active' : ''}`;
          tab.textContent = `${pack.icon} ${pack.name}`;
          tab.addEventListener('click', () => {
            tabsContainer.querySelectorAll('.pack-tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            renderPages(pack.id);
          });
          tabsContainer.appendChild(tab);
        });

        renderPages(activePack);
      }

      // 60 Magic Sticker Drawer Modal
      document.getElementById('btnStickerDrawer').addEventListener('click', () => {
        populateStickers();
        openModal('stickerModal');
      });
      document.getElementById('btnCloseStickers').addEventListener('click', () => closeModal('stickerModal'));

      function populateStickers() {
        const catTabs = document.getElementById('stickerCatTabs');
        const grid = document.getElementById('stickersGrid');
        if (!catTabs || !grid) return;

        catTabs.innerHTML = '';
        const categories = [
          { id: 'stars_magic', name: '⭐ Stars & Magic' },
          { id: 'cute_animals', name: '🐾 Cute Animals' },
          { id: 'yummy_snacks', name: '🍦 Yummy Snacks' },
          { id: 'toys_gadgets', name: '🚀 Toys & Gadgets' },
          { id: 'expressive_moods', name: '💖 Expressive Moods' },
          { id: 'dinos_nature', name: '🦖 Dinos & Nature' }
        ];

        const renderStickers = (catId) => {
          grid.innerHTML = '';
          const filtered = window.STICKERS_DATA.filter(s => s.category === catId);
          filtered.forEach(sticker => {
            const btn = document.createElement('button');
            btn.className = 'sticker-btn';
            btn.title = sticker.name;
            btn.innerHTML = sticker.svg;
            btn.addEventListener('click', () => {
              window.studio.currentTool = 'sticker';
              window.studio.selectedSticker = sticker;
              document.querySelectorAll('.tool-btn[data-tool]').forEach(b => b.classList.remove('active'));
              document.getElementById('btnStickerDrawer').classList.add('active');
              closeModal('stickerModal');
              if (window.soundEngine) window.soundEngine.playStickerChime();
            });
            grid.appendChild(btn);
          });
        };

        categories.forEach((cat, idx) => {
          const tab = document.createElement('button');
          tab.className = `pack-tab ${idx === 0 ? 'active' : ''}`;
          tab.textContent = cat.name;
          tab.addEventListener('click', () => {
            catTabs.querySelectorAll('.pack-tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            renderStickers(cat.id);
          });
          catTabs.appendChild(tab);
        });

        renderStickers(categories[0].id);
      }

      // WASM Decolorizer Photo Uploader
      const uploaderModal = document.getElementById('uploaderModal');
      const fileInput = document.getElementById('decolorizeFileInput');
      const prevCanvas = document.getElementById('decolorizePreviewCanvas');
      const prevCtx = prevCanvas.getContext('2d');
      let uploadedRawImage = null;
      let lastProcessedData = null;

      document.getElementById('btnOpenUploader').addEventListener('click', () => openModal('uploaderModal'));
      document.getElementById('btnCloseUploader').addEventListener('click', () => closeModal('uploaderModal'));
      document.getElementById('btnSelectPhoto').addEventListener('click', () => fileInput.click());

      fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (re) => {
          const img = new Image();
          img.onload = () => {
            uploadedRawImage = img;
            triggerDecolorize();
          };
          img.src = re.target.result;
        };
        reader.readAsDataURL(file);
      });

      const threshSlider = document.getElementById('edgeThresholdSlider');
      const thickSlider = document.getElementById('thicknessSlider');
      const contrastSlider = document.getElementById('contrastSlider');

      threshSlider.addEventListener('input', (e) => {
        document.getElementById('cutoffVal').textContent = e.target.value;
        triggerDecolorize();
      });
      thickSlider.addEventListener('input', (e) => {
        document.getElementById('thickVal').textContent = e.target.value;
        triggerDecolorize();
      });
      contrastSlider.addEventListener('input', (e) => {
        document.getElementById('contrastVal').textContent = (parseInt(e.target.value) / 100).toFixed(1) + 'x';
        triggerDecolorize();
      });

      async function triggerDecolorize() {
        if (!uploadedRawImage) return;
        const w = 400;
        const h = 400;
        prevCanvas.width = w;
        prevCanvas.height = h;

        prevCtx.drawImage(uploadedRawImage, 0, 0, w, h);
        const rawData = prevCtx.getImageData(0, 0, w, h);

        const options = {
          threshold: parseInt(threshSlider.value, 10),
          thickness: parseInt(thickSlider.value, 10),
          contrast: parseInt(contrastSlider.value, 10),
          invertMode: 0
        };

        const converted = await window.wasmEngine.processImage(rawData, options);
        lastProcessedData = converted;
        prevCtx.putImageData(converted, 0, 0);
      }

      document.getElementById('btnApplyDecolorize').addEventListener('click', () => {
        if (!lastProcessedData) return;
        window.studio.saveState();
        // Scale to studio canvas
        window.studio.ctx.drawImage(prevCanvas, 0, 0, window.studio.width, window.studio.height);
        document.getElementById('currentArtworkTitle').textContent = 'Custom Decolorized Photo';
        closeModal('uploaderModal');
        if (window.soundEngine) window.soundEngine.playFanfare();
      });

      document.getElementById('btnDownloadDecolorize').addEventListener('click', () => {
        if (!lastProcessedData) return;
        const a = document.createElement('a');
        a.download = 'decolorized_outline.png';
        a.href = prevCanvas.toDataURL('image/png');
        a.click();
      });

      // Quick Save to Gallery
      document.getElementById('btnQuickSave').addEventListener('click', () => {
        window.studio.saveToGallery();
      });

      // Gallery Modal
      document.getElementById('btnOpenGallery').addEventListener('click', () => {
        populateGallery();
        openModal('galleryModal');
      });
      document.getElementById('btnCloseGallery').addEventListener('click', () => closeModal('galleryModal'));

      function populateGallery() {
        const grid = document.getElementById('galleryGrid');
        if (!grid) return;
        grid.innerHTML = '';
        const savedArt = JSON.parse(localStorage.getItem('my_saved_art') || '[]');
        if (savedArt.length === 0) {
          grid.innerHTML = '<p style="color: var(--text-muted); grid-column: 1 / -1; text-align: center; padding: 40px;">No saved artwork yet! Create some drawings and click "Save to My Art"!</p>';
          return;
        }

        savedArt.forEach(art => {
          const card = document.createElement('div');
          card.className = 'page-card';
          card.innerHTML = `
            <div class="page-thumb"><img src="${art.dataUrl}" style="max-width: 100%; max-height: 100%; object-fit: contain;"></div>
            <div class="page-info-title">${art.title}</div>
            <span class="page-badge">${art.date}</span>
          `;
          card.addEventListener('click', () => {
            const img = new Image();
            img.onload = () => {
              window.studio.saveState();
              window.studio.ctx.drawImage(img, 0, 0, window.studio.width, window.studio.height);
              closeModal('galleryModal');
            };
            img.src = art.dataUrl;
          });
          grid.appendChild(card);
        });
      }

      // Parent Security & Travel Gate
      let parentMathAnswer = 0;
      function generateMathPrompt() {
        const a = Math.floor(Math.random() * 8) + 3;
        const b = Math.floor(Math.random() * 8) + 3;
        parentMathAnswer = a * b;
        document.getElementById('parentMathPrompt').textContent = `${a} × ${b} = ?`;
        document.getElementById('parentMathInput').value = '';
      }

      document.getElementById('btnParentGate').addEventListener('click', () => {
        generateMathPrompt();
        document.getElementById('parentGateLockView').style.display = 'block';
        document.getElementById('parentSettingsView').style.display = 'none';
        openModal('parentGateModal');
      });
      document.getElementById('btnCloseParentGate').addEventListener('click', () => closeModal('parentGateModal'));

      document.getElementById('btnUnlockParentGate').addEventListener('click', () => {
        const val = parseInt(document.getElementById('parentMathInput').value, 10);
        if (val === parentMathAnswer) {
          document.getElementById('parentGateLockView').style.display = 'none';
          document.getElementById('parentSettingsView').style.display = 'block';
        } else {
          alert('Incorrect answer. Please try again.');
          generateMathPrompt();
        }
      });

      // Screen-Time Timers
      document.querySelectorAll('.screen-timer-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          const min = parseInt(btn.dataset.min, 10);
          if (window.studio.screenTimeTimer) clearInterval(window.studio.screenTimeTimer);
          window.studio.timeRemainingSec = min * 60;
          window.studio.screenTimeTimer = setInterval(() => {
            window.studio.timeRemainingSec--;
            if (window.studio.timeRemainingSec <= 0) {
              clearInterval(window.studio.screenTimeTimer);
              document.getElementById('restScreenOverlay').style.display = 'flex';
            }
          }, 1000);
          alert(`Flight screen timer set for ${min} minutes!`);
          closeModal('parentGateModal');
        });
      });

      document.getElementById('btnCancelTimer').addEventListener('click', () => {
        if (window.studio.screenTimeTimer) {
          clearInterval(window.studio.screenTimeTimer);
          window.studio.screenTimeTimer = null;
        }
        alert('Screen time limit disabled.');
      });

      document.getElementById('btnDismissRestScreen').addEventListener('click', () => {
        document.getElementById('restScreenOverlay').style.display = 'none';
      });

      document.getElementById('btnBatchPrint').addEventListener('click', () => {
        window.studio.printOutline();
      });
      document.getElementById('btnPrintOutline').addEventListener('click', () => {
        window.studio.printOutline();
      });

      // Export Menu
      document.getElementById('btnExport').addEventListener('click', () => openModal('exportModal'));
      document.getElementById('btnCloseExport').addEventListener('click', () => closeModal('exportModal'));

      document.getElementById('btnDownloadColoredPNG').addEventListener('click', () => {
        window.studio.downloadPNG(false);
        closeModal('exportModal');
      });
      document.getElementById('btnDownloadOutlinePNG').addEventListener('click', () => {
        window.studio.downloadPNG(true);
        closeModal('exportModal');
      });
      document.getElementById('btnPrintSheet').addEventListener('click', () => {
        window.studio.printOutline();
        closeModal('exportModal');
      });

      // JSON Project Save & Load
      document.getElementById('btnSaveJSONProject').addEventListener('click', () => {
        const project = {
          version: '2.0-ULTRA',
          date: new Date().toISOString(),
          page: window.studio.currentPage,
          dataUrl: window.studio.canvas.toDataURL('image/png'),
          currentColor: window.studio.currentColor,
          currentPalette: window.studio.currentPaletteKey
        };
        const blob = new Blob([JSON.stringify(project, null, 2)], { type: 'application/json' });
        const a = document.createElement('a');
        a.download = 'coloring_project.json';
        a.href = URL.createObjectURL(blob);
        a.click();
        closeModal('exportModal');
      });

      const jsonFileInput = document.getElementById('jsonProjectInput');
      document.getElementById('btnLoadJSONProject').addEventListener('click', () => jsonFileInput.click());
      jsonFileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (re) => {
          try {
            const project = JSON.parse(re.target.result);
            if (project.page) {
              window.studio.currentPage = project.page;
              document.getElementById('currentArtworkTitle').textContent = project.page.title;
            }
            if (project.dataUrl) {
              const img = new Image();
              img.onload = () => {
                window.studio.saveState();
                window.studio.ctx.drawImage(img, 0, 0, window.studio.width, window.studio.height);
              };
              img.src = project.dataUrl;
            }
            if (project.currentColor) window.studio.setColor(project.currentColor);
            closeModal('exportModal');
          } catch (err) {
            alert('Failed to parse project file: ' + err.message);
          }
        };
        reader.readAsText(file);
      });

    });
  </script>
</body>
</html>
"""

output = template.replace('%%WASM_BASE64%%', wasm_b64)
with open('index.html', 'w') as f:
    f.write(output)

print("Generated index.html successfully.")
