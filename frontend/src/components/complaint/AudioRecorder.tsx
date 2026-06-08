import { Mic, MicOff, Trash2 } from 'lucide-react'
import { useMediaRecorder } from '../../hooks/useMediaRecorder'

interface AudioRecorderProps {
  onAudioChange: (blob: Blob | null) => void
  error?: string
}

export default function AudioRecorder({ onAudioChange, error }: AudioRecorderProps) {
  const {
    startRecording,
    stopRecording,
    audioBlob,
    audioURL,
    status,
    clearRecording,
    durationSeconds,
  } = useMediaRecorder()

  function handleStop() {
    stopRecording()
  }

  function handleClear() {
    clearRecording()
    onAudioChange(null)
  }

  // notify parent when blob changes
  if (audioBlob && status === 'stopped') {
    onAudioChange(audioBlob)
  }

  return (
    <div>
      {status === 'idle' && !audioBlob && (
        <button
          type="button"
          onClick={startRecording}
          className="flex items-center gap-2 px-4 py-2 border border-dashed border-slate-300 rounded text-sm text-slate-600 hover:bg-slate-50"
        >
          <Mic size={16} />
          Record Audio (optional, max 25MB)
        </button>
      )}

      {status === 'recording' && (
        <div className="flex items-center gap-3 p-3 border border-red-200 rounded bg-red-50">
          <span className="inline-block w-3 h-3 rounded-full bg-red-500 animate-pulse" />
          <span className="text-sm text-red-700 font-medium">Recording… {durationSeconds}s</span>
          <button
            type="button"
            onClick={handleStop}
            className="ml-auto flex items-center gap-1 px-3 py-1 bg-red-600 text-white text-sm rounded hover:bg-red-700"
          >
            <MicOff size={14} /> Stop
          </button>
        </div>
      )}

      {status === 'stopped' && audioURL && (
        <div className="p-3 border border-slate-200 rounded bg-slate-50">
          <audio src={audioURL} controls className="w-full h-8" />
          <div className="flex items-center justify-between mt-2">
            <span className="text-xs text-slate-500">{durationSeconds}s recorded</span>
            <button
              type="button"
              onClick={handleClear}
              className="flex items-center gap-1 text-xs text-red-600 hover:text-red-800"
            >
              <Trash2 size={13} /> Clear
            </button>
          </div>
        </div>
      )}

      {error && <p className="mt-1 text-xs text-red-600">{error}</p>}
    </div>
  )
}
