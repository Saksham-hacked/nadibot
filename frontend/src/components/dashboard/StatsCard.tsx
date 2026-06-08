interface StatsCardProps {
  label: string
  value: string | number
  sub?: string
}

export default function StatsCard({ label, value, sub }: StatsCardProps) {
  return (
    <div className="bg-white border border-slate-200 rounded-lg p-5 shadow-sm">
      <p className="text-xs font-medium text-slate-500 uppercase tracking-wide mb-1">{label}</p>
      <p className="text-3xl font-bold text-slate-800">{value}</p>
      {sub && <p className="text-xs text-slate-400 mt-1">{sub}</p>}
    </div>
  )
}
