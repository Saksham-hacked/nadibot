import AppShell from '../components/layout/AppShell'
import ComplaintForm from '../components/complaint/ComplaintForm'

export default function ReportPage() {
  return (
    <AppShell>
      <div className="max-w-2xl mx-auto px-4 py-6">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-slate-800">Submit a Complaint</h1>
          <p className="text-sm text-slate-500 mt-1">
            Report a water issue in your area. Your complaint will be reviewed by the relevant authority.
          </p>
        </div>
        <ComplaintForm />
      </div>
    </AppShell>
  )
}
