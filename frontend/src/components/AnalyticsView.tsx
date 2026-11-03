import React, { useEffect, useState, useMemo } from 'react';
import { AgGridReact } from 'ag-grid-react';
import { ColDef } from 'ag-grid-community';
import { DollarSign, ShoppingCart, KeyRound, Users, Activity, TrendingUp, RefreshCw, BarChart3, Download, Check } from 'lucide-react';

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
  const [exported, setExported] = useState(false);

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

  const handleExportCSV = () => {
    if (transactions.length === 0) return;
    const headers = ['Captured At', 'Resource Title', 'PayPal Order ID', 'Capture ID', 'Amount', 'Currency', 'Status'];
    const rows = transactions.map(t => [
      `"${t.captured_at}"`,
      `"${t.resource_title}"`,
      `"${t.paypal_order_id}"`,
      `"${t.paypal_capture_id}"`,
      t.amount,
      `"${t.currency}"`,
      `"${t.status}"`
    ]);
    const csvContent = "data:text/csv;charset=utf-8," + [headers.join(','), ...rows.map(e => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `paymesh_ledger_${new Date().toISOString().slice(0, 10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    setExported(true);
    setTimeout(() => setExported(false), 2500);
  };

  const columnDefs = useMemo<ColDef<TransactionRow>[]>(() => [
    {
      headerName: 'Captured Date (UTC)',
      field: 'captured_at',
      sortable: true,
      filter: true,
      width: 195,
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
      width: 210,
      cellRenderer: (params: any) => (
        <span className="font-mono text-xs font-bold text-blue-400">{params.value}</span>
      ),
    },
    {
      headerName: 'Capture ID',
      field: 'paypal_capture_id',
      sortable: true,
      filter: true,
      width: 210,
      cellRenderer: (params: any) => (
        <span className="font-mono text-xs font-bold text-emerald-400">{params.value}</span>
      ),
    },
    {
      headerName: 'Gross Amount',
      field: 'amount',
      sortable: true,
      filter: true,
      width: 140,
      cellRenderer: (params: any) => (
        <span className="font-mono font-black text-amber-300">
          ${params.data?.amount?.toFixed(2)} {params.data?.currency}
        </span>
      ),
    },
    {
      headerName: 'Capture State',
      field: 'status',
      sortable: true,
      filter: true,
      width: 130,
      cellRenderer: (params: any) => (
        <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
          {params.value}
        </span>
      ),
    },
  ], []);

  const defaultColDef = useMemo<ColDef>(() => ({
    resizable: true,
  }), []);

  return (
    <div className="space-y-8">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b-2 border-slate-900">
        <div>
          <div className="inline-flex items-center space-x-2 px-3 py-0.5 rounded-full bg-emerald-100 text-emerald-950 border-2 border-slate-900 font-mono text-xs font-bold shadow-neo-sm mb-2">
            <BarChart3 className="w-3.5 h-3.5 text-emerald-700" />
            <span>AG GRID ENTERPRISE INTEGRATION</span>
          </div>
          <h2 className="font-display font-black text-2xl sm:text-3xl text-slate-900 tracking-tight">
            Financial Ledger &amp; Conversion Analytics
          </h2>
          <p className="text-xs sm:text-sm text-slate-600 font-medium">
            Immutable audit record of executed PayPal Sandbox Orders v2 captures and machine usage events.
          </p>
        </div>

        <div className="flex items-center space-x-2 self-start sm:self-auto">
          <button
            onClick={handleExportCSV}
            className="flex items-center space-x-1.5 px-3 py-2 rounded-xl bg-white hover:bg-slate-100 border-2 border-slate-900 text-xs font-mono font-bold text-slate-800 shadow-neo-sm hover:-translate-y-0.5 transition-all"
            title="Export Ledger to CSV"
          >
            {exported ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Download className="w-3.5 h-3.5" />}
            <span>{exported ? 'Exported!' : 'Export CSV'}</span>
          </button>

          <button
            onClick={fetchData}
            className="flex items-center space-x-2 px-3.5 py-2 rounded-xl bg-white hover:bg-slate-100 border-2 border-slate-900 text-xs font-mono font-bold text-slate-900 shadow-neo-sm hover:-translate-y-0.5 transition-all"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Refresh Ledger</span>
          </button>
        </div>
      </div>

      {/* KPI Stat Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <div className="p-4 rounded-2xl bg-white border-2 border-slate-900 shadow-neo">
          <div className="flex items-center space-x-1.5 text-slate-600 text-xs mb-1 font-mono font-bold">
            <DollarSign className="w-4 h-4 text-emerald-600" />
            <span>Revenue</span>
          </div>
          <div className="text-2xl font-black text-slate-900 font-mono">
            ${summary ? summary.total_revenue_usd.toFixed(2) : '0.00'}
          </div>
          <div className="text-[10px] text-slate-500 font-mono mt-1">USD Captured</div>
        </div>

        <div className="p-4 rounded-2xl bg-white border-2 border-slate-900 shadow-neo">
          <div className="flex items-center space-x-1.5 text-slate-600 text-xs mb-1 font-mono font-bold">
            <ShoppingCart className="w-4 h-4 text-brand-600" />
            <span>Orders</span>
          </div>
          <div className="text-2xl font-black text-slate-900 font-mono">
            {summary ? summary.captured_transactions_count : 0}
          </div>
          <div className="text-[10px] text-slate-500 font-mono mt-1">PayPal Verified</div>
        </div>

        <div className="p-4 rounded-2xl bg-white border-2 border-slate-900 shadow-neo">
          <div className="flex items-center space-x-1.5 text-slate-600 text-xs mb-1 font-mono font-bold">
            <KeyRound className="w-4 h-4 text-amber-500" />
            <span>Entitlements</span>
          </div>
          <div className="text-2xl font-black text-slate-900 font-mono">
            {summary ? summary.active_entitlements_count : 0}
          </div>
          <div className="text-[10px] text-slate-500 font-mono mt-1">Active Bearer Tokens</div>
        </div>

        <div className="p-4 rounded-2xl bg-white border-2 border-slate-900 shadow-neo">
          <div className="flex items-center space-x-1.5 text-slate-600 text-xs mb-1 font-mono font-bold">
            <Users className="w-4 h-4 text-indigo-600" />
            <span>Agents</span>
          </div>
          <div className="text-2xl font-black text-slate-900 font-mono">
            {summary ? summary.unique_agents_count : 0}
          </div>
          <div className="text-[10px] text-slate-500 font-mono mt-1">Autonomous Buyers</div>
        </div>

        <div className="p-4 rounded-2xl bg-white border-2 border-slate-900 shadow-neo">
          <div className="flex items-center space-x-1.5 text-slate-600 text-xs mb-1 font-mono font-bold">
            <TrendingUp className="w-4 h-4 text-teal-600" />
            <span>Conversion</span>
          </div>
          <div className="text-2xl font-black text-slate-900 font-mono">
            {summary ? summary.conversion_rate_pct : 100}%
          </div>
          <div className="text-[10px] text-slate-500 font-mono mt-1">Challenge to Capture</div>
        </div>

        <div className="p-4 rounded-2xl bg-white border-2 border-slate-900 shadow-neo">
          <div className="flex items-center space-x-1.5 text-slate-600 text-xs mb-1 font-mono font-bold">
            <Activity className="w-4 h-4 text-purple-600" />
            <span>API Calls</span>
          </div>
          <div className="text-2xl font-black text-slate-900 font-mono">
            {summary ? summary.total_usage_events : 0}
          </div>
          <div className="text-[10px] text-slate-500 font-mono mt-1">Protected Exchanges</div>
        </div>
      </div>

      {/* AG Grid Transaction Table Neo-Card */}
      <div className="p-6 rounded-2xl bg-white border-2 border-slate-900 shadow-neo space-y-4">
        <div className="flex items-center justify-between pb-3 border-b-2 border-slate-100">
          <div className="flex items-center space-x-2">
            <span className="font-display font-extrabold text-base text-slate-900">
              Verified PayPal Sandbox Financial Ledger
            </span>
            <span className="text-[11px] font-mono px-2 py-0.5 rounded-full bg-slate-100 text-slate-700 border border-slate-300">
              Real-Time Sync
            </span>
          </div>
          <span className="text-xs text-slate-600 font-mono font-bold">
            {transactions.length} Recorded Transactions
          </span>
        </div>

        <div className="ag-theme-alpine-dark w-full h-[460px] rounded-xl overflow-hidden border-2 border-slate-900 shadow-inner">
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
