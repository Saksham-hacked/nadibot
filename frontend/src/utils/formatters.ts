export function formatDate(iso: string): string {
  return new Intl.DateTimeFormat('en-IN', {
    dateStyle: 'medium',
  }).format(new Date(iso))
}

export function formatDateTime(iso: string): string {
  return new Intl.DateTimeFormat('en-IN', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(iso))
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
