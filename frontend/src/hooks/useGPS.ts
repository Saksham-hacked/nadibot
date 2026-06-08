import { useState, useCallback } from 'react'

interface GPSState {
  latitude: number | null
  longitude: number | null
  accuracy: number | null
  loading: boolean
  error: string | null
  retry: () => void
}

const GPS_ERROR_MESSAGES: Record<number, string> = {
  1: 'Location access was denied. Please allow location access in your browser to submit a complaint.',
  2: 'Your location could not be determined. Please try again.',
  3: 'Location request timed out. Please try again.',
}

export function useGPS(): GPSState {
  const [latitude, setLatitude] = useState<number | null>(null)
  const [longitude, setLongitude] = useState<number | null>(null)
  const [accuracy, setAccuracy] = useState<number | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const capture = useCallback(() => {
    setLoading(true)
    setError(null)
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setLatitude(pos.coords.latitude)
        setLongitude(pos.coords.longitude)
        setAccuracy(pos.coords.accuracy)
        setLoading(false)
      },
      (err) => {
        setError(GPS_ERROR_MESSAGES[err.code] ?? 'An unknown error occurred.')
        setLoading(false)
      },
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
    )
  }, [])

  // capture on first mount via a ref trick — avoids useEffect lint issues
  const [started, setStarted] = useState(false)
  if (!started) {
    setStarted(true)
    capture()
  }

  return { latitude, longitude, accuracy, loading, error, retry: capture }
}
