import React, { useState } from 'react';
import { Bot, Sparkles, ShieldCheck, CheckCircle2, AlertTriangle, ExternalLink, ArrowRight, Play, Terminal, Lock, Unlock } from 'lucide-react';

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
    addLog('INFO', `Executing task: "${task}" with max budget limit $${budget.toFixed(2)} USD`);

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
        addLog('L402', `Received HTTP 402 challenge with offer for ${data.recommendation.resource_title}`, data.challenge);
        addLog('INFO', `Deterministic policy result: ${data.recommendation.policy_reason}`);
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

  const handleApproveAndPay = async () => {
    if (!challenge) return;
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
      addLog('SUCCESS', `PayPal Sandbox Order Created: ${sessData.paypal_order_id}`, sessData);

      // 2. Server-side Capture
      addLog('INFO', 'Buyer approved. Capturing and verifying PayPal order on server...');
      const capRes = await fetch(`/api/v1/payment-sessions/${sessData.session_id}/capture`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
      });
      const capData = await capRes.json();
      addLog('SUCCESS', `PayPal Capture Verified: Status ${capData.status} (Capture ID: ${capData.paypal_capture_id})`, capData);
      
      setBearerToken(capData.access_token);
      addLog('INFO', `Issued Scoped Bearer Token: ${capData.access_token}`);

      // 3. Retrieve Protected Content
      addLog('INFO', `Retrieving protected resource content using Bearer token...`);
      const contentRes = await fetch(`/api/v1/resources/${capData.resource_slug}/content`, {
        headers: { Authorization: `Bearer ${capData.access_token}` },
      });
      const contentData = await contentRes.json();
      setUnlockedData(contentData);
      addLog('SUCCESS', 'HTTP 200 OK — Unlocked Protected Channel3 Dataset!', contentData);
      setStatus('COMPLETED');
    } catch (e: any) {
      addLog('ERROR', `Payment or retrieval error: ${e.message}`);
      setStatus('AWAITING_APPROVAL');
    }
  };

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Controls and Offer Cards */}
        <div className="lg:col-span-7 space-y-6">
          <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl">
            <div className="flex items-center space-x-2 mb-4">
              <Bot className="w-5 h-5 text-blue-400" />
              <h2 className="text-base font-bold text-white">PayMesh AI — Autonomous Commerce Agent</h2>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Research Prompt / Goal</label>
                <textarea
                  rows={3}
                  value={task}
                  onChange={(e) => setTask(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-sm text-white focus:outline-none focus:border-blue-500 font-mono"
                />
              </div>

              <div className="flex gap-4">
                <div className="flex-1">
                  <label className="block text-xs font-semibold text-slate-300 mb-1">Spending Policy Limit (USD)</label>
                  <input
                    type="number"
                    value={budget}
                    step="0.01"
                    onChange={(e) => setBudget(parseFloat(e.target.value) || 0)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-sm text-white focus:outline-none focus:border-blue-500 font-mono"
                  />
                </div>
                <div className="flex items-end">
                  <button
                    onClick={handleRunTask}
                    disabled={status === 'DISCOVERING' || status === 'PAYING'}
                    className="h-[42px] px-6 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs transition flex items-center space-x-2 shadow-lg shadow-blue-600/30 disabled:opacity-50"
                  >
                    <Play className="w-3.5 h-3.5 fill-current" />
                    <span>{status === 'DISCOVERING' ? 'Discovering...' : 'Run Agent'}</span>
                  </button>
                </div>
              </div>
            </div>

            {/* Presets */}
            <div className="mt-4 pt-4 border-t border-slate-800 flex items-center space-x-2 text-xs text-slate-400">
              <span className="font-semibold text-slate-500">Presets:</span>
              <button
                onClick={() => setTask('Compare high-performance mechanical keyboards with ultra-low latency under budget.')}
                className="hover:text-blue-400 underline decoration-slate-700"
              >
                Keyboards (Channel3)
              </button>
              <span>&bull;</span>
              <button
                onClick={() => setTask('Curated technology and economics news feed.')}
                className="hover:text-blue-400 underline decoration-slate-700"
              >
                News Feed
              </button>
            </div>
          </div>

          {/* Recommendation & Policy Gate Card */}
          {recommendation && (
            <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl space-y-4 animate-in fade-in">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">
                    L402 CHALLENGE
                  </span>
                  <span className="text-xs font-semibold text-white">{recommendation.resource_title}</span>
                </div>
                <span className="text-sm font-extrabold text-emerald-400 font-mono">
                  ${recommendation.amount.toFixed(2)} {recommendation.currency}
                </span>
              </div>

              <p className="text-xs text-slate-300 leading-relaxed">{recommendation.explanation}</p>

              {/* Policy Indicator */}
              <div
                className={`p-3 rounded-xl border flex items-center space-x-2 text-xs font-mono ${
                  recommendation.policy_allowed
                    ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400'
                    : 'bg-red-500/10 border-red-500/20 text-red-400'
                }`}
              >
                {recommendation.policy_allowed ? (
                  <ShieldCheck className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                ) : (
                  <AlertTriangle className="w-4 h-4 text-red-400 flex-shrink-0" />
                )}
                <span>{recommendation.policy_reason}</span>
              </div>

              {/* Action / Checkout */}
              {status !== 'COMPLETED' && (
                <div className="pt-2 flex items-center justify-between">
                  <div className="text-[11px] text-slate-400 flex items-center space-x-1">
                    <Lock className="w-3.5 h-3.5 text-amber-400" />
                    <span>Protected access locked until PayPal capture</span>
                  </div>

                  {recommendation.policy_allowed && (
                    <button
                      onClick={handleApproveAndPay}
                      disabled={status === 'PAYING'}
                      className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-xs shadow-lg shadow-emerald-600/20 transition flex items-center space-x-1.5 disabled:opacity-50"
                    >
                      <span>{status === 'PAYING' ? 'Capturing PayPal Order...' : 'Approve & Pay via PayPal Sandbox'}</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                  )}
                </div>
              )}
            </div>
          )}

          {/* Unlocked Protected Content Presentation */}
          {unlockedData && (
            <div className="p-6 rounded-2xl bg-slate-900 border border-emerald-500/40 shadow-2xl space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <div className="flex items-center space-x-2">
                  <Unlock className="w-5 h-5 text-emerald-400" />
                  <h3 className="text-base font-bold text-white">Unlocked: {unlockedData.title}</h3>
                </div>
                <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">
                  Bearer Token Verified
                </span>
              </div>

              <div className="text-xs text-slate-400 mb-2">
                <strong>Source:</strong> {unlockedData.attribution}
              </div>

              {unlockedData.data && unlockedData.data.benchmarks ? (
                <div className="space-y-3">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {unlockedData.data.benchmarks.map((item: any) => (
                      <div key={item.provider_item_id} className="p-3.5 rounded-xl bg-slate-950 border border-slate-800 text-xs flex flex-col justify-between">
                        <div>
                          <div className="flex items-center justify-between mb-1.5">
                            <span className="font-bold text-white">{item.brand}</span>
                            <span className="font-mono text-emerald-400 font-bold">${item.price}</span>
                          </div>
                          <div className="text-slate-300 font-medium mb-1">{item.title}</div>
                          <div className="text-[11px] text-slate-500 space-y-0.5 font-mono">
                            <div>Latency: <span className="text-blue-400">{item.latency_ms} ms</span></div>
                            <div>Switch: {item.switch_type}</div>
                          </div>
                        </div>
                        <a
                          href={item.source_url}
                          target="_blank"
                          rel="noreferrer"
                          className="mt-3 inline-flex items-center space-x-1 text-[11px] text-blue-400 hover:text-blue-300 font-semibold"
                        >
                          <span>Channel3 Verified Link</span>
                          <ExternalLink className="w-3 h-3" />
                        </a>
                      </div>
                    ))}
                  </div>

                  {unlockedData.data.market_insights && (
                    <div className="p-3 rounded-xl bg-blue-950/40 border border-blue-500/30 text-xs text-blue-200">
                      <strong>AI Summary: </strong>
                      {unlockedData.data.market_insights.recommendation}
                    </div>
                  )}
                </div>
              ) : (
                <pre className="p-3 bg-slate-950 rounded-lg text-xs font-mono text-slate-300 overflow-x-auto">
                  {JSON.stringify(unlockedData, null, 2)}
                </pre>
              )}
            </div>
          )}
        </div>

        {/* Right Column: Real-time Terminal Log */}
        <div className="lg:col-span-5 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Terminal className="w-4 h-4 text-slate-400" />
              <h3 className="text-xs font-bold text-white uppercase tracking-wider">Protocol Inspection Log</h3>
            </div>
            <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400">
              STATUS: {status}
            </span>
          </div>

          <div className="bg-slate-950 border border-slate-800 rounded-2xl p-4 font-mono text-[11px] h-[550px] overflow-y-auto space-y-2.5 shadow-2xl">
            {logs.length === 0 ? (
              <div className="text-slate-600 italic">// Ready. Run an agent task to observe L402 challenge and PayPal capture in real time.</div>
            ) : (
              logs.map((log, idx) => {
                let badgeClass = 'text-blue-400';
                if (log.type === 'L402') badgeClass = 'text-amber-400 font-bold';
                if (log.type === 'SUCCESS') badgeClass = 'text-emerald-400 font-bold';
                if (log.type === 'ERROR') badgeClass = 'text-red-400 font-bold';

                return (
                  <div key={idx} className="leading-relaxed border-b border-slate-900 pb-2">
                    <span className="text-slate-600">[{log.time}]</span>{' '}
                    <span className={badgeClass}>[{log.type}]</span> {log.message}
                    {log.data && (
                      <pre className="mt-1 text-[10px] text-slate-400 bg-slate-900/80 p-2 rounded overflow-x-auto border border-slate-800">
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
    </div>
  );
};
