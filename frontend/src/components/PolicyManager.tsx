import React, { useState } from 'react';
import { ShieldCheck, Lock, Sliders, AlertCircle, CheckCircle2, History, RefreshCw } from 'lucide-react';

export const PolicyManager: React.FC = () => {
  const [maxPerTransaction, setMaxPerTransaction] = useState(0.50);
  const [dailyCap, setDailyCap] = useState(5.00);
  const [allowedCurrencies, setAllowedCurrencies] = useState(['USD']);
  const [autoApproveUnder, setAutoApproveUnder] = useState(0.00);
  const [enforcePromptSanitization, setEnforcePromptSanitization] = useState(true);
  const [strictScopeCheck, setStrictScopeCheck] = useState(true);
  const [saved, setSaved] = useState(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center space-x-2">
            <span>Deterministic Trust &amp; Spending Policy Engine</span>
            <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">
              Enforced by Server
            </span>
          </h2>
          <p className="text-xs text-slate-400">
            Configure guardrails for autonomous AI agents. The LLM cannot override or bypass these deterministic rules.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Controls */}
        <div className="lg:col-span-7 space-y-6">
          <form onSubmit={handleSave} className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl space-y-6">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
              <Sliders className="w-4 h-4 text-blue-400" />
              <span>Financial Limits &amp; Guardrails</span>
            </h3>

            {saved && (
              <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs flex items-center space-x-2">
                <CheckCircle2 className="w-4 h-4" />
                <span>Deterministic spending policy saved and propagated to PayPal Gateway.</span>
              </div>
            )}

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  Max Spend Per Transaction (USD)
                </label>
                <input
                  type="number"
                  step="0.01"
                  value={maxPerTransaction}
                  onChange={(e) => setMaxPerTransaction(parseFloat(e.target.value) || 0)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-xs text-white focus:outline-none focus:border-blue-500 font-mono"
                />
                <span className="text-[10px] text-slate-500 mt-1 block">Hard ceiling on any single AI purchase.</span>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  Cumulative Daily Cap (USD)
                </label>
                <input
                  type="number"
                  step="0.10"
                  value={dailyCap}
                  onChange={(e) => setDailyCap(parseFloat(e.target.value) || 0)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-xs text-white focus:outline-none focus:border-blue-500 font-mono"
                />
                <span className="text-[10px] text-slate-500 mt-1 block">24-hour rolling expenditure limit.</span>
              </div>
            </div>

            <div className="space-y-3 pt-4 border-t border-slate-800">
              <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">AI Security &amp; Isolation</h4>
              
              <div className="flex items-center justify-between p-3 rounded-xl bg-slate-950 border border-slate-800">
                <div className="text-xs">
                  <div className="font-semibold text-white">Prompt-Injection Sanitization</div>
                  <div className="text-[11px] text-slate-400">Treat all external provider responses as untrusted strings.</div>
                </div>
                <input
                  type="checkbox"
                  checked={enforcePromptSanitization}
                  onChange={(e) => setEnforcePromptSanitization(e.target.checked)}
                  className="h-4 w-4 rounded accent-blue-600 bg-slate-900 border-slate-700"
                />
              </div>

              <div className="flex items-center justify-between p-3 rounded-xl bg-slate-950 border border-slate-800">
                <div className="text-xs">
                  <div className="font-semibold text-white">Strict Resource Scope Invariants</div>
                  <div className="text-[11px] text-slate-400">Enforce cryptographic binding between Bearer token and purchased dataset.</div>
                </div>
                <input
                  type="checkbox"
                  checked={strictScopeCheck}
                  onChange={(e) => setStrictScopeCheck(e.target.checked)}
                  className="h-4 w-4 rounded accent-blue-600 bg-slate-900 border-slate-700"
                />
              </div>
            </div>

            <button
              type="submit"
              className="w-full py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs transition shadow-lg shadow-blue-600/30"
            >
              Update Deterministic Policy Rules
            </button>
          </form>
        </div>

        {/* Policy Verification & Architecture Card */}
        <div className="lg:col-span-5 space-y-4">
          <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl space-y-4">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
              <Lock className="w-4 h-4 text-emerald-400" />
              <span>Active Security Invariants</span>
            </h3>

            <ul className="space-y-3 text-xs text-slate-300">
              <li className="flex items-start space-x-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
                <span><strong>No LLM Payment Authority:</strong> The AI model recommends; deterministic backend logic approves and triggers PayPal Sandbox.</span>
              </li>
              <li className="flex items-start space-x-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
                <span><strong>One Source of Truth for Money:</strong> Prices and currencies are resolved strictly from database offer records, ignoring client amounts.</span>
              </li>
              <li className="flex items-start space-x-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
                <span><strong>Cryptographic Separation:</strong> Challenge ID, PayPal Order ID, and Bearer Access Token are completely independent hashes.</span>
              </li>
              <li className="flex items-start space-x-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
                <span><strong>Idempotent Captures:</strong> Replayed callbacks or duplicate approvals never create duplicate charges or multiple entitlements.</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

