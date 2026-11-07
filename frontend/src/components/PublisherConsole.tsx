import React, { useState } from 'react';
import { PlusCircle, Tag, Check, AlertCircle, ShoppingBag, Eye, DollarSign, Clock, Layers, Wand2 } from 'lucide-react';
import { formatApiError } from '../utils/error';

export const PublisherConsole: React.FC<{ onNavigateToCatalogue?: () => void }> = ({ onNavigateToCatalogue }) => {
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

  const handleAutoSlug = () => {
    if (title) {
      const generated = title
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/(^-|-$)+/g, '');
      setSlug(generated);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);

    // Client-side validations
    const cleanSlug = slug.trim();
    const slugRegex = /^[a-zA-Z0-9_\-]+$/;
    if (!cleanSlug || !slugRegex.test(cleanSlug)) {
      setMessage({
        text: 'Invalid Resource Slug: only letters, numbers, hyphens (-), and underscores (_) are allowed (no spaces or periods). Click "Auto Slug" to generate one.',
        type: 'error'
      });
      setLoading(false);
      return;
    }

    if (description.trim().length < 5) {
      setMessage({
        text: 'Description must be at least 5 characters long.',
        type: 'error'
      });
      setLoading(false);
      return;
    }

    const offerRegex = /^[a-zA-Z0-9_\-]+$/;
    if (!offerCode.trim() || !offerRegex.test(offerCode.trim())) {
      setMessage({
        text: 'Invalid Offer Code: only letters, numbers, hyphens (-), and underscores (_) are allowed.',
        type: 'error'
      });
      setLoading(false);
      return;
    }

    const priceNum = parseFloat(price);
    if (isNaN(priceNum) || priceNum <= 0) {
      setMessage({
        text: 'Price must be a positive number (e.g. 0.05).',
        type: 'error'
      });
      setLoading(false);
      return;
    }

    try {
      // 1. Create Resource
      const resRes = await fetch('/api/v1/publisher/resources', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          slug: cleanSlug,
          title: title.trim(),
          description: description.trim(),
          resource_type: resourceType,
          provider,
        }),
      });

      if (!resRes.ok) {
        const err = await resRes.json().catch(() => ({}));
        throw new Error(formatApiError(err, 'Failed to create resource'));
      }

      const resourceData = await resRes.json();

      // 2. Create Pricing Offer
      const offRes = await fetch(`/api/v1/publisher/resources/${resourceData.id}/offers`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          offer_code: offerCode.trim(),
          title: offerTitle.trim(),
          description: `Access to ${title.trim()}`,
          price_amount: priceNum,
          currency: 'USD',
          pricing_model: 'one_time',
          duration_seconds: parseInt(duration) || 3600,
        }),
      });

      if (!offRes.ok) {
        const offErr = await offRes.json().catch(() => ({}));
        throw new Error(formatApiError(offErr, 'Failed to create offer'));
      }

      setMessage({ text: `Successfully published resource "${title}" with $${price} USD offer!`, type: 'success' });
      setSlug('');
      setTitle('');
      setDescription('');
    } catch (e: any) {
      setMessage({ text: formatApiError(e, 'Failed to publish resource'), type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8 max-w-4xl mx-auto">
      {/* Header */}
      <div className="pb-4 border-b-2 border-slate-900">
        <div className="inline-flex items-center space-x-2 px-3 py-0.5 rounded-full bg-amber-100 text-amber-950 border-2 border-slate-900 font-mono text-xs font-bold shadow-neo-sm mb-2">
          <ShoppingBag className="w-3.5 h-3.5 text-amber-600" />
          <span>MERCHANT STUDIO</span>
        </div>
        <h2 className="font-display font-black text-2xl sm:text-3xl text-slate-900 tracking-tight">
          Publish Dataset or API
        </h2>
        <p className="text-xs sm:text-sm text-slate-600 font-medium">
          Publish verified APIs and datasets with automated HTTP 402 paywalls, custom pricing offers, and PayPal Sandbox settlement.
        </p>
      </div>

      <div data-tour="publisher-form" className="grid grid-cols-1 md:grid-cols-12 gap-8 items-start">
        {/* Form Column */}
        <div className="md:col-span-7">
          <div className="p-4 sm:p-8 rounded-2xl bg-white border-2 border-slate-900 shadow-neo space-y-6">
            {message && (
              <div
                className={`p-3.5 rounded-xl text-xs font-mono font-bold flex items-center justify-between border-2 ${
                  message.type === 'success'
                    ? 'bg-emerald-100 text-emerald-950 border-emerald-800'
                    : 'bg-red-100 text-red-950 border-red-800'
                }`}
              >
                <div className="flex items-center space-x-2.5">
                  {message.type === 'success' ? <Check className="w-4 h-4 text-emerald-700" /> : <AlertCircle className="w-4 h-4 text-red-600" />}
                  <span>{message.text}</span>
                </div>
                {message.type === 'success' && onNavigateToCatalogue && (
                  <button
                    onClick={onNavigateToCatalogue}
                    className="underline hover:text-emerald-800 ml-2 text-[11px]"
                  >
                    View in Catalogue &rarr;
                  </button>
                )}
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-5">
              <div>
                <label className="block text-xs font-mono font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                  Dataset / API Title
                </label>
                <div className="flex flex-col sm:flex-row gap-2">
                  <input
                    type="text"
                    placeholder="e.g. Ultra-Low Latency Switch Profiles"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    required
                    className="flex-1 bg-slate-50 border-2 border-slate-900 rounded-xl p-2.5 text-xs text-slate-900 font-bold focus:outline-none focus:bg-white focus:ring-2 focus:ring-brand-500 shadow-inner"
                  />
                  <button
                    type="button"
                    onClick={handleAutoSlug}
                    className="px-3.5 py-2 min-h-[40px] bg-slate-100 hover:bg-slate-200 border-2 border-slate-900 rounded-xl text-[11px] font-mono font-bold flex items-center justify-center space-x-1.5 shadow-neo-sm shrink-0"
                    title="Generate slug from title"
                  >
                    <Wand2 className="w-3.5 h-3.5 text-brand-600" />
                    <span>Auto Slug</span>
                  </button>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-mono font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                    Resource Slug
                  </label>
                  <input
                    type="text"
                    placeholder="e.g. gpu-latencies-2026"
                    value={slug}
                    onChange={(e) => setSlug(e.target.value)}
                    required
                    className={`w-full bg-slate-50 border-2 rounded-xl p-2.5 text-xs text-slate-900 font-mono focus:outline-none focus:bg-white focus:ring-2 shadow-inner ${
                      slug && !/^[a-zA-Z0-9_\-]+$/.test(slug)
                        ? 'border-red-600 focus:ring-red-500'
                        : 'border-slate-900 focus:ring-brand-500'
                    }`}
                  />
                  {slug && !/^[a-zA-Z0-9_\-]+$/.test(slug) ? (
                    <p className="mt-1 text-[10px] font-mono font-bold text-red-600">
                      No spaces or dots. Use letters, numbers, hyphens (-) or underscores (_).
                    </p>
                  ) : (
                    <p className="mt-1 text-[10px] font-mono text-slate-500">
                      Unique identifier for URL /api/v1/resources/:slug
                    </p>
                  )}
                </div>
                <div>
                  <label className="block text-xs font-mono font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                    Provider
                  </label>
                  <select
                    value={provider}
                    onChange={(e) => setProvider(e.target.value)}
                    className="w-full bg-slate-50 border-2 border-slate-900 rounded-xl p-2.5 text-xs text-slate-900 font-bold focus:outline-none focus:bg-white focus:ring-2 focus:ring-brand-500 shadow-inner"
                  >
                    <option value="channel3">Channel3 Product Intelligence</option>
                    <option value="paymesh_wire">PayMesh Intelligence Wire</option>
                    <option value="custom_merchant">Custom Merchant API</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-mono font-bold text-slate-700 uppercase tracking-wider mb-1.5">
                  Description
                </label>
                <textarea
                  rows={2}
                  placeholder="Describe dataset contents, frequency, and schema for AI agents..."
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  required
                  className="w-full bg-slate-50 border-2 border-slate-900 rounded-xl p-2.5 text-xs text-slate-900 focus:outline-none focus:bg-white focus:ring-2 focus:ring-brand-500 shadow-inner"
                />
              </div>

              {/* Pricing Offer Specification */}
              <div className="p-4 rounded-xl bg-slate-50 border-2 border-slate-900 space-y-4 shadow-neo-sm">
                <div className="flex items-center space-x-2 text-xs font-mono font-bold text-slate-800 uppercase">
                  <Tag className="w-3.5 h-3.5 text-brand-600" />
                  <span>Initial Pricing &amp; Access Offer</span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-[11px] font-mono font-bold text-slate-600 mb-1">
                      Offer Code (Identifier)
                    </label>
                    <input
                      type="text"
                      value={offerCode}
                      onChange={(e) => setOfferCode(e.target.value)}
                      required
                      className="w-full bg-white border-2 border-slate-900 rounded-lg p-2 text-xs font-mono text-slate-900"
                    />
                  </div>
                  <div>
                    <label className="block text-[11px] font-mono font-bold text-slate-600 mb-1">
                      Display Title (e.g. 1-Hour Verified Access)
                    </label>
                    <input
                      type="text"
                      value={offerTitle}
                      onChange={(e) => setOfferTitle(e.target.value)}
                      required
                      className="w-full bg-white border-2 border-slate-900 rounded-lg p-2 text-xs text-slate-900"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-[11px] font-mono font-bold text-slate-600 mb-1">
                      Price (USD)
                    </label>
                    <div className="relative">
                      <span className="absolute left-2.5 top-1/2 -translate-y-1/2 text-slate-500 font-mono font-bold">$</span>
                      <input
                        type="number"
                        step="0.01"
                        value={price}
                        onChange={(e) => setPrice(e.target.value)}
                        required
                        className="w-full bg-white border-2 border-slate-900 rounded-lg pl-6 pr-2 p-2 text-xs font-mono font-bold text-slate-900"
                      />
                    </div>
                  </div>
                  <div>
                    <label className="block text-[11px] font-mono font-bold text-slate-600 mb-1">
                      Duration (Seconds)
                    </label>
                    <input
                      type="number"
                      value={duration}
                      onChange={(e) => setDuration(e.target.value)}
                      required
                      className="w-full bg-white border-2 border-slate-900 rounded-lg p-2 text-xs font-mono text-slate-900"
                    />
                  </div>
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full neo-button-amber py-3 px-6 flex items-center justify-center space-x-2 text-xs font-black uppercase tracking-wider disabled:opacity-50"
              >
                <PlusCircle className="w-4 h-4 stroke-[2.5]" />
                <span>{loading ? 'Publishing...' : 'Publish Resource & Activate L402 Offer'}</span>
              </button>
            </form>
          </div>
        </div>

        {/* Live Preview Column */}
        <div className="md:col-span-5 space-y-4">
          <div className="p-6 rounded-2xl bg-white border-2 border-slate-900 shadow-neo space-y-4">
            <div className="flex items-center space-x-2 pb-3 border-b-2 border-slate-100">
              <Eye className="w-4 h-4 text-slate-700" />
              <h3 className="font-display font-extrabold text-xs text-slate-900 uppercase tracking-wider">
                Catalogue Preview
              </h3>
            </div>

            <div className="p-4 rounded-xl bg-slate-50 border-2 border-slate-900 space-y-3 shadow-neo-sm">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-amber-300 text-slate-950 border border-slate-900 uppercase">
                  {provider}
                </span>
                <span className="text-[10px] font-mono text-slate-500">
                  /{slug || 'preview-slug'}
                </span>
              </div>

              <div className="font-display font-extrabold text-sm text-slate-900">
                {title || 'Example Dataset Title'}
              </div>

              <p className="text-xs text-slate-600">
                {description || 'Description preview of how this product will be summarized for AI agents.'}
              </p>

              <div className="p-2.5 rounded-lg bg-white border border-slate-300 flex items-center justify-between">
                <span className="text-xs font-bold text-slate-800">{offerTitle}</span>
                <span className="text-xs font-mono font-black text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded border border-emerald-600">
                  ${parseFloat(price || '0').toFixed(2)} USD
                </span>
              </div>
            </div>

            <div className="text-[11px] font-mono text-slate-500 leading-relaxed bg-slate-50 p-3 rounded-xl border border-slate-200">
              💡 <strong>Activation:</strong> Once published, this resource appears immediately in the marketplace catalogue, returns machine-readable L402 payment challenges, and supports automated PayPal Sandbox checkout.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
