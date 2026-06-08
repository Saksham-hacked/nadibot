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
import { Spinner } from '../components/ui/Spinner'
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

  const loading = overviewQ.isLoading || categoriesQ.isLoading || trendsQ.isLoading

  return (
    <AppShell>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Water Governance Dashboard</h1>
          <p className="text-sm text-slate-500 mt-1">Overview of complaints and incidents across Uttarakhand.</p>
        </div>

        {loading && (
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

        {categoriesQ.data && trendsQ.data && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <CategoryChart data={categoriesQ.data.categories} />
            <TrendChart data={trendsQ.data} />
          </div>
        )}

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
