import React, { useState } from 'react';
import { Bot, Database, BarChart3, ShieldCheck, ShoppingBag, Terminal, Cpu, Menu, X, Compass } from 'lucide-react';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  onStartTour?: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ activeTab, setActiveTab, onStartTour }) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const tabs = [
    { id: 'workspace', label: 'AI Commerce Agent', shortLabel: 'Agent', icon: Bot },
    { id: 'policy', label: 'Spending Policy & Trust', shortLabel: 'Policy', icon: ShieldCheck },
    { id: 'catalogue', label: 'API & Data Catalogue', shortLabel: 'Catalogue', icon: Database },
    { id: 'analytics', label: 'Financial Ledger', shortLabel: 'Ledger', icon: BarChart3 },
    { id: 'publisher', label: 'Merchant Studio', shortLabel: 'Merchant', icon: ShoppingBag },
  ];

  const handleTabClick = (tabId: string) => {
    setActiveTab(tabId);
    setMobileMenuOpen(false);
  };

  return (
    <header className="border-b-2 border-slate-900 bg-white sticky top-0 z-50 shadow-sm">
      <div className="max-w-7xl mx-auto px-3 sm:px-4 h-16 sm:h-20 flex items-center justify-between">
        {/* Brand Logo & Tagline */}
        <div 
          data-tour="brand-header"
          className="flex items-center space-x-2.5 sm:space-x-3.5 cursor-pointer group shrink-0"
          onClick={() => handleTabClick('workspace')}
        >
          {/* Isometric Neo-Tech Logo Icon */}
          <div className="relative shrink-0">
            <div className="h-9 w-9 sm:h-11 sm:w-11 rounded-xl bg-gradient-to-br from-brand-500 via-brand-600 to-amber-400 border-2 border-slate-900 flex items-center justify-center font-black text-white text-sm sm:text-base shadow-neo-sm group-hover:-translate-y-0.5 group-hover:shadow-neo transition-all">
              <span className="drop-shadow">PM</span>
            </div>
            <div className="absolute -top-1 -right-1 w-3 h-3 sm:w-3.5 sm:h-3.5 bg-amber-400 border-2 border-slate-900 rounded-full flex items-center justify-center">
              <span className="w-1 h-1 bg-slate-900 rounded-full"></span>
            </div>
          </div>

          <span className="font-display font-black text-lg sm:text-xl tracking-tight text-slate-900 group-hover:text-brand-600 transition-colors whitespace-nowrap">
            PayMesh<span className="text-amber-500">.AI</span>
          </span>
        </div>

        {/* Desktop Navigation Tabs (Compact at lg: 1024px, Full at xl: 1280px+) */}
        <nav data-tour="nav-tabs" className="hidden lg:flex items-center space-x-2 xl:space-x-3.5">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => handleTabClick(tab.id)}
                className={`flex items-center space-x-2 xl:space-x-2.5 px-3 xl:px-4 py-2 rounded-xl text-xs font-bold transition-all whitespace-nowrap ${
                  isActive
                    ? 'bg-amber-400 text-slate-950 border-2 border-slate-900 shadow-neo-sm translate-x-[-1px] translate-y-[-1px]'
                    : 'text-slate-700 hover:text-slate-950 hover:bg-slate-100 border-2 border-transparent hover:border-slate-300'
                }`}
              >
                <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-slate-950' : 'text-slate-500'}`} />
                <span className="hidden xl:inline">{tab.label}</span>
                <span className="inline xl:hidden">{tab.shortLabel}</span>
              </button>
            );
          })}
        </nav>

        {/* Status Badges & Controls */}
        <div className="flex items-center space-x-2 sm:space-x-3 shrink-0">
          {onStartTour && (
            <button
              onClick={onStartTour}
              className="hidden md:flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-amber-400 hover:bg-amber-300 border-2 border-slate-900 text-xs font-mono font-bold text-slate-950 shadow-neo-sm hover:-translate-y-0.5 transition-all whitespace-nowrap"
              title="Start 15-Step Guided Tour"
            >
              <Compass className="w-3.5 h-3.5" />
              <span>Tour Guide</span>
            </button>
          )}

          <div 
            data-tour="sandbox-status-badge"
            className="flex items-center space-x-1.5 sm:space-x-2 px-2 sm:px-3 py-1.5 rounded-xl bg-emerald-50 border-2 border-emerald-800 text-emerald-950 text-xs font-mono font-bold shadow-[2px_2px_0px_0px_rgba(6,78,59,1)] cursor-help shrink-0"
            title="PayPal Sandbox (Test Environment) — OAuth 2.0 and Orders v2 server-side capture active"
          >
            <span className="relative flex h-2.5 w-2.5 shrink-0">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-600"></span>
            </span>
            <span className="hidden sm:inline">PayPal Sandbox</span>
            <span className="text-[10px] px-1 py-0.2 bg-emerald-200 text-emerald-900 rounded border border-emerald-700 whitespace-nowrap">Orders v2</span>
          </div>

          <a
            href="/docs"
            target="_blank"
            rel="noopener noreferrer"
            className="hidden xl:flex items-center space-x-1.5 px-3 py-1.5 rounded-xl bg-white border-2 border-slate-900 text-xs font-mono font-bold text-slate-800 hover:bg-amber-100 shadow-neo-sm hover:-translate-y-0.5 transition-all whitespace-nowrap"
            title="Interactive REST API Documentation (OpenAPI / Swagger)"
          >
            <Terminal className="w-3.5 h-3.5 text-brand-600" />
            <span>API Docs</span>
          </a>

          {/* Mobile Menu Button - Accessible 44x44px Touch Target */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="lg:hidden w-10 h-10 sm:w-11 sm:h-11 flex items-center justify-center rounded-xl bg-slate-100 border-2 border-slate-900 text-slate-900 shadow-neo-sm hover:bg-slate-200 active:translate-y-0.5 transition"
            aria-label="Toggle Navigation Menu"
            aria-expanded={mobileMenuOpen}
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Animated Drawer */}
      {mobileMenuOpen && (
        <div className="lg:hidden border-t-2 border-slate-900 bg-white px-4 py-3 space-y-2 animate-neo-pop shadow-md max-h-[calc(100vh-5rem)] overflow-y-auto">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => handleTabClick(tab.id)}
                className={`w-full min-h-[44px] flex items-center space-x-3 px-3.5 py-2.5 rounded-xl text-xs font-bold transition-all ${
                  isActive
                    ? 'bg-amber-400 text-slate-950 border-2 border-slate-900 shadow-neo-sm'
                    : 'text-slate-700 hover:bg-slate-100 border-2 border-transparent'
                }`}
              >
                <Icon className="w-4 h-4 shrink-0" />
                <span>{tab.label}</span>
              </button>
            );
          })}
          {onStartTour && (
            <button
              onClick={() => {
                setMobileMenuOpen(false);
                onStartTour();
              }}
              className="w-full min-h-[44px] flex items-center space-x-3 px-3.5 py-2.5 rounded-xl text-xs font-bold bg-amber-400 text-slate-950 border-2 border-slate-900 shadow-neo-sm hover:bg-amber-300 transition"
            >
              <Compass className="w-4 h-4 text-slate-950 shrink-0" />
              <span>Take Interactive Tour (15 Steps)</span>
            </button>
          )}
          <div className="pt-2 border-t border-slate-200 flex justify-between gap-2">
            <a
              href="/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 min-h-[40px] flex items-center justify-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-100 border border-slate-300 text-xs font-mono font-bold text-slate-800 hover:bg-amber-100 transition"
            >
              <Terminal className="w-3.5 h-3.5 text-brand-600" />
              <span>Swagger /docs</span>
            </a>
            <a
              href="/api/v1/agent/mcp/manifest"
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 min-h-[40px] flex items-center justify-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-100 border border-slate-300 text-xs font-mono font-bold text-slate-800 hover:bg-amber-100 transition"
            >
              <Cpu className="w-3.5 h-3.5 text-indigo-600" />
              <span>MCP Manifest</span>
            </a>
          </div>
        </div>
      )}
    </header>
  );
};
