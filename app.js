// Version 2 ULTRA Core Studio & Canvas Handler
// High-performance HTML5 Canvas coloring, flood fill, sticker stamping, undo/redo, and gallery

class ColoringStudio {
    constructor() {
        this.canvas = document.getElementById('mainCanvas');
        this.ctx = this.canvas.getContext('2d', { willReadFrequently: true });

        // Resolution of coloring pages
        this.width = 1200;
        this.height = 1200;
        this.canvas.width = this.width;
        this.canvas.height = this.height;

        // Tool state
        this.currentTool = 'bucket'; // 'brush', 'bucket', 'rainbow', 'glow', 'eraser', 'sticker'
        this.currentColor = '#FF3D00';
        this.brushSize = 18;
        this.rainbowHue = 0;
        this.isDrawing = false;
        this.lastX = 0;
        this.lastY = 0;

        // History buffer (Undo / Redo)
        this.undoStack = [];
        this.redoStack = [];
        this.maxHistory = 15;

        // Current page and sticker
        this.currentPage = null;
        this.selectedSticker = null;

        // 5 Custom Color Swatch Palettes (50 Colors Total)
        this.palettes = {
            "rainbow": {
                name: "Rainbow Brights",
                colors: ["#FF0000", "#FF5722", "#FF9800", "#FFEB3B", "#76FF03", "#00E676", "#00E5FF", "#2979FF", "#651FFF", "#D500F9"]
            },
            "pastel": {
                name: "Soft Pastels",
                colors: ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF", "#E8BAFF", "#FFC6FF", "#BDB2FF", "#A0C4FF", "#9BF6FF"]
            },
            "cyber": {
                name: "Cyber Neon",
                colors: ["#00F0FF", "#FF007F", "#00FF88", "#FFE600", "#B026FF", "#FF3366", "#33FFCC", "#FF9900", "#7B2CBF", "#FFFFFF"]
            },
            "island": {
                name: "808 Island Tones",
                colors: ["#006994", "#138808", "#FF8C00", "#FFD700", "#E32636", "#40E0D0", "#DEB887", "#8B4513", "#2E8B57", "#20B2AA"]
            },
            "metallic": {
                name: "Metallic Gold/Silver",
                colors: ["#D4AF37", "#FFD700", "#C5A059", "#E5E4E2", "#C0C0C0", "#A8A8A8", "#8A9A5B", "#B87333", "#E6C280", "#4A4A4A"]
            }
        };
        this.currentPaletteKey = "rainbow";

        // Screen time timer
        this.screenTimeMinutes = 0;
        this.screenTimeTimer = null;
        this.timeRemainingSec = 0;

        this.initEventListeners();
        this.renderPalettes();
        this.initFirstPage();
    }

    saveState() {
        if (this.undoStack.length >= this.maxHistory) {
            this.undoStack.shift();
        }
        const imgData = this.ctx.getImageData(0, 0, this.width, this.height);
        this.undoStack.push(imgData);
        this.redoStack = []; // Clear redo
    }

    undo() {
        if (this.undoStack.length > 0) {
            const currentImg = this.ctx.getImageData(0, 0, this.width, this.height);
            this.redoStack.push(currentImg);
            const prevImg = this.undoStack.pop();
            this.ctx.putImageData(prevImg, 0, 0);
            if (window.soundEngine) window.soundEngine.playBrushSwoosh();
        }
    }

    redo() {
        if (this.redoStack.length > 0) {
            const currentImg = this.ctx.getImageData(0, 0, this.width, this.height);
            this.undoStack.push(currentImg);
            const nextImg = this.redoStack.pop();
            this.ctx.putImageData(nextImg, 0, 0);
            if (window.soundEngine) window.soundEngine.playBrushSwoosh();
        }
    }

    initFirstPage() {
        if (window.COLORING_PAGES && window.COLORING_PAGES.length > 0) {
            this.loadPage(window.COLORING_PAGES[0]);
        }
    }

    loadPage(page) {
        this.currentPage = page;
        const img = new Image();
        const svgBlob = new Blob([page.svg], { type: 'image/svg+xml;charset=utf-8' });
        const url = URL.createObjectURL(svgBlob);

        img.onload = () => {
            this.ctx.fillStyle = "#ffffff";
            this.ctx.fillRect(0, 0, this.width, this.height);
            this.ctx.drawImage(img, 0, 0, this.width, this.height);
            URL.revokeObjectURL(url);
            this.undoStack = [];
            this.redoStack = [];
            document.getElementById('currentArtworkTitle').textContent = page.title;
        };
        img.src = url;
    }

    renderPalettes() {
        const tabsContainer = document.getElementById('paletteTabs');
        const swatchesContainer = document.getElementById('swatchesGrid');
        if (!tabsContainer || !swatchesContainer) return;

        tabsContainer.innerHTML = '';
        Object.keys(this.palettes).forEach(key => {
            const pal = this.palettes[key];
            const btn = document.createElement('button');
            btn.className = `palette-tab-btn ${key === this.currentPaletteKey ? 'active' : ''}`;
            btn.textContent = pal.name;
            btn.addEventListener('click', () => {
                this.currentPaletteKey = key;
                this.renderPalettes();
            });
            tabsContainer.appendChild(btn);
        });

        swatchesContainer.innerHTML = '';
        const currentPal = this.palettes[this.currentPaletteKey];
        currentPal.colors.forEach(color => {
            const swatch = document.createElement('div');
            swatch.className = `swatch-item ${color.toLowerCase() === this.currentColor.toLowerCase() ? 'active' : ''}`;
            swatch.style.backgroundColor = color;
            swatch.addEventListener('click', () => {
                this.setColor(color);
                this.renderPalettes();
            });
            swatchesContainer.appendChild(swatch);
        });
    }

    setColor(color) {
        this.currentColor = color;
        const colorPreview = document.getElementById('activeColorDisplay');
        if (colorPreview) colorPreview.style.backgroundColor = color;
    }

    getCanvasCoordinates(e) {
        const rect = this.canvas.getBoundingClientRect();
        const scaleX = this.width / rect.width;
        const scaleY = this.height / rect.height;
        return {
            x: Math.floor((e.clientX - rect.left) * scaleX),
            y: Math.floor((e.clientY - rect.top) * scaleY)
        };
    }

    initEventListeners() {
        const handleStart = (clientX, clientY) => {
            const rect = this.canvas.getBoundingClientRect();
            const x = Math.floor((clientX - rect.left) * (this.width / rect.width));
            const y = Math.floor((clientY - rect.top) * (this.height / rect.height));

            if (this.currentTool === 'bucket') {
                this.saveState();
                this.floodFill(x, y, this.currentColor);
                if (window.soundEngine) window.soundEngine.playBucketPop();
            } else if (this.currentTool === 'sticker') {
                if (this.selectedSticker) {
                    this.saveState();
                    this.stampSticker(x, y, this.selectedSticker);
                    if (window.soundEngine) window.soundEngine.playStickerChime();
                }
            } else {
                this.saveState();
                this.isDrawing = true;
                this.lastX = x;
                this.lastY = y;
                this.drawStroke(x, y, false);
                if (window.soundEngine) window.soundEngine.playBrushSwoosh();
            }
        };

        const handleMove = (clientX, clientY) => {
            if (!this.isDrawing) return;
            const rect = this.canvas.getBoundingClientRect();
            const x = Math.floor((clientX - rect.left) * (this.width / rect.width));
            const y = Math.floor((clientY - rect.top) * (this.height / rect.height));
            this.drawStroke(x, y, true);
        };

        const handleEnd = () => {
            this.isDrawing = false;
        };

        // Mouse events
        this.canvas.addEventListener('mousedown', (e) => handleStart(e.clientX, e.clientY));
        window.addEventListener('mousemove', (e) => handleMove(e.clientX, e.clientY));
        window.addEventListener('mouseup', handleEnd);

        // Touch events
        this.canvas.addEventListener('touchstart', (e) => {
            e.preventDefault();
            if (e.touches.length > 0) {
                handleStart(e.touches[0].clientX, e.touches[0].clientY);
            }
        }, { passive: false });

        window.addEventListener('touchmove', (e) => {
            if (!this.isDrawing) return;
            e.preventDefault();
            if (e.touches.length > 0) {
                handleMove(e.touches[0].clientX, e.touches[0].clientY);
            }
        }, { passive: false });

        window.addEventListener('touchend', handleEnd);

        // Tool buttons
        document.querySelectorAll('.tool-btn[data-tool]').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.tool-btn[data-tool]').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                this.currentTool = btn.dataset.tool;
            });
        });

        // Brush slider
        const brushSlider = document.getElementById('brushSizeSlider');
        if (brushSlider) {
            brushSlider.addEventListener('input', (e) => {
                this.brushSize = parseInt(e.target.value, 10);
                document.getElementById('brushSizeLabel').textContent = `${this.brushSize}px`;
            });
        }

        // Undo & Redo buttons
        const undoBtn = document.getElementById('btnUndo');
        if (undoBtn) undoBtn.addEventListener('click', () => this.undo());
        const redoBtn = document.getElementById('btnRedo');
        if (redoBtn) redoBtn.addEventListener('click', () => this.redo());

        // Clear Canvas
        const clearBtn = document.getElementById('btnClear');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => {
                if (this.currentPage) {
                    this.saveState();
                    this.loadPage(this.currentPage);
                }
            });
        }
    }

    drawStroke(x, y, isMove) {
        this.ctx.beginPath();
        this.ctx.lineCap = 'round';
        this.ctx.lineJoin = 'round';

        if (this.currentTool === 'eraser') {
            this.ctx.strokeStyle = '#ffffff';
            this.ctx.lineWidth = this.brushSize * 1.5;
            this.ctx.shadowBlur = 0;
        } else if (this.currentTool === 'rainbow') {
            this.rainbowHue = (this.rainbowHue + 4) % 360;
            this.ctx.strokeStyle = `hsl(${this.rainbowHue}, 100%, 50%)`;
            this.ctx.lineWidth = this.brushSize;
            this.ctx.shadowBlur = 0;
        } else if (this.currentTool === 'glow') {
            this.ctx.strokeStyle = this.currentColor;
            this.ctx.lineWidth = this.brushSize;
            this.ctx.shadowColor = this.currentColor;
            this.ctx.shadowBlur = 18;
        } else {
            // Standard brush
            this.ctx.strokeStyle = this.currentColor;
            this.ctx.lineWidth = this.brushSize;
            this.ctx.shadowBlur = 0;
        }

        if (isMove) {
            this.ctx.moveTo(this.lastX, this.lastY);
            this.ctx.lineTo(x, y);
            this.ctx.stroke();
        } else {
            this.ctx.arc(x, y, this.ctx.lineWidth / 2, 0, Math.PI * 2);
            this.ctx.fillStyle = this.ctx.strokeStyle;
            this.ctx.fill();
        }

        this.lastX = x;
        this.lastY = y;
    }

    stampSticker(x, y, sticker) {
        const img = new Image();
        const svgBlob = new Blob([sticker.svg], { type: 'image/svg+xml;charset=utf-8' });
        const url = URL.createObjectURL(svgBlob);
        const stampSize = this.brushSize * 4;

        img.onload = () => {
            this.ctx.drawImage(img, x - stampSize / 2, y - stampSize / 2, stampSize, stampSize);
            URL.revokeObjectURL(url);
        };
        img.src = url;
    }

    // High-Speed WASM / Breadth-First Flood Fill
    floodFill(startX, startY, fillHex) {
        const imgData = this.ctx.getImageData(0, 0, this.width, this.height);
        const data = imgData.data;

        // Convert target hex to RGB
        const fillR = parseInt(fillHex.slice(1, 3), 16);
        const fillG = parseInt(fillHex.slice(3, 5), 16);
        const fillB = parseInt(fillHex.slice(5, 7), 16);

        const startIndex = (startY * this.width + startX) * 4;
        const targetR = data[startIndex];
        const targetG = data[startIndex + 1];
        const targetB = data[startIndex + 2];

        // Do not fill if target is identical or if target is dark outline
        if (Math.abs(targetR - fillR) < 8 && Math.abs(targetG - fillG) < 8 && Math.abs(targetB - fillB) < 8) {
            return;
        }

        // Outline protection: black/very dark border threshold
        if (targetR < 40 && targetG < 40 && targetB < 40) {
            return;
        }

        const tolerance = 48;
        const match = (idx) => {
            const r = data[idx];
            const g = data[idx + 1];
            const b = data[idx + 2];
            return (
                Math.abs(r - targetR) <= tolerance &&
                Math.abs(g - targetG) <= tolerance &&
                Math.abs(b - targetB) <= tolerance
            );
        };

        const queue = [startX, startY];
        const visited = new Uint8Array(this.width * this.height);
        visited[startY * this.width + startX] = 1;

        let head = 0;
        while (head < queue.length) {
            const x = queue[head++];
            const y = queue[head++];
            const curIdx = (y * this.width + x) * 4;

            data[curIdx] = fillR;
            data[curIdx + 1] = fillG;
            data[curIdx + 2] = fillB;
            data[curIdx + 3] = 255;

            // 4-way neighbors
            const neighbors = [
                x + 1, y,
                x - 1, y,
                x, y + 1,
                x, y - 1
            ];

            for (let i = 0; i < neighbors.length; i += 2) {
                const nx = neighbors[i];
                const ny = neighbors[i + 1];

                if (nx >= 0 && nx < this.width && ny >= 0 && ny < this.height) {
                    const pos = ny * this.width + nx;
                    if (!visited[pos]) {
                        visited[pos] = 1;
                        const nIdx = pos * 4;
                        if (match(nIdx)) {
                            queue.push(nx, ny);
                        }
                    }
                }
            }
        }

        this.ctx.putImageData(imgData, 0, 0);
    }

    // Save to Local Gallery
    saveToGallery() {
        const thumbUrl = this.canvas.toDataURL('image/jpeg', 0.85);
        const savedArt = JSON.parse(localStorage.getItem('my_saved_art') || '[]');
        savedArt.unshift({
            id: 'art_' + Date.now(),
            title: this.currentPage ? this.currentPage.title : 'My Masterpiece',
            date: new Date().toLocaleDateString(),
            dataUrl: thumbUrl
        });
        localStorage.setItem('my_saved_art', JSON.stringify(savedArt.slice(0, 30)));
        this.triggerConfetti();
        if (window.soundEngine) window.soundEngine.playFanfare();
    }

    // Confetti Burst Animation
    triggerConfetti() {
        const cCanvas = document.getElementById('confettiCanvas');
        if (!cCanvas) return;
        const cCtx = cCanvas.getContext('2d');
        cCanvas.width = window.innerWidth;
        cCanvas.height = window.innerHeight;

        const particles = [];
        const colors = ['#00F0FF', '#FF007F', '#00FF88', '#FFEA00', '#B026FF', '#FF9900'];

        for (let i = 0; i < 90; i++) {
            particles.push({
                x: cCanvas.width / 2,
                y: cCanvas.height / 2,
                vx: (Math.random() - 0.5) * 16,
                vy: (Math.random() - 0.5) * 16 - 4,
                size: Math.random() * 8 + 4,
                color: colors[Math.floor(Math.random() * colors.length)],
                alpha: 1
            });
        }

        let animFrame;
        const renderConfetti = () => {
            cCtx.clearRect(0, 0, cCanvas.width, cCanvas.height);
            let active = false;
            particles.forEach(p => {
                p.x += p.vx;
                p.y += p.vy;
                p.vy += 0.3; // gravity
                p.alpha -= 0.015;
                if (p.alpha > 0) {
                    active = true;
                    cCtx.fillStyle = p.color;
                    cCtx.globalAlpha = p.alpha;
                    cCtx.fillRect(p.x, p.y, p.size, p.size);
                }
            });
            cCtx.globalAlpha = 1;
            if (active) {
                animFrame = requestAnimationFrame(renderConfetti);
            } else {
                cancelAnimationFrame(animFrame);
                cCtx.clearRect(0, 0, cCanvas.width, cCanvas.height);
            }
        };
        renderConfetti();
    }

    // Export formats
    downloadPNG(outlineOnly = false) {
        if (outlineOnly && this.currentPage) {
            // Render clean black & white line-art to separate offscreen canvas
            const off = document.createElement('canvas');
            off.width = this.width;
            off.height = this.height;
            const offCtx = off.getContext('2d');
            const img = new Image();
            const svgBlob = new Blob([this.currentPage.svg], { type: 'image/svg+xml;charset=utf-8' });
            const url = URL.createObjectURL(svgBlob);
            img.onload = () => {
                offCtx.fillStyle = "#ffffff";
                offCtx.fillRect(0, 0, this.width, this.height);
                offCtx.drawImage(img, 0, 0, this.width, this.height);
                URL.revokeObjectURL(url);
                const a = document.createElement('a');
                a.download = `${this.currentPage.id}_outline.png`;
                a.href = off.toDataURL('image/png');
                a.click();
            };
            img.src = url;
        } else {
            const a = document.createElement('a');
            a.download = `${this.currentPage ? this.currentPage.id : 'artwork'}_colored.png`;
            a.href = this.canvas.toDataURL('image/png');
            a.click();
        }
    }

    // Print Outline
    printOutline() {
        const printWindow = window.open('', '_blank');
        const imgData = this.canvas.toDataURL('image/png');
        printWindow.document.write(`
            <html>
            <head>
              <title>${this.currentPage ? this.currentPage.title : 'Coloring Sheet'}</title>
              <style>
                @page { size: auto; margin: 15mm; }
                body { margin: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; font-family: sans-serif; }
                h1 { margin-bottom: 8px; font-size: 22px; }
                img { max-width: 95vw; max-height: 85vh; object-fit: contain; }
              </style>
            </head>
            <body>
              <h1>${this.currentPage ? this.currentPage.title : 'Coloring Page'}</h1>
              <img src="${imgData}" />
              <script>
                window.onload = function() { window.print(); window.close(); };
              <\/script>
            </body>
            </html>
        `);
        printWindow.document.close();
    }
}

// Global App Initialization
window.addEventListener('DOMContentLoaded', () => {
    window.studio = new ColoringStudio();
});
