import { MapContainer, TileLayer, CircleMarker } from 'react-leaflet'
import { useState, Component } from 'react'
import { useQuery } from '@tanstack/react-query'
import { getGeospatialData } from '../../api/analytics'
import MarkerPopup from './MarkerPopup'
import Spinner from '../ui/Spinner'
import type { GeospatialIncident } from '../../types/analytics'
import type { Category, Severity, IncidentStatus } from '../../types/common'
import { MAP_CENTER, MAP_ZOOM_DEFAULT, SEVERITY_COLORS, CATEGORIES, SEVERITIES, COMPLAINT_STATUSES } from '../../utils/constants'
import { STATUS_LABELS } from '../../types/common'

// Simple error boundary to prevent map crash from bubbling up
class MapErrorBoundary extends Component<{ children: React.ReactNode }, { hasError: boolean }> {
  constructor(props: { children: React.ReactNode }) {
    super(props)
    this.state = { hasError: false }
  }
  static getDerivedStateFromError() { return { hasError: true } }
  render() {
    if (this.state.hasError) {
      return (
        <div className="flex items-center justify-center h-full text-slate-500 text-sm">
          Map failed to load. Please refresh.
        </div>
      )
    }
    return this.props.children
  }
}

export default function IncidentMap() {
  const [categoryFilter, setCategoryFilter] = useState<Category | 'All'>('All')
  const [severityFilter, setSeverityFilter] = useState<Severity | 'All'>('All')
  const [statusFilter, setStatusFilter] = useState<IncidentStatus | 'All'>('All')

  const { data, isLoading, isError } = useQuery({
    queryKey: ['geospatial'],
    queryFn: getGeospatialData,
  })

  const incidents: GeospatialIncident[] = (data?.incidents ?? []).filter((inc) => {
    if (categoryFilter !== 'All' && inc.category !== categoryFilter) return false
    if (severityFilter !== 'All' && inc.severity !== severityFilter) return false
    if (statusFilter !== 'All' && inc.status !== statusFilter) return false
    return true
  })

  return (
    <div className="relative h-full flex flex-col">
      {/* Filter bar */}
      <div className="flex flex-wrap gap-2 p-3 bg-white border-b border-slate-200 z-10">
        <select
          value={categoryFilter}
          onChange={(e) => setCategoryFilter(e.target.value as Category | 'All')}
          className="text-xs border border-slate-300 rounded px-2 py-1.5 text-slate-700 bg-white focus:outline-none focus:ring-1 focus:ring-[#1a56db]"
        >
          <option value="All">All Categories</option>
          {CATEGORIES.map((c) => <option key={c} value={c}>{c}</option>)}
        </select>
        <select
          value={severityFilter}
          onChange={(e) => setSeverityFilter(e.target.value as Severity | 'All')}
          className="text-xs border border-slate-300 rounded px-2 py-1.5 text-slate-700 bg-white focus:outline-none focus:ring-1 focus:ring-[#1a56db]"
        >
          <option value="All">All Severities</option>
          {SEVERITIES.map((s) => <option key={s} value={s}>{s}</option>)}
        </select>
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value as IncidentStatus | 'All')}
          className="text-xs border border-slate-300 rounded px-2 py-1.5 text-slate-700 bg-white focus:outline-none focus:ring-1 focus:ring-[#1a56db]"
        >
          <option value="All">All Statuses</option>
          {COMPLAINT_STATUSES.map((s) => <option key={s} value={s}>{STATUS_LABELS[s]}</option>)}
        </select>
        {isLoading && <Spinner size="sm" />}
        {isError && <span className="text-xs text-red-500 self-center">Failed to load incidents</span>}
        <span className="text-xs text-slate-500 self-center ml-auto">
          {incidents.length} incident(s) shown
        </span>
      </div>

      {/* Map */}
      <div className="flex-1">
        <MapErrorBoundary>
          <MapContainer
            center={MAP_CENTER}
            zoom={MAP_ZOOM_DEFAULT}
            style={{ height: '100%', width: '100%' }}
          >
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution="&copy; OpenStreetMap contributors"
            />
            {incidents.map((inc) => (
              <CircleMarker
                key={inc.incident_id}
                center={[inc.latitude, inc.longitude]}
                radius={8 + Math.min(inc.complaint_count * 2, 16)}
                pathOptions={{
                  fillColor: SEVERITY_COLORS[inc.severity],
                  color: SEVERITY_COLORS[inc.severity],
                  fillOpacity: 0.8,
                  weight: 1,
                }}
              >
                <MarkerPopup key={`popup-${inc.incident_id}`} incident={inc} />
              </CircleMarker>
            ))}
          </MapContainer>
        </MapErrorBoundary>
      </div>

      {/* Legend */}
      <div className="absolute bottom-6 left-3 z-[1000] bg-white border border-slate-200 rounded shadow p-3 space-y-1.5">
        <p className="text-xs font-semibold text-slate-600 mb-1">Severity</p>
        {SEVERITIES.map((s) => (
          <div key={s} className="flex items-center gap-2">
            <span
              className="inline-block w-3 h-3 rounded-full"
              style={{ backgroundColor: SEVERITY_COLORS[s] }}
            />
            <span className="text-xs text-slate-700">{s}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
