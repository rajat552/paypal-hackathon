import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { AgentWorkspace } from './components/AgentWorkspace';
import { CatalogueView } from './components/CatalogueView';
import { AnalyticsView } from './components/AnalyticsView';
import { PublisherConsole } from './components/PublisherConsole';
import { PolicyManager } from './components/PolicyManager';
import { OnboardingTour } from './components/OnboardingTour';
import { 
  Terminal, 
  Database, 
  ExternalLink, 
  Github, 
  Layers, 
  Cpu, 
  ShieldCheck, 
  CreditCard,
  FileCode,
  BookOpen,
  Compass
} from 'lucide-react';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState('workspace');
  const [targetResourceSlug, setTargetResourceSlug] = useState<string | null>(null);
  // Launch tour directly whenever anyone visits or reloads the URL
  const [isTourOpen, setIsTourOpen] = useState(true);

  const handleSelectResource = (slug: string) => {
    setTargetResourceSlug(slug);
    setActiveTab('workspace');
  };

  const handleStartTour = () => {
    setIsTourOpen(true);
  };

  return (
    <div className="min-h-screen bg-blueprint-grid text-slate-900 flex flex-col font-sans selection:bg-amber-300 selection:text-slate-950">
      <Navbar 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        onStartTour={handleStartTour}
      />
      
      <main className="flex-1 max-w-7xl mx-auto px-4 py-8 sm:py-10 w-full">
        {activeTab === 'workspace' && (
          <AgentWorkspace 
            targetResourceSlug={targetResourceSlug} 
            onClearTarget={() => setTargetResourceSlug(null)} 
          />
        )}
        {activeTab === 'policy' && <PolicyManager />}
        {activeTab === 'catalogue' && <CatalogueView onSelectResource={handleSelectResource} />}
        {activeTab === 'analytics' && <AnalyticsView />}
        {activeTab === 'publisher' && <PublisherConsole onNavigateToCatalogue={() => setActiveTab('catalogue')} />}
      </main>

      <OnboardingTour
        activeTab={activeTab}
        onNavigateTab={setActiveTab}
        isOpen={isTourOpen}
        onClose={() => setIsTourOpen(false)}
        onStartTour={handleStartTour}
      />

      {/* Developer Ecosystem Footer inspired by MLH Reference Screenshot 3 */}
      <footer className="border-t-2 border-slate-900 bg-white py-12 text-slate-800 mt-16 shadow-inner">
        <div className="max-w-7xl mx-auto px-4 space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-center pb-8 border-b-2 border-slate-100">
            <div className="md:col-span-7 space-y-2">
              <div className="inline-flex items-center space-x-2 px-2.5 py-0.5 rounded-md bg-amber-300 text-slate-950 border-2 border-slate-900 font-mono text-[11px] font-bold shadow-neo-sm">
                <span>DEVELOPER PLATFORM &amp; STANDARDS</span>
              </div>
              <h3 className="font-display font-black text-xl sm:text-2xl text-slate-900 tracking-tight">
                Built for Developers, AI Agents &amp; Verified Payments
              </h3>
              <p className="text-xs sm:text-sm text-slate-600 font-medium max-w-xl leading-relaxed">
                PayMesh AI connects HTTP 402 challenge negotiation with PayPal Sandbox Orders v2 capture, server-enforced spending policies, and the Model Context Protocol (MCP) standard.
              </p>
            </div>

            {/* Square Ecosystem Links */}
            <div className="md:col-span-5 flex flex-wrap gap-2.5 justify-start md:justify-end">
              <a
                href="https://github.com/rajat552/paypal-hackathon"
                target="_blank"
                rel="noreferrer"
                className="h-11 px-3 bg-white hover:bg-amber-100 border-2 border-slate-900 rounded-xl shadow-neo-sm flex items-center space-x-2 text-xs font-mono font-bold text-slate-900 hover:-translate-y-0.5 transition-all"
                title="View GitHub Repository"
              >
                <Github className="w-4 h-4" />
                <span>GitHub</span>
              </a>

              <a
                href="/docs"
                target="_blank"
                rel="noreferrer"
                className="h-11 px-3 bg-white hover:bg-amber-100 border-2 border-slate-900 rounded-xl shadow-neo-sm flex items-center space-x-2 text-xs font-mono font-bold text-slate-900 hover:-translate-y-0.5 transition-all"
                title="Interactive Swagger OpenAPI"
              >
                <Terminal className="w-4 h-4 text-brand-600" />
                <span>Swagger</span>
              </a>

              <a
                href="/api/v1/agent/mcp/manifest"
                target="_blank"
                rel="noreferrer"
                className="h-11 px-3 bg-white hover:bg-amber-100 border-2 border-slate-900 rounded-xl shadow-neo-sm flex items-center space-x-2 text-xs font-mono font-bold text-slate-900 hover:-translate-y-0.5 transition-all"
                title="Model Context Protocol Manifest"
              >
                <Cpu className="w-4 h-4 text-indigo-600" />
                <span>MCP Manifest</span>
              </a>

              <a
                href="https://developer.paypal.com"
                target="_blank"
                rel="noreferrer"
                className="h-11 px-3 bg-white hover:bg-amber-100 border-2 border-slate-900 rounded-xl shadow-neo-sm flex items-center space-x-2 text-xs font-mono font-bold text-slate-900 hover:-translate-y-0.5 transition-all"
                title="PayPal Developer Portal"
              >
                <CreditCard className="w-4 h-4 text-brand-500" />
                <span>PayPal Sandbox</span>
              </a>

              <button
                onClick={handleStartTour}
                className="h-11 px-3 bg-amber-400 hover:bg-amber-300 border-2 border-slate-900 rounded-xl shadow-neo-sm flex items-center space-x-2 text-xs font-mono font-bold text-slate-950 hover:-translate-y-0.5 transition-all cursor-pointer"
                title="Start 15-Step Guided Tour"
              >
                <Compass className="w-4 h-4" />
                <span>Tour Guide</span>
              </button>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 text-xs font-mono text-slate-500">
            <div>
              <strong className="text-slate-800">PayMesh AI</strong> &bull; A Trust &amp; Payment Infrastructure for Autonomous AI Commerce &bull; PayPal AI Hackathon 2026
            </div>
            <div className="flex items-center space-x-4">
              <span>MIT License</span>
              <span>&bull;</span>
              <span>FastAPI + React 18 + AG Grid</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
