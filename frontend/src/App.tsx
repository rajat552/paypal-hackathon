import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { AgentWorkspace } from './components/AgentWorkspace';
import { CatalogueView } from './components/CatalogueView';
import { AnalyticsView } from './components/AnalyticsView';
import { PublisherConsole } from './components/PublisherConsole';
import { PolicyManager } from './components/PolicyManager';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState('workspace');

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <main className="flex-1 max-w-7xl mx-auto px-4 py-8 w-full">
        {activeTab === 'workspace' && <AgentWorkspace />}
        {activeTab === 'policy' && <PolicyManager />}
        {activeTab === 'catalogue' && <CatalogueView onSelectResource={() => setActiveTab('workspace')} />}
        {activeTab === 'analytics' && <AnalyticsView />}
        {activeTab === 'publisher' && <PublisherConsole />}
      </main>

      <footer className="border-t border-slate-900 bg-slate-950 py-6 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div>
            <strong>PayMesh AI</strong> &bull; A Trust &amp; Payment Infrastructure for Autonomous AI Commerce &bull; PayPal AI Hackathon 2026
          </div>
          <div className="flex items-center space-x-4">
            <a href="/docs" target="_blank" className="hover:text-slate-300">Swagger API</a>
            <a href="/api/v1/agent/mcp/manifest" target="_blank" className="hover:text-slate-300">MCP Manifest</a>
            <a href="https://github.com/rajat552/paypal-hackathon" target="_blank" rel="noreferrer" className="hover:text-slate-300">GitHub Repository</a>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
