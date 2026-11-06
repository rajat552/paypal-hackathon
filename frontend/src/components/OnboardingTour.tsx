import React, { useState, useEffect, useRef, useCallback } from 'react';
import { 
  Compass, 
  X, 
  ChevronRight, 
  ChevronLeft, 
  CheckCircle2, 
  Sparkles, 
  HelpCircle,
  ExternalLink
} from 'lucide-react';

export interface TourStep {
  id: string;
  tab: 'workspace' | 'policy' | 'catalogue' | 'analytics' | 'publisher' | null;
  selector: string;
  title: string;
  description: string;
  badge?: string;
  preferredPosition?: 'top' | 'bottom' | 'left' | 'right' | 'center';
}

export const TOUR_STEPS: TourStep[] = [
  {
    id: 'welcome',
    tab: 'workspace',
    selector: '[data-tour="brand-header"]',
    title: 'Welcome to PayMesh AI',
    badge: 'Introduction',
    description: 'PayMesh AI provides trust and payment infrastructure for autonomous AI commerce. It connects HTTP 402 challenge negotiation with verified PayPal Sandbox Orders v2 captures and server-side policy enforcement.',
    preferredPosition: 'bottom',
  },
  {
    id: 'navigation',
    tab: 'workspace',
    selector: '[data-tour="nav-tabs"]',
    title: 'Main Navigation',
    badge: 'Overview',
    description: 'Switch between all 5 core modules: AI Commerce Agent, Spending Policy & Trust, API & Data Catalogue, Financial Ledger, and Merchant Studio.',
    preferredPosition: 'bottom',
  },
  {
    id: 'workspace',
    tab: 'workspace',
    selector: '[data-tour="scenario-selector"]',
    title: 'Agent Scenarios & Mission Presets',
    badge: 'Scenarios',
    description: 'Select a pre-configured procurement scenario—such as Channel3 Hardware Latency benchmarks or PayMesh Wire market feeds—to automatically load sample goals and spending limits.',
    preferredPosition: 'bottom',
  },
  {
    id: 'task-input',
    tab: 'workspace',
    selector: '[data-tour="agent-input-form"]',
    title: 'Research Task Input & Spending Limit',
    badge: 'Goal Formulation',
    description: 'Describe the data or intelligence you want the agent to purchase, and define a strict per-run spending limit in USD that the agent cannot exceed.',
    preferredPosition: 'top',
  },
  {
    id: 'dispatch-agent',
    tab: 'workspace',
    selector: '[data-tour="dispatch-button"]',
    title: 'Dispatch AI Agent',
    badge: 'Agent Execution',
    description: 'Dispatches the AI agent to search available resources, verify price limits against spending policies, and negotiate machine-readable payment challenges.',
    preferredPosition: 'top',
  },
  {
    id: 'protocol-inspector',
    tab: 'workspace',
    selector: '[data-tour="protocol-inspector"]',
    title: 'Real-Time Protocol Inspector',
    badge: 'L402 & MCP Stream',
    description: 'A live developer terminal showing Model Context Protocol (MCP) tool execution, state transitions, HTTP 402 challenge payloads, and server-side policy verifications.',
    preferredPosition: 'left',
  },
  {
    id: 'l402-challenge',
    tab: 'workspace',
    selector: '[data-tour="l402-challenge-section"]',
    title: 'L402 Payment Challenge & Negotiation',
    badge: 'HTTP 402 Standard',
    description: 'When an agent attempts to access a protected resource, the server responds with HTTP 402 Payment Required, containing pre-negotiated pricing and merchant terms under the L402 standard.',
    preferredPosition: 'bottom',
  },
  {
    id: 'spending-policy',
    tab: 'policy',
    selector: '[data-tour="policy-header"]',
    title: 'Spending Policies & Trust Engine',
    badge: 'Safety Guardrails',
    description: 'Large language models are probabilistic and susceptible to prompt injection. PayMesh AI removes payment authorization from the LLM, enforcing deterministic financial rules on the server.',
    preferredPosition: 'bottom',
  },
  {
    id: 'budget-gauge',
    tab: 'policy',
    selector: '[data-tour="budget-gauge"]',
    title: '24-Hour Rolling Budget Utilization',
    badge: 'Budget Controls',
    description: 'Track cumulative expenditures against your daily allowance in real time. This database-verified ceiling prevents runaway agent loops from overspending.',
    preferredPosition: 'bottom',
  },
  {
    id: 'policy-form',
    tab: 'policy',
    selector: '[data-tour="policy-form"]',
    title: 'Server-Enforced Constraints',
    badge: 'Rule Configuration',
    description: 'Configure maximum spend per transaction, daily quotas, prompt-injection sanitization, and strict dataset scope enforcement. Updates take effect immediately in runtime.',
    preferredPosition: 'top',
  },
  {
    id: 'catalogue',
    tab: 'catalogue',
    selector: '[data-tour="catalogue-header"]',
    title: 'API & Data Catalogue',
    badge: 'Data Marketplace',
    description: 'Browse verified datasets, hardware benchmark feeds, and market wires. Resources are protected by L402 paywalls and accessible through micro-payments.',
    preferredPosition: 'bottom',
  },
  {
    id: 'catalogue-agent-dispatch',
    tab: 'catalogue',
    selector: '[data-tour="catalogue-run-agent"]',
    title: 'Agent Resource Dispatch',
    badge: '1-Click Procurement',
    description: 'Clicking "Run Agent" on any catalogue card automatically routes back to the Workspace, pre-populating the agent prompt with the selected resource slug.',
    preferredPosition: 'top',
  },
  {
    id: 'paypal-checkout',
    tab: 'workspace',
    selector: '[data-tour="sandbox-status-badge"]',
    title: 'PayPal Sandbox Checkout & Capture',
    badge: 'Server Capture',
    description: 'Approved transactions trigger server-side PayPal Orders v2 captures via OAuth 2.0. No credit card credentials are ever exposed to the AI model or client code.',
    preferredPosition: 'bottom',
  },
  {
    id: 'settlement-ledger',
    tab: 'analytics',
    selector: '[data-tour="settlement-ledger"]',
    title: 'Financial Ledger & AG Grid Analytics',
    badge: 'Reconciliation',
    description: 'Review an immutable audit log of verified PayPal captures, active access tokens, conversion rates, and gross amounts. Export all ledger records directly to CSV.',
    preferredPosition: 'top',
  },
  {
    id: 'publisher-studio',
    tab: 'publisher',
    selector: '[data-tour="publisher-form"]',
    title: 'Merchant Studio & Developer Resources',
    badge: 'Publishing & Docs',
    description: 'Monetize proprietary APIs by configuring L402 pricing offers with auto-slug generation. Explore OpenAPI Swagger docs at /docs and replay this tour anytime from the header.',
    preferredPosition: 'top',
  },
];

interface OnboardingTourProps {
  activeTab: string;
  onNavigateTab: (tab: string) => void;
  isOpen: boolean;
  onClose: () => void;
  onStartTour: () => void;
}

export const OnboardingTour: React.FC<OnboardingTourProps> = ({
  activeTab,
  onNavigateTab,
  isOpen,
  onClose,
  onStartTour,
}) => {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [targetRect, setTargetRect] = useState<DOMRect | null>(null);
  const [popoverPos, setPopoverPos] = useState<{ top: number; left: number }>({ top: 100, left: 100 });
  const popoverRef = useRef<HTMLDivElement>(null);

  const currentStep = TOUR_STEPS[currentStepIndex];

  // Reset to step 0 whenever tour is opened
  useEffect(() => {
    if (isOpen) {
      setCurrentStepIndex(0);
    }
  }, [isOpen]);

  // 2. Measure & update target positioning
  const updateTargetPosition = useCallback(() => {
    if (!isOpen || !currentStep) return;

    const el = document.querySelector(currentStep.selector);
    if (!el) {
      // Element not in DOM yet or on another tab; fallback to centered
      setTargetRect(null);
      setPopoverPos({
        top: Math.max(80, window.innerHeight / 2 - 150),
        left: Math.max(20, window.innerWidth / 2 - 200),
      });
      return;
    }

    const rect = el.getBoundingClientRect();
    setTargetRect(rect);

    // Auto-scroll target into view if outside viewport
    const isInView = (
      rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
      rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );

    if (!isInView) {
      el.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'nearest' });
    }

    // Compute Popover Coordinates based on preferred position & viewport margins
    const popoverWidth = Math.min(420, window.innerWidth - 32);
    const popoverHeight = 240;
    const padding = 16;

    let top = rect.bottom + padding;
    let left = rect.left + (rect.width / 2) - (popoverWidth / 2);

    // If preferred is top or bottom overflows viewport
    if (currentStep.preferredPosition === 'top' || (top + popoverHeight > window.innerHeight && rect.top > popoverHeight + padding)) {
      top = rect.top - popoverHeight - padding;
    } else if (currentStep.preferredPosition === 'left' && rect.left > popoverWidth + padding) {
      top = rect.top;
      left = rect.left - popoverWidth - padding;
    } else if (currentStep.preferredPosition === 'right' && (rect.right + popoverWidth + padding < window.innerWidth)) {
      top = rect.top;
      left = rect.right + padding;
    }

    // Boundary constraints
    left = Math.max(16, Math.min(window.innerWidth - popoverWidth - 16, left));
    top = Math.max(80, Math.min(window.innerHeight - popoverHeight - 16, top));

    setPopoverPos({ top, left });
  }, [isOpen, currentStep]);

  // 3. Handle cross-tab navigation when step changes
  useEffect(() => {
    if (!isOpen || !currentStep) return;

    if (currentStep.tab && currentStep.tab !== activeTab) {
      onNavigateTab(currentStep.tab);
    }

    // Give DOM time to render newly selected tab
    const timer = setTimeout(() => {
      updateTargetPosition();
    }, 250);

    return () => clearTimeout(timer);
  }, [isOpen, currentStepIndex, currentStep, activeTab, onNavigateTab, updateTargetPosition]);

  // 4. Update on window resize or scroll
  useEffect(() => {
    if (!isOpen) return;

    const handleResizeOrScroll = () => {
      updateTargetPosition();
    };

    window.addEventListener('resize', handleResizeOrScroll, { passive: true });
    window.addEventListener('scroll', handleResizeOrScroll, { passive: true });

    return () => {
      window.removeEventListener('resize', handleResizeOrScroll);
      window.removeEventListener('scroll', handleResizeOrScroll);
    };
  }, [isOpen, updateTargetPosition]);

  // 5. Keyboard Navigation
  useEffect(() => {
    if (!isOpen) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        handleSkip();
      } else if (e.key === 'ArrowRight' || e.key === 'Enter') {
        if (currentStepIndex < TOUR_STEPS.length - 1) {
          handleNext();
        } else {
          handleFinish();
        }
      } else if (e.key === 'ArrowLeft') {
        handlePrev();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, currentStepIndex]);

  const handleNext = () => {
    if (currentStepIndex < TOUR_STEPS.length - 1) {
      setCurrentStepIndex((prev) => prev + 1);
    } else {
      handleFinish();
    }
  };

  const handlePrev = () => {
    if (currentStepIndex > 0) {
      setCurrentStepIndex((prev) => prev - 1);
    }
  };

  const handleFinish = () => {
    localStorage.setItem('paymesh_tour_completed', 'true');
    onClose();
  };

  const handleSkip = () => {
    localStorage.setItem('paymesh_tour_dismissed', 'true');
    onClose();
  };

  if (!isOpen || !currentStep) return null;

  const progressPct = Math.round(((currentStepIndex + 1) / TOUR_STEPS.length) * 100);

  return (
    <div className="fixed inset-0 pointer-events-auto" style={{ zIndex: 99990 }}>
      {/* 1. Backdrop Overlay with Spotlight Cutout */}
      <svg 
        className="absolute inset-0 w-full h-full pointer-events-none transition-all duration-300"
        style={{ zIndex: 99991 }}
      >
        <defs>
          <mask id="tour-spotlight-mask">
            <rect x="0" y="0" width="100%" height="100%" fill="white" />
            {targetRect && (
              <rect
                x={targetRect.left - 6}
                y={targetRect.top - 6}
                width={targetRect.width + 12}
                height={targetRect.height + 12}
                rx="14"
                ry="14"
                fill="black"
              />
            )}
          </mask>
        </defs>
        <rect
          x="0"
          y="0"
          width="100%"
          height="100%"
          fill="rgba(15, 23, 42, 0.72)"
          mask="url(#tour-spotlight-mask)"
        />
      </svg>

      {/* Target Active Highlight Border */}
      {targetRect && (
        <div
          className="fixed pointer-events-none rounded-2xl border-2 border-amber-400 shadow-[0_0_20px_rgba(251,191,36,0.6)] transition-all duration-300"
          style={{
            zIndex: 99992,
            top: targetRect.top - 6,
            left: targetRect.left - 6,
            width: targetRect.width + 12,
            height: targetRect.height + 12,
          }}
        />
      )}

      {/* 2. Interactive Tour Popover Card - Elevated with zIndex 99999 so it is 100% bright and highlighted above the backdrop */}
      <div
        ref={popoverRef}
        role="dialog"
        aria-label={`Onboarding Tour - Step ${currentStepIndex + 1} of ${TOUR_STEPS.length}`}
        className="fixed w-full max-w-[430px] bg-white border-2 border-slate-900 rounded-3xl p-5 sm:p-6 shadow-neo-lg animate-neo-pop space-y-4"
        style={{
          zIndex: 99999,
          top: `${popoverPos.top}px`,
          left: `${popoverPos.left}px`,
        }}
      >
        {/* Header: Badge & Controls */}
        <div className="flex items-center justify-between pb-3 border-b-2 border-slate-100">
          <div className="flex items-center space-x-2">
            <span className="text-[11px] font-mono font-black px-2.5 py-0.5 rounded-md bg-amber-300 text-slate-950 border-2 border-slate-900 shadow-[1px_1px_0px_0px_rgba(15,23,42,1)] uppercase">
              {currentStep.badge || `Step ${currentStepIndex + 1}`}
            </span>
            <span className="text-xs font-mono font-bold text-slate-500">
              {currentStepIndex + 1} / {TOUR_STEPS.length}
            </span>
          </div>

          <div className="flex items-center space-x-1.5">
            <button
              onClick={handleSkip}
              className="px-2 py-0.5 rounded text-[11px] font-mono font-bold text-slate-500 hover:text-slate-900 hover:bg-slate-100 transition"
              title="Exit Tour"
            >
              Exit
            </button>
            <button
              onClick={handleSkip}
              className="p-1 rounded-lg hover:bg-slate-100 text-slate-600 transition"
              aria-label="Close tour"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Content Body */}
        <div className="space-y-2">
          <h3 className="font-display font-black text-lg text-slate-900 leading-snug">
            {currentStep.title}
          </h3>
          <p className="text-xs text-slate-600 font-medium leading-relaxed font-sans">
            {currentStep.description}
          </p>
        </div>

        {/* Progress Bar */}
        <div className="space-y-1 pt-1">
          <div className="w-full h-2 bg-slate-100 rounded-full border border-slate-900 overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-amber-400 to-brand-500 rounded-full transition-all duration-300"
              style={{ width: `${progressPct}%` }}
            />
          </div>
          <div className="flex justify-between text-[10px] font-mono text-slate-400">
            <span>Progress: {progressPct}%</span>
            <span>Tab: {currentStep.tab ? currentStep.tab.toUpperCase() : 'GLOBAL'}</span>
          </div>
        </div>

        {/* Footer Navigation Buttons: Exit Tour on Left, Back & Next on Right */}
        <div className="flex items-center justify-between pt-2 border-t-2 border-slate-100 gap-2">
          <button
            onClick={handleSkip}
            className="px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-red-50 hover:text-red-700 hover:border-red-600 border-2 border-slate-900 text-xs font-mono font-bold text-slate-700 flex items-center space-x-1.5 shadow-neo-sm transition"
            title="Exit Tour Anytime"
          >
            <X className="w-3.5 h-3.5 stroke-[2.5]" />
            <span>Exit Tour</span>
          </button>

          <div className="flex items-center space-x-2">
            {currentStepIndex > 0 && (
              <button
                onClick={handlePrev}
                className="px-3 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 border-2 border-slate-900 text-xs font-mono font-bold text-slate-800 flex items-center space-x-1 shadow-neo-sm transition"
                title="Go Back to Previous Step"
              >
                <ChevronLeft className="w-3.5 h-3.5 stroke-[2.5]" />
                <span>Back</span>
              </button>
            )}

            <button
              onClick={handleNext}
              className="neo-button-amber py-2 px-4 text-xs font-black uppercase tracking-wider flex items-center space-x-1.5"
            >
              <span>{currentStepIndex === TOUR_STEPS.length - 1 ? 'Finish Tour 🎉' : 'Next Step'}</span>
              <ChevronRight className="w-3.5 h-3.5 stroke-[2.5]" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
