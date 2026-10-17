import React, { useState } from 'react';

export function OutboundPitch({ selectedElement, onGenerate, isLoading }) {
  const [tone, setTone] = useState('Assertive & Premium');
  const [output, setOutput] = useState('');
  const [copied, setCopied] = useState(false);

  const handleGenerate = () => {
    if (onGenerate) {
      onGenerate(tone, setOutput);
    }
  };

  const handleCopy = () => {
    if (output) {
      navigator.clipboard.writeText(output);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="bg-zinc-950 border border-zinc-900 p-6 rounded-xl flex flex-col justify-between">
      <div>
        <h3 className="text-xs font-bold uppercase tracking-widest text-violet-400 mb-4 flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-violet-500 animate-pulse"></span>
          Outbound Pitch Synthesizer
        </h3>

        {selectedElement && (
          <div className="mb-4 p-2.5 bg-zinc-900/60 border border-zinc-800 rounded text-xs font-mono">
            <span className="text-zinc-500 block text-[9px] uppercase">Target Anchor</span>
            <span className="text-violet-300 font-semibold">{selectedElement.type}: {selectedElement.value}</span>
          </div>
        )}

        <div className="mb-4">
          <label className="block text-[10px] text-zinc-500 uppercase font-mono mb-1">Tone Vector</label>
          <select
            value={tone}
            onChange={(e) => setTone(e.target.value)}
            className="w-full bg-zinc-900 border border-zinc-800 p-2 rounded text-xs text-zinc-200 font-mono focus:outline-none focus:border-violet-500/50"
          >
            <option>Assertive & Premium</option>
            <option>GAAP Auditable Compliance</option>
            <option>Operational Speedup & ROI</option>
          </select>
        </div>

        <button
          type="button"
          onClick={handleGenerate}
          disabled={isLoading || !selectedElement}
          className="w-full py-2.5 bg-violet-600 hover:bg-violet-500 active:bg-violet-700 text-white font-bold rounded-lg text-xs font-mono transition-all disabled:opacity-30 disabled:pointer-events-none"
        >
          {isLoading ? 'Synthesizing Pitch Vector...' : 'Synthesize Value Hook'}
        </button>
      </div>

      {output && (
        <div className="mt-4 p-4 bg-zinc-900/80 border border-zinc-800 rounded text-xs font-mono">
          <p className="text-violet-200 whitespace-pre-wrap leading-relaxed">{output}</p>
          <div className="mt-3 flex items-center justify-between pt-2 border-t border-zinc-800">
            <span className="text-[9px] text-zinc-500 italic">Demo asset — verify compliance before dispatch.</span>
            <button
              type="button"
              onClick={handleCopy}
              className="text-violet-400 hover:text-violet-300 underline text-[10px] font-mono transition-colors"
            >
              {copied ? 'Copied to Clipboard!' : 'Copy Pitch'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
