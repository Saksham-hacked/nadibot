import { useQuery } from '@tanstack/react-query'
import AppShell from '../components/layout/AppShell'
import { useReporterId } from '../hooks/useReporterId'
import { getComplaintsByReporter } from '../api/complaints'
import Badge from '../components/ui/Badge'
import { Spinner } from '../components/ui/Spinner'
import { Alert } from '../components/ui/Alert'
import { formatDate, truncateId } from '../utils/formatters'

export default function TrackPage() {
  const { reporterId } = useReporterId()

  const { data, isLoading, isError } = useQuery({
    queryKey: ['complaints', reporterId],
    queryFn: () => getComplaintsByReporter(reporterId),
    enabled: !!reporterId,
  })

  return (
    <AppShell>
      <div className="max-w-3xl mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold text-slate-800 mb-1">Track Your Reports</h1>
        <p className="text-sm text-slate-500 mb-6">Complaints submitted from this device.</p>

        <div className="bg-slate-50 border border-slate-200 rounded px-4 py-3 mb-6">
          <p className="text-xs text-slate-500 mb-0.5">Your Reporter ID</p>
          <p className="font-mono text-xs text-slate-700 break-all">{reporterId}</p>
        </div>

        {isLoading && (
          <div className="flex justify-center py-10">
            <Spinner />
          </div>
        )}

        {isError && (
          <Alert variant="error" message="Could not load your complaints. Please try again." />
        )}

        {data && data.total === 0 && (
          <div className="text-center py-12 border border-dashed border-slate-300 rounded-lg text-slate-500 text-sm">
            No complaints found for your device.
            <br />
            Use the Report button to submit your first complaint.
          </div>
        )}

        {data && data.complaints.length > 0 && (
          <div className="space-y-4">
            <p className="text-xs text-slate-500">{data.total} complaint(s) found</p>
            {data.complaints.map((c) => (
              <div
                key={c.complaint_id}
                className="border border-slate-200 rounded-lg p-5 bg-white shadow-sm space-y-3"
              >
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <p className="font-mono text-xs text-slate-400">{truncateId(c.complaint_id)}</p>
                    <p className="text-sm font-semibold text-slate-800 mt-0.5">
                      {c.category} — {c.subcategory}
                    </p>
                  </div>
                  <div className="flex gap-1.5 flex-shrink-0">
                    <Badge type="severity" value={c.severity} />
                    <Badge type="status" value={c.status} />
                  </div>
                </div>

                {c.summary && (
                  <p className="text-sm text-slate-700">{c.summary}</p>
                )}

                <div className="text-xs text-slate-500 space-y-0.5">
                  <p>Incident: <span className="font-mono">{truncateId(c.incident_id)}</span></p>
                  <p>{c.district}, {c.state}</p>
                  <p>Submitted: {formatDate(c.created_at)}</p>
                </div>

                {c.image_url && (
                  <a
                    href={c.image_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-xs text-[#1a56db] hover:underline"
                  >
                    View Image
                  </a>
                )}

                {c.audio_url && (
                  <audio src={c.audio_url} controls className="w-full h-8 mt-1" />
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </AppShell>
  )
}
