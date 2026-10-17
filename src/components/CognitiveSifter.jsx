import React, { useState, useCallback } from 'react';

export function CognitiveSifter({ rawInput, onSiftComplete, isProcessing, onClear, onDemoLoad }) {
  const [dragActive, setDragActive] = useState(false);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setDragActive(false);

    if (e.dataTransfer.files?.[0]) {
      const reader = new FileReader();
      reader.onload = (event) => onSiftComplete(event.target?.result || '');
      reader.readAsText(e.dataTransfer.files[0]);
    }
  }, [onSiftComplete]);

  return (
    <div
      onDragEnter={() => setDragActive(true)}
      onDragOver={(e) => e.preventDefault()}
      onDragLeave={() => setDragActive(false)}
      onDrop={handleDrop}
      className={`p-6 border border-dashed rounded-xl transition-all bg-zinc-950/60 ${
        dragActive ? 'border-emerald-400 bg-emerald-950/20' : 'border-zinc-800'
      }`}
    >
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xs font-bold uppercase tracking-widest text-emerald-400 flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          Document Ingestion Gateway
        </h3>
        <div className="flex gap-2">
          {onDemoLoad && (
            <button
              type="button"
              onClick={onDemoLoad}
              className="text-[10px] uppercase font-mono px-2 py-1 bg-zinc-900 hover:bg-zinc-800 text-zinc-300 border border-zinc-800 rounded transition-all"
            >
              Load Demo Manifesto
            </button>
          )}
          {onClear && (
            <button
              type="button"
              onClick={onClear}
              className="text-[10px] uppercase font-mono px-2 py-1 bg-zinc-900 hover:bg-zinc-800 text-zinc-400 border border-zinc-800 rounded transition-all"
            >
              Clear
            </button>
          )}
        </div>
      </div>

      <textarea
        value={rawInput}
        onChange={(e) => onSiftComplete(e.target.value)}
        placeholder="Paste raw text or drag and drop manifesto files here..."
        disabled={isProcessing}
        className="w-full h-44 bg-zinc-900/80 border border-zinc-800 rounded-lg p-3 text-xs font-mono text-zinc-200 resize-none focus:outline-none focus:border-emerald-500/50 transition-colors"
      />

      <div className="mt-2 flex items-center justify-between text-[10px] text-zinc-500 font-mono">
        <span>Characters: {rawInput.length}</span>
        <span>Drag & Drop plain text file (.txt, .md, .json)</span>
      </div>
    </div>
  );
}
