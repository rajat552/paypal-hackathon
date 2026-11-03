import React, { useEffect, useState } from 'react';
import { Database, ShieldCheck, ArrowRight, Tag, Layers, RefreshCw } from 'lucide-react';

interface Offer {
  id: string;
  offer_code: string;
  title: string;
  description: string;
  amount: number;
  currency: string;
  pricing_model: string;
  duration_seconds: number;
}

interface Resource {
  id: string;
  slug: string;
  title: string;
  description: string;
  resource_type: string;
  provider: string;
  publisher_name: string;
  offers: Offer[];
}

export const CatalogueView: React.FC<{ onSelectResource?: (slug: string) => void }> = ({ onSelectResource }) => {
  const [resources, setResources] = useState<Resource[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchCatalogue = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/catalogue');
      const data = await res.json();
      setResources(data.resources || []);
    } catch (e) {
      console.error('Failed to load catalogue', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCatalogue();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white">PayMesh AI — API &amp; Data Marketplace</h2>
          <p className="text-xs text-slate-400">Discover publisher datasets, APIs, and machine-readable pricing offers.</p>
        </div>
        <button
          onClick={fetchCatalogue}
          className="flex items-center space-x-1 text-xs bg-slate-800 hover:bg-slate-700 px-3 py-1.5 rounded-lg text-slate-300 transition"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh</span>
        </button>
      </div>

      {loading ? (
        <div className="p-12 text-center text-slate-500 font-mono text-sm">Loading catalogue...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {resources.map((res) => (
            <div key={res.id} className="p-6 rounded-2xl bg-slate-900 border border-slate-800 hover:border-slate-700 transition flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">
                    {res.provider.toUpperCase()}
                  </span>
                  <span className="text-xs text-slate-400 font-mono">/{res.slug}</span>
                </div>
                <h3 className="text-lg font-bold text-white mb-2">{res.title}</h3>
                <p className="text-xs text-slate-400 mb-4 leading-relaxed">{res.description}</p>
                
                <div className="space-y-2 mb-4">
                  <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">Available Plans:</span>
                  {res.offers.map((offer) => (
                    <div key={offer.id} className="p-2.5 rounded-lg bg-slate-950 border border-slate-800/80 flex items-center justify-between text-xs">
                      <div>
                        <div className="font-semibold text-white">{offer.title}</div>
                        <div className="text-[11px] text-slate-500 font-mono">Duration: {Math.round(offer.duration_seconds / 60)} mins &bull; Model: {offer.pricing_model}</div>
                      </div>
                      <div className="font-extrabold text-emerald-400 font-mono text-sm">
                        ${offer.amount.toFixed(2)} {offer.currency}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="pt-4 border-t border-slate-800 flex items-center justify-between">
                <span className="text-xs text-slate-500">{res.publisher_name}</span>
                <a
                  href={`/api/v1/resources/${res.slug}/content`}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center space-x-1.5 text-xs text-blue-400 hover:text-blue-300 font-semibold"
                >
                  <span>Test 402 Endpoint</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </a>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
