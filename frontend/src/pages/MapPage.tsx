import AppShell from '../components/layout/AppShell'
import IncidentMap from '../components/map/IncidentMap'

export default function MapPage() {
  return (
    <AppShell fullHeight>
      <div className="h-[calc(100vh-56px)] flex flex-col">
        <div className="px-4 py-3 bg-white border-b border-slate-200">
          <h1 className="text-base font-bold text-slate-800">Water Incident Map</h1>
          <p className="text-xs text-slate-500">Live incidents reported across Uttarakhand</p>
        </div>
        <div className="flex-1">
          <IncidentMap />
        </div>
      </div>
    </AppShell>
  )
}
