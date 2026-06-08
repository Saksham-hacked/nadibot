import type { Category, Severity, ComplaintStatus, IncidentStatus } from './common'

export interface AnalyticsOverview {
  total_complaints: number
  open_complaints: number
  resolved_complaints: number
  critical_complaints: number
  total_incidents: number
  open_incidents: number
  resolved_incidents: number
  resolution_rate: number
  average_resolution_time: number
}

export interface CategoryCount {
  category: string
  count: number
}

export interface CategoryDistribution {
  categories: CategoryCount[]
}

export interface DistrictCount {
  district: string
  count: number
}

export interface DistrictDistribution {
  districts: DistrictCount[]
}

export interface TrendPoint {
  date: string
  count: number
}

export interface TrendsResponse {
  range: string
  complaints: TrendPoint[]
  incidents: TrendPoint[]
}

export interface GeospatialComplaint {
  complaint_id: string
  latitude: number
  longitude: number
  category: Category
  severity: Severity
  status: ComplaintStatus
}

export interface GeospatialIncident {
  incident_id: string
  title: string
  latitude: number
  longitude: number
  category: Category
  severity: Severity
  status: IncidentStatus
  complaint_count: number
  district: string
  state: string
  created_at: string
}

export interface GeospatialResponse {
  complaints: GeospatialComplaint[]
  incidents: GeospatialIncident[]
}
