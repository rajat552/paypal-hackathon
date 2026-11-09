import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { AgentWorkspace } from './components/AgentWorkspace';
import { CatalogueView, TargetResourcePayload } from './components/CatalogueView';
import { AnalyticsView } from './components/AnalyticsView';
import { PublisherConsole } from './components/PublisherConsole';
import { PolicyManager } from './components/PolicyManager';
import { OnboardingTour } from './components/OnboardingTour';
import { NotFound } from './components/NotFound';
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

const VALID_TABS = ['workspace', 'policy', 'catalogue', 'analytics', 'publisher'];

export interface CheckoutReturnPayload {
  status: 'success' | 'cancelled';
  sessionId?: string;
  token?: string;
  payerId?: string;
}

// Helper to check if current pathname or hash is an invalid route (404)
const isRouteNotFound = (): boolean => {
  if (typeof window === 'undefined') return false;
  const pathname = window.location.pathname.replace(/\/+$/, '') || '/';
  const hash = window.location.hash.replace(/^#/, '').toLowerCase();

  // PayPal Sandbox Return and Cancel routes are valid application endpoints
  if (pathname === '/checkout/success' || pathname === '/checkout/cancel') {
    return false;
  }

  // Explicit /404 path or #404 hash
  if (pathname === '/404' || hash === '404') {
    return true;
  }

  // Root path or index.html
  if (pathname === '/' || pathname === '/index.html') {
    // If there is a non-empty hash, it must be in VALID_TABS
    if (hash && !VALID_TABS.includes(hash)) {
      return true;
    }
    return false;
  }

  // If path directly matches one of our valid tabs (e.g. /workspace, /policy)
  const directTab = pathname.replace(/^\//, '').toLowerCase();
  if (VALID_TABS.includes(directTab)) {
    return false;
  }

  // Any other unknown path is a 404
  return true;
};

export const App: React.FC = () => {
  // Read initial tab from URL hash (e.g. #publisher), direct pathname, or localStorage
  const getInitialTab = (): string => {
    if (typeof window !== 'undefined') {
      const pathname = window.location.pathname;
      if (pathname === '/checkout/success' || pathname === '/checkout/cancel') {
        return 'workspace';
      }

      const hash = window.location.hash.replace('#', '').toLowerCase();
      if (VALID_TABS.includes(hash)) return hash;

      const directTab = window.location.pathname.replace(/^\//, '').toLowerCase();
      if (VALID_TABS.includes(directTab)) return directTab;

      const saved = localStorage.getItem('paymesh_active_tab');
      if (saved && VALID_TABS.includes(saved)) return saved;
    }
    return 'workspace';
  };

  const [isNotFound, setIsNotFound] = useState<boolean>(isRouteNotFound);
  const [currentPath, setCurrentPath] = useState<string>(() => {
    if (typeof window !== 'undefined') {
      return `${window.location.pathname}${window.location.hash}`;
    }
    return '/';
  });

  const [checkoutReturn, setCheckoutReturn] = useState<CheckoutReturnPayload | null>(() => {
    if (typeof window === 'undefined') return null;
    const pathname = window.location.pathname;
    const params = new URLSearchParams(window.location.search);
    if (pathname === '/checkout/success') {
      return {
        status: 'success',
        sessionId: params.get('session_id') || undefined,
        token: params.get('token') || undefined,
        payerId: params.get('PayerID') || undefined,
      };
    }
    if (pathname === '/checkout/cancel') {
      return {
        status: 'cancelled',
        sessionId: params.get('session_id') || undefined,
        token: params.get('token') || undefined,
      };
    }
    return null;
  });

  const [activeTab, setActiveTabState] = useState<string>(getInitialTab);
  const [targetResource, setTargetResource] = useState<TargetResourcePayload | null>(null);

  // Auto-launch tour only on initial visit if neither completed nor dismissed
  const [isTourOpen, setIsTourOpen] = useState<boolean>(() => {
    if (typeof window !== 'undefined') {
      const completed = localStorage.getItem('paymesh_tour_completed');
      const dismissed = localStorage.getItem('paymesh_tour_dismissed');
      return !completed && !dismissed;
    }
    return false;
  });

  const setActiveTab = (tab: string) => {
    setIsNotFound(false);
    setActiveTabState(tab);
    if (typeof window !== 'undefined') {
      localStorage.setItem('paymesh_active_tab', tab);
      if (window.location.pathname !== '/' && window.location.pathname !== '/index.html') {
        window.history.pushState(null, '', `/#${tab}`);
        setCurrentPath(`/#${tab}`);
      } else if (window.location.hash !== `#${tab}`) {
        window.location.hash = tab;
        setCurrentPath(`/#${tab}`);
      }
    }
  };

  const handleBackToHome = () => {
    setIsNotFound(false);
    setActiveTab('workspace');
    if (typeof window !== 'undefined') {
      window.history.pushState(null, '', '/#workspace');
      setCurrentPath('/#workspace');
    }
  };

  const handleGoBack = () => {
    if (typeof window !== 'undefined' && window.history.length > 1) {
      window.history.back();
      setTimeout(() => {
        if (isRouteNotFound()) {
          handleBackToHome();
        } else {
          setIsNotFound(false);
        }
      }, 150);
    } else {
      handleBackToHome();
    }
  };

  const handleNavigateTab = (tab: string) => {
    setIsNotFound(false);
    setActiveTab(tab);
  };

  // Sync tab with browser back/forward history navigation and hash changes
  React.useEffect(() => {
    const handleLocationChange = () => {
      const notFound = isRouteNotFound();
      setIsNotFound(notFound);
      setCurrentPath(`${window.location.pathname}${window.location.hash}`);

      if (!notFound) {
        const pathname = window.location.pathname;
        const params = new URLSearchParams(window.location.search);
        if (pathname === '/checkout/success') {
          setActiveTabState('workspace');
          setCheckoutReturn({
            status: 'success',
            sessionId: params.get('session_id') || undefined,
            token: params.get('token') || undefined,
            payerId: params.get('PayerID') || undefined,
          });
          return;
        }
        if (pathname === '/checkout/cancel') {
          setActiveTabState('workspace');
          setCheckoutReturn({
            status: 'cancelled',
            sessionId: params.get('session_id') || undefined,
            token: params.get('token') || undefined,
          });
          return;
        }

        const hash = window.location.hash.replace('#', '').toLowerCase();
        if (VALID_TABS.includes(hash)) {
          setActiveTabState(hash);
          localStorage.setItem('paymesh_active_tab', hash);
        } else {
          const directTab = window.location.pathname.replace(/^\//, '').toLowerCase();
          if (VALID_TABS.includes(directTab)) {
            setActiveTabState(directTab);
            localStorage.setItem('paymesh_active_tab', directTab);
          }
        }
      }
    };

    window.addEventListener('popstate', handleLocationChange);
    window.addEventListener('hashchange', handleLocationChange);
    return () => {
      window.removeEventListener('popstate', handleLocationChange);
      window.removeEventListener('hashchange', handleLocationChange);
    };
  }, []);

  const handleSelectResource = (target: TargetResourcePayload) => {
    setTargetResource(target);
    setActiveTab('workspace');
  };

  const handleStartTour = () => {
    setIsTourOpen(true);
  };

  return (
    <div className="min-h-screen bg-blueprint-grid text-slate-900 flex flex-col font-sans selection:bg-amber-300 selection:text-slate-950 overflow-x-hidden w-full">
      <Navbar 
        activeTab={isNotFound ? '' : activeTab} 
        setActiveTab={setActiveTab} 
        onStartTour={handleStartTour}
      />
      
      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 pt-8 sm:pt-12 pb-12 sm:pb-16 w-full">
        {isNotFound ? (
          <NotFound 
            onNavigateHome={handleBackToHome}
            onGoBack={handleGoBack}
            onNavigateTab={handleNavigateTab}
            currentPath={currentPath}
          />
        ) : (
          <>
            <div className={activeTab === 'workspace' ? 'block' : 'hidden'}>
              <AgentWorkspace 
                targetResource={targetResource} 
                onClearTarget={() => setTargetResource(null)} 
                checkoutReturn={checkoutReturn}
                onClearCheckoutReturn={() => setCheckoutReturn(null)}
              />
            </div>
            {activeTab === 'policy' && <PolicyManager />}
            {activeTab === 'catalogue' && <CatalogueView onSelectResource={handleSelectResource} />}
            {activeTab === 'analytics' && <AnalyticsView />}
            {activeTab === 'publisher' && <PublisherConsole onNavigateToCatalogue={() => setActiveTab('catalogue')} />}
          </>
        )}
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
                rel="noopener noreferrer"
                className="h-11 px-3 bg-white hover:bg-amber-100 border-2 border-slate-900 rounded-xl shadow-neo-sm flex items-center space-x-2 text-xs font-mono font-bold text-slate-900 hover:-translate-y-0.5 transition-all"
                title="View GitHub Repository"
              >
                <Github className="w-4 h-4" />
                <span>GitHub</span>
              </a>

              <a
                href="/docs"
                target="_blank"
                rel="noopener noreferrer"
                className="h-11 px-3 bg-white hover:bg-amber-100 border-2 border-slate-900 rounded-xl shadow-neo-sm flex items-center space-x-2 text-xs font-mono font-bold text-slate-900 hover:-translate-y-0.5 transition-all"
                title="Interactive Swagger OpenAPI"
              >
                <Terminal className="w-4 h-4 text-brand-600" />
                <span>Swagger</span>
              </a>

              <a
                href="/api/v1/agent/mcp/manifest"
                target="_blank"
                rel="noopener noreferrer"
                className="h-11 px-3 bg-white hover:bg-amber-100 border-2 border-slate-900 rounded-xl shadow-neo-sm flex items-center space-x-2 text-xs font-mono font-bold text-slate-900 hover:-translate-y-0.5 transition-all"
                title="Model Context Protocol Manifest"
              >
                <Cpu className="w-4 h-4 text-indigo-600" />
                <span>MCP Manifest</span>
              </a>

              <a
                href="https://developer.paypal.com"
                target="_blank"
                rel="noopener noreferrer"
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
