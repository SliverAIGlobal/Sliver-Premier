export class AudioEngine {
  private context: AudioContext | null = null;
  private oscillators: OscillatorNode[] = [];
  private gainNode: GainNode | null = null;

  async init(): Promise<void> {
    if (this.context || typeof window === 'undefined') return;

    const AudioContextClass = window.AudioContext || (window as any).webkitAudioContext;
    if (!AudioContextClass) return;

    this.context = new AudioContextClass();
    this.gainNode = this.context.createGain();
    this.gainNode.gain.setValueAtTime(0.05, this.context.currentTime);
    this.gainNode.connect(this.context.destination);

    // Create 3 harmonic oscillators
    this.oscillators = [1, 2, 3].map(() => {
      const osc = this.context!.createOscillator();
      osc.connect(this.gainNode!);
      osc.start();
      return osc;
    });
  }

  playHarmonic(integrity: number): void {
    if (!this.context || !this.gainNode) return;

    const frequencies = integrity < 86.5
      ? [207, 246, 293] // Turbulent minor triad
      : [216, 270, 324]; // Laminar major triad

    const t = this.context.currentTime;
    this.oscillators.forEach((osc, idx) => {
      osc.frequency.setTargetAtTime(frequencies[idx], t, 0.3);
    });
  }

  destroy(): void {
    this.oscillators.forEach(osc => {
      try { osc.stop(); osc.disconnect(); } catch {}
    });
    if (this.context) {
      this.context.close();
      this.context = null;
    }
  }
}

export const audioEngine = new AudioEngine();
