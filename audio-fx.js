// Procedural Web Audio API Engine for Version 2 ULTRA
// Zero external mp3/wav files - 100% offline pure synthesized audio

class SoundEngine {
    constructor() {
        this.ctx = null;
        this.soundEnabled = true;
        this.bgmEnabled = false;
        this.bgmTimer = null;
        this.bgmGain = null;
    }

    init() {
        if (!this.ctx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (AudioContext) {
                this.ctx = new AudioContext();
            }
        }
        if (this.ctx && this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
    }

    toggleSound(enable) {
        this.soundEnabled = enable !== undefined ? enable : !this.soundEnabled;
        return this.soundEnabled;
    }

    toggleBGM(enable) {
        this.bgmEnabled = enable !== undefined ? enable : !this.bgmEnabled;
        if (this.bgmEnabled) {
            this.startBGM();
        } else {
            this.stopBGM();
        }
        return this.bgmEnabled;
    }

    // Bucket Pop - Clean bubble burst sound
    playBucketPop() {
        if (!this.soundEnabled) return;
        this.init();
        if (!this.ctx) return;

        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();

        osc.type = 'sine';
        // Upward pitch bend (bubble effect)
        osc.frequency.setValueAtTime(320, now);
        osc.frequency.exponentialRampToValueAtTime(780, now + 0.12);

        gain.gain.setValueAtTime(0.25, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.14);

        osc.connect(gain);
        gain.connect(this.ctx.destination);

        osc.start(now);
        osc.stop(now + 0.15);
    }

    // Brush Swoosh - Subtle airy stroke sound
    playBrushSwoosh() {
        if (!this.soundEnabled) return;
        this.init();
        if (!this.ctx) return;

        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();

        osc.type = 'triangle';
        osc.frequency.setValueAtTime(220, now);
        osc.frequency.exponentialRampToValueAtTime(140, now + 0.08);

        gain.gain.setValueAtTime(0.08, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.09);

        osc.connect(gain);
        gain.connect(this.ctx.destination);

        osc.start(now);
        osc.stop(now + 0.1);
    }

    // Sticker Chime - High crystalline double ping
    playStickerChime() {
        if (!this.soundEnabled) return;
        this.init();
        if (!this.ctx) return;

        const now = this.ctx.currentTime;
        const freqs = [880, 1320, 1760];

        freqs.forEach((freq, idx) => {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();

            osc.type = 'sine';
            const startTime = now + idx * 0.05;
            osc.frequency.setValueAtTime(freq, startTime);

            gain.gain.setValueAtTime(0.18, startTime);
            gain.gain.exponentialRampToValueAtTime(0.001, startTime + 0.35);

            osc.connect(gain);
            gain.connect(this.ctx.destination);

            osc.start(startTime);
            osc.stop(startTime + 0.36);
        });
    }

    // Fanfare Reward - Major triad celebratory arpeggio
    playFanfare() {
        if (!this.soundEnabled) return;
        this.init();
        if (!this.ctx) return;

        const now = this.ctx.currentTime;
        // C5, E5, G5, C6 triumphant chord progression
        const notes = [523.25, 659.25, 783.99, 1046.50];

        notes.forEach((freq, idx) => {
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();

            osc.type = 'triangle';
            const startTime = now + idx * 0.11;
            osc.frequency.setValueAtTime(freq, startTime);

            gain.gain.setValueAtTime(0.22, startTime);
            gain.gain.exponentialRampToValueAtTime(0.001, startTime + (idx === notes.length - 1 ? 0.8 : 0.4));

            osc.connect(gain);
            gain.connect(this.ctx.destination);

            osc.start(startTime);
            osc.stop(startTime + (idx === notes.length - 1 ? 0.85 : 0.45));
        });
    }

    // Calm Travel Synth BGM Chords (Ambient Pentatonic Loop)
    startBGM() {
        this.init();
        if (!this.ctx) return;
        if (this.bgmTimer) clearInterval(this.bgmTimer);

        // Pentatonic chords (frequencies in Hz): Fmaj9, Cmaj7, Am9, Gsus4
        const chordProgression = [
            [174.61, 261.63, 329.63, 392.00], // F3, C4, E4, G4
            [130.81, 196.00, 246.94, 329.63], // C3, G3, B3, E4
            [110.00, 164.81, 220.00, 261.63], // A2, E3, A3, C4
            [98.00, 146.83, 196.00, 293.66]   // G2, D3, G3, D4
        ];

        let chordIndex = 0;

        const playChord = () => {
            if (!this.bgmEnabled || !this.ctx) return;
            const now = this.ctx.currentTime;
            const chord = chordProgression[chordIndex % chordProgression.length];
            chordIndex++;

            chord.forEach(freq => {
                const osc = this.ctx.createOscillator();
                const filter = this.ctx.createBiquadFilter();
                const gain = this.ctx.createGain();

                osc.type = 'sine';
                osc.frequency.setValueAtTime(freq, now);

                // Low-pass warmth
                filter.type = 'lowpass';
                filter.frequency.setValueAtTime(600, now);

                // Soft fade-in and slow release (4 seconds)
                gain.gain.setValueAtTime(0.0001, now);
                gain.gain.linearRampToValueAtTime(0.035, now + 1.2);
                gain.gain.exponentialRampToValueAtTime(0.0001, now + 4.2);

                osc.connect(filter);
                filter.connect(gain);
                gain.connect(this.ctx.destination);

                osc.start(now);
                osc.stop(now + 4.3);
            });
        };

        playChord();
        this.bgmTimer = setInterval(playChord, 4500);
    }

    stopBGM() {
        if (this.bgmTimer) {
            clearInterval(this.bgmTimer);
            this.bgmTimer = null;
        }
    }
}

// Global Sound Engine instance
window.soundEngine = new SoundEngine();
