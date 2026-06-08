import { Link, NavLink, useNavigate } from 'react-router-dom'
import { Droplets, Menu, X } from 'lucide-react'
import { useState } from 'react'
import { useAdminKey } from '../../hooks/useAdminKey'

export default function Navbar() {
  const [open, setOpen] = useState(false)
  const { adminKey, clearKey } = useAdminKey()
  const navigate = useNavigate()

  const navClass = ({ isActive }: { isActive: boolean }) =>
    `text-sm font-medium px-3 py-1 rounded transition-colors ${
      isActive
        ? 'text-[#1a56db] bg-blue-50'
        : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
    }`

  function handleLogout() {
    clearKey()
    navigate('/admin')
  }

  return (
    <nav className="bg-white border-b border-slate-200 sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-14">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2">
            <Droplets size={22} className="text-[#1a56db]" />
            <span className="font-bold text-slate-800 text-base tracking-tight">NadiBot</span>
          </Link>

          {/* Desktop nav */}
          <div className="hidden sm:flex items-center gap-1">
            <NavLink to="/" end className={navClass}>Home</NavLink>
            <NavLink to="/report" className={navClass}>Report Issue</NavLink>
            <NavLink to="/map" className={navClass}>Incident Map</NavLink>
            <NavLink to="/track" className={navClass}>Track Report</NavLink>
            {adminKey ? (
              <>
                <NavLink to="/admin/dashboard" className={navClass}>Dashboard</NavLink>
                <button
                  onClick={handleLogout}
                  className="ml-2 text-sm font-medium px-3 py-1 rounded border border-slate-300 text-slate-600 hover:bg-slate-100"
                >
                  Logout
                </button>
              </>
            ) : (
              <NavLink
                to="/admin"
                className="ml-2 text-sm font-medium px-3 py-1 rounded border border-slate-300 text-slate-600 hover:bg-slate-100"
              >
                Admin
              </NavLink>
            )}
          </div>

          {/* Mobile hamburger */}
          <button
            className="sm:hidden p-2 rounded text-slate-600 hover:bg-slate-100"
            onClick={() => setOpen(!open)}
            aria-label="Toggle menu"
          >
            {open ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {open && (
        <div className="sm:hidden border-t border-slate-200 bg-white px-4 py-3 flex flex-col gap-1">
          <NavLink to="/" end className={navClass} onClick={() => setOpen(false)}>Home</NavLink>
          <NavLink to="/report" className={navClass} onClick={() => setOpen(false)}>Report Issue</NavLink>
          <NavLink to="/map" className={navClass} onClick={() => setOpen(false)}>Incident Map</NavLink>
          <NavLink to="/track" className={navClass} onClick={() => setOpen(false)}>Track Report</NavLink>
          {adminKey ? (
            <>
              <NavLink to="/admin/dashboard" className={navClass} onClick={() => setOpen(false)}>Dashboard</NavLink>
              <button onClick={handleLogout} className="text-left text-sm font-medium px-3 py-1 rounded text-slate-600 hover:bg-slate-100">
                Logout
              </button>
            </>
          ) : (
            <NavLink to="/admin" className={navClass} onClick={() => setOpen(false)}>Admin</NavLink>
          )}
        </div>
      )}
    </nav>
  )
}
