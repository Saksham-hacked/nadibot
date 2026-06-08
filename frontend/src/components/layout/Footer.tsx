import { Droplets } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function Footer() {
  return (
    <footer className="bg-slate-50 border-t border-slate-200 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <Droplets size={18} className="text-[#1a56db]" />
            <span className="font-bold text-slate-700 text-sm">NadiBot</span>
          </div>
          <p className="text-xs text-slate-500">
            AI-Powered Water Governance Platform · Uttarakhand, India
          </p>
          <div className="flex gap-4">
            <Link to="/report" className="text-xs text-slate-500 hover:text-slate-700">Report Issue</Link>
            <Link to="/map" className="text-xs text-slate-500 hover:text-slate-700">Incident Map</Link>
            <Link to="/track" className="text-xs text-slate-500 hover:text-slate-700">Track Report</Link>
          </div>
        </div>
        <p className="mt-4 text-xs text-slate-400">
          © {new Date().getFullYear()} NadiBot. For official government use only.
        </p>
      </div>
    </footer>
  )
}
