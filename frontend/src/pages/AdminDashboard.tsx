import { useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useQueries } from '@tanstack/react-query'
import { useAdminKey } from '../hooks/useAdminKey'
import { getAnalyticsOverview, getCategoryDistribution, getTrends } from '../api/analytics'
import { getIncidents } from '../api/incidents'
import AppShell from '../components/layout/AppShell'
import StatsCard from '../components/dashboard/StatsCard'
import CategoryChart from '../components/dashboard/CategoryChart'
import TrendChart from '../components/dashboard/TrendChart'
import IncidentTable from '../components/dashboard/IncidentTable'
import Spinner from '../components/ui/Spinner'
import { formatPercent, formatHours } from '../utils/formatters'

export default function AdminDashboard() {
  const { adminKey } = useAdminKey()
  const navigate = useNavigate()

  useEffect(() => {
    if (!adminKey) navigate('/admin', { replace: true })
  }, [adminKey, navigate])

  const [overviewQ, categoriesQ, trendsQ, incidentsQ] = useQueries({
    queries: [
      {
        queryKey: ['overview', adminKey],
        queryFn: () => getAnalyticsOverview(adminKey!),
        enabled: !!adminKey,
      },
      {
        queryKey: ['categories', adminKey],
        queryFn: () => getCategoryDistribution(adminKey!),
        enabled: !!adminKey,
      },
      {
        queryKey: ['trends', '30d', adminKey],
        queryFn: () => getTrends('30d', adminKey!),
        enabled: !!adminKey,
      },
      {
        queryKey: ['incidents', { page: 1, page_size: 5 }, adminKey],
        queryFn: () => getIncidents({ page: 1, page_size: 5 }, adminKey!),
        enabled: !!adminKey,
      },
    ],
  })

  // ── Debug logging ────────────────────────────────────────────────────────
  useEffect(() => {
    console.log('[AdminDashboard] adminKey present:', !!adminKey)
  }, [adminKey])

  useEffect(() => {
    console.log('[AdminDashboard] overviewQ  →', {
      status: overviewQ.status,
      isLoading: overviewQ.isLoading,
      isError: overviewQ.isError,
      error: overviewQ.error,
      data: overviewQ.data,
    })
  }, [overviewQ.status, overviewQ.data, overviewQ.error])

  useEffect(() => {
    console.log('[AdminDashboard] categoriesQ →', {
      status: categoriesQ.status,
      isLoading: categoriesQ.isLoading,
      isError: categoriesQ.isError,
      error: categoriesQ.error,
      data: categoriesQ.data,
      'data.categories': categoriesQ.data?.categories,
    })
  }, [categoriesQ.status, categoriesQ.data, categoriesQ.error])

  useEffect(() => {
    console.log('[AdminDashboard] trendsQ    →', {
      status: trendsQ.status,
      isLoading: trendsQ.isLoading,
      isError: trendsQ.isError,
      error: trendsQ.error,
      data: trendsQ.data,
      complaintsLen: trendsQ.data?.complaints?.length,
      incidentsLen:  trendsQ.data?.incidents?.length,
    })
  }, [trendsQ.status, trendsQ.data, trendsQ.error])

  useEffect(() => {
    console.log('[AdminDashboard] incidentsQ →', {
      status: incidentsQ.status,
      isLoading: incidentsQ.isLoading,
      isError: incidentsQ.isError,
      error: incidentsQ.error,
      data: incidentsQ.data,
    })
  }, [incidentsQ.status, incidentsQ.data, incidentsQ.error])
  // ────────────────────────────────────────────────────────────────────────

  const anyLoading = overviewQ.isLoading || categoriesQ.isLoading || trendsQ.isLoading || incidentsQ.isLoading

  return (
    <AppShell>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Water Governance Dashboard</h1>
          <p className="text-sm text-slate-500 mt-1">Overview of complaints and incidents across Uttarakhand.</p>
        </div>

        {anyLoading && (
          <div className="flex justify-center py-8">
            <Spinner />
          </div>
        )}

        {overviewQ.data && (
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
            <StatsCard label="Total Complaints" value={overviewQ.data.total_complaints} />
            <StatsCard label="Open Complaints" value={overviewQ.data.open_complaints} />
            <StatsCard label="Resolved" value={overviewQ.data.resolved_complaints} />
            <StatsCard label="Critical" value={overviewQ.data.critical_complaints} />
            <StatsCard label="Total Incidents" value={overviewQ.data.total_incidents} />
            <StatsCard
              label="Resolution Rate"
              value={formatPercent(overviewQ.data.resolution_rate)}
              sub={`Avg. ${formatHours(overviewQ.data.average_resolution_time)}`}
            />
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {categoriesQ.isError ? (
            <div className="bg-white border border-slate-200 rounded-lg p-5 shadow-sm flex items-center justify-center h-[290px] text-sm text-slate-400">
              Failed to load category data.
            </div>
          ) : (
            <CategoryChart data={categoriesQ.data?.categories ?? []} />
          )}

          {trendsQ.isError ? (
            <div className="bg-white border border-slate-200 rounded-lg p-5 shadow-sm flex items-center justify-center h-[290px] text-sm text-slate-400">
              Failed to load trends data.
            </div>
          ) : trendsQ.data ? (
            <TrendChart data={trendsQ.data} />
          ) : null}
        </div>

        {incidentsQ.data && (
          <div>
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-base font-semibold text-slate-800">Recent Incidents</h2>
              <Link to="/admin/incidents" className="text-sm text-[#1a56db] hover:underline">
                View All Incidents →
              </Link>
            </div>
            <IncidentTable incidents={incidentsQ.data.incidents} />
          </div>
        )}
      </div>
    </AppShell>
  )
}
