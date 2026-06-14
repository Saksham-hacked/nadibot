import type { Incident } from '../../types/incident'
import StatusBadge from './StatusBadge'
import { truncateId } from '../../utils/formatters'

interface IncidentTableProps {
  incidents: Incident[]
  onUpdate?: (incident: Incident) => void
  showActions?: boolean
}

export default function IncidentTable({ incidents, onUpdate, showActions = false }: IncidentTableProps) {
  if (incidents.length === 0) {
    return (
      <div className="text-center py-10 text-slate-500 text-sm border border-slate-200 rounded-lg">
        No incidents found.
      </div>
    )
  }

  return (
    <div className="overflow-x-auto rounded-lg border border-slate-200">
      <table className="min-w-full text-sm">
        <thead className="bg-slate-50 border-b border-slate-200">
          <tr>
            <th className="px-4 py-3 text-left text-xs font-semibold text-slate-600 uppercase tracking-wide">ID</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-slate-600 uppercase tracking-wide">Title</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-slate-600 uppercase tracking-wide">Category</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-slate-600 uppercase tracking-wide">Severity</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-slate-600 uppercase tracking-wide">Status</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-slate-600 uppercase tracking-wide">District</th>
            <th className="px-4 py-3 text-left text-xs font-semibold text-slate-600 uppercase tracking-wide">Complaints</th>
            {showActions && (
              <th className="px-4 py-3 text-left text-xs font-semibold text-slate-600 uppercase tracking-wide">Actions</th>
            )}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-100">
          {incidents.map((inc) => (
            <tr key={inc.incident_id} className="hover:bg-slate-50">
              <td className="px-4 py-3 font-mono text-xs text-slate-500">{truncateId(inc.incident_id)}</td>
              <td className="px-4 py-3 text-slate-800 max-w-[200px] truncate">{inc.title}</td>
              <td className="px-4 py-3 text-slate-600">{inc.category}</td>
              <td className="px-4 py-3">
                <StatusBadge type="severity" value={inc.severity}>{inc.severity}</StatusBadge>
              </td>
              <td className="px-4 py-3">
                <StatusBadge type="status" value={inc.status}>{inc.status}</StatusBadge>
              </td>
              <td className="px-4 py-3 text-slate-600">{inc.district}</td>
              <td className="px-4 py-3 text-slate-600">{inc.complaint_count}</td>
              {showActions && (
                <td className="px-4 py-3">
                  <button
                    onClick={() => onUpdate?.(inc)}
                    className="text-xs px-3 py-1 border border-[#1a56db] text-[#1a56db] rounded hover:bg-blue-50"
                  >
                    Update
                  </button>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
