import React, { useState, useRef, useEffect } from 'react';

export function AuditTerminal({ chatHistory = [], onSubmit, isLoading }) {
  const [query, setQuery] = useState('');
  const messagesEndRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim() && !isLoading) {
      onSubmit(query);
      setQuery('');
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory, isLoading]);

  return (
    <div className="bg-zinc-950 border border-zinc-900 rounded-xl p-6 h-[480px] flex flex-col justify-between">
      <div>
        <h3 className="text-xs font-bold uppercase tracking-widest text-amber-400 mb-3 flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-amber-500 animate-pulse"></span>
          Cognitive Audit Advisor
        </h3>

        <div className="h-[340px] overflow-y-auto space-y-3 pr-1 text-xs font-mono">
          {chatHistory.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-center text-zinc-600 p-4">
              <span className="text-2xl mb-2">⚖️</span>
              <p>Query document compliance, SEC risk markers, or structural parameters.</p>
            </div>
          ) : (
            chatHistory.map((msg, idx) => (
              <div
                key={idx}
                className={`p-3 rounded-lg border text-xs font-mono ${
                  msg.role === 'user'
                    ? 'bg-zinc-900 border-zinc-800 ml-auto max-w-[85%] text-zinc-200'
                    : 'bg-amber-950/20 border-amber-900/40 mr-auto max-w-[90%] text-amber-200'
                }`}
              >
                <div className="text-[9px] uppercase text-zinc-500 mb-1">
                  {msg.role === 'user' ? 'Operator' : 'Audit Advisor AI'}
                </div>
                <p className="whitespace-pre-wrap leading-relaxed">{msg.text}</p>
              </div>
            ))
          )}
          {isLoading && (
            <div className="bg-amber-950/20 border border-amber-900/30 p-3 rounded-lg mr-auto max-w-[80%] text-amber-400 animate-pulse text-xs font-mono">
              Evaluating compliance parameters...
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      <form onSubmit={handleSubmit} className="flex gap-2 pt-3 border-t border-zinc-900">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask about compliance or risk factors..."
          disabled={isLoading}
          className="flex-1 bg-zinc-900 border border-zinc-800 rounded-lg px-3 py-2 text-xs font-mono text-zinc-200 focus:outline-none focus:border-amber-500/50"
        />
        <button
          type="submit"
          disabled={isLoading || !query.trim()}
          className="px-4 py-2 bg-amber-500 hover:bg-amber-400 text-black font-bold rounded-lg text-xs font-mono transition-all disabled:opacity-30 disabled:pointer-events-none"
        >
          Query
        </button>
      </form>
    </div>
  );
}
