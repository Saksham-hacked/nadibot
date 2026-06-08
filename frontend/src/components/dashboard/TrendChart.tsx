import {
  LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer,
} from 'recharts'
import type { TrendsResponse } from '../../types/analytics'

interface TrendChartProps {
  data: TrendsResponse
}

interface MergedPoint {
  date: string
  Complaints: number
  Incidents: number
}

function formatLabel(dateStr: string): string {
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-IN', { month: 'short', day: 'numeric' })
}

export default function TrendChart({ data }: TrendChartProps) {
  const dateMap = new Map<string, MergedPoint>()

  data?.complaints?.forEach(({ date, count }) => {
    dateMap.set(date, { date, Complaints: count, Incidents: 0 })
  })
  data?.incidents?.forEach(({ date, count }) => {
    const existing = dateMap.get(date)
    if (existing) existing.Incidents = count
    else dateMap.set(date, { date, Complaints: 0, Incidents: count })
  })

  const merged = Array.from(dateMap.values())
    .sort((a, b) => a.date.localeCompare(b.date))
    .map((pt) => ({ ...pt, date: formatLabel(pt.date) }))

  return (
    <div className="bg-white border border-slate-200 rounded-lg p-5 shadow-sm">
      <h3 className="text-sm font-semibold text-slate-700 mb-4">Trend (last {data?.range})</h3>
      <ResponsiveContainer width="100%" height={220}>
        <LineChart data={merged} margin={{ top: 0, right: 8, left: -20, bottom: 0 }}>
          <XAxis dataKey="date" tick={{ fontSize: 10, fill: '#64748b' }} interval="preserveStartEnd" />
          <YAxis tick={{ fontSize: 10, fill: '#64748b' }} allowDecimals={false} />
          <Tooltip contentStyle={{ fontSize: 12, border: '1px solid #e2e8f0' }} />
          <Legend wrapperStyle={{ fontSize: 11 }} />
          <Line type="monotone" dataKey="Complaints" stroke="#1a56db" dot={false} strokeWidth={2} />
          <Line type="monotone" dataKey="Incidents" stroke="#dc2626" dot={false} strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
