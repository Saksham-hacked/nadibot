import { Popup } from 'react-leaflet'
import Badge from '../ui/Badge'
import type { GeospatialIncident } from '../../types/analytics'
import { formatDate } from '../../utils/formatters'

interface MarkerPopupProps {
  incident: GeospatialIncident
}

export default function MarkerPopup({ incident }: MarkerPopupProps) {
  return (
    <Popup>
      <div className="space-y-1.5 min-w-[200px]">
        <p className="font-semibold text-slate-800 text-sm leading-snug">{incident.title}</p>
        <div className="flex flex-wrap gap-1">
          <Badge type="category">{incident.category}</Badge>
          <Badge type="severity" value={incident.severity} />
          <Badge type="status" value={incident.status} />
        </div>
        <p className="text-xs text-slate-600">{incident.complaint_count} complaint(s)</p>
        <p className="text-xs text-slate-600">{incident.district}, {incident.state}</p>
        <p className="text-xs text-slate-400">Reported: {formatDate(incident.created_at)}</p>
      </div>
    </Popup>
  )
}
