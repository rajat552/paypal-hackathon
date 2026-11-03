import React, { useState } from 'react';
import { PlusCircle, Tag, Check, AlertCircle } from 'lucide-react';

export const PublisherConsole: React.FC = () => {
  const [slug, setSlug] = useState('');
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [resourceType, setResourceType] = useState('product_intelligence');
  const [provider, setProvider] = useState('channel3');

  // Offer fields
  const [offerCode, setOfferCode] = useState('standard_1h');
  const [offerTitle, setOfferTitle] = useState('1-Hour Verified Access');
  const [price, setPrice] = useState('0.05');
  const [duration, setDuration] = useState('3600');

  const [message, setMessage] = useState<{ text: string; type: 'success' | 'error' } | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);

    try {
      // 1. Create Resource
      const resRes = await fetch('/api/v1/publisher/resources', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          slug,
          title,
          description,
          resource_type: resourceType,
          provider,
        }),
      });

      if (!resRes.ok) {
        const err = await resRes.json();
        throw new Error(err.detail || 'Failed to create resource');
      }

      const resourceData = await resRes.json();

      // 2. Create Pricing Offer
      const offRes = await fetch(`/api/v1/publisher/resources/${resourceData.id}/offers`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          offer_code: offerCode,
          title: offerTitle,
          description: `Access to ${title}`,
          price_amount: parseFloat(price),
          currency: 'USD',
          pricing_model: 'one_time',
          duration_seconds: parseInt(duration),
        }),
      });

      if (!offRes.ok) {
        throw new Error('Failed to create offer');
      }

      setMessage({ text: `Successfully published resource "${title}" with $${price} offer!`, type: 'success' });
      setSlug('');
      setTitle('');
      setDescription('');
    } catch (e: any) {
      setMessage({ text: e.message, type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-xl">
        <h2 className="text-xl font-bold text-white mb-2">Merchant &amp; Publisher Studio</h2>
        <p className="text-xs text-slate-400 mb-6">
          Expose a new dataset or API with an authoritative PayMesh AI L402 challenge and PayPal Sandbox price.
        </p>

        {message && (
          <div
            className={`p-3 rounded-xl mb-6 text-xs flex items-center space-x-2 ${
              message.type === 'success'
                ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                : 'bg-red-500/10 text-red-400 border border-red-500/20'
            }`}
          >
            {message.type === 'success' ? <Check className="w-4 h-4" /> : <AlertCircle className="w-4 h-4" />}
            <span>{message.text}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Resource Slug</label>
              <input
                type="text"
                placeholder="e.g. gpu-benchmarks-2026"
                value={slug}
                onChange={(e) => setSlug(e.target.value)}
                required
                className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-xs text-white focus:outline-none focus:border-blue-500 font-mono"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Provider Type</label>
              <select
                value={provider}
                onChange={(e) => setProvider(e.target.value)}
                className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-xs text-white focus:outline-none focus:border-blue-500"
              >
                <option value="channel3">Channel3 Product Intelligence</option>
                <option value="crawlerpal_demo">CrawlerPal Demo Data</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Product Title</label>
            <input
              type="text"
              placeholder="e.g. Next-Gen GPU Performance & Latency Matrix"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
              className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-xs text-white focus:outline-none focus:border-blue-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Description</label>
            <textarea
              rows={3}
              placeholder="Detailed description of what the dataset contains..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
              className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-xs text-white focus:outline-none focus:border-blue-500"
            />
          </div>

          <div className="pt-4 border-t border-slate-800">
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Initial Access Offer</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Price (USD)</label>
                <input
                  type="number"
                  step="0.01"
                  value={price}
                  onChange={(e) => setPrice(e.target.value)}
                  required
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-xs text-white focus:outline-none focus:border-blue-500 font-mono"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Access Duration (Seconds)</label>
                <input
                  type="number"
                  value={duration}
                  onChange={(e) => setDuration(e.target.value)}
                  required
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-xs text-white focus:outline-none focus:border-blue-500 font-mono"
                />
              </div>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs shadow-lg shadow-blue-600/30 transition flex items-center justify-center space-x-2 disabled:opacity-50"
          >
            <PlusCircle className="w-4 h-4" />
            <span>{loading ? 'Publishing...' : 'Publish Data Product & Offer'}</span>
          </button>
        </form>
      </div>
    </div>
  );
};
