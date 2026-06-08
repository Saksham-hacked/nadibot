import type { Category, Severity, IncidentStatus } from './common'

export interface Incident {
  incident_id: string
  title: string
  category: Category
  severity: Severity
  authority: string
  status: IncidentStatus
  latitude: number
  longitude: number
  district: string
  state: string
  complaint_count: number
  created_at: string
  updated_at: string
  notes?: string | null
}

export interface IncidentListResponse {
  incidents: Incident[]
  total: number
  page: number
  page_size: number
}

export interface IncidentFilters {
  authority?: string
  status?: IncidentStatus
  district?: string
  page?: number
  page_size?: number
}

export interface IncidentStatusResponse {
  incident_id: string
  status: IncidentStatus
  updated_at: string
}

export interface IncidentNotesResponse {
  incident_id: string
  notes: string
  updated_at: string
}
