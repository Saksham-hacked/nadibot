import { useNavigate } from 'react-router-dom'
import { CheckCircle, Copy } from 'lucide-react'
import type { ComplaintResponse } from '../../types/complaint'
import Badge from '../ui/Badge'
import { formatDateTime } from '../../utils/formatters'

interface SubmissionSuccessProps {
  complaint: ComplaintResponse
}

export default function SubmissionSuccess({ complaint }: SubmissionSuccessProps) {
  const navigate = useNavigate()

  function copyToClipboard(text: string) {
    navigator.clipboard.writeText(text).catch(() => undefined)
  }

  return (
    <div className="max-w-lg mx-auto py-10 px-4 space-y-6">
      <div className="flex flex-col items-center text-center gap-2">
        <CheckCircle size={48} className="text-green-500" />
        <h1 className="text-2xl font-bold text-slate-800">Complaint Submitted Successfully</h1>
        <p className="text-sm text-slate-500">
          Your complaint has been received and routed to {complaint.authority}.
        </p>
      </div>

      <div className="border border-slate-200 rounded-lg p-5 space-y-4 bg-white shadow-sm">
        <div>
          <p className="text-xs text-slate-500 mb-1">Complaint ID</p>
          <p className="font-mono text-sm text-slate-800 bg-slate-50 px-3 py-2 rounded border border-slate-200 break-all">
            {complaint.complaint_id}
          </p>
        </div>
        <div>
          <p className="text-xs text-slate-500 mb-1">Incident ID</p>
          <p className="font-mono text-sm text-slate-700 bg-slate-50 px-3 py-2 rounded border border-slate-200 break-all">
            {complaint.incident_id}
          </p>
        </div>

        <div className="flex flex-wrap gap-2">
          <Badge type="category">{complaint.category}</Badge>
          <Badge type="severity" value={complaint.severity} />
          <Badge type="category">{complaint.authority}</Badge>
        </div>

        {complaint.summary && (
          <div>
            <p className="text-xs text-slate-500 mb-1">AI Summary</p>
            <p className="text-sm text-slate-700 bg-slate-50 px-3 py-2 rounded border border-slate-200">
              {complaint.summary}
            </p>
          </div>
        )}

        <div>
          <p className="text-xs text-slate-500 mb-1">Submitted</p>
          <p className="text-sm text-slate-700">{formatDateTime(complaint.created_at)}</p>
        </div>

        <div>
          <p className="text-xs text-slate-500 mb-1">Reporter ID</p>
          <div className="flex items-center gap-2">
            <p className="font-mono text-xs text-slate-700 bg-slate-50 px-3 py-2 rounded border border-slate-200 flex-1 break-all">
              {complaint.reporter_id}
            </p>
            <button
              onClick={() => copyToClipboard(complaint.reporter_id)}
              className="p-2 rounded border border-slate-200 hover:bg-slate-100 text-slate-500"
              title="Copy Reporter ID"
            >
              <Copy size={15} />
            </button>
          </div>
          <p className="text-xs text-slate-400 mt-1">Save your Reporter ID to track this complaint.</p>
        </div>
      </div>

      <div className="flex gap-3">
        <button
          onClick={() => navigate('/report')}
          className="flex-1 py-2.5 text-sm font-medium bg-[#1a56db] text-white rounded hover:bg-blue-700"
        >
          Report Another Issue
        </button>
        <button
          onClick={() => navigate('/track')}
          className="flex-1 py-2.5 text-sm font-medium border border-slate-300 rounded hover:bg-slate-50 text-slate-700"
        >
          Track My Reports
        </button>
      </div>
    </div>
  )
}
