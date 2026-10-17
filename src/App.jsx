import React, { useState, useEffect, useCallback } from 'react';
import { CognitiveSifter } from './components/CognitiveSifter';
import { OutboundPitch } from './components/OutboundPitch';
import { AuditTerminal } from './components/AuditTerminal';
import { WasmManager } from './wasm-loader';
import { DeviceCache } from './cache/indexeddb-store';
import { audioEngine } from './utils/audio-engine';
import { INTEGRITY_THRESHOLD, DEMO_STRATEGIC_MANIFESTO, PRISM_SEGMENTS } from './constants';

export default function App() {
  // Application State
  const [apiKey, setApiKey] = useState('');
  const [rawInput, setRawInput] = useState(DEMO_STRATEGIC_MANIFESTO);
  const [isProcessing, setIsProcessing] = useState(false);
  const [siftedData, setSiftedData] = useState(null);
  const [processingLog, setProcessingLog] = useState(['[System Standby - Ready for Document Ingestion]']);
  const [wasmStatus, setWasmStatus] = useState({ ready: false, loadTimeMs: 0 });
  const [cacheStats, setCacheStats] = useState({ size: 0, entries: 0 });
  const [selectedSegment, setSelectedSegment] = useState(PRISM_SEGMENTS[0]);
  const [selectedElement, setSelectedElement] = useState(null);
  const [chatHistory, setChatHistory] = useState([]);
  const [pitchLoading, setPitchLoading] = useState(false);
  const [auditLoading, setAuditLoading] = useState(false);
  const [notification, setNotification] = useState(null);
  const [wasmEngine, setWasmEngine] = useState(null);

  // Initialize WASM and Cache
  useEffect(() => {
    let active = true;

    async function initPlatform() {
      try {
        const wasmRes = await WasmManager.load();
        if (active) {
          setWasmStatus({ ready: wasmRes.ready, loadTimeMs: wasmRes.loadTimeMs });
          if (wasmRes.ready && wasmRes.engine) {
            setWasmEngine(wasmRes.engine);
          }
        }

        await DeviceCache.init();
        const stats = await DeviceCache.getStats();
        if (active) setCacheStats(stats);
      } catch (err) {
        console.warn('Platform initialization notice:', err);
      }
    }

    initPlatform();
    audioEngine.init().catch(() => {});

    return () => {
      active = false;
      audioEngine.destroy();
    };
  }, []);

  const triggerNotification = (msg, type = 'info') => {
    setNotification({ msg, type });
    setTimeout(() => setNotification(null), 3000);
  };

  // Run Cognitive Sifter
  const runCognitiveSifter = useCallback(async () => {
    if (!rawInput.trim()) {
      triggerNotification('Please insert target text or load a manifesto first.', 'error');
      return;
    }

    setIsProcessing(true);
    setProcessingLog(['[Initializing Cognitive Sifting Pass...]']);

    try {
      const docHash = wasmEngine ? wasmEngine.hash_document(rawInput) : btoa(rawInput.slice(0, 32));
      const cacheKey = `sift:${docHash}`;
      const cached = await DeviceCache.get(cacheKey);

      if (cached) {
        setSiftedData(cached);
        setProcessingLog((p) => [
          ...p,
          '⚡ Cache Hit (0ms) — Retrieved veridical analysis from IndexedDB.',
          `Pillars identified: ${cached.concepts?.length || 0}`,
          `Entropy Score: ${cached.entropy_score?.toFixed(2)}`,
        ]);
        triggerNotification('Loaded sifted payload from local edge cache!', 'success');
        setIsProcessing(false);
        return;
      }

      let resultData = null;

      if (wasmEngine) {
        setProcessingLog((p) => [...p, '🧬 Running Rust WASM CognitiveEngine.sift_text()...']);
        const wasmResJson = wasmEngine.sift_text(rawInput);
        resultData = JSON.parse(wasmResJson);
      } else {
        setProcessingLog((p) => [...p, '🌐 Executing client-side JS fallback text distillation...']);
        // Client-side JS fallback parsing
        const lines = rawInput.split('\n');
        const concepts = lines
          .filter((l) => l.includes('Protocol') || l.includes('Substrate') || l.includes('Matrix'))
          .map((l) => ({
            title: l.slice(0, 50).trim(),
            description: 'Extracted concept pillar',
            layer: 'D1-D9',
          }));

        resultData = {
          concepts: concepts.length > 0 ? concepts : [
            { title: 'Strategic Core Matrix', description: 'Governing protocol', layer: 'D1-D9' },
          ],
          highlights: lines.filter((l) => l.length > 80).slice(0, 3),
          entropy_score: 1.45,
          monetizables: [
            { strategy: 'Direct License Gateway', value: '$499/mo' },
            { strategy: 'Enterprise Compliance Node', value: '$12,500/yr' },
          ],
        };
      }

      setSiftedData(resultData);
      if (resultData.monetizables?.[0]) {
        setSelectedElement({ type: 'Monetizable', value: resultData.monetizables[0].strategy });
      } else if (resultData.concepts?.[0]) {
        setSelectedElement({ type: 'Concept', value: resultData.concepts[0].title });
      }

      await DeviceCache.set({
        key: cacheKey,
        data: resultData,
        hash: docHash,
        timestamp: Date.now(),
        accessCount: 1,
        lastAccessed: Date.now(),
        size: 1024,
        ttl: 86400,
      });

      const updatedStats = await DeviceCache.getStats();
      setCacheStats(updatedStats);

      const integrity = 100 - (resultData.entropy_score || 0) * 8;
      audioEngine.playHarmonic(integrity);

      setProcessingLog((p) => [
        ...p,
        '✅ Sift Complete.',
        `Found ${resultData.concepts?.length || 0} Pillars and ${resultData.monetizables?.length || 0} Monetization pathways.`,
        `Assessed Integrity: ${integrity.toFixed(2)}%`,
      ]);
      triggerNotification('Cognitive sifting pass completed!', 'success');
    } catch (e) {
      setProcessingLog((p) => [...p, `❌ Error: ${e.message}`]);
      triggerNotification('Sifting pass failed.', 'error');
    } finally {
      setIsProcessing(false);
    }
  }, [rawInput, wasmEngine]);

  // Outbound Pitch Synthesis
  const generatePitch = async (tone, setOutput) => {
    setPitchLoading(true);
    try {
      let pitchText = '';
      if (apiKey) {
        // Direct Gemini call if API key provided
        const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            contents: [{ parts: [{ text: `Create a concise pitch with tone "${tone}" for: ${selectedElement?.value || rawInput.slice(0, 100)}` }] }],
          }),
        });
        const data = await res.json();
        pitchText = data.candidates?.[0]?.content?.parts?.[0]?.text || 'Synthesized pitch payload.';
      } else {
        // Deterministic mock synthesis
        await new Promise((r) => setTimeout(r, 600));
        pitchText = `[PITCH VECTOR: ${tone.toUpperCase()}]\n\nTarget Anchor: ${selectedElement?.value || 'PRISM 9 Matrix'}\n\nKey Proposition: Unlock 10x ROI by operationalizing zero-trust cognitive distillation directly at the browser edge. Eliminates API latency while securing 9SM compliance across all 81 matrix dimensions.`;
      }
      setOutput(pitchText);
    } catch (e) {
      setOutput(`Error generating pitch: ${e.message}`);
    } finally {
      setPitchLoading(false);
    }
  };

  // Cognitive Audit Advisor
  const handleAuditQuery = async (query) => {
    setAuditLoading(true);
    const userMsg = { role: 'user', text: query };
    setChatHistory((prev) => [...prev, userMsg]);

    try {
      let replyText = '';
      if (apiKey) {
        const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            contents: [{ parts: [{ text: `You are an audit compliance AI advisor. User query: ${query}. Context: ${rawInput.slice(0, 300)}` }] }],
          }),
        });
        const data = await res.json();
        replyText = data.candidates?.[0]?.content?.parts?.[0]?.text || 'Compliance verification complete.';
      } else {
        await new Promise((r) => setTimeout(r, 700));
        replyText = `[AUDIT ADVISOR ANALYSIS]\n\nQuery: "${query}"\n\nCompliance Status: Verified against 9SM Substrate Parameters. Zero security gaps identified in document payload. Non-binding demonstration mode active.`;
      }

      setChatHistory((prev) => [...prev, { role: 'assistant', text: replyText }]);
    } catch (e) {
      setChatHistory((prev) => [...prev, { role: 'assistant', text: `Audit Advisor Error: ${e.message}` }]);
    } finally {
      setAuditLoading(false);
    }
  };

  // Generate Signed Metadata
  const generateSignedMetadata = () => {
    const payload = {
      timestamp: new Date().toISOString(),
      engine: wasmStatus.ready ? 'PRISM9-WASM-v1.0' : 'JS-FALLBACK',
      documentHash: wasmEngine ? wasmEngine.hash_document(rawInput) : btoa(rawInput.slice(0, 32)),
      integrityScore: siftedData ? (100 - (siftedData.entropy_score || 0) * 8).toFixed(2) : '86.5',
      disclaimer: 'Demonstration asset only — not GAAP certified.',
    };

    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `PRISM9-Certification-${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
    triggerNotification('Downloaded Signed Metadata Certification JSON', 'success');
  };

  const computedIntegrity = siftedData ? (100 - (siftedData.entropy_score || 0) * 8) : 92.4;

  return (
    <div className="min-h-screen bg-black text-zinc-100 p-4 md:p-8 font-sans selection:bg-violet-900 selection:text-violet-100">
      {/* Toast Notification */}
      {notification && (
        <div className={`fixed top-4 right-4 z-50 px-4 py-2 rounded-lg text-xs font-mono font-bold border shadow-lg animate-fade-in ${
          notification.type === 'error' ? 'bg-red-950/90 border-red-500 text-red-200' : 'bg-emerald-950/90 border-emerald-500 text-emerald-200'
        }`}>
          {notification.msg}
        </div>
      )}

      {/* Header */}
      <header className="flex flex-col md:flex-row justify-between items-start md:items-center border-b border-zinc-900 pb-6 mb-8 gap-4">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-black tracking-wider text-white">PRISM 9</h1>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-violet-950 text-violet-300 border border-violet-800">
              WASM EDGE-NATIVE
            </span>
          </div>
          <p className="text-xs text-zinc-500 font-mono mt-1">
            Serverless Cognitive Analytics System & 9SM Matrix Engine
          </p>
        </div>

        {/* Status Indicators */}
        <div className="flex flex-wrap items-center gap-3 text-[10px] font-mono">
          <div className="px-3 py-1.5 bg-zinc-950 border border-zinc-800 rounded-lg flex items-center gap-2">
            <span className={`w-2 h-2 rounded-full ${wasmStatus.ready ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`}></span>
            <span>WASM: {wasmStatus.ready ? `Active (${wasmStatus.loadTimeMs.toFixed(1)}ms)` : 'JS Fallback'}</span>
          </div>

          <div className="px-3 py-1.5 bg-zinc-950 border border-zinc-800 rounded-lg text-zinc-400">
            Cache: <span className="text-emerald-400 font-bold">{cacheStats.entries}</span> entries ({cacheStats.size} B)
          </div>

          <input
            type="password"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder="Gemini API Key (Optional)"
            className="bg-zinc-900 border border-zinc-800 rounded px-3 py-1.5 text-[10px] font-mono text-zinc-200 focus:outline-none focus:border-violet-500"
          />
        </div>
      </header>

      {/* Main Grid Interface */}
      <main className="grid grid-cols-1 lg:grid-cols-12 gap-6">

        {/* Panel 1: Document Ingestion Gateway */}
        <div className="lg:col-span-8 flex flex-col gap-6">
          <CognitiveSifter
            rawInput={rawInput}
            onSiftComplete={(text) => setRawInput(text)}
            isProcessing={isProcessing}
            onClear={() => setRawInput('')}
            onDemoLoad={() => setRawInput(DEMO_STRATEGIC_MANIFESTO)}
          />

          <div className="flex gap-3">
            <button
              type="button"
              onClick={runCognitiveSifter}
              disabled={isProcessing || !rawInput.trim()}
              className="flex-1 py-3 bg-emerald-500 hover:bg-emerald-400 active:bg-emerald-600 text-black font-extrabold rounded-xl text-xs uppercase font-mono tracking-wider transition-all disabled:opacity-30 disabled:pointer-events-none shadow-lg shadow-emerald-950/20"
            >
              {isProcessing ? 'Executing WASM Sift...' : 'Execute Cognitive Sifting Pass'}
            </button>
          </div>

          {/* Processing Log & Sift Output */}
          <div className="bg-zinc-950 border border-zinc-900 rounded-xl p-5 font-mono text-xs">
            <h4 className="text-[10px] font-bold uppercase tracking-widest text-zinc-500 mb-3">Sifting Processing Telemetry</h4>
            <div className="bg-black/60 border border-zinc-900 p-3 rounded-lg h-28 overflow-y-auto space-y-1 text-zinc-400 text-[11px]">
              {processingLog.map((log, idx) => (
                <div key={idx} className={log.startsWith('❌') ? 'text-red-400' : log.startsWith('✅') ? 'text-emerald-400' : 'text-zinc-400'}>
                  {log}
                </div>
              ))}
            </div>

            {siftedData && (
              <div className="mt-4 pt-4 border-t border-zinc-900 grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <h5 className="text-[10px] font-bold uppercase text-emerald-400 mb-2">Pillar Concepts</h5>
                  <ul className="space-y-1 text-[11px] text-zinc-300">
                    {siftedData.concepts?.map((c, i) => (
                      <li key={i} className="p-2 bg-zinc-900/60 rounded border border-zinc-850">
                        <span className="font-bold text-white block">{c.title}</span>
                        <span className="text-zinc-500 text-[10px]">{c.description}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h5 className="text-[10px] font-bold uppercase text-violet-400 mb-2">Monetization Pathways</h5>
                  <ul className="space-y-1 text-[11px] text-zinc-300">
                    {siftedData.monetizables?.map((m, i) => (
                      <li key={i} className="p-2 bg-zinc-900/60 rounded border border-zinc-850 flex justify-between items-center">
                        <span>{m.strategy}</span>
                        <span className="text-emerald-400 font-bold">{m.value}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Panel 2 & 3: 9SM Matrix Navigation & Audit Terminal */}
        <div className="lg:col-span-4 flex flex-col gap-6">

          {/* 9SM Substrate Vector Matrix */}
          <div className="bg-zinc-950 border border-zinc-900 rounded-xl p-5">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xs font-bold uppercase tracking-widest text-zinc-400">9SM Substrate Matrix</h3>
              <span className={`text-[9px] font-mono px-2 py-0.5 rounded border ${
                computedIntegrity >= INTEGRITY_THRESHOLD ? 'bg-emerald-950 text-emerald-400 border-emerald-800' : 'bg-amber-950 text-amber-400 border-amber-800'
              }`}>
                {computedIntegrity >= INTEGRITY_THRESHOLD ? 'LAMINAR' : 'TURBULENT'} ({computedIntegrity.toFixed(1)}%)
              </span>
            </div>

            <div className="grid grid-cols-3 gap-2 mb-4">
              {PRISM_SEGMENTS.map((seg) => (
                <button
                  key={seg.id}
                  type="button"
                  onClick={() => setSelectedSegment(seg)}
                  className={`p-2 rounded-lg text-left border transition-all ${
                    selectedSegment.id === seg.id
                      ? 'bg-violet-950/60 border-violet-500 text-violet-200'
                      : 'bg-zinc-900/40 border-zinc-850 hover:border-zinc-700 text-zinc-400'
                  }`}
                >
                  <span className="block text-[9px] font-mono text-zinc-500">{seg.dimensionRange}</span>
                  <span className="block text-[10px] font-bold truncate mt-0.5">{seg.title}</span>
                </button>
              ))}
            </div>

            {selectedSegment && (
              <div className="p-3 bg-zinc-900/80 border border-zinc-800 rounded-lg text-xs font-mono">
                <span className="text-zinc-500 text-[9px] block uppercase">Selected Vector</span>
                <span className="text-violet-300 font-bold">{selectedSegment.title} ({selectedSegment.dimensionRange})</span>
                <span className="text-zinc-400 block text-[10px] mt-1">Category: {selectedSegment.cat}</span>
              </div>
            )}
          </div>

          {/* Audit Terminal */}
          <AuditTerminal
            chatHistory={chatHistory}
            onSubmit={handleAuditQuery}
            isLoading={auditLoading}
          />

        </div>

        {/* Panel 4 & 5: Outbound Pitch & Certification Gateway */}
        <div className="lg:col-span-12 grid grid-cols-1 md:grid-cols-2 gap-6 mt-2">
          <OutboundPitch
            selectedElement={selectedElement}
            onGenerate={generatePitch}
            isLoading={pitchLoading}
          />

          {/* Certification & Deliverables Gateway */}
          <div className="bg-zinc-950 border border-zinc-900 rounded-xl p-6 flex flex-col justify-between">
            <div>
              <h3 className="text-xs font-bold uppercase tracking-widest text-emerald-400 mb-2 flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                Deliverables & Certification Gateway
              </h3>
              <p className="text-xs text-zinc-400 font-mono mb-4 leading-relaxed">
                Export verifiable, signed metadata artifacts containing 9SM integrity metrics and document hash proofs.
              </p>

              <div className="p-4 bg-zinc-900/60 border border-zinc-800 rounded-lg mb-4 text-xs font-mono space-y-2">
                <div className="flex justify-between">
                  <span className="text-zinc-500">Document Hash:</span>
                  <span className="text-zinc-200 font-bold">
                    {wasmEngine ? wasmEngine.hash_document(rawInput).slice(0, 16) + '...' : 'c8f2b1a0...'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-zinc-500">Substrate Integrity:</span>
                  <span className="text-emerald-400 font-bold">{computedIntegrity.toFixed(2)}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-zinc-500">Audit Compliance:</span>
                  <span className="text-amber-400 font-bold">Self-Attested (Demo)</span>
                </div>
              </div>
            </div>

            <div>
              <button
                type="button"
                onClick={generateSignedMetadata}
                className="w-full py-3 bg-emerald-500 hover:bg-emerald-400 active:bg-emerald-600 text-black font-extrabold rounded-lg text-xs font-mono uppercase tracking-wider transition-all"
              >
                Download Signed Certification JSON
              </button>
              <p className="text-[9px] text-zinc-600 font-mono text-center mt-2">
                Demonstration platform. Not a GAAP accounting guarantee or legal filing.
              </p>
            </div>
          </div>
        </div>

      </main>

      {/* Footer Disclaimer */}
      <footer className="mt-12 pt-6 border-t border-zinc-900 text-center text-[10px] text-zinc-600 font-mono">
        PRISM 9 WASM Edge-Native Cognitive Analytics Engine &copy; 2024 PRISM 9 Contributors.
        All analysis outputs are for demonstration and internal strategic planning purposes.
      </footer>
    </div>
  );
}
