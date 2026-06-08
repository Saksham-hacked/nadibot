import { MapContainer, TileLayer, Marker } from 'react-leaflet'
import { Spinner } from '../ui/Spinner'
import { Alert } from '../ui/Alert'

interface LocationCaptureProps {
  latitude: number | null
  longitude: number | null
  accuracy: number | null
  loading: boolean
  error: string | null
  onRetry: () => void
}

export default function LocationCapture({
  latitude,
  longitude,
  accuracy,
  loading,
  error,
  onRetry,
}: LocationCaptureProps) {
  return (
    <div className="space-y-4">
      {loading && (
        <div className="flex items-center gap-3 text-slate-600">
          <Spinner size="sm" />
          <span className="text-sm">Capturing your location…</span>
        </div>
      )}

      {error && (
        <div className="space-y-3">
          <Alert variant="error" message={error} />
          <button
            type="button"
            onClick={onRetry}
            className="px-4 py-2 text-sm border border-slate-300 rounded hover:bg-slate-50"
          >
            Retry Location
          </button>
        </div>
      )}

      {latitude !== null && longitude !== null && accuracy !== null && (
        <div className="space-y-3">
          <div className="grid grid-cols-3 gap-3 p-4 bg-slate-50 border border-slate-200 rounded text-sm">
            <div>
              <p className="text-xs text-slate-500 mb-0.5">Latitude</p>
              <p className="font-mono font-medium text-slate-800">{latitude.toFixed(6)}</p>
            </div>
            <div>
              <p className="text-xs text-slate-500 mb-0.5">Longitude</p>
              <p className="font-mono font-medium text-slate-800">{longitude.toFixed(6)}</p>
            </div>
            <div>
              <p className="text-xs text-slate-500 mb-0.5">Accuracy</p>
              <p className="font-mono font-medium text-slate-800">{Math.round(accuracy)}m</p>
            </div>
          </div>

          <div className="h-48 rounded border border-slate-200 overflow-hidden">
            <MapContainer
              center={[latitude, longitude]}
              zoom={15}
              style={{ height: '100%', width: '100%' }}
              zoomControl={false}
            >
              <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
              <Marker position={[latitude, longitude]} />
            </MapContainer>
          </div>

          <button
            type="button"
            onClick={onRetry}
            className="text-sm text-[#1a56db] hover:underline"
          >
            Recapture Location
          </button>
        </div>
      )}
    </div>
  )
}
