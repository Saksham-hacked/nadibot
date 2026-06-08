export type ComplaintStatus = 'OPEN' | 'IN_PROGRESS' | 'RESOLVED'
export type IncidentStatus = 'OPEN' | 'IN_PROGRESS' | 'RESOLVED'
export type Severity = 'Low' | 'Medium' | 'High' | 'Critical'
export type Category =
  | 'Water Supply'
  | 'Water Quality'
  | 'Infrastructure'
  | 'Flooding'
  | 'Drainage'
  | 'Groundwater'
  | 'Sanitation'
  | 'Other'

export const STATUS_LABELS: Record<ComplaintStatus, string> = {
  OPEN: 'Open',
  IN_PROGRESS: 'In Progress',
  RESOLVED: 'Resolved',
}

export const SEVERITY_LABELS: Record<Severity, string> = {
  Low: 'Low',
  Medium: 'Medium',
  High: 'High',
  Critical: 'Critical',
}
