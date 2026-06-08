import type { ComplaintStatus, Severity } from '../../types/common'
import { STATUS_LABELS, SEVERITY_LABELS } from '../../types/common'

type BadgeType = 'status' | 'severity' | 'category'

interface BadgeProps {
  type: BadgeType
  value?: ComplaintStatus | Severity
  children: React.ReactNode
}

const statusClasses: Record<ComplaintStatus, string> = {
  OPEN: 'bg-blue-100 text-blue-800',
  IN_PROGRESS: 'bg-yellow-100 text-yellow-800',
  RESOLVED: 'bg-green-100 text-green-800',
}

const severityClasses: Record<Severity, string> = {
  Critical: 'bg-red-100 text-red-800',
  High: 'bg-orange-100 text-orange-800',
  Medium: 'bg-yellow-100 text-yellow-800',
  Low: 'bg-green-100 text-green-800',
}

export default function StatusBadge({ type, value, children }: BadgeProps) {
  let cls = 'bg-slate-100 text-slate-700'
  let label: React.ReactNode = children

  if (type === 'status' && value) {
    cls = statusClasses[value as ComplaintStatus] ?? cls
    label = STATUS_LABELS[value as ComplaintStatus] ?? children
  } else if (type === 'severity' && value) {
    cls = severityClasses[value as Severity] ?? cls
    label = SEVERITY_LABELS[value as Severity] ?? children
  }

  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${cls}`}>
      {label}
    </span>
  )
}
