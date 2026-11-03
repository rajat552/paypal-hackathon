import React, { useEffect, useState, useMemo } from 'react';
import { AgGridReact } from 'ag-grid-react';
import { ColDef } from 'ag-grid-community';
import { DollarSign, ShoppingCart, KeyRound, Users, Activity, TrendingUp, RefreshCw } from 'lucide-react';

interface SummaryData {
  total_revenue_usd: number;
  captured_transactions_count: number;
  active_entitlements_count: number;
  unique_agents_count: number;
  conversion_rate_pct: number;
  total_usage_events: number;
}

interface TransactionRow {
  id: string;
  paypal_order_id: string;
  paypal_capture_id: string;
  amount: number;
  currency: string;
  status: string;
  resource_title: string;
  resource_slug: string;
  captured_at: string;
}

export const AnalyticsView: React.FC = () => {
  const [summary, setSummary] = useState<SummaryData | null>(null);
  const [transactions, setTransactions] = useState<TransactionRow[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [sumRes, txRes] = await Promise.all([
        fetch('/api/v1/publisher/analytics/summary'),
        fetch('/api/v1/publisher/analytics/transactions?limit=100'),
      ]);
      const sumData = await sumRes.json();
      const txData = await txRes.json();
      setSummary(sumData);
      setTransactions(txData.items || []);
    } catch (e) {
      console.error('Error fetching analytics data', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const columnDefs = useMemo<ColDef<TransactionRow>[]>(() => [
    {
      headerName: 'Captured Date (UTC)',
      field: 'captured_at',
      sortable: true,
      filter: true,
      width: 190,
      valueFormatter: (params) => {
        if (!params.value) return '';
        try {
          return new Date(params.value).toLocaleString();
        } catch {
          return params.value;
        }
      },
    },
    {
      headerName: 'Resource Title',
      field: 'resource_title',
      sortable: true,
      filter: true,
      flex: 1,
      minWidth: 200,
    },
    {
      headerName: 'PayPal Order ID',
      field: 'paypal_order_id',
      sortable: true,
      filter: true,
      width: 220,
      cellRenderer: (params: any) => (
        <span className="font-mono text-xs text-blue-400">{params.value}</span>
      ),
    },
    {
      headerName: 'Capture ID',
      field: 'paypal_capture_id',
      sortable: true,
      filter: true,
      width: 220,
      cellRenderer: (params: any) => (
        <span className="font-mono text-xs text-emerald-400">{params.value}</span>
      ),
    },
    {
      headerName: 'Gross Amount',
      field: 'amount',
      sortable: true,
      filter: true,
      width: 140,
      cellRenderer: (params: any) => (
        <span className="font-mono font-bold text-white">
          ${params.data?.amount?.toFixed(2)} {params.data?.currency}
        </span>
      ),
    },
    {
      headerName: 'Status',
      field: 'status',
      sortable: true,
      filter: true,
      width: 130,
      cellRenderer: (params: any) => (
        <span className="px-2 py-0.5 rounded text-[11px] font-mono font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          {params.value}
        </span>
      ),
    },
  ], []);

  const defaultColDef = useMemo<ColDef>(() => ({
    resizable: true,
  }), []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center space-x-2">
            <span>PayMesh AI — Verified Financial Ledger &amp; Usage Analytics</span>
            <span className="text-xs px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20 font-mono">
              Powered by AG Grid
            </span>
          </h2>
          <p className="text-xs text-slate-400">
            Real-time ledger of verified PayPal Sandbox micro-transactions and machine-readable data requests.
          </p>
        </div>
        <button
          onClick={fetchData}
          className="flex items-center space-x-1.5 text-xs bg-slate-800 hover:bg-slate-700 px-3 py-1.5 rounded-lg text-slate-300 transition"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh Ledger</span>
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
        <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
          <div className="flex items-center space-x-2 text-slate-400 text-xs mb-1">
            <DollarSign className="w-4 h-4 text-emerald-400" />
            <span>Captured Revenue</span>
          </div>
          <div className="text-xl font-extrabold text-white font-mono">
            ${summary ? summary.total_revenue_usd.toFixed(2) : '0.00'}
          </div>
        </div>

        <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
          <div className="flex items-center space-x-2 text-slate-400 text-xs mb-1">
            <ShoppingCart className="w-4 h-4 text-blue-400" />
            <span>Completed Orders</span>
          </div>
          <div className="text-xl font-extrabold text-white font-mono">
            {summary ? summary.captured_transactions_count : 0}
          </div>
        </div>

        <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
          <div className="flex items-center space-x-2 text-slate-400 text-xs mb-1">
            <KeyRound className="w-4 h-4 text-amber-400" />
            <span>Active Entitlements</span>
          </div>
          <div className="text-xl font-extrabold text-white font-mono">
            {summary ? summary.active_entitlements_count : 0}
          </div>
        </div>

        <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
          <div className="flex items-center space-x-2 text-slate-400 text-xs mb-1">
            <Users className="w-4 h-4 text-indigo-400" />
            <span>Unique Agents</span>
          </div>
          <div className="text-xl font-extrabold text-white font-mono">
            {summary ? summary.unique_agents_count : 0}
          </div>
        </div>

        <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
          <div className="flex items-center space-x-2 text-slate-400 text-xs mb-1">
            <TrendingUp className="w-4 h-4 text-cyan-400" />
            <span>Capture Conversion</span>
          </div>
          <div className="text-xl font-extrabold text-white font-mono">
            {summary ? summary.conversion_rate_pct : 100}%
          </div>
        </div>

        <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
          <div className="flex items-center space-x-2 text-slate-400 text-xs mb-1">
            <Activity className="w-4 h-4 text-purple-400" />
            <span>Content Usage Calls</span>
          </div>
          <div className="text-xl font-extrabold text-white font-mono">
            {summary ? summary.total_usage_events : 0}
          </div>
        </div>
      </div>

      {/* AG Grid Transaction Table */}
      <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 space-y-4 shadow-xl">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-white">Verified PayPal Sandbox Transaction Log</h3>
          <span className="text-xs text-slate-500 font-mono">{transactions.length} recorded events</span>
        </div>

        <div className="ag-theme-alpine-dark w-full h-[450px] rounded-xl overflow-hidden border border-slate-800">
          <AgGridReact<TransactionRow>
            rowData={transactions}
            columnDefs={columnDefs}
            defaultColDef={defaultColDef}
            pagination={true}
            paginationPageSize={10}
            animateRows={true}
          />
        </div>
      </div>
    </div>
  );
};
