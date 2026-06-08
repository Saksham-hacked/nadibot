import { Link } from 'react-router-dom'
import AppShell from '../components/layout/AppShell'

export default function NotFound() {
  return (
    <AppShell>
      <div className="max-w-md mx-auto px-4 py-24 text-center">
        <p className="text-6xl font-bold text-slate-200 mb-4">404</p>
        <h1 className="text-xl font-bold text-slate-800 mb-2">Page Not Found</h1>
        <p className="text-sm text-slate-500 mb-8">
          The page you are looking for does not exist.
        </p>
        <Link
          to="/"
          className="px-5 py-2.5 bg-[#1a56db] text-white text-sm font-medium rounded hover:bg-blue-700"
        >
          Return to Home
        </Link>
      </div>
    </AppShell>
  )
}
