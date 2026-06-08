import { adminAxios } from './axios'
import type {
  IncidentListResponse,
  IncidentFilters,
  IncidentStatusResponse,
  IncidentNotesResponse,
} from '../types/incident'

export async function getIncidents(
  filters: IncidentFilters,
  adminKey: string
): Promise<IncidentListResponse> {
  const res = await adminAxios(adminKey).get('/api/v1/incidents', {
    params: filters,
  })
  return res.data
}

export async function updateIncidentStatus(
  incidentId: string,
  status: string,
  adminKey: string
): Promise<IncidentStatusResponse> {
  const res = await adminAxios(adminKey).patch(
    `/api/v1/incidents/${incidentId}/status`,
    { status }
  )
  return res.data
}

export async function updateIncidentNotes(
  incidentId: string,
  notes: string,
  adminKey: string
): Promise<IncidentNotesResponse> {
  const res = await adminAxios(adminKey).patch(
    `/api/v1/incidents/${incidentId}/notes`,
    { notes }
  )
  return res.data
}
