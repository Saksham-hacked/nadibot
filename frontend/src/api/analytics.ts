import { adminAxios, publicAxios } from './axios'
import type {
  AnalyticsOverview,
  CategoryDistribution,
  DistrictDistribution,
  TrendsResponse,
  GeospatialResponse,
} from '../types/analytics'

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function tag(fn: string) {
  return `[analytics/${fn}]`
}

// ---------------------------------------------------------------------------
// Overview
// ---------------------------------------------------------------------------

export async function getAnalyticsOverview(
  adminKey: string
): Promise<AnalyticsOverview> {
  const T = tag('getAnalyticsOverview')
  console.log(`${T} → GET /api/v1/analytics/overview`)
  try {
    const res = await adminAxios(adminKey).get('/api/v1/analytics/overview')
    console.log(`${T} ✓ status=${res.status}`, res.data)
    return res.data
  } catch (err: any) {
    console.error(`${T} ✗ error`, err?.response?.status, err?.response?.data ?? err?.message)
    throw err
  }
}

// ---------------------------------------------------------------------------
// Categories
// ---------------------------------------------------------------------------

/**
 * Backend returns: CategoryStat[]  →  [{ category, count }, ...]
 * Frontend expects: CategoryDistribution  →  { categories: [{ category, count }, ...] }
 *
 * We normalise here so the chart never has to know about the shape mismatch.
 */
export async function getCategoryDistribution(
  adminKey: string
): Promise<CategoryDistribution> {
  const T = tag('getCategoryDistribution')
  console.log(`${T} → GET /api/v1/analytics/categories`)
  try {
    const res = await adminAxios(adminKey).get('/api/v1/analytics/categories')
    console.log(`${T} ✓ status=${res.status} raw response:`, res.data)

    // Backend sends a plain array; wrap it in the shape the UI expects.
    let categories: { category: string; count: number }[]

    if (Array.isArray(res.data)) {
      console.log(
        `${T} ⚠ Backend returned a plain array (${res.data.length} items). ` +
        `Wrapping into { categories: [...] } to match the frontend type.`
      )
      categories = res.data
    } else if (res.data && Array.isArray(res.data.categories)) {
      // Already the expected shape – just pass it through.
      console.log(`${T} ✓ Backend returned expected { categories: [...] } shape.`)
      categories = res.data.categories
    } else {
      console.warn(`${T} ⚠ Unexpected response shape:`, res.data, ' – defaulting to empty array.')
      categories = []
    }

    const result: CategoryDistribution = { categories }
    console.log(`${T} → returning to chart:`, result)
    return result
  } catch (err: any) {
    console.error(`${T} ✗ error`, err?.response?.status, err?.response?.data ?? err?.message)
    throw err
  }
}

// ---------------------------------------------------------------------------
// Districts
// ---------------------------------------------------------------------------

export async function getDistrictDistribution(
  adminKey: string
): Promise<DistrictDistribution> {
  const T = tag('getDistrictDistribution')
  console.log(`${T} → GET /api/v1/analytics/districts`)
  try {
    const res = await adminAxios(adminKey).get('/api/v1/analytics/districts')
    console.log(`${T} ✓ status=${res.status}`, res.data)

    let districts: { district: string; count: number }[]
    if (Array.isArray(res.data)) {
      console.log(`${T} ⚠ Plain array returned, wrapping into { districts: [...] }.`)
      districts = res.data
    } else {
      districts = res.data?.districts ?? []
    }

    return { districts }
  } catch (err: any) {
    console.error(`${T} ✗ error`, err?.response?.status, err?.response?.data ?? err?.message)
    throw err
  }
}

// ---------------------------------------------------------------------------
// Trends
// ---------------------------------------------------------------------------

/**
 * Backend TrendPoint shape:  { date: string, complaints: number, incidents: number }
 * Backend TrendsResponse:    { range: string, data: TrendPoint[] }
 *
 * Frontend TrendsResponse:   { range, complaints: { date, count }[], incidents: { date, count }[] }
 *
 * We split the merged backend points into two separate arrays here.
 */
export async function getTrends(
  range: '7d' | '30d' | '90d',
  adminKey: string
): Promise<TrendsResponse> {
  const T = tag('getTrends')
  console.log(`${T} → GET /api/v1/analytics/trends?range=${range}`)
  try {
    const res = await adminAxios(adminKey).get('/api/v1/analytics/trends', {
      params: { range },
    })
    console.log(`${T} ✓ status=${res.status} raw response:`, res.data)

    const raw = res.data

    // ---- Detect and handle both possible backend shapes ----

    // Shape A (current backend): { range, data: [{ date, complaints, incidents }] }
    if (raw && Array.isArray(raw.data)) {
      console.log(
        `${T} ⚠ Backend returned merged-point shape { range, data: [...] }. ` +
        `Splitting into separate complaints[] / incidents[] arrays.`
      )
      const complaints = raw.data.map((pt: any) => ({ date: pt.date, count: pt.complaints ?? 0 }))
      const incidents  = raw.data.map((pt: any) => ({ date: pt.date, count: pt.incidents  ?? 0 }))
      console.log(`${T} → complaints series (${complaints.length} pts):`, complaints)
      console.log(`${T} → incidents  series (${incidents.length}  pts):`, incidents)

      const result: TrendsResponse = { range: raw.range ?? range, complaints, incidents }
      console.log(`${T} → returning to chart:`, result)
      return result
    }

    // Shape B (expected frontend shape): { range, complaints: [...], incidents: [...] }
    if (raw && Array.isArray(raw.complaints) && Array.isArray(raw.incidents)) {
      console.log(`${T} ✓ Backend returned expected split-series shape.`)
      return raw as TrendsResponse
    }

    // Fallback – return empty series and warn loudly
    console.warn(
      `${T} ⚠ Unrecognised trends response shape. Rendering will show "No data available". Raw:`,
      raw
    )
    return { range, complaints: [], incidents: [] }
  } catch (err: any) {
    console.error(`${T} ✗ error`, err?.response?.status, err?.response?.data ?? err?.message)
    throw err
  }
}

// ---------------------------------------------------------------------------
// Geospatial
// ---------------------------------------------------------------------------

export async function getGeospatialData(): Promise<GeospatialResponse> {
  const T = tag('getGeospatialData')
  console.log(`${T} → GET /api/v1/analytics/geospatial`)
  try {
    const res = await publicAxios.get('/api/v1/analytics/geospatial')
    console.log(`${T} ✓ status=${res.status}`, res.data)
    return res.data
  } catch (err: any) {
    console.error(`${T} ✗ error`, err?.response?.status, err?.response?.data ?? err?.message)
    throw err
  }
}
