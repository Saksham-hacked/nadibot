import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useAdminKey } from '../hooks/useAdminKey'
import { getIncidents, updateIncidentStatus, updateIncidentNotes } from '../api/incidents'
import type { Incident, IncidentFilters } from '../types/incident'
import type { IncidentStatus } from '../types/common'
import AppShell from '../components/layout/AppShell'
import IncidentTable from '../components/dashboard/IncidentTable'
import Modal from '../components/ui/Modal'
import { Alert } from '../components/ui/Alert'
import { Spinner } from '../components/ui/Spinner'
import { COMPLAINT_STATUSES, AUTHORITIES } from '../utils/constants'
import { STATUS_LABELS } from '../types/common'

export default function AdminIncidents() {
  const { adminKey } = useAdminKey()
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  useEffect(() => {
    if (!adminKey) navigate('/admin', { replace: true })
  }, [adminKey, navigate])

  const [filters, setFilters] = useState<IncidentFilters>({ page: 1, page_size: 20 })
  const [authorityFilter, setAuthorityFilter] = useState('')
  const [districtFilter, setDistrictFilter] = useState('')
  const [statusFilter, setStatusFilter] = useState<IncidentStatus | ''>('')

  const [selectedIncident, setSelectedIncident] = useState<Incident | null>(null)
  const [modalStatus, setModalStatus] = useState<IncidentStatus>('OPEN')
  const [modalNotes, setModalNotes] = useState('')
  const [modalSuccess, setModalSuccess] = useState<string | null>(null)
  const [modalError, setModalError] = useState<string | null>(null)

  function applyFilters() {
    setFilters({
      page: 1,
      page_size: 20,
      authority: authorityFilter || undefined,
      district: districtFilter || undefined,
      status: (statusFilter as IncidentStatus) || undefined,
    })
  }

  const { data, isLoading, isError } = useQuery({
    queryKey: ['incidents', filters, adminKey],
    queryFn: () => getIncidents(filters, adminKey!),
    enabled: !!adminKey,
  })

  const saveMutation = useMutation({
    mutationFn: async () => {
      if (!selectedIncident || !adminKey) return
      await updateIncidentStatus(selectedIncident.incident_id, modalStatus, adminKey)
      if (modalNotes.trim()) {
        await updateIncidentNotes(selectedIncident.incident_id, modalNotes.trim(), adminKey)
      }
    },
    onSuccess: () => {
      setModalSuccess('Incident updated successfully.')
      queryClient.invalidateQueries({ queryKey: ['incidents'] })
      setTimeout(() => {
        setSelectedIncident(null)
        setModalSuccess(null)
      }, 1000)
    },
    onError: (err: unknown) => {
      const detail =
        err && typeof err === 'object' && 'response' in err
          ? (err as { response?: { data?: { detail?: string } } }).response?.data?.detail
          : undefined
      setModalError(detail ?? 'Failed to update incident.')
    },
  })

  function openModal(incident: Incident) {
    setSelectedIncident(incident)
    setModalStatus(incident.status)
    setModalNotes(incident.notes ?? '')
    setModalSuccess(null)
    setModalError(null)
  }

  const totalPages = data ? Math.ceil(data.total / (filters.page_size ?? 20)) : 1
  const currentPage = filters.page ?? 1

  return (
    <AppShell>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
        <div>
          <h1 className="text-2xl font-bold text-slate-800">Incident Management</h1>
          <p className="text-sm text-slate-500 mt-1">Review and update incident statuses.</p>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap gap-3 p-4 bg-slate-50 border border-slate-200 rounded-lg">
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value as IncidentStatus | '')}
            className="text-sm border border-slate-300 rounded px-3 py-1.5 bg-white focus:outline-none focus:ring-1 focus:ring-[#1a56db]"
          >
            <option value="">All Statuses</option>
            {COMPLAINT_STATUSES.map((s) => (
              <option key={s} value={s}>{STATUS_LABELS[s]}</option>
            ))}
          </select>
          <select
            value={authorityFilter}
            onChange={(e) => setAuthorityFilter(e.target.value)}
            className="text-sm border border-slate-300 rounded px-3 py-1.5 bg-white focus:outline-none focus:ring-1 focus:ring-[#1a56db]"
          >
            <option value="">All Authorities</option>
            {AUTHORITIES.map((a) => (
              <option key={a} value={a}>{a}</option>
            ))}
          </select>
          <input
            value={districtFilter}
            onChange={(e) => setDistrictFilter(e.target.value)}
            placeholder="Filter by district"
            className="text-sm border border-slate-300 rounded px-3 py-1.5 bg-white focus:outline-none focus:ring-1 focus:ring-[#1a56db]"
          />
          <button
            onClick={applyFilters}
            className="px-4 py-1.5 bg-[#1a56db] text-white text-sm rounded hover:bg-blue-700"
          >
            Apply
          </button>
        </div>

        {isLoading && (
          <div className="flex justify-center py-8">
            <Spinner />
          </div>
        )}
        {isError && (
          <Alert variant="error" message="Failed to load incidents. Please try again." />
        )}

        {data && (
          <>
            <IncidentTable incidents={data.incidents} onUpdate={openModal} showActions />
            <div className="flex items-center justify-between text-sm text-slate-600">
              <span>Page {currentPage} of {totalPages} — {data.total} total</span>
              <div className="flex gap-2">
                <button
                  onClick={() => setFilters((f) => ({ ...f, page: Math.max(1, (f.page ?? 1) - 1) }))}
                  disabled={currentPage <= 1}
                  className="px-3 py-1.5 border border-slate-300 rounded hover:bg-slate-50 disabled:opacity-40"
                >
                  Prev
                </button>
                <button
                  onClick={() => setFilters((f) => ({ ...f, page: (f.page ?? 1) + 1 }))}
                  disabled={currentPage >= totalPages}
                  className="px-3 py-1.5 border border-slate-300 rounded hover:bg-slate-50 disabled:opacity-40"
                >
                  Next
                </button>
              </div>
            </div>
          </>
        )}
      </div>

      <Modal
        isOpen={!!selectedIncident}
        onClose={() => setSelectedIncident(null)}
        title="Update Incident"
      >
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Status</label>
            <select
              value={modalStatus}
              onChange={(e) => setModalStatus(e.target.value as IncidentStatus)}
              className="w-full border border-slate-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#1a56db]"
            >
              {COMPLAINT_STATUSES.map((s) => (
                <option key={s} value={s}>{STATUS_LABELS[s]}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">
              Resolution Notes <span className="text-slate-400 font-normal">(optional)</span>
            </label>
            <textarea
              value={modalNotes}
              onChange={(e) => setModalNotes(e.target.value)}
              rows={3}
              placeholder="Add notes about resolution steps taken…"
              className="w-full border border-slate-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#1a56db] resize-none"
            />
          </div>

          {modalSuccess && <Alert variant="success" message={modalSuccess} />}
          {modalError && <Alert variant="error" message={modalError} />}

          <div className="flex gap-3 pt-1">
            <button
              onClick={() => setSelectedIncident(null)}
              className="flex-1 py-2 border border-slate-300 rounded text-sm text-slate-700 hover:bg-slate-50"
            >
              Cancel
            </button>
            <button
              onClick={() => saveMutation.mutate()}
              disabled={saveMutation.isPending}
              className="flex-1 py-2 bg-[#1a56db] text-white text-sm rounded hover:bg-blue-700 disabled:opacity-60 flex items-center justify-center gap-2"
            >
              {saveMutation.isPending ? <><Spinner size="sm" /> Saving…</> : 'Save Changes'}
            </button>
          </div>
        </div>
      </Modal>
    </AppShell>
  )
}
