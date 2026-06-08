import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAdminKey } from '../hooks/useAdminKey'
import { getAnalyticsOverview } from '../api/analytics'
import { Alert } from '../components/ui/Alert'
import { Spinner } from '../components/ui/Spinner'
import { Droplets } from 'lucide-react'

export default function AdminLogin() {
  const { adminKey, setKey } = useAdminKey()
  const navigate = useNavigate()
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (adminKey) navigate('/admin/dashboard', { replace: true })
  }, [adminKey, navigate])

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!input.trim()) return
    setLoading(true)
    setError(null)
    try {
      await getAnalyticsOverview(input.trim())
      setKey(input.trim())
      navigate('/admin/dashboard', { replace: true })
    } catch (err: unknown) {
      const status =
        err &&
        typeof err === 'object' &&
        'response' in err
          ? (err as { response?: { status?: number } }).response?.status
          : undefined
      if (status === 401 || status === 403) {
        setError('Invalid admin key. Please try again.')
      } else {
        setError('Could not reach server. Is the backend running?')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center px-4">
      <div className="w-full max-w-sm bg-white border border-slate-200 rounded-lg shadow-sm p-8">
        <div className="flex flex-col items-center mb-6">
          <Droplets size={32} className="text-[#1a56db] mb-2" />
          <h1 className="text-lg font-bold text-slate-800">NadiBot Admin</h1>
          <p className="text-xs text-slate-500 mt-1">Water Governance Dashboard</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Admin Key</label>
            <input
              type="password"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Enter admin key"
              className="w-full border border-slate-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[#1a56db]"
              autoComplete="current-password"
            />
          </div>

          {error && <Alert variant="error" message={error} />}

          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="w-full py-2.5 bg-[#1a56db] text-white text-sm font-semibold rounded hover:bg-blue-700 disabled:opacity-60 flex items-center justify-center gap-2"
          >
            {loading ? <><Spinner size="sm" /> Signing in…</> : 'Sign In'}
          </button>
        </form>
      </div>
    </div>
  )
}
