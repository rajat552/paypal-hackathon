import React from 'react';
import { Bot, Database, BarChart3, ShieldCheck, ShoppingBag, Terminal, CheckCircle2 } from 'lucide-react';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({ activeTab, setActiveTab }) => {
  const tabs = [
    { id: 'workspace', label: 'AI Commerce Agent', icon: Bot },
    { id: 'policy', label: 'Spending Policy & Trust', icon: ShieldCheck },
    { id: 'catalogue', label: 'API & Data Catalogue', icon: Database },
    { id: 'analytics', label: 'Financial Ledger (AG Grid)', icon: BarChart3 },
    { id: 'publisher', label: 'Merchant Studio', icon: ShoppingBag },
  ];

  return (
    <header className="border-b-2 border-slate-900 bg-white sticky top-0 z-50 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 h-20 flex items-center justify-between">
        {/* Brand Logo & Tagline */}
        <div 
          className="flex items-center space-x-3.5 cursor-pointer group"
          onClick={() => setActiveTab('workspace')}
        >
          {/* Isometric Neo-Tech Logo Icon */}
          <div className="relative">
            <div className="h-11 w-11 rounded-xl bg-gradient-to-br from-brand-500 via-brand-600 to-amber-400 border-2 border-slate-900 flex items-center justify-center font-black text-white text-base shadow-neo-sm group-hover:-translate-y-0.5 group-hover:shadow-neo transition-all">
              <span className="drop-shadow">PM</span>
            </div>
            <div className="absolute -top-1 -right-1 w-3.5 h-3.5 bg-amber-400 border-2 border-slate-900 rounded-full flex items-center justify-center">
              <span className="w-1 h-1 bg-slate-900 rounded-full"></span>
            </div>
          </div>

          <div className="flex flex-col">
            <div className="flex items-center space-x-2">
              <span className="font-display font-black text-xl tracking-tight text-slate-900 group-hover:text-brand-600 transition-colors">
                PayMesh<span className="text-amber-500">.AI</span>
              </span>
              <span className="text-[10px] px-2 py-0.5 rounded-md bg-amber-300 text-slate-950 border-2 border-slate-900 font-mono font-bold shadow-[1px_1px_0px_0px_rgba(15,23,42,1)]">
                PAYPAL HACKATHON 2026
              </span>
            </div>
            <span className="text-xs text-slate-600 font-medium hidden sm:inline-block">
              A Trust &amp; Payment Infrastructure for Autonomous AI Commerce
            </span>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="hidden lg:flex items-center space-x-2">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-3.5 py-2 rounded-xl text-xs font-bold transition-all ${
                  isActive
                    ? 'bg-amber-400 text-slate-950 border-2 border-slate-900 shadow-neo-sm translate-x-[-1px] translate-y-[-1px]'
                    : 'text-slate-700 hover:text-slate-950 hover:bg-slate-100 border-2 border-transparent hover:border-slate-300'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-slate-950' : 'text-slate-500'}`} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>

        {/* Sandbox Status & Quick Links */}
        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2 px-3 py-1.5 rounded-xl bg-emerald-50 border-2 border-emerald-800 text-emerald-950 text-xs font-mono font-bold shadow-[2px_2px_0px_0px_rgba(6,78,59,1)]">
            <span className="relative flex h-2.5 w-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-600"></span>
            </span>
            <span className="hidden sm:inline">PayPal Sandbox</span>
            <span className="text-[10px] px-1 py-0.2 bg-emerald-200 text-emerald-900 rounded border border-emerald-700">Orders v2</span>
          </div>

          <a
            href="/docs"
            target="_blank"
            rel="noreferrer"
            className="hidden md:flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-white border-2 border-slate-900 text-xs font-mono font-bold text-slate-800 hover:bg-amber-100 shadow-neo-sm hover:-translate-y-0.5 transition-all"
            title="Interactive OpenAPI / Swagger Documentation"
          >
            <Terminal className="w-3.5 h-3.5 text-brand-600" />
            <span>API Docs</span>
          </a>
        </div>
      </div>

      {/* Mobile Tab Navigation Bar */}
      <div className="lg:hidden border-t border-slate-200 px-4 py-2 flex overflow-x-auto space-x-2 bg-slate-50">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-bold whitespace-nowrap transition-all ${
                isActive
                  ? 'bg-amber-400 text-slate-950 border-2 border-slate-900 shadow-sm'
                  : 'text-slate-600 hover:bg-slate-200'
              }`}
            >
              <Icon className="w-3.5 h-3.5" />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </div>
    </header>
  );
};
