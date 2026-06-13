function safeDate(iso: string | null | undefined): Date | null {
  if (!iso) return null
  const d = new Date(iso)
  return isNaN(d.getTime()) ? null : d
}

export function formatDate(iso: string | null | undefined): string {
  const d = safeDate(iso)
  if (!d) return '—'
  return new Intl.DateTimeFormat('en-IN', {
    dateStyle: 'medium',
  }).format(d)
}

export function formatDateTime(iso: string | null | undefined): string {
  const d = safeDate(iso)
  if (!d) return '—'
  return new Intl.DateTimeFormat('en-IN', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(d)
}

export function formatHours(hours: number): string {
  if (hours < 24) return `${Math.round(hours)} hrs`
  const days = Math.floor(hours / 24)
  const remaining = Math.round(hours % 24)
  return remaining > 0 ? `${days}d ${remaining}h` : `${days} days`
}

export function truncateId(id: string, chars = 8): string {
  return id?.slice(0, chars).toUpperCase()
}

export function formatPercent(value: number): string {
  return `${value.toFixed(1)}%`
}
