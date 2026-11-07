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
    description: 'PayMesh AI lets autonomous AI agents buy data and APIs safely using PayPal Sandbox—without giving the AI a credit card.',
    preferredPosition: 'bottom',
  },
  {
    id: 'navigation',
    tab: 'workspace',
    selector: '[data-tour="nav-tabs"]',
    title: 'Main Navigation Bar',
    badge: 'Overview',
    description: 'Use these tabs to switch between the AI Agent Studio, Spending Limits, API Catalogue, Financial Ledger, and Merchant Studio.',
    preferredPosition: 'bottom',
  },
  {
    id: 'workspace',
    tab: 'workspace',
    selector: '[data-tour="scenario-selector"]',
    title: 'Try a Sample Scenario',
    badge: 'Quick Start',
    description: 'Click a preset scenario—like Hardware Latency or Market Intelligence—to quickly test the AI agent with a sample goal and budget.',
    preferredPosition: 'bottom',
  },
  {
    id: 'task-input',
    tab: 'workspace',
    selector: '[data-tour="agent-input-form"]',
    title: 'Set Goal & Spending Limit',
    badge: 'Goal Setup',
    description: 'Type what data you want the AI to buy, and enter the maximum dollar amount (USD) the AI is allowed to spend.',
    preferredPosition: 'top',
  },
  {
    id: 'dispatch-agent',
    tab: 'workspace',
    selector: '[data-tour="dispatch-button"]',
    title: 'Run the AI Agent',
    badge: 'Execution',
    description: 'Click "Dispatch Agent" to let the AI search for the dataset and request a payment challenge within your budget.',
    preferredPosition: 'bottom',
  },
  {
    id: 'protocol-inspector',
    tab: 'workspace',
    selector: '[data-tour="protocol-inspector"]',
    title: 'Live Activity Terminal',
    badge: 'Live Log',
    description: 'Watch the AI agent\'s step-by-step actions, tool calls, and payment challenge messages in real time.',
    preferredPosition: 'left',
  },
  {
    id: 'l402-challenge',
    tab: 'workspace',
    selector: '[data-tour="l402-challenge-section"]',
    title: 'Payment Required (HTTP 402)',
    badge: 'Payment Protocol',
    description: 'When the AI requests paid data, the server returns a secure payment challenge with the exact price and access terms.',
    preferredPosition: 'bottom',
  },
  {
    id: 'spending-policy',
    tab: 'policy',
    selector: '[data-tour="policy-header"]',
    title: 'Spending Rules & Safety',
    badge: 'Safety Rules',
    description: 'Set hard financial rules on the server so the AI can never overspend or get tricked into unauthorized payments.',
    preferredPosition: 'bottom',
  },
  {
    id: 'budget-gauge',
    tab: 'policy',
    selector: '[data-tour="budget-gauge"]',
    title: 'Daily Budget Tracker',
    badge: 'Budget Tracker',
    description: 'See how much money has been spent in the last 24 hours against your daily limit in real time.',
    preferredPosition: 'bottom',
  },
  {
    id: 'policy-form',
    tab: 'policy',
    selector: '[data-tour="policy-form"]',
    title: 'Custom Limit Settings',
    badge: 'Rule Settings',
    description: 'Adjust the maximum spend per purchase, allowed currencies, and prompt safety guardrails.',
    preferredPosition: 'top',
  },
  {
    id: 'catalogue',
    tab: 'catalogue',
    selector: '[data-tour="catalogue-header"]',
    title: 'Dataset Marketplace',
    badge: 'Marketplace',
    description: 'Browse available intelligence feeds, switch latency benchmarks, and verified data for sale.',
    preferredPosition: 'bottom',
  },
  {
    id: 'catalogue-agent-dispatch',
    tab: 'catalogue',
    selector: '[data-tour="catalogue-run-agent"]',
    title: '1-Click Agent Purchase',
    badge: '1-Click Buy',
    description: 'Click "Run Agent" on any dataset card to instantly instruct the AI to purchase that specific dataset.',
    preferredPosition: 'bottom',
  },
  {
    id: 'paypal-checkout',
    tab: 'workspace',
    selector: '[data-tour="sandbox-status-badge"]',
    title: 'PayPal Sandbox Payments',
    badge: 'Verified Checkout',
    description: 'All purchases are safely tested and verified using PayPal Sandbox Orders v2 before unlocking data.',
    preferredPosition: 'bottom',
  },
  {
    id: 'settlement-ledger',
    tab: 'analytics',
    selector: '[data-tour="settlement-ledger"]',
    title: 'Financial Transaction Ledger',
    badge: 'Audit Ledger',
    description: 'Review every completed PayPal payment, capture ID, and timestamp in an interactive table with CSV export.',
    preferredPosition: 'top',
  },
  {
    id: 'publisher-studio',
    tab: 'publisher',
    selector: '[data-tour="publisher-form"]',
    title: 'Publish Your Own API',
    badge: 'Merchant Studio',
    description: 'Data sellers can publish new APIs, set custom prices, and earn money when AI agents buy their data.',
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
    const popoverWidth = Math.min(420, window.innerWidth - 32);
    const popoverHeight = popoverRef.current ? popoverRef.current.offsetHeight : 290;
    const padding = 20;
    const navbarHeight = 80;

    if (!el) {
      setTargetRect(null);
      setPopoverPos({
        top: Math.max(80, Math.round(window.innerHeight / 2 - 140)),
        left: Math.max(16, Math.round((window.innerWidth - popoverWidth) / 2)),
      });
      return;
    }

    const rect = el.getBoundingClientRect();
    if (rect.width === 0 || rect.height === 0) {
      return;
    }

    setTargetRect(rect);

    // Auto-scroll target into view if outside viewport
    const isInView = (
      rect.top >= 90 &&
      rect.bottom <= (window.innerHeight - 70)
    );

    if (!isInView) {
      el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    // Determine best position for popover (avoiding overlap with target)
    let top = 100;
    let left = rect.left + (rect.width / 2) - (popoverWidth / 2);

    const spaceAbove = rect.top;
    const spaceBelow = window.innerHeight - rect.bottom;
    const spaceLeft = rect.left;
    const spaceRight = window.innerWidth - rect.right;

    if (currentStep.preferredPosition === 'bottom' && spaceBelow >= popoverHeight + padding) {
      top = rect.bottom + padding;
    } else if (currentStep.preferredPosition === 'top' && (spaceAbove - navbarHeight) >= popoverHeight + padding) {
      top = rect.top - popoverHeight - padding;
    } else if (currentStep.preferredPosition === 'left' && spaceLeft >= popoverWidth + padding) {
      top = rect.top;
      left = rect.left - popoverWidth - padding;
    } else if (currentStep.preferredPosition === 'right' && spaceRight >= popoverWidth + padding) {
      top = rect.top;
      left = rect.right + padding;
    } else if (spaceBelow >= popoverHeight + padding) {
      top = rect.bottom + padding;
    } else if ((spaceAbove - navbarHeight) >= popoverHeight + padding) {
      top = rect.top - popoverHeight - padding;
    } else {
      top = Math.max(85, window.innerHeight - popoverHeight - 20);
    }

    // Clamp coordinates safely within screen
    left = Math.max(16, Math.min(window.innerWidth - popoverWidth - 16, left));
    top = Math.max(80, Math.min(window.innerHeight - popoverHeight - 16, top));

    setPopoverPos({ top: Math.round(top), left: Math.round(left) });
  }, [isOpen, currentStep]);

  // 3. Handle cross-tab navigation and multi-interval element locator
  useEffect(() => {
    if (!isOpen || !currentStep) return;

    if (currentStep.tab && currentStep.tab !== activeTab) {
      onNavigateTab(currentStep.tab);
    }

    // Staggered attempts to guarantee element is found even on async loads
    const intervals = [40, 120, 250, 450, 750, 1200, 1800];
    const timers = intervals.map((delay) =>
      setTimeout(() => {
        updateTargetPosition();
      }, delay)
    );

    return () => {
      timers.forEach(clearTimeout);
    };
  }, [isOpen, currentStepIndex, currentStep, activeTab, onNavigateTab, updateTargetPosition]);

  // 4. Update on window resize or scroll
  useEffect(() => {
    if (!isOpen || !currentStep) return;

    const handleResizeOrScroll = () => {
      const el = document.querySelector(currentStep.selector);
      if (el) {
        const rect = el.getBoundingClientRect();
        if (rect.width > 0 && rect.height > 0) {
          setTargetRect(rect);
        }
      }
    };

    window.addEventListener('resize', handleResizeOrScroll, { passive: true });
    window.addEventListener('scroll', handleResizeOrScroll, { passive: true });

    return () => {
      window.removeEventListener('resize', handleResizeOrScroll);
      window.removeEventListener('scroll', handleResizeOrScroll);
    };
  }, [isOpen, currentStep]);

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
    // Maintain current page (Step 15 is on Merchant Studio / last page)
    window.scrollTo({ top: 0, behavior: 'smooth' });
    setCurrentStepIndex(0);
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
      {/* 1. Backdrop Overlay & Focused Spotlight Cutout */}
      {targetRect ? (
        <div
          className="fixed pointer-events-none rounded-2xl transition-all duration-300"
          style={{
            zIndex: 99991,
            top: `${Math.round(targetRect.top - 8)}px`,
            left: `${Math.round(targetRect.left - 8)}px`,
            width: `${Math.round(targetRect.width + 16)}px`,
            height: `${Math.round(targetRect.height + 16)}px`,
            boxShadow: '0 0 0 9999px rgba(15, 23, 42, 0.76), 0 0 25px 6px rgba(245, 158, 11, 0.85)',
            border: '3px solid #F59E0B',
            outline: '2px solid rgba(255, 255, 255, 0.9)',
          }}
        >
          {/* Pulsing Target Indicator Badge */}
          <div className="absolute -top-3.5 left-4 px-2.5 py-0.5 rounded-full bg-amber-400 text-slate-950 font-mono text-[10px] font-black uppercase tracking-wider shadow-md flex items-center space-x-1.5 animate-pulse border border-slate-950">
            <span className="w-1.5 h-1.5 rounded-full bg-slate-950" />
            <span>Target Highlight</span>
          </div>
        </div>
      ) : (
        <div 
          className="fixed inset-0 bg-slate-950/75 pointer-events-none transition-opacity duration-300" 
          style={{ zIndex: 99991 }}
        />
      )}

      {/* 2. Interactive Tour Popover Card - Elevated with zIndex 99999 so it is 100% bright and highlighted above the backdrop */}
      <div
        ref={popoverRef}
        role="dialog"
        aria-label={`Onboarding Tour - Step ${currentStepIndex + 1} of ${TOUR_STEPS.length}`}
        className="fixed w-[calc(100vw-32px)] sm:w-full max-w-[430px] bg-white border-2 border-slate-900 rounded-2xl sm:rounded-3xl p-4 sm:p-6 shadow-neo-lg animate-neo-pop space-y-3.5 sm:space-y-4"
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
