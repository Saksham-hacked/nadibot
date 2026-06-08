import type { ComplaintListItem } from '../../types/complaint'
import StatusBadge from './StatusBadge'
import { formatDate, truncateId } from '../../utils/formatters'

interface ComplaintTableProps {
  complaints: ComplaintListItem[]
}

export default function ComplaintTable({ complaints }: ComplaintTableProps) {
  if (complaints.length === 0) {
    return (
      <div className="text-center py-10 text-slate-500 text-sm border border-slate-200 rounded-lg">
        No complaints found.
      </div>
    )
  }

  return (
    <div className="overflow-x-auto rounded-lg border border-slate-200">
      <table className="min-w-full text-sm">
        <thead className="bg-slate-50 border-b border-slate-200">
          <tr>
            <th className="px-4 py-3 text-left text-xs font-semibold text-slate-600 uppercase tracking-wide">ID</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-slate-600 uppercase tracking-wide">Category</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-slate-600 uppercase tracking-wide">Severity</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-slate-600 uppercase tracking-wide">Status</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-slate-600 uppercase tracking-wide">District</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-slate-600 uppercase tracking-wide">Submitted</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {complaints.map((c) => (
            <tr key={c.complaint_id} className="hover:bg-slate-50">
              <td className="px-4 py-3 font-mono text-xs text-slate-500">{truncateId(c.complaint_id)}</td>
              <td className="px-4 py-3 text-slate-700">{c.category}</td>
              <td className="px-4 py-3">
                <StatusBadge type="severity" value={c.severity}>{c.severity}</StatusBadge>
              </td>
              <td className="px-4 py-3">
                <StatusBadge type="status" value={c.status}>{c.status}</StatusBadge>
              </td>
              <td className="px-4 py-3 text-slate-600">{c.district}</td>
              <td className="px-4 py-3 text-slate-500">{formatDate(c.created_at)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
