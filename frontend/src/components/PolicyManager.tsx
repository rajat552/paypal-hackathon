import React, { useState, useEffect } from 'react';
import { ShieldCheck, Lock, Sliders, AlertCircle, CheckCircle2, History, RefreshCw, KeyRound, DollarSign, Check, Activity, Percent, Loader2 } from 'lucide-react';

export const PolicyManager: React.FC = () => {
  const [maxPerTransaction, setMaxPerTransaction] = useState(0.50);
  const [dailyCap, setDailyCap] = useState(5.00);
  const [allowedCurrencies, setAllowedCurrencies] = useState(['USD']);
  const [autoApproveUnder, setAutoApproveUnder] = useState(0.00);
  const [enforcePromptSanitization, setEnforcePromptSanitization] = useState(true);
  const [strictScopeCheck, setStrictScopeCheck] = useState(true);
  const [currentUtilized, setCurrentUtilized] = useState(0.00);
  const [utilizedPct, setUtilizedPct] = useState(0);
  
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const fetchPolicyConfig = async () => {
    setLoading(true);
    setErrorMsg(null);
    try {
      const res = await fetch('/api/v1/agent/policy/config');
      if (res.ok) {
        const data = await res.json();
        setMaxPerTransaction(data.max_per_transaction);
        setDailyCap(data.daily_cap);
        setAllowedCurrencies(data.allowed_currencies || ['USD']);
        setAutoApproveUnder(data.auto_approve_under || 0.0);
        setEnforcePromptSanitization(data.enforce_prompt_sanitization ?? true);
        setStrictScopeCheck(data.strict_scope_check ?? true);
        setCurrentUtilized(data.current_utilized_24h || 0.0);
        setUtilizedPct(data.utilized_pct || 0);
      }
    } catch (err: any) {
      console.error('Failed to load policy configuration:', err);
      setErrorMsg('Could not fetch server policy. Using active local parameters.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPolicyConfig();
  }, []);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setErrorMsg(null);

    try {
      const res = await fetch('/api/v1/agent/policy/config', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          max_per_transaction: maxPerTransaction,
          daily_cap: dailyCap,
          allowed_currencies: allowedCurrencies,
          auto_approve_under: autoApproveUnder,
          enforce_prompt_sanitization: enforcePromptSanitization,
          strict_scope_check: strictScopeCheck
        })
      });

      if (res.ok) {
        const updated = await res.json();
        setMaxPerTransaction(updated.max_per_transaction);
        setDailyCap(updated.daily_cap);
        setCurrentUtilized(updated.current_utilized_24h || 0.0);
        setUtilizedPct(updated.utilized_pct || 0);
        setSaved(true);
        setTimeout(() => setSaved(false), 3500);
      } else {
        const errData = await res.json();
        throw new Error(errData.detail || 'Server rejected policy update');
      }
    } catch (err: any) {
      setErrorMsg(err.message || 'Failed to save policy');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-8">
      {/* Top Banner with warm gradient */}
      <div className="relative overflow-hidden rounded-3xl border-2 border-slate-900 bg-gradient-to-r from-amber-500 via-amber-400 to-yellow-400 p-6 sm:p-8 shadow-neo text-slate-950">
        <div className="relative z-10 max-w-3xl space-y-2">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-slate-950 text-white font-mono text-xs font-bold shadow-[2px_2px_0px_0px_rgba(255,255,255,0.8)]">
            <ShieldCheck className="w-3.5 h-3.5 text-amber-400" />
            <span>DETERMINISTIC TRUST ENGINE</span>
          </div>

          <h2 className="font-display font-black text-2xl sm:text-4xl tracking-tight text-slate-950">
            Autonomous Spending Guardrails &amp; Policy
          </h2>
          <p className="text-xs sm:text-sm font-medium text-slate-900 max-w-2xl">
            Large Language Models are probabilistic and susceptible to prompt injection. PayMesh AI removes payment authorization from the LLM entirely: deterministic rules run on the server before any PayPal Sandbox Order is created.
          </p>
        </div>
      </div>

      {/* Visual Budget Utilization Meter Card */}
      <div className="p-6 rounded-2xl bg-white border-2 border-slate-900 shadow-neo space-y-3">
        <div className="flex items-center justify-between text-xs font-mono font-bold">
          <div className="flex items-center space-x-2 text-slate-800">
            <Activity className="w-4 h-4 text-brand-600" />
            <span>24-Hour Rolling Budget Utilization (Database-Verified)</span>
          </div>
          <div className="flex items-center space-x-3">
            <button
              onClick={fetchPolicyConfig}
              className="p-1 rounded hover:bg-slate-100 text-slate-600"
              title="Refresh live budget metrics"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            </button>
            <span className="text-slate-600">${currentUtilized.toFixed(2)} / ${dailyCap.toFixed(2)} USD ({utilizedPct}%)</span>
          </div>
        </div>

        {/* Progress Bar Container */}
        <div className="w-full h-4 bg-slate-100 rounded-full border-2 border-slate-900 overflow-hidden p-0.5">
          <div 
            className="h-full bg-gradient-to-r from-emerald-500 to-amber-400 rounded-full transition-all duration-500 shadow-inner"
            style={{ width: `${Math.max(4, Math.min(100, utilizedPct))}%` }}
          ></div>
        </div>

        <div className="flex justify-between text-[11px] font-mono text-slate-500 pt-1">
          <span>$0.00 spent</span>
          <span>Rolling Cap: ${dailyCap.toFixed(2)} USD</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Controls Form */}
        <div className="lg:col-span-7 space-y-6">
          <form onSubmit={handleSave} className="p-6 sm:p-8 rounded-2xl bg-white border-2 border-slate-900 shadow-neo space-y-6">
            <div className="flex items-center justify-between pb-4 border-b-2 border-slate-100">
              <div className="flex items-center space-x-2.5">
                <div className="p-2 bg-amber-100 border-2 border-slate-900 rounded-lg text-slate-950 shadow-neo-sm">
                  <Sliders className="w-4 h-4" />
                </div>
                <h3 className="font-display font-extrabold text-base text-slate-900">
                  Financial Limits &amp; Constraints
                </h3>
              </div>
              <span className="text-xs font-mono font-bold px-2 py-0.5 rounded-md bg-emerald-100 text-emerald-900 border-2 border-emerald-800">
                ACTIVE IN RUNTIME
              </span>
            </div>

            {saved && (
              <div className="p-3.5 rounded-xl bg-emerald-100 border-2 border-emerald-800 text-emerald-950 text-xs font-mono font-bold flex items-center space-x-2 shadow-neo-sm animate-in fade-in">
                <CheckCircle2 className="w-4 h-4 text-emerald-700 flex-shrink-0" />
                <span>Deterministic spending policy saved and active across all agent runs.</span>
              </div>
            )}

            {errorMsg && (
              <div className="p-3.5 rounded-xl bg-red-100 border-2 border-red-800 text-red-950 text-xs font-mono font-bold flex items-center space-x-2 shadow-neo-sm">
                <AlertCircle className="w-4 h-4 text-red-700 flex-shrink-0" />
                <span>{errorMsg}</span>
              </div>
            )}

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5 font-mono">
                  Max Spend Per Transaction
                </label>
                <div className="relative">
                  <span className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500 font-mono font-bold">$</span>
                  <input
                    type="number"
                    step="0.01"
                    value={maxPerTransaction}
                    onChange={(e) => setMaxPerTransaction(parseFloat(e.target.value) || 0)}
                    className="w-full bg-slate-50 border-2 border-slate-900 rounded-xl pl-8 pr-3.5 py-2.5 text-sm text-slate-900 font-mono font-bold focus:outline-none focus:bg-white focus:ring-2 focus:ring-brand-500 shadow-inner"
                  />
                </div>
                <span className="text-[11px] text-slate-500 mt-1.5 block font-medium">Hard ceiling on any single AI micro-purchase.</span>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5 font-mono">
                  Cumulative Daily Cap
                </label>
                <div className="relative">
                  <span className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500 font-mono font-bold">$</span>
                  <input
                    type="number"
                    step="0.10"
                    value={dailyCap}
                    onChange={(e) => setDailyCap(parseFloat(e.target.value) || 0)}
                    className="w-full bg-slate-50 border-2 border-slate-900 rounded-xl pl-8 pr-3.5 py-2.5 text-sm text-slate-900 font-mono font-bold focus:outline-none focus:bg-white focus:ring-2 focus:ring-brand-500 shadow-inner"
                  />
                </div>
                <span className="text-[11px] text-slate-500 mt-1.5 block font-medium">24-hour rolling expenditure quota.</span>
              </div>
            </div>

            <div className="space-y-3.5 pt-4 border-t-2 border-slate-100">
              <h4 className="text-xs font-mono font-bold text-slate-600 uppercase tracking-wider">
                AI Security &amp; Protocol Isolation
              </h4>
              
              <label className="flex items-center justify-between p-3.5 rounded-xl bg-slate-50 border-2 border-slate-900 cursor-pointer shadow-neo-sm hover:bg-amber-50 transition-colors">
                <div className="text-xs pr-4">
                  <div className="font-bold text-slate-900">Prompt-Injection Sanitization</div>
                  <div className="text-[11px] text-slate-600 mt-0.5">Treat external data provider payloads as untrusted strings.</div>
                </div>
                <input
                  type="checkbox"
                  checked={enforcePromptSanitization}
                  onChange={(e) => setEnforcePromptSanitization(e.target.checked)}
                  className="h-5 w-5 rounded accent-amber-500 border-2 border-slate-900 cursor-pointer"
                />
              </label>

              <label className="flex items-center justify-between p-3.5 rounded-xl bg-slate-50 border-2 border-slate-900 cursor-pointer shadow-neo-sm hover:bg-amber-50 transition-colors">
                <div className="text-xs pr-4">
                  <div className="font-bold text-slate-900">Strict Resource Scope Invariants</div>
                  <div className="text-[11px] text-slate-600 mt-0.5">Enforce cryptographic binding between Bearer token and purchased dataset.</div>
                </div>
                <input
                  type="checkbox"
                  checked={strictScopeCheck}
                  onChange={(e) => setStrictScopeCheck(e.target.checked)}
                  className="h-5 w-5 rounded accent-amber-500 border-2 border-slate-900 cursor-pointer"
                />
              </label>
            </div>

            <button
              type="submit"
              disabled={saving}
              className="w-full neo-button-amber py-3 px-6 flex items-center justify-center space-x-2 text-xs font-black uppercase tracking-wider disabled:opacity-50"
            >
              {saving ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Saving Policy to Server...</span>
                </>
              ) : (
                <>
                  <Check className="w-4 h-4 stroke-[2.5]" />
                  <span>Update Deterministic Policy Rules</span>
                </>
              )}
            </button>
          </form>
        </div>

        {/* Policy Verification & Architecture Card */}
        <div className="lg:col-span-5 space-y-4">
          <div className="p-6 sm:p-8 rounded-2xl bg-white border-2 border-slate-900 shadow-neo space-y-4">
            <div className="flex items-center space-x-2.5 pb-3 border-b-2 border-slate-100">
              <div className="p-1.5 bg-emerald-100 border-2 border-slate-900 rounded-lg text-emerald-800 shadow-neo-sm">
                <Lock className="w-4 h-4" />
              </div>
              <h3 className="font-display font-extrabold text-sm text-slate-900 uppercase tracking-wider">
                Cryptographic Security Invariants
              </h3>
            </div>

            <ul className="space-y-4 text-xs text-slate-700">
              <li className="flex items-start space-x-3 p-3 bg-slate-50 rounded-xl border border-slate-200">
                <CheckCircle2 className="w-5 h-5 text-emerald-600 flex-shrink-0 mt-0.5" />
                <div>
                  <strong className="text-slate-900 block font-bold">No LLM Payment Authority</strong>
                  <span className="text-[11px] text-slate-600">The model only suggests tasks; server-side code evaluates spending limits and approves PayPal checkout.</span>
                </div>
              </li>
              <li className="flex items-start space-x-3 p-3 bg-slate-50 rounded-xl border border-slate-200">
                <CheckCircle2 className="w-5 h-5 text-emerald-600 flex-shrink-0 mt-0.5" />
                <div>
                  <strong className="text-slate-900 block font-bold">Server-Calculated Purchase Units</strong>
                  <span className="text-[11px] text-slate-600">Pricing is looked up directly in the database. Agent prompt parameters cannot tamper with transaction price.</span>
                </div>
              </li>
              <li className="flex items-start space-x-3 p-3 bg-slate-50 rounded-xl border border-slate-200">
                <CheckCircle2 className="w-5 h-5 text-emerald-600 flex-shrink-0 mt-0.5" />
                <div>
                  <strong className="text-slate-900 block font-bold">Token &amp; Order ID Separation</strong>
                  <span className="text-[11px] text-slate-600">Challenge ID (`chl_...`), PayPal Order ID, and Bearer token (`pm_live_...`) are distinct and cryptographically hashed.</span>
                </div>
              </li>
              <li className="flex items-start space-x-3 p-3 bg-slate-50 rounded-xl border border-slate-200">
                <CheckCircle2 className="w-5 h-5 text-emerald-600 flex-shrink-0 mt-0.5" />
                <div>
                  <strong className="text-slate-900 block font-bold">Idempotent Captures</strong>
                  <span className="text-[11px] text-slate-600">Server prevents duplicate captures or double payments even if network drops or agent retries.</span>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};
