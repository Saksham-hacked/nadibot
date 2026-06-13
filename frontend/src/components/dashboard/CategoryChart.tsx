import { useEffect } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import type { CategoryCount } from '../../types/analytics'

interface CategoryChartProps {
  data: CategoryCount[]
}

export default function CategoryChart({ data }: CategoryChartProps) {
  useEffect(() => {
    console.log('[CategoryChart] received data prop:', data)
    if (!data || data.length === 0) {
      console.warn('[CategoryChart] ⚠ data is empty or undefined — "No data available" will render.')
    } else {
      console.log(`[CategoryChart] ✓ ${data.length} categories to render:`, data.map(d => `${d.category}=${d.count}`).join(', '))
    }
  }, [data])

  if (!data || data.length === 0) {
    return (
      <div className="bg-white border border-slate-200 rounded-lg p-5 shadow-sm">
        <h3 className="text-sm font-semibold text-slate-700 mb-4">Complaints by Category</h3>
        <div className="flex items-center justify-center h-[220px] text-sm text-slate-400">No data available</div>
      </div>
    )
  }

  return (
    <div className="bg-white border border-slate-200 rounded-lg p-5 shadow-sm">
      <h3 className="text-sm font-semibold text-slate-700 mb-4">Complaints by Category</h3>
      <ResponsiveContainer width="100%" height={220}>
        <BarChart data={data} margin={{ top: 0, right: 8, left: -20, bottom: 40 }}>
          <XAxis
            dataKey="category"
            tick={{ fontSize: 10, fill: '#64748b' }}
            angle={-35}
            textAnchor="end"
            interval={0}
          />
          <YAxis tick={{ fontSize: 10, fill: '#64748b' }} allowDecimals={false} />
          <Tooltip
            contentStyle={{ fontSize: 12, border: '1px solid #e2e8f0' }}
            cursor={{ fill: '#f1f5f9' }}
          />
          <Bar dataKey="count" fill="#1a56db" radius={[3, 3, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
