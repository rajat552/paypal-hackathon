import React, { useState } from 'react';
import { 
  Bot, 
  Sparkles, 
  ShieldCheck, 
  CheckCircle2, 
  AlertTriangle, 
  ExternalLink, 
  ArrowRight, 
  Play, 
  Terminal, 
  Lock, 
  Unlock, 
  Copy, 
  Check, 
  Zap, 
  Keyboard, 
  Newspaper,
  Layers,
  CreditCard,
  X,
  RefreshCw,
  Loader2
} from 'lucide-react';

interface LogEntry {
  type: 'INFO' | 'L402' | 'SUCCESS' | 'ERROR';
  time: string;
  message: string;
  data?: any;
}

export const AgentWorkspace: React.FC = () => {
  const [task, setTask] = useState('Compare high-performance mechanical keyboards with ultra-low latency under budget.');
  const [budget, setBudget] = useState(0.10);
  const [status, setStatus] = useState<'IDLE' | 'DISCOVERING' | 'AWAITING_APPROVAL' | 'PAYING' | 'COMPLETED'>('IDLE');
  const [recommendation, setRecommendation] = useState<any>(null);
  const [challenge, setChallenge] = useState<any>(null);
  const [bearerToken, setBearerToken] = useState<string | null>(null);
  const [unlockedData, setUnlockedData] = useState<any>(null);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [copiedToken, setCopiedToken] = useState(false);
  const [copiedLog, setCopiedLog] = useState(false);
  const [showCheckoutModal, setShowCheckoutModal] = useState(false);
  const [agentRunMeta, setAgentRunMeta] = useState<{
    ai_mode?: string;
    ai_provider?: string;
    ai_model?: string;
    interpreted_intent?: string;
    comparison_reasoning?: string;
  } | null>(null);

  const addLog = (type: LogEntry['type'], message: string, data?: any) => {
    setLogs((prev) => [
      ...prev,
      {
        type,
        time: new Date().toLocaleTimeString(),
        message,
        data,
      },
    ]);
  };

  const handleRunTask = async () => {
    setStatus('DISCOVERING');
    setRecommendation(null);
    setChallenge(null);
    setUnlockedData(null);
    setBearerToken(null);
    setShowCheckoutModal(false);
    setAgentRunMeta(null);
    addLog('INFO', `Starting AI commerce orchestration for task: "${task}"`);
    addLog('INFO', `Enforcing strict spending policy limit: $${budget.toFixed(2)} USD`);

    try {
      const res = await fetch('/api/v1/agent/runs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task, budget_limit: budget }),
      });
      const data = await res.json();

      if (data.recommendation) {
        setRecommendation(data.recommendation);
        setChallenge(data.challenge);
        setAgentRunMeta({
          ai_mode: data.ai_mode,
          ai_provider: data.ai_provider,
          ai_model: data.ai_model,
          interpreted_intent: data.interpreted_intent,
          comparison_reasoning: data.comparison_reasoning,
        });

        if (data.tool_calls_trace && Array.isArray(data.tool_calls_trace)) {
          data.tool_calls_trace.forEach((tc: any) => {
            addLog('INFO', `Tool Executed: ${tc.tool}`, tc.arguments);
          });
        }

        if (data.ai_mode === 'live_llm') {
          addLog('SUCCESS', `AI Reasoning: ${data.ai_provider} (${data.ai_model})`);
        } else {
          addLog('INFO', 'AI Engine: Deterministic Policy Gateway active (offline fallback mode)');
        }

        addLog('L402', `HTTP 402 Payment Required issued for "${data.recommendation.resource_title}"`, data.challenge);
        addLog('INFO', `Deterministic policy gate: ${data.recommendation.policy_reason}`);
        setStatus('AWAITING_APPROVAL');
      } else {
        addLog('ERROR', data.summary || 'No matching resources found');
        setStatus('IDLE');
      }
    } catch (e: any) {
      addLog('ERROR', `Task execution failed: ${e.message}`);
      setStatus('IDLE');
    }
  };

  const handleConfirmAndCapture = async () => {
    if (!challenge) return;
    setShowCheckoutModal(false);
    setStatus('PAYING');
    addLog('INFO', 'Initiating PayPal Sandbox checkout order (intent: CAPTURE)...');

    try {
      // 1. Create Payment Session
      const sessRes = await fetch('/api/v1/payment-sessions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          challenge_id: challenge.challenge_id,
          offer_id: challenge.offer_id,
          buyer_confirmed: true,
        }),
      });
      const sessData = await sessRes.json();
      if (!sessRes.ok) {
        throw new Error(sessData.detail || 'Failed to initialize PayPal payment session');
      }
      addLog('SUCCESS', `PayPal Sandbox Order Created: ${sessData.paypal_order_id}`, sessData);

      // 2. Server-side Capture
      addLog('INFO', 'Buyer confirmed approval. Capturing PayPal Order via server credentials...');
      const capRes = await fetch(`/api/v1/payment-sessions/${sessData.session_id}/capture`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });
      const capData = await capRes.json();
      if (!capRes.ok) {
        throw new Error(capData.detail || 'PayPal server capture failed');
      }
      addLog('SUCCESS', `PayPal Capture Verified: Status ${capData.status} (Capture ID: ${capData.paypal_capture_id})`, capData);
      
      setBearerToken(capData.access_token);
      addLog('INFO', `Issued Cryptographic Bearer Token: ${capData.access_token}`);

      // 3. Retrieve Protected Content
      addLog('INFO', `Exchanging Bearer token for protected dataset from /api/v1/resources/${capData.resource_slug}/content...`);
      const contentRes = await fetch(`/api/v1/resources/${capData.resource_slug}/content`, {
        headers: { Authorization: `Bearer ${capData.access_token}` },
      });
      const contentData = await contentRes.json();
      if (!contentRes.ok) {
        throw new Error(contentData.detail || 'Failed to unlock protected dataset');
      }
      setUnlockedData(contentData);
      addLog('SUCCESS', 'HTTP 200 OK — Decrypted and unlocked protected intelligence data!', contentData);
      setStatus('COMPLETED');
    } catch (e: any) {
      addLog('ERROR', `Payment or retrieval error: ${e.message}`);
      setStatus('AWAITING_APPROVAL');
    }
  };

  const copyTokenToClipboard = () => {
    if (bearerToken) {
      navigator.clipboard.writeText(bearerToken);
      setCopiedToken(true);
      setTimeout(() => setCopiedToken(false), 2000);
    }
  };

  const copyLogToClipboard = () => {
    const text = logs.map(l => `[${l.time}] [${l.type}] ${l.message} ${l.data ? JSON.stringify(l.data) : ''}`).join('\n');
    navigator.clipboard.writeText(text);
    setCopiedLog(true);
    setTimeout(() => setCopiedLog(false), 2000);
  };

  const clearLogs = () => {
    setLogs([]);
  };

  return (
    <div className="space-y-8">
      {/* Hero Header Section */}
      <div className="relative overflow-hidden rounded-3xl border-2 border-slate-900 bg-white p-6 sm:p-10 shadow-neo bg-blueprint-grid">
        <div className="relative z-10 max-w-4xl space-y-4">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-amber-300 text-slate-950 border-2 border-slate-900 font-mono text-xs font-bold shadow-[2px_2px_0px_0px_rgba(15,23,42,1)]">
            <Zap className="w-3.5 h-3.5 fill-current" />
            <span>PAYPAL AI HACKATHON 2026 ARCHITECTURE</span>
          </div>

          <h1 className="font-display font-black text-3xl sm:text-5xl tracking-tight text-slate-900 leading-tight">
            The Trust &amp; Payment Mesh for <span className="text-brand-500 underline decoration-amber-400 decoration-wavy decoration-2">Autonomous AI</span> Commerce
          </h1>

          <p className="text-sm sm:text-base text-slate-600 font-medium leading-relaxed max-w-2xl">
            AI agents shouldn't hold credit cards. PayMesh AI empowers programmatic clients to negotiate machine-readable <strong>L402 payment challenges</strong>, enforce strict spending guardrails, and execute verified <strong>PayPal Sandbox Orders v2</strong> server captures.
          </p>

          {/* Quick Metrics Bar */}
          <div className="pt-2 grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="p-3 bg-slate-50 border-2 border-slate-900 rounded-xl shadow-neo-sm">
              <div className="font-display font-black text-xl text-brand-600">$0.01</div>
              <div className="text-[11px] font-bold text-slate-600 uppercase tracking-wider font-mono">Micro-Payments</div>
            </div>
            <div className="p-3 bg-slate-50 border-2 border-slate-900 rounded-xl shadow-neo-sm">
              <div className="font-display font-black text-xl text-emerald-600">100%</div>
              <div className="text-[11px] font-bold text-slate-600 uppercase tracking-wider font-mono">Policy Enforced</div>
            </div>
            <div className="p-3 bg-slate-50 border-2 border-slate-900 rounded-xl shadow-neo-sm">
              <div className="font-display font-black text-xl text-amber-500">&lt; 120ms</div>
              <div className="text-[11px] font-bold text-slate-600 uppercase tracking-wider font-mono">Capture Latency</div>
            </div>
            <div className="p-3 bg-slate-50 border-2 border-slate-900 rounded-xl shadow-neo-sm">
              <div className="font-display font-black text-xl text-indigo-600">L402 / MCP</div>
              <div className="text-[11px] font-bold text-slate-600 uppercase tracking-wider font-mono">Open Protocol</div>
            </div>
          </div>
        </div>
      </div>

      {/* Preset Track Cards */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Layers className="w-4 h-4 text-slate-700" />
            <h3 className="font-display font-bold text-sm text-slate-900 uppercase tracking-wider">
              Select an AI Agent Mission Track
            </h3>
          </div>
          <span className="text-xs font-mono text-slate-500">Click track to auto-load prompt and policy</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Track 1: Channel3 Hardware Intelligence */}
          <div 
            onClick={() => {
              setTask('Compare high-performance mechanical keyboards with ultra-low latency under budget.');
              setBudget(0.10);
            }}
            className="group cursor-pointer p-4 bg-white border-2 border-slate-900 rounded-2xl shadow-neo hover:-translate-y-0.5 hover:shadow-neo-lg transition-all flex items-center justify-between gap-4"
          >
            <div className="flex items-center space-x-3.5">
              <div className="h-11 w-11 rounded-xl bg-blue-100 border-2 border-slate-900 flex items-center justify-center text-blue-700 shadow-neo-sm">
                <Keyboard className="w-6 h-6" />
              </div>
              <div>
                <div className="flex items-center space-x-2">
                  <span className="font-display font-extrabold text-sm text-slate-900 group-hover:text-brand-600 transition-colors">
                    Hardware Latency Benchmarks
                  </span>
                  <span className="text-[10px] px-1.5 py-0.5 bg-blue-100 text-blue-800 rounded font-mono font-bold">
                    Channel3
                  </span>
                </div>
                <p className="text-xs text-slate-600 mt-0.5">
                  Micro-purchase switch latency &amp; retail profiles ($0.05 / session)
                </p>
              </div>
            </div>

            <div className="h-9 w-9 rounded-xl bg-amber-400 border-2 border-slate-900 flex items-center justify-center text-slate-950 shadow-neo-sm group-hover:translate-x-1 transition-transform flex-shrink-0">
              <ArrowRight className="w-4 h-4 stroke-[2.5]" />
            </div>
          </div>

          {/* Track 2: CrawlerPal News Feed */}
          <div 
            onClick={() => {
              setTask('Curated technology and economics news feed.');
              setBudget(0.05);
            }}
            className="group cursor-pointer p-4 bg-white border-2 border-slate-900 rounded-2xl shadow-neo hover:-translate-y-0.5 hover:shadow-neo-lg transition-all flex items-center justify-between gap-4"
          >
            <div className="flex items-center space-x-3.5">
              <div className="h-11 w-11 rounded-xl bg-emerald-100 border-2 border-slate-900 flex items-center justify-center text-emerald-700 shadow-neo-sm">
                <Newspaper className="w-6 h-6" />
              </div>
              <div>
                <div className="flex items-center space-x-2">
                  <span className="font-display font-extrabold text-sm text-slate-900 group-hover:text-emerald-700 transition-colors">
                    Economics &amp; Tech Intelligence
                  </span>
                  <span className="text-[10px] px-1.5 py-0.5 bg-emerald-100 text-emerald-800 rounded font-mono font-bold">
                    CrawlerPal
                  </span>
                </div>
                <p className="text-xs text-slate-600 mt-0.5">
                  Pay-per-query machine access to real-time articles ($0.01 / request)
                </p>
              </div>
            </div>

            <div className="h-9 w-9 rounded-xl bg-amber-400 border-2 border-slate-900 flex items-center justify-center text-slate-950 shadow-neo-sm group-hover:translate-x-1 transition-transform flex-shrink-0">
              <ArrowRight className="w-4 h-4 stroke-[2.5]" />
            </div>
          </div>
        </div>
      </div>

      {/* Main Grid: Left Column + Right Column */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Column: Interactive Agent Studio */}
        <div className="lg:col-span-7 space-y-6">
          {/* Agent Goal Input Card */}
          <div className="p-6 rounded-2xl bg-white border-2 border-slate-900 shadow-neo space-y-5">
            <div className="flex items-center justify-between pb-3 border-b-2 border-slate-100">
              <div className="flex items-center space-x-2.5">
                <div className="p-1.5 bg-brand-50 border-2 border-slate-900 rounded-lg text-brand-600 shadow-neo-sm">
                  <Bot className="w-4 h-4" />
                </div>
                <h2 className="font-display font-extrabold text-base text-slate-900">
                  AI Commerce Agent Studio
                </h2>
              </div>
              <span className="text-xs font-mono px-2 py-0.5 rounded-full bg-slate-100 text-slate-700 border border-slate-300">
                L402 Protocol Active
              </span>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5 font-mono">
                  Autonomous Agent Prompt / Goal
                </label>
                <textarea
                  rows={3}
                  value={task}
                  onChange={(e) => setTask(e.target.value)}
                  className="w-full bg-slate-50 border-2 border-slate-900 rounded-xl p-3.5 text-sm text-slate-900 font-mono focus:outline-none focus:bg-white focus:ring-2 focus:ring-brand-500 shadow-inner"
                  placeholder="Describe data or intelligence requirement..."
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-12 gap-4">
                <div className="sm:col-span-7">
                  <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5 font-mono">
                    Spending Policy Limit (USD)
                  </label>
                  <div className="relative">
                    <span className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500 font-mono font-bold">$</span>
                    <input
                      type="number"
                      value={budget}
                      step="0.01"
                      onChange={(e) => setBudget(parseFloat(e.target.value) || 0)}
                      className="w-full bg-slate-50 border-2 border-slate-900 rounded-xl pl-8 pr-3.5 py-2.5 text-sm text-slate-900 font-mono font-bold focus:outline-none focus:bg-white focus:ring-2 focus:ring-brand-500 shadow-inner"
                    />
                  </div>
                </div>

                <div className="sm:col-span-5 flex items-end">
                  <button
                    onClick={handleRunTask}
                    disabled={status === 'DISCOVERING' || status === 'PAYING'}
                    className="w-full neo-button-amber py-2.5 px-4 flex items-center justify-center space-x-2 text-xs font-black uppercase tracking-wider disabled:opacity-50"
                  >
                    {status === 'DISCOVERING' ? (
                      <Loader2 className="w-4 h-4 animate-spin text-slate-950" />
                    ) : (
                      <Play className="w-4 h-4 fill-current stroke-[1.5]" />
                    )}
                    <span>{status === 'DISCOVERING' ? 'Discovering...' : 'Dispatch Agent'}</span>
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* L402 Challenge & Payment Gate Card */}
          {recommendation && (
            <div className="p-6 rounded-2xl bg-white border-2 border-slate-900 shadow-neo space-y-5 animate-in fade-in">
              {agentRunMeta && (
                <div className="flex items-center justify-between text-xs font-mono px-3.5 py-2 rounded-xl border-2 border-slate-900 bg-slate-100 shadow-neo-sm">
                  <div className="flex items-center space-x-2">
                    <span className={`w-2.5 h-2.5 rounded-full ${agentRunMeta.ai_mode === 'live_llm' ? 'bg-emerald-500 animate-pulse' : 'bg-blue-500'}`} />
                    <span className="font-bold text-slate-900">
                      {agentRunMeta.ai_mode === 'live_llm'
                        ? `AI Model: ${agentRunMeta.ai_provider} (${agentRunMeta.ai_model})`
                        : 'AI Gateway: Deterministic Procurement & Policy Engine'}
                    </span>
                  </div>
                  <span className="text-[10px] px-2 py-0.5 rounded font-bold uppercase tracking-wider bg-white border border-slate-300 text-slate-700">
                    {agentRunMeta.ai_mode === 'live_llm' ? 'Live Tool-Calling' : 'Deterministic Mode'}
                  </span>
                </div>
              )}

              <div className="flex items-center justify-between pb-3 border-b-2 border-slate-100">
                <div className="flex items-center space-x-2">
                  <span className="text-xs font-mono font-bold px-2 py-0.5 rounded-md bg-amber-400 text-slate-950 border-2 border-slate-900 shadow-[1px_1px_0px_0px_rgba(15,23,42,1)]">
                    HTTP 402 CHALLENGE
                  </span>
                  <span className="font-display font-extrabold text-sm text-slate-900">
                    {recommendation.resource_title}
                  </span>
                </div>
                <div className="flex items-center space-x-1 font-mono font-black text-base text-slate-950 px-2.5 py-1 bg-amber-100 border-2 border-slate-900 rounded-lg shadow-neo-sm">
                  <span>${recommendation.amount.toFixed(2)}</span>
                  <span className="text-xs text-slate-600">{recommendation.currency}</span>
                </div>
              </div>

              <p className="text-xs text-slate-700 leading-relaxed font-medium bg-slate-50 p-3.5 rounded-xl border border-slate-200">
                {recommendation.explanation}
              </p>

              {/* Policy Assessment Strip */}
              <div
                className={`p-3.5 rounded-xl border-2 flex items-center space-x-2.5 text-xs font-mono font-bold ${
                  recommendation.policy_allowed
                    ? 'bg-emerald-50 border-emerald-800 text-emerald-950'
                    : 'bg-red-50 border-red-800 text-red-950'
                }`}
              >
                {recommendation.policy_allowed ? (
                  <ShieldCheck className="w-5 h-5 text-emerald-700 flex-shrink-0" />
                ) : (
                  <AlertTriangle className="w-5 h-5 text-red-600 flex-shrink-0" />
                )}
                <span>Policy Evaluation: {recommendation.policy_reason}</span>
              </div>

              {/* Action / Checkout Area */}
              {status !== 'COMPLETED' && (
                <div className="pt-2 flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-t-2 border-slate-100">
                  <div className="text-xs text-slate-600 font-mono flex items-center space-x-1.5">
                    <Lock className="w-3.5 h-3.5 text-amber-500" />
                    <span>Protected access locked until PayPal Sandbox capture</span>
                  </div>

                  {recommendation.policy_allowed && (
                    <button
                      onClick={() => setShowCheckoutModal(true)}
                      disabled={status === 'PAYING'}
                      className="neo-button-blue py-2.5 px-5 flex items-center justify-center space-x-2 text-xs font-bold uppercase tracking-wider disabled:opacity-50"
                    >
                      <CreditCard className="w-4 h-4" />
                      <span>{status === 'PAYING' ? 'Capturing PayPal Order...' : 'Approve & Pay via PayPal Sandbox'}</span>
                      <ArrowRight className="w-3.5 h-3.5 stroke-[2.5]" />
                    </button>
                  )}
                </div>
              )}
            </div>
          )}

          {/* Unlocked Protected Content Presentation */}
          {unlockedData && (
            <div className="p-6 rounded-2xl bg-white border-2 border-emerald-600 shadow-neo space-y-5 animate-in slide-in-from-bottom-2">
              <div className="flex items-center justify-between pb-3 border-b-2 border-emerald-100">
                <div className="flex items-center space-x-2">
                  <div className="p-1.5 bg-emerald-100 border-2 border-emerald-800 rounded-lg text-emerald-800">
                    <Unlock className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="font-display font-black text-base text-slate-900">
                      Unlocked: {unlockedData.title}
                    </h3>
                    <div className="text-[11px] text-slate-500 font-mono">
                      Attribution: {unlockedData.attribution}
                    </div>
                  </div>
                </div>

                <div className="flex items-center space-x-2">
                  {bearerToken && (
                    <button
                      onClick={copyTokenToClipboard}
                      className="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 border-2 border-slate-900 rounded-lg text-[11px] font-mono font-bold flex items-center space-x-1 text-slate-800 shadow-neo-sm"
                      title="Copy Bearer Token"
                    >
                      {copiedToken ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
                      <span>{copiedToken ? 'Copied' : 'Token'}</span>
                    </button>
                  )}
                  <span className="text-xs px-2.5 py-1 rounded-lg bg-emerald-100 text-emerald-900 border-2 border-emerald-700 font-mono font-bold shadow-neo-sm">
                    Verified 200 OK
                  </span>
                </div>
              </div>

              {/* If Channel3 Hardware Benchmarks */}
              {unlockedData.data && unlockedData.data.benchmarks ? (
                <div className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
                    {unlockedData.data.benchmarks.map((item: any) => (
                      <div 
                        key={item.provider_item_id} 
                        className="p-4 rounded-xl bg-slate-50 border-2 border-slate-900 text-xs flex flex-col justify-between shadow-neo-sm hover:shadow-neo transition-all"
                      >
                        <div>
                          <div className="flex items-center justify-between mb-1.5">
                            <span className="font-display font-black text-slate-900 text-sm">{item.brand}</span>
                            <span className="font-mono text-emerald-700 font-black text-sm bg-emerald-100 px-2 py-0.5 rounded border border-emerald-600">
                              ${item.price}
                            </span>
                          </div>
                          <div className="text-slate-800 font-bold mb-2 leading-tight">{item.title}</div>
                          
                          <div className="p-2.5 bg-white rounded-lg border border-slate-200 space-y-1 font-mono text-[11px] text-slate-600">
                            <div className="flex justify-between">
                              <span>Switch:</span>
                              <span className="font-bold text-slate-900">{item.switch_type}</span>
                            </div>
                            <div className="flex justify-between">
                              <span>Measured Latency:</span>
                              <span className="font-bold text-brand-600">{item.latency_ms} ms</span>
                            </div>
                          </div>
                        </div>

                        <a
                          href={item.source_url}
                          target="_blank"
                          rel="noreferrer"
                          className="mt-3 inline-flex items-center justify-center space-x-1.5 py-1.5 px-3 rounded-lg bg-brand-50 hover:bg-brand-100 border border-brand-300 text-brand-700 font-mono font-bold text-xs transition-colors"
                        >
                          <span>Channel3 Retail Link</span>
                          <ExternalLink className="w-3.5 h-3.5" />
                        </a>
                      </div>
                    ))}
                  </div>

                  {unlockedData.data.market_insights && (
                    <div className="p-4 rounded-xl bg-amber-50 border-2 border-slate-900 shadow-neo-sm text-xs text-slate-900 space-y-1">
                      <div className="font-mono font-bold uppercase text-amber-800 flex items-center space-x-1">
                        <Sparkles className="w-3.5 h-3.5 text-amber-600" />
                        <span>Channel3 Market Synthesis:</span>
                      </div>
                      <p className="font-medium leading-relaxed">
                        {unlockedData.data.market_insights.recommendation}
                      </p>
                    </div>
                  )}
                </div>
              ) : (
                <pre className="p-4 bg-slate-900 text-emerald-400 rounded-xl text-xs font-mono overflow-x-auto border-2 border-slate-900 shadow-inner">
                  {JSON.stringify(unlockedData, null, 2)}
                </pre>
              )}
            </div>
          )}
        </div>

        {/* Right Column: Dark Protocol Terminal Inspector */}
        <div className="lg:col-span-5 space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Terminal className="w-4 h-4 text-slate-900" />
              <h3 className="font-display font-extrabold text-sm text-slate-900 uppercase tracking-wider">
                Protocol Inspector (L402 / MCP)
              </h3>
            </div>
            <div className="flex items-center space-x-2">
              {logs.length > 0 && (
                <>
                  <button
                    onClick={copyLogToClipboard}
                    className="px-2 py-0.5 rounded bg-white hover:bg-slate-100 border-2 border-slate-900 text-[11px] font-mono font-bold text-slate-700 shadow-neo-sm flex items-center space-x-1"
                    title="Copy All Log Entries"
                  >
                    {copiedLog ? <Check className="w-3 h-3 text-emerald-600" /> : <Copy className="w-3 h-3" />}
                    <span>{copiedLog ? 'Copied' : 'Copy'}</span>
                  </button>
                  <button
                    onClick={clearLogs}
                    className="px-2 py-0.5 rounded bg-white hover:bg-slate-100 border-2 border-slate-900 text-[11px] font-mono font-bold text-slate-700 shadow-neo-sm flex items-center space-x-1"
                    title="Clear Terminal Log"
                  >
                    <RefreshCw className="w-3 h-3" />
                    <span>Clear</span>
                  </button>
                </>
              )}
              <span className="text-[11px] font-mono font-bold px-2 py-0.5 rounded-md bg-amber-300 text-slate-950 border-2 border-slate-900 shadow-neo-sm">
                STATE: {status}
              </span>
            </div>
          </div>

          {/* High-Contrast Technical Terminal */}
          <div className="bg-[#0b0f19] border-2 border-slate-900 rounded-2xl p-4 font-mono text-[11px] h-[580px] overflow-y-auto space-y-2.5 shadow-neo">
            {logs.length === 0 ? (
              <div className="text-slate-500 italic pt-6 text-center">
                // Ready for execution.
                <br />
                // Select a preset mission or enter a prompt, then click "Dispatch Agent"
                <br />
                // to observe the live HTTP 402 handshake and PayPal capture.
              </div>
            ) : (
              logs.map((log, idx) => {
                let badgeStyle = 'bg-blue-900/60 text-blue-300 border-blue-600';
                if (log.type === 'L402') badgeStyle = 'bg-amber-400 text-slate-950 font-black border-amber-300';
                if (log.type === 'SUCCESS') badgeStyle = 'bg-emerald-500 text-slate-950 font-black border-emerald-400';
                if (log.type === 'ERROR') badgeStyle = 'bg-red-500 text-white font-black border-red-400';

                return (
                  <div key={idx} className="leading-relaxed border-b border-slate-800/80 pb-2.5 last:border-0">
                    <div className="flex items-center space-x-2 mb-1">
                      <span className="text-slate-500 text-[10px]">[{log.time}]</span>
                      <span className={`px-1.5 py-0.2 rounded text-[10px] border ${badgeStyle}`}>
                        {log.type}
                      </span>
                    </div>
                    <div className="text-slate-200 font-medium pl-1">{log.message}</div>
                    {log.data && (
                      <pre className="mt-1.5 text-[10px] text-slate-400 bg-slate-950/90 p-2.5 rounded-lg overflow-x-auto border border-slate-800 shadow-inner">
                        {JSON.stringify(log.data, null, 2)}
                      </pre>
                    )}
                  </div>
                );
              })
            )}
          </div>
        </div>
      </div>

      {/* FinTech Checkout Confirmation Modal */}
      {showCheckoutModal && recommendation && challenge && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/70 backdrop-blur-sm animate-in fade-in">
          <div className="relative w-full max-w-md bg-white border-2 border-slate-900 rounded-3xl p-6 sm:p-7 shadow-neo-lg animate-neo-pop space-y-5">
            <div className="flex items-center justify-between pb-3 border-b-2 border-slate-100">
              <div className="flex items-center space-x-2">
                <div className="p-1.5 bg-amber-300 border-2 border-slate-900 rounded-lg text-slate-950 shadow-neo-sm">
                  <CreditCard className="w-4 h-4" />
                </div>
                <h3 className="font-display font-black text-base text-slate-900">
                  PayPal Sandbox Authorization
                </h3>
              </div>
              <button
                onClick={() => setShowCheckoutModal(false)}
                className="p-1.5 rounded-lg hover:bg-slate-100 text-slate-600"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="space-y-3 font-mono text-xs text-slate-700">
              <div className="p-3 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5">
                <div className="flex justify-between">
                  <span className="text-slate-500">Resource:</span>
                  <span className="font-bold text-slate-900">{recommendation.resource_title}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Offer Code:</span>
                  <span className="font-bold text-slate-900">{challenge.offer_id}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Challenge ID:</span>
                  <span className="text-slate-900 font-bold truncate max-w-[180px]">{challenge.challenge_id}</span>
                </div>
              </div>

              <div className="p-3 bg-emerald-50 rounded-xl border-2 border-emerald-700 flex items-center justify-between text-emerald-950">
                <span className="font-bold">Total Capture Amount:</span>
                <span className="font-black text-base">${recommendation.amount.toFixed(2)} {recommendation.currency}</span>
              </div>

              <div className="text-[11px] text-slate-500 leading-relaxed font-sans">
                🔒 <strong>Server-Side Capture:</strong> Authorizing will dispatch an OAuth 2.0 capture request directly to PayPal Sandbox Orders v2. Upon capture, a scoped cryptographic Bearer token will be granted immediately.
              </div>
            </div>

            <div className="flex items-center space-x-3 pt-2">
              <button
                type="button"
                onClick={() => setShowCheckoutModal(false)}
                className="flex-1 py-2.5 px-4 rounded-xl bg-slate-100 hover:bg-slate-200 border-2 border-slate-900 text-xs font-mono font-bold text-slate-800 transition"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleConfirmAndCapture}
                className="flex-1 neo-button-amber py-2.5 px-4 text-xs font-black uppercase tracking-wider flex items-center justify-center space-x-1.5"
              >
                <span>Authorize &amp; Pay</span>
                <ArrowRight className="w-3.5 h-3.5 stroke-[2.5]" />
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
