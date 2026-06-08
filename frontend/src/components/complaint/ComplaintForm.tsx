import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'
import { submitComplaint } from '../../api/complaints'
import { useReporterId } from '../../hooks/useReporterId'
import { useGPS } from '../../hooks/useGPS'
import { useMediaRecorder } from '../../hooks/useMediaRecorder'
import LocationCapture from './LocationCapture'
import ImageUpload from './ImageUpload'
import AudioRecorder from './AudioRecorder'
import { Alert } from '../ui/Alert'
import { Spinner } from '../ui/Spinner'

type Step = 1 | 2 | 3

export default function ComplaintForm() {
  const navigate = useNavigate()
  const { reporterId } = useReporterId()
  const gps = useGPS()
  const mediaRecorder = useMediaRecorder()

  const [step, setStep] = useState<Step>(1)
  const [text, setText] = useState('')
  const [imageFile, setImageFile] = useState<File | null>(null)
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null)
  const [stepError, setStepError] = useState<string | null>(null)
  const [apiError, setApiError] = useState<string | null>(null)

  const { latitude, longitude, accuracy } = gps

  const mutation = useMutation({
    mutationFn: (fd: FormData) => submitComplaint(fd),
    onSuccess: (data) => {
      navigate('/report/success', { state: { complaint: data } })
    },
    onError: (err: unknown) => {
      const detail =
        err && typeof err === 'object' && 'response' in err
          ? (err as { response?: { data?: { detail?: string } } }).response?.data?.detail
          : undefined
      setApiError(detail ?? 'Something went wrong. Please try again.')
    },
  })

  function goToStep2() {
    if (latitude === null || longitude === null || accuracy === null) {
      setStepError('Please allow location access to continue.')
      return
    }
    setStepError(null)
    setStep(2)
  }

  function goToStep3() {
    if (!text.trim() && !imageFile && !audioBlob) {
      setStepError('Please provide at least one of: description, image, or audio recording.')
      return
    }
    setStepError(null)
    setStep(3)
  }

  function handleSubmit() {
    if (!latitude || !longitude || !accuracy) return
    setApiError(null)

    const fd = new FormData()
    if (text.trim()) fd.append('text', text.trim())
    if (imageFile) fd.append('image', imageFile)
    if (audioBlob) {
      const ext = audioBlob.type.includes('ogg') ? 'ogg' : 'webm'
      fd.append('audio', new File([audioBlob], `recording.${ext}`, { type: audioBlob.type }))
    }
    fd.append('reporter_id', reporterId)
    fd.append('latitude', String(latitude))
    fd.append('longitude', String(longitude))
    fd.append('accuracy', String(accuracy))
    fd.append('location_source', 'browser_gps')

    mutation.mutate(fd)
  }

  const stepLabels = ['Location', 'Your Complaint', 'Review & Submit']

  return (
    <div className="max-w-xl mx-auto py-8 px-4">
      {/* Step indicator */}
      <div className="flex items-center mb-8">
        {stepLabels.map((label, idx) => {
          const n = (idx + 1) as Step
          const active = step === n
          const done = step > n
          return (
            <div key={n} className="flex items-center flex-1 last:flex-none">
              <div className="flex flex-col items-center">
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold border-2 ${
                    done
                      ? 'bg-[#1a56db] border-[#1a56db] text-white'
                      : active
                      ? 'border-[#1a56db] text-[#1a56db] bg-white'
                      : 'border-slate-300 text-slate-400 bg-white'
                  }`}
                >
                  {done ? '✓' : n}
                </div>
                <span
                  className={`text-xs mt-1 text-center ${
                    active ? 'text-[#1a56db] font-medium' : 'text-slate-400'
                  }`}
                >
                  {label}
                </span>
              </div>
              {idx < stepLabels.length - 1 && (
                <div
                  className={`flex-1 h-0.5 mx-2 mb-5 ${done ? 'bg-[#1a56db]' : 'bg-slate-200'}`}
                />
              )}
            </div>
          )
        })}
      </div>

      {/* Step 1 — Location */}
      {step === 1 && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold text-slate-800">Step 1 — Capture Your Location</h2>
          <LocationCapture
            latitude={gps.latitude}
            longitude={gps.longitude}
            accuracy={gps.accuracy}
            loading={gps.loading}
            error={gps.error}
            onRetry={gps.retry}
          />
          {stepError && <Alert variant="error" message={stepError} />}
          <div className="pt-2">
            <button
              type="button"
              onClick={goToStep2}
              disabled={latitude === null || gps.loading}
              className="w-full py-2.5 bg-[#1a56db] text-white text-sm font-medium rounded hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>
        </div>
      )}

      {/* Step 2 — Complaint details */}
      {step === 2 && (
        <div className="space-y-5">
          <h2 className="text-lg font-semibold text-slate-800">Step 2 — Your Complaint</h2>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Description <span className="text-slate-400 font-normal">(optional)</span>
            </label>
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              rows={4}
              placeholder="Describe the water issue in detail…"
              className="w-full border border-slate-300 rounded px-3 py-2 text-sm text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-[#1a56db] resize-none"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Image <span className="text-slate-400 font-normal">(optional)</span>
            </label>
            <ImageUpload file={imageFile} onChange={setImageFile} />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Audio Recording <span className="text-slate-400 font-normal">(optional)</span>
            </label>
            <AudioRecorder onAudioChange={setAudioBlob} />
          </div>

          {stepError && <Alert variant="error" message={stepError} />}

          <div className="flex gap-3 pt-2">
            <button
              type="button"
              onClick={() => { setStepError(null); setStep(1) }}
              className="flex-1 py-2.5 border border-slate-300 text-slate-700 text-sm font-medium rounded hover:bg-slate-50"
            >
              Back
            </button>
            <button
              type="button"
              onClick={goToStep3}
              className="flex-1 py-2.5 bg-[#1a56db] text-white text-sm font-medium rounded hover:bg-blue-700"
            >
              Next
            </button>
          </div>
        </div>
      )}

      {/* Step 3 — Review & Submit */}
      {step === 3 && (
        <div className="space-y-5">
          <h2 className="text-lg font-semibold text-slate-800">Step 3 — Review & Submit</h2>

          <div className="border border-slate-200 rounded-lg divide-y divide-slate-100">
            <Row label="Location">
              {latitude?.toFixed(6)}, {longitude?.toFixed(6)} (±{Math.round(accuracy ?? 0)}m)
            </Row>
            {text && (
              <Row label="Description">
                {text.length > 100 ? text.slice(0, 100) + '…' : text}
              </Row>
            )}
            {imageFile && <Row label="Image">{imageFile.name}</Row>}
            {audioBlob && (
              <Row label="Audio">
                Recording attached ({mediaRecorder.durationSeconds}s)
              </Row>
            )}
            <Row label="Reporter ID">
              <span className="font-mono text-xs break-all">{reporterId}</span>
              <p className="text-xs text-slate-400 mt-0.5">
                This ID is your anonymous identifier. Save it to track your complaint.
              </p>
            </Row>
          </div>

          {apiError && <Alert variant="error" message={apiError} />}

          <div className="flex gap-3 pt-2">
            <button
              type="button"
              onClick={() => { setApiError(null); setStep(2) }}
              className="flex-1 py-2.5 border border-slate-300 text-slate-700 text-sm font-medium rounded hover:bg-slate-50"
            >
              Back
            </button>
            <button
              type="button"
              onClick={handleSubmit}
              disabled={mutation.isPending}
              className="flex-1 py-2.5 bg-[#1a56db] text-white text-sm font-medium rounded hover:bg-blue-700 disabled:opacity-60 flex items-center justify-center gap-2"
            >
              {mutation.isPending ? <><Spinner size="sm" /> Submitting…</> : 'Submit Complaint'}
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

function Row({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="px-4 py-3">
      <p className="text-xs text-slate-500 mb-0.5">{label}</p>
      <div className="text-sm text-slate-800">{children}</div>
    </div>
  )
}
