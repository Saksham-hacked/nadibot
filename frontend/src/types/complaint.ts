import type { Category, Severity, ComplaintStatus } from './common'

export interface ComplaintResponse {
  complaint_id: string
  incident_id: string
  reporter_id: string
  category: Category
  subcategory: string
  severity: Severity
  authority: string
  status: ComplaintStatus
  summary: string
  confidence: number
  latitude: number
  longitude: number
  district: string
  state: string
  locality: string
  image_url: string | null
  audio_url: string | null
  transcript: string | null
  image_summary: string | null
  created_at: string
}

export interface ComplaintListItem {
  complaint_id: string
  incident_id: string
  reporter_id: string
  category: Category
  subcategory: string
  severity: Severity
  authority: string
  status: ComplaintStatus
  summary: string
  latitude: number
  longitude: number
  district: string
  state: string
  locality: string
  image_url: string | null
  audio_url: string | null
  created_at: string
  updated_at: string
}

export interface ComplaintListResponse {
  complaints: ComplaintListItem[]
  total: number
}
