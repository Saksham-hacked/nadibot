import { useState, useRef, useCallback, useEffect } from 'react'

type RecordingStatus = 'idle' | 'recording' | 'stopped'

interface MediaRecorderState {
  startRecording: () => void
  stopRecording: () => void
  audioBlob: Blob | null
  audioURL: string | null
  status: RecordingStatus
  clearRecording: () => void
  durationSeconds: number
}

export function useMediaRecorder(): MediaRecorderState {
  const [status, setStatus] = useState<RecordingStatus>('idle')
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null)
  const [audioURL, setAudioURL] = useState<string | null>(null)
  const [durationSeconds, setDurationSeconds] = useState(0)

  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const chunksRef = useRef<Blob[]>([])
  const streamRef = useRef<MediaStream | null>(null)
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null)
  const urlRef = useRef<string | null>(null)

  const mimeType = MediaRecorder.isTypeSupported('audio/webm')
    ? 'audio/webm'
    : 'audio/ogg'

  const startRecording = useCallback(async () => {
    chunksRef.current = []
    setDurationSeconds(0)
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    streamRef.current = stream
    const recorder = new MediaRecorder(stream, { mimeType })
    mediaRecorderRef.current = recorder

    recorder.ondataavailable = (e) => {
      if (e.data.size > 0) chunksRef.current.push(e.data)
    }

    recorder.onstop = () => {
      const blob = new Blob(chunksRef.current, { type: mimeType })
      const url = URL.createObjectURL(blob)
      urlRef.current = url
      setAudioBlob(blob)
      setAudioURL(url)
      setStatus('stopped')
    }

    recorder.start()
    setStatus('recording')

    intervalRef.current = setInterval(() => {
      setDurationSeconds((prev) => prev + 1)
    }, 1000)
  }, [mimeType])

  const stopRecording = useCallback(() => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current)
      intervalRef.current = null
    }
    mediaRecorderRef.current?.stop()
    streamRef.current?.getTracks().forEach((t) => t.stop())
  }, [])

  const clearRecording = useCallback(() => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current)
      intervalRef.current = null
    }
    if (urlRef.current) {
      URL.revokeObjectURL(urlRef.current)
      urlRef.current = null
    }
    streamRef.current?.getTracks().forEach((t) => t.stop())
    setAudioBlob(null)
    setAudioURL(null)
    setStatus('idle')
    setDurationSeconds(0)
    chunksRef.current = []
  }, [])

  useEffect(() => {
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current)
      if (urlRef.current) URL.revokeObjectURL(urlRef.current)
      streamRef.current?.getTracks().forEach((t) => t.stop())
    }
  }, [])

  return { startRecording, stopRecording, audioBlob, audioURL, status, clearRecording, durationSeconds }
}
