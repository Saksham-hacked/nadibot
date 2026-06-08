import type { ComplaintStatus, Severity } from '../../types/common'
import { STATUS_LABELS, SEVERITY_LABELS } from '../../types/common'

type BadgeKind = 'status' | 'severity' | 'category' | 'default'

interface BadgeProps {
  /** Either `variant` or `type` accepted — both map to the same thing */
  variant?: BadgeKind
  type?: BadgeKind
  value?: string
  children?: React.ReactNode
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

export function Badge({ variant, type, value, children }: BadgeProps) {
  const kind: BadgeKind = variant ?? type ?? 'default'
  const base = 'inline-flex items-center px-2 py-0.5 rounded text-xs font-medium'

  if (kind === 'status') {
    const key = (value ?? String(children)) as ComplaintStatus
    const cls = statusClasses[key] ?? 'bg-slate-100 text-slate-700'
    const label = STATUS_LABELS[key] ?? children ?? value
    return <span className={`${base} ${cls}`}>{label}</span>
  }

  if (kind === 'severity') {
    const key = (value ?? String(children)) as Severity
    const cls = severityClasses[key] ?? 'bg-slate-100 text-slate-700'
    const label = SEVERITY_LABELS[key] ?? children ?? value
    return <span className={`${base} ${cls}`}>{label}</span>
  }

  // category or default
  return <span className={`${base} bg-slate-100 text-slate-700`}>{children ?? value}</span>
}

export default Badge
