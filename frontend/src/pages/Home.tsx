import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { getGeospatialData } from '../api/analytics'
import AppShell from '../components/layout/AppShell'
import { Droplets, MapPin, ClipboardList, CheckCircle } from 'lucide-react'

export default function Home() {
  const { data } = useQuery({
    queryKey: ['geospatial'],
    queryFn: getGeospatialData,
  })

  return (
    <AppShell>
      {/* Hero */}
      <section className="bg-white border-b border-slate-200">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16 text-center">
          <div className="flex justify-center mb-4">
            <Droplets size={44} className="text-[#1a56db]" />
          </div>
          <h1 className="text-3xl sm:text-4xl font-bold text-slate-900 mb-3">NadiBot</h1>
          <p className="text-lg text-slate-600 mb-8">
            AI-Powered Water Issue Reporting for Citizens
          </p>
          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <Link
              to="/report"
              className="px-6 py-3 bg-[#1a56db] text-white font-semibold rounded text-sm hover:bg-blue-700"
            >
              Report an Issue
            </Link>
            <Link
              to="/map"
              className="px-6 py-3 border border-[#1a56db] text-[#1a56db] font-semibold rounded text-sm hover:bg-blue-50"
            >
              View Incident Map
            </Link>
            <Link
              to="/track"
              className="px-6 py-3 text-slate-600 font-semibold rounded text-sm hover:bg-slate-100"
            >
              Track My Reports
            </Link>
          </div>
        </div>
      </section>

      {/* Live counts */}
      {data && (
        <section className="bg-slate-50 border-b border-slate-200">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex flex-col sm:flex-row gap-6 justify-center text-center">
            <div>
              <p className="text-2xl font-bold text-slate-800">{data.incidents.length}</p>
              <p className="text-xs text-slate-500 mt-0.5">Active Incidents on Map</p>
            </div>
            <div className="hidden sm:block w-px bg-slate-200" />
            <div>
              <p className="text-2xl font-bold text-slate-800">{data.complaints.length}</p>
              <p className="text-xs text-slate-500 mt-0.5">Total Complaints Reported</p>
            </div>
          </div>
        </section>
      )}

      {/* Feature cards */}
      <section className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-14">
        <h2 className="text-xl font-bold text-slate-800 text-center mb-8">
          How NadiBot Works
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          <FeatureCard
            icon={<ClipboardList size={28} className="text-[#1a56db]" />}
            title="Submit a Complaint"
            description="Describe the water issue using text, a photo, or a voice recording. Your location is captured automatically."
          />
          <FeatureCard
            icon={<MapPin size={28} className="text-[#1a56db]" />}
            title="AI Routing"
            description="NadiBot analyses your complaint and routes it to the correct authority — PHED, Municipality, or Disaster Management."
          />
          <FeatureCard
            icon={<CheckCircle size={28} className="text-[#1a56db]" />}
            title="Track Your Report"
            description="Use your anonymous Reporter ID to track the status of your complaint at any time."
          />
        </div>
      </section>
    </AppShell>
  )
}

function FeatureCard({ icon, title, description }: {
  icon: React.ReactNode
  title: string
  description: string
}) {
  return (
    <div className="border border-slate-200 rounded-lg p-6 bg-white shadow-sm">
      <div className="mb-3">{icon}</div>
      <h3 className="font-semibold text-slate-800 mb-2">{title}</h3>
      <p className="text-sm text-slate-600 leading-relaxed">{description}</p>
    </div>
  )
}
