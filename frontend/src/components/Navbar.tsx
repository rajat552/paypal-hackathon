import React from 'react';
import { Bot, Database, BarChart3, ShieldCheck, ShoppingBag, Sliders } from 'lucide-react';

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
    { id: 'publisher', label: 'Merchant Console', icon: ShoppingBag },
  ];

  return (
    <header className="border-b border-slate-800/80 bg-slate-900/90 backdrop-blur sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setActiveTab('workspace')}>
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-blue-600 via-indigo-600 to-cyan-500 flex items-center justify-center font-black text-white shadow-lg shadow-blue-500/25 ring-1 ring-white/20">
            PM
          </div>
          <div className="flex flex-col">
            <div className="flex items-center space-x-2">
              <span className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-white via-slate-100 to-slate-300 bg-clip-text text-transparent">
                PayMesh AI
              </span>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/25 font-mono font-medium">
                PayPal AI 2026
              </span>
            </div>
            <span className="text-[10px] text-slate-400 font-medium">
              Trust &amp; Payment Infrastructure for Autonomous AI Commerce
            </span>
          </div>
        </div>

        <nav className="hidden md:flex space-x-1">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-xs font-semibold transition ${
                  isActive
                    ? 'bg-blue-600 text-white shadow-md shadow-blue-600/25 ring-1 ring-blue-400/30'
                    : 'text-slate-400 hover:text-white hover:bg-slate-800/80'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </nav>

        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-mono">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>PayPal Sandbox Verified</span>
          </div>
        </div>
      </div>
    </header>
  );
};
