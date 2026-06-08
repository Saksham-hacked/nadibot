import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import ReportPage from './pages/ReportPage'
import SubmissionSuccessPage from './pages/SubmissionSuccessPage'
import MapPage from './pages/MapPage'
import TrackPage from './pages/TrackPage'
import AdminLogin from './pages/AdminLogin'
import AdminDashboard from './pages/AdminDashboard'
import AdminIncidents from './pages/AdminIncidents'
import NotFound from './pages/NotFound'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/report" element={<ReportPage />} />
        <Route path="/report/success" element={<SubmissionSuccessPage />} />
        <Route path="/map" element={<MapPage />} />
        <Route path="/track" element={<TrackPage />} />
        <Route path="/admin" element={<AdminLogin />} />
        <Route path="/admin/dashboard" element={<AdminDashboard />} />
        <Route path="/admin/incidents" element={<AdminIncidents />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  )
}
