import React from 'react';
import { 
  ArrowLeft, 
  ArrowRight, 
  Bot, 
  ShieldCheck, 
  Database, 
  BarChart3, 
  ShoppingBag, 
  Compass, 
  AlertTriangle,
  Radio,
  ExternalLink
} from 'lucide-react';

interface NotFoundProps {
  onNavigateHome: () => void;
  onGoBack: () => void;
  onNavigateTab: (tab: string) => void;
  currentPath?: string;
}

export const NotFound: React.FC<NotFoundProps> = ({
  onNavigateHome,
  onGoBack,
  onNavigateTab,
  currentPath
}) => {
  // Determine displayed path/hash for diagnostics
  const displayRoute = currentPath || (typeof window !== 'undefined' 
    ? `${window.location.pathname}${window.location.hash || ''}`
    : '/404');

  const destinations = [
    {
      id: 'workspace',
      title: 'AI Commerce Agent',
      desc: 'Autonomous task execution, L402 challenge negotiation & PayPal capture.',
      icon: Bot,
      color: 'bg-amber-300'
    },
    {
      id: 'policy',
      title: 'Spending Policy & Trust',
      desc: 'Set per-transaction ceilings, daily limits, and merchant whitelists.',
      icon: ShieldCheck,
      color: 'bg-emerald-300'
    },
    {
      id: 'catalogue',
      title: 'API & Data Catalogue',
      desc: 'Explore monetized pay-per-call data streams and protected assets.',
      icon: Database,
      color: 'bg-blue-300'
    },
    {
      id: 'analytics',
      title: 'Financial Ledger',
      desc: 'Live AG Grid analytics, settlement statuses, and PayPal order records.',
      icon: BarChart3,
      color: 'bg-indigo-300'
    },
    {
      id: 'publisher',
      title: 'Merchant Studio',
      desc: 'Publish and monetize APIs with automated 402 challenge generation.',
      icon: ShoppingBag,
      color: 'bg-pink-300'
    }
  ];

  return (
    <div className="max-w-4xl mx-auto py-8 sm:py-12 animate-neo-pop">
      {/* Main 404 Neo-Card */}
      <div className="bg-white border-2 border-slate-900 rounded-2xl shadow-neo p-6 sm:p-10 relative overflow-hidden">
        {/* Subtle decorative grid overlay accent */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-amber-100/40 rounded-bl-full pointer-events-none -z-0"></div>

        {/* Status Badge & Protocol Header */}
        <div className="flex flex-wrap items-center justify-between gap-3 pb-6 border-b-2 border-slate-100 relative z-10">
          <div className="inline-flex items-center space-x-2 px-3 py-1 bg-amber-100 border-2 border-slate-900 rounded-lg text-xs font-mono font-bold text-slate-900 shadow-neo-sm">
            <span className="w-2 h-2 rounded-full bg-amber-500 animate-ping"></span>
            <span className="w-2 h-2 rounded-full bg-amber-500 -ml-3"></span>
            <span>HTTP 404 — ROUTE UNRESOLVED</span>
          </div>

          <div className="flex items-center space-x-2 text-xs font-mono text-slate-500">
            <Radio className="w-3.5 h-3.5 text-brand-600 animate-pulse" />
            <span>PROTOCOL: PAYMESH-MESH-ROUTER</span>
          </div>
        </div>

        {/* Central 404 Graphic & Hero Text */}
        <div className="py-8 text-center relative z-10">
          {/* Visual Mesh Diagnostic Node Diagram */}
          <div className="inline-flex items-center justify-center p-3 sm:p-4 mb-6 bg-slate-50 border-2 border-slate-900 rounded-2xl shadow-neo-sm">
            <div className="flex items-center space-x-2 sm:space-x-3 text-xs font-mono">
              <div className="flex items-center space-x-1 px-2.5 py-1 bg-emerald-100 border border-slate-900 rounded-md font-bold text-slate-900">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                <span>MESH NODE: ONLINE</span>
              </div>
              <span className="text-slate-400 font-bold">&rarr;</span>
              <div className="flex items-center space-x-1 px-2.5 py-1 bg-rose-100 border border-slate-900 rounded-md font-bold text-rose-900">
                <AlertTriangle className="w-3.5 h-3.5 text-rose-600" />
                <span className="truncate max-w-[150px] sm:max-w-[200px]">{displayRoute}</span>
              </div>
              <span className="text-slate-400 font-bold">&rarr;</span>
              <div className="px-2.5 py-1 bg-amber-100 border border-slate-900 rounded-md font-bold text-slate-900">
                <span>0x404 DISCONNECTED</span>
              </div>
            </div>
          </div>

          {/* Prominent 404 Title */}
          <div className="relative inline-block mb-3">
            <h1 className="font-display font-black text-7xl sm:text-9xl text-slate-900 tracking-tight select-none">
              404
            </h1>
            <div className="absolute -bottom-2 -right-4 px-2.5 py-0.5 bg-amber-400 border-2 border-slate-900 rounded-md font-mono text-xs font-black shadow-neo-sm rotate-6">
              LOST PACKET
            </div>
          </div>

          <h2 className="font-display font-black text-2xl sm:text-3xl text-slate-900 tracking-tight mt-2 mb-3">
            Looks like this page doesn't exist.
          </h2>

          <p className="text-sm sm:text-base text-slate-600 font-medium max-w-lg mx-auto leading-relaxed mb-6">
            The page you're looking for may have been moved, renamed, or is temporarily unavailable. Let's get you back to PayMesh AI.
          </p>

          {/* Diagnostic Route Info Bar */}
          <div className="max-w-md mx-auto mb-8 p-3 bg-slate-900 border-2 border-slate-900 rounded-xl text-left shadow-neo-sm">
            <div className="flex items-center justify-between text-[11px] font-mono text-slate-400 pb-1 border-b border-slate-800 mb-1.5">
              <span>UNRESOLVED_TARGET</span>
              <span className="text-amber-400">PAYMESH_ROUTER_V1</span>
            </div>
            <div className="font-mono text-xs text-amber-300 break-all">
              GET {displayRoute} &rarr; 404 NOT_FOUND
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-3.5 max-w-md mx-auto">
            <button
              onClick={onNavigateHome}
              className="w-full sm:w-auto flex-1 h-12 px-6 bg-amber-400 hover:bg-amber-300 border-2 border-slate-900 rounded-xl shadow-neo font-display font-bold text-sm text-slate-950 flex items-center justify-center space-x-2 hover:-translate-y-0.5 active:translate-y-0 transition-all cursor-pointer"
            >
              <span>Back to Home</span>
              <ArrowRight className="w-4 h-4" />
            </button>

            <button
              onClick={onGoBack}
              className="w-full sm:w-auto flex-1 h-12 px-6 bg-white hover:bg-slate-100 border-2 border-slate-900 rounded-xl shadow-neo font-display font-bold text-sm text-slate-800 flex items-center justify-center space-x-2 hover:-translate-y-0.5 active:translate-y-0 transition-all cursor-pointer"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Go Back</span>
            </button>
          </div>
        </div>

        {/* Quick Platform Destinations Section */}
        <div className="pt-8 border-t-2 border-slate-100 relative z-10">
          <div className="flex items-center justify-between mb-4">
            <span className="text-xs font-mono font-bold text-slate-500 uppercase tracking-wider">
              Or Jump Directly to Platform Sections:
            </span>
            <span className="text-xs font-mono text-slate-400">5 Active Modules</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
            {destinations.map((dest) => {
              const Icon = dest.icon;
              return (
                <button
                  key={dest.id}
                  onClick={() => onNavigateTab(dest.id)}
                  className="p-3.5 bg-slate-50 hover:bg-white border-2 border-slate-900 rounded-xl shadow-neo-sm hover:shadow-neo hover:-translate-y-0.5 transition-all text-left flex items-start space-x-3 group cursor-pointer"
                >
                  <div className={`p-2 rounded-lg border-2 border-slate-900 ${dest.color} shrink-0`}>
                    <Icon className="w-4 h-4 text-slate-900" />
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="font-display font-bold text-xs sm:text-sm text-slate-900 group-hover:text-brand-600 flex items-center justify-between">
                      <span className="truncate">{dest.title}</span>
                      <ExternalLink className="w-3 h-3 text-slate-400 group-hover:text-brand-600 opacity-0 group-hover:opacity-100 transition-opacity shrink-0 ml-1" />
                    </div>
                    <p className="text-[11px] text-slate-600 line-clamp-2 mt-0.5">
                      {dest.desc}
                    </p>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Subtitle Footer inside Card */}
        <div className="mt-8 pt-4 border-t border-slate-200 text-center relative z-10">
          <p className="text-xs font-mono text-slate-500">
            PayMesh AI &mdash; A Trust &amp; Payment Infrastructure for Autonomous AI Commerce.
          </p>
        </div>
      </div>
    </div>
  );
};

