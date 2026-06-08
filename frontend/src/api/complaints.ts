import { publicAxios } from './axios'
import type { ComplaintResponse, ComplaintListResponse } from '../types/complaint'

export async function submitComplaint(data: FormData): Promise<ComplaintResponse> {
  const res = await publicAxios.post('/api/v1/complaints', data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return res.data
}

export async function getComplaintsByReporter(
  reporterId: string
): Promise<ComplaintListResponse> {
  const res = await publicAxios.get('/api/v1/complaints', {
    params: { reporter_id: reporterId },
  })
  return res.data
}
