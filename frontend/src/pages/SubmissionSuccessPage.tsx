import { useLocation, Navigate } from 'react-router-dom'
import AppShell from '../components/layout/AppShell'
import SubmissionSuccess from '../components/complaint/SubmissionSuccess'
import type { ComplaintResponse } from '../types/complaint'

interface LocationState {
  complaint: ComplaintResponse
}

export default function SubmissionSuccessPage() {
  const location = useLocation()
  const state = location.state as LocationState | null

  if (!state?.complaint) {
    return <Navigate to="/report" replace />
  }

  return (
    <AppShell>
      <SubmissionSuccess complaint={state.complaint} />
    </AppShell>
  )
}
