import { adminAxios, publicAxios } from './axios'
import type {
  AnalyticsOverview,
  CategoryDistribution,
  DistrictDistribution,
  TrendsResponse,
  GeospatialResponse,
} from '../types/analytics'

export async function getAnalyticsOverview(
  adminKey: string
): Promise<AnalyticsOverview> {
  const res = await adminAxios(adminKey).get('/api/v1/analytics/overview')
  return res.data
}

export async function getCategoryDistribution(
  adminKey: string
): Promise<CategoryDistribution> {
  const res = await adminAxios(adminKey).get('/api/v1/analytics/categories')
  return res.data
}

export async function getDistrictDistribution(
  adminKey: string
): Promise<DistrictDistribution> {
  const res = await adminAxios(adminKey).get('/api/v1/analytics/districts')
  return res.data
}

export async function getTrends(
  range: '7d' | '30d' | '90d',
  adminKey: string
): Promise<TrendsResponse> {
  const res = await adminAxios(adminKey).get('/api/v1/analytics/trends', {
    params: { range },
  })
  return res.data
}

export async function getGeospatialData(): Promise<GeospatialResponse> {
  const res = await publicAxios.get('/api/v1/analytics/geospatial')
  return res.data
}
