import type { Category, Severity, ComplaintStatus } from '../types/common'

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

export const CATEGORIES: Category[] = [
  'Water Supply',
  'Water Quality',
  'Infrastructure',
  'Flooding',
  'Drainage',
  'Groundwater',
  'Sanitation',
  'Other',
]

export const SEVERITIES: Severity[] = ['Low', 'Medium', 'High', 'Critical']

export const COMPLAINT_STATUSES: ComplaintStatus[] = [
  'OPEN',
  'IN_PROGRESS',
  'RESOLVED',
]

export const AUTHORITIES: string[] = [
  'PHED',
  'Municipality',
  'Disaster Management',
  'Water Resources Department',
  'General Grievance',
]

export const MAP_CENTER: [number, number] = [30.0668, 79.0193]
export const MAP_ZOOM_DEFAULT = 8

export const SEVERITY_COLORS: Record<Severity, string> = {
  Critical: '#dc2626',
  High: '#ea580c',
  Medium: '#ca8a04',
  Low: '#16a34a',
}
