// Sliver Kids WASM Coloring Studio v2 ULTRA - Procedural Web Audio FX & Calm Travel Synth BGM
// Pure offline procedural synthesizer with zero external audio files.

class ProceduralAudioEngine {
  constructor() {
    this.ctx = null;
    this.bgmPlaying = false;
    this.bgmOscillators = [];
    this.bgmGain = null;
    this.muted = false;
  }

  ensureContext() {
    if (!this.ctx) {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if (AudioContextClass) {
        this.ctx = new AudioContextClass();
      }
    }
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
    return this.ctx;
  }

  // Pop Sound (Bucket Fill)
  playBucketPop() {
    if (this.muted) return;
    const ctx = this.ensureContext();
    if (!ctx) return;

    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = 'sine';
    const now = ctx.currentTime;
    osc.frequency.setValueAtTime(260, now);
    osc.frequency.exponentialRampToValueAtTime(780, now + 0.08);

    gain.gain.setValueAtTime(0.25, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.12);

    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.start(now);
    osc.stop(now + 0.12);
  }

  // Magic Sticker Chime
  playStickerChime() {
    if (this.muted) return;
    const ctx = this.ensureContext();
    if (!ctx) return;

    const notes = [523.25, 659.25, 783.99, 1046.50]; // C5, E5, G5, C6 arpeggio
    notes.forEach((freq, idx) => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = 'triangle';
      const start = ctx.currentTime + idx * 0.045;
      osc.frequency.setValueAtTime(freq, start);

      gain.gain.setValueAtTime(0.18, start);
      gain.gain.exponentialRampToValueAtTime(0.001, start + 0.25);

      osc.connect(gain);
      gain.connect(ctx.destination);

      osc.start(start);
      osc.stop(start + 0.25);
    });
  }

  // Brush Swoosh Sound
  playBrushSwoosh() {
    if (this.muted) return;
    const ctx = this.ensureContext();
    if (!ctx) return;

    // Filtered noise swoosh
    const bufferSize = ctx.sampleRate * 0.08;
    const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) {
      data[i] = Math.random() * 2 - 1;
    }

    const noise = ctx.createBufferSource();
    noise.buffer = buffer;

    const filter = ctx.createBiquadFilter();
    filter.type = 'bandpass';
    filter.frequency.setValueAtTime(800, ctx.currentTime);
    filter.Q.setValueAtTime(3.0, ctx.currentTime);

    const gain = ctx.createGain();
    const now = ctx.currentTime;
    gain.gain.setValueAtTime(0.08, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);

    noise.connect(filter);
    filter.connect(gain);
    gain.connect(ctx.destination);

    noise.start(now);
  }

  // Fanfare Reward Chord (Celebration & Confetti)
  playFanfare() {
    if (this.muted) return;
    const ctx = this.ensureContext();
    if (!ctx) return;

    // Major Triad with Octaves (C4, G4, C5, E5, G5, C6)
    const chord = [261.63, 392.00, 523.25, 659.25, 783.99, 1046.50];
    chord.forEach((freq, i) => {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();

      osc.type = 'sine';
      const now = ctx.currentTime + i * 0.03;
      osc.frequency.setValueAtTime(freq, now);

      gain.gain.setValueAtTime(0.15, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 1.2);

      osc.connect(gain);
      gain.connect(ctx.destination);

      osc.start(now);
      osc.stop(now + 1.2);
    });
  }

  // Calm Travel Synth BGM (Relaxing Flight Chords)
  toggleTravelBgm() {
    if (this.bgmPlaying) {
      this.stopTravelBgm();
      return false;
    } else {
      this.startTravelBgm();
      return true;
    }
  }

  startTravelBgm() {
    const ctx = this.ensureContext();
    if (!ctx) return;

    this.stopTravelBgm();

    const masterGain = ctx.createGain();
    masterGain.gain.setValueAtTime(0.06, ctx.currentTime);
    masterGain.connect(ctx.destination);
    this.bgmGain = masterGain;

    // Solfeggio / Ambient calming drone: 432Hz root, 528Hz love, 288Hz harmonic
    const freqs = [216.0, 288.0, 324.0, 432.0, 528.0];
    this.bgmOscillators = freqs.map((f, i) => {
      const osc = ctx.createOscillator();
      const subGain = ctx.createGain();

      osc.type = i % 2 === 0 ? 'sine' : 'triangle';
      osc.frequency.setValueAtTime(f, ctx.currentTime);

      // Low Frequency Oscillator for subtle gentle breathing pulse
      const lfo = ctx.createOscillator();
      const lfoGain = ctx.createGain();
      lfo.frequency.setValueAtTime(0.15 + i * 0.05, ctx.currentTime);
      lfoGain.gain.setValueAtTime(0.02, ctx.currentTime);

      lfo.connect(subGain.gain);
      subGain.gain.setValueAtTime(0.04, ctx.currentTime);

      osc.connect(subGain);
      subGain.connect(masterGain);

      lfo.start();
      osc.start();

      return { osc, lfo };
    });

    this.bgmPlaying = true;
  }

  stopTravelBgm() {
    if (this.bgmOscillators && this.bgmOscillators.length) {
      this.bgmOscillators.forEach(({ osc, lfo }) => {
        try {
          osc.stop();
          lfo.stop();
        } catch (e) {}
      });
      this.bgmOscillators = [];
    }
    this.bgmPlaying = false;
  }
}

export const proceduralAudio = new ProceduralAudioEngine();
if (typeof window !== 'undefined') {
  window.ProceduralAudio = proceduralAudio;
}
