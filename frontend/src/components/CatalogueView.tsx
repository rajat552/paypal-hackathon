import React, { useEffect, useState } from 'react';
import { Database, ShieldCheck, ArrowRight, Tag, Layers, RefreshCw, ExternalLink, Search, Cpu, Globe, Filter, X } from 'lucide-react';

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
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');

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

  const categories = [
    { id: 'all', label: 'All Products' },
    { id: 'channel3', label: 'Channel3 Hardware' },
    { id: 'paymesh_wire', label: 'PayMesh Wire & Feeds' },
  ];

  const filteredResources = resources.filter(r => {
    const matchesSearch = 
      r.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      r.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
      r.provider.toLowerCase().includes(searchTerm.toLowerCase()) ||
      r.slug.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesCategory = 
      selectedCategory === 'all' || 
      r.provider.toLowerCase() === selectedCategory.toLowerCase() ||
      (selectedCategory === 'paymesh_wire' && (r.provider.toLowerCase() === 'paymesh_wire' || r.provider.toLowerCase() === 'crawlerpal_demo'));

    return matchesSearch && matchesCategory;
  });

  return (
    <div className="space-y-8">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b-2 border-slate-900">
        <div>
          <div className="inline-flex items-center space-x-2 px-3 py-0.5 rounded-full bg-blue-100 text-blue-900 border-2 border-slate-900 font-mono text-xs font-bold shadow-neo-sm mb-2">
            <Database className="w-3.5 h-3.5 text-brand-600" />
            <span>RESOURCE &amp; DATA REGISTRY</span>
          </div>
          <h2 className="font-display font-black text-2xl sm:text-3xl text-slate-900 tracking-tight">
            API &amp; Data Product Marketplace
          </h2>
          <p className="text-xs sm:text-sm text-slate-600 font-medium">
            Browse verified data feeds, benchmark datasets, and resources protected by L402 paywalls.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search datasets..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="bg-white border-2 border-slate-900 rounded-xl pl-9 pr-3.5 py-2 text-xs font-mono font-bold text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-brand-500 shadow-neo-sm"
            />
            {searchTerm && (
              <button 
                onClick={() => setSearchTerm('')}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-700"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            )}
          </div>

          <button
            onClick={fetchCatalogue}
            className="p-2.5 rounded-xl bg-white hover:bg-slate-100 border-2 border-slate-900 text-slate-900 shadow-neo-sm hover:-translate-y-0.5 transition-all"
            title="Refresh Dataset Directory"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Category Filter Chips */}
      <div className="flex items-center space-x-2 overflow-x-auto pb-1">
        <Filter className="w-3.5 h-3.5 text-slate-500 mr-1 flex-shrink-0" />
        {categories.map((cat) => (
          <button
            key={cat.id}
            onClick={() => setSelectedCategory(cat.id)}
            className={`px-3 py-1.5 rounded-xl text-xs font-mono font-bold transition-all whitespace-nowrap ${
              selectedCategory === cat.id
                ? 'bg-amber-400 text-slate-950 border-2 border-slate-900 shadow-neo-sm'
                : 'bg-white text-slate-700 hover:bg-slate-100 border-2 border-slate-300'
            }`}
          >
            {cat.label}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="p-16 text-center text-slate-500 font-mono text-sm bg-white border-2 border-slate-900 rounded-2xl shadow-neo">
          // Loading resource catalogue...
        </div>
      ) : filteredResources.length === 0 ? (
        <div className="p-16 text-center bg-white border-2 border-slate-900 rounded-2xl shadow-neo space-y-3">
          <div className="font-display font-extrabold text-slate-900 text-base">
            No matching datasets found
          </div>
          <p className="text-xs text-slate-500 font-mono">
            No products match the filter "{searchTerm || selectedCategory}".
          </p>
          <button
            onClick={() => { setSearchTerm(''); setSelectedCategory('all'); }}
            className="px-4 py-2 rounded-xl bg-amber-400 border-2 border-slate-900 text-xs font-mono font-bold text-slate-950 shadow-neo-sm"
          >
            Reset Filters
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filteredResources.map((res) => (
            <div 
              key={res.id} 
              className="p-6 rounded-2xl bg-white border-2 border-slate-900 shadow-neo hover:shadow-neo-lg hover:-translate-y-1 transition-all flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between mb-3.5">
                  <div className="flex items-center space-x-2">
                    <span className="text-[11px] font-mono font-black px-2.5 py-0.5 rounded-md bg-amber-300 text-slate-950 border-2 border-slate-900 shadow-[1px_1px_0px_0px_rgba(15,23,42,1)] uppercase">
                      {res.provider}
                    </span>
                    <span className="text-[11px] font-mono text-slate-500 font-bold">
                      /{res.slug}
                    </span>
                  </div>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-slate-100 text-slate-600 font-mono border border-slate-300">
                    {res.resource_type}
                  </span>
                </div>

                <h3 className="font-display font-extrabold text-lg text-slate-900 mb-2 leading-snug">
                  {res.title}
                </h3>
                <p className="text-xs text-slate-600 mb-4 leading-relaxed font-medium">
                  {res.description}
                </p>
                
                {/* Available Offers / Plans */}
                <div className="space-y-2.5 mb-5">
                  <span className="text-[11px] font-mono font-bold text-slate-500 uppercase tracking-wider block">
                    Available Pricing Offers:
                  </span>
                  {res.offers.map((offer) => (
                    <div 
                      key={offer.id} 
                      className="p-3 rounded-xl bg-slate-50 border-2 border-slate-900 flex items-center justify-between text-xs shadow-neo-sm"
                    >
                      <div>
                        <div className="font-bold text-slate-900">{offer.title}</div>
                        <div className="text-[11px] text-slate-500 font-mono">
                          Duration: {Math.round(offer.duration_seconds / 60)} mins &bull; Model: {offer.pricing_model}
                        </div>
                      </div>
                      <div className="font-mono font-black text-emerald-700 bg-emerald-100 px-2.5 py-1 rounded-lg border border-emerald-600 text-sm shadow-[1px_1px_0px_0px_rgba(15,23,42,1)]">
                        ${offer.amount.toFixed(2)} {offer.currency}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="pt-4 border-t-2 border-slate-100 flex items-center justify-between">
                <div className="text-xs font-mono text-slate-500 font-semibold">
                  By {res.publisher_name}
                </div>
                
                <div className="flex items-center space-x-2">
                  <a
                    href={`/api/v1/resources/${res.slug}/content`}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center space-x-1 px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 border-2 border-slate-900 text-xs font-mono font-bold text-slate-800 shadow-neo-sm transition-all"
                  >
                    <span>HTTP 402</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>

                  {onSelectResource && (
                    <button
                      onClick={() => onSelectResource(res.slug)}
                      className="inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-amber-400 hover:bg-amber-300 border-2 border-slate-900 text-xs font-display font-black text-slate-950 shadow-neo-sm transition-all"
                    >
                      <span>Run Agent</span>
                      <ArrowRight className="w-3.5 h-3.5 stroke-[2.5]" />
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
