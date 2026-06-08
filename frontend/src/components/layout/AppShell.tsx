import Navbar from './Navbar'
import Footer from './Footer'

interface AppShellProps {
  children: React.ReactNode
  fullHeight?: boolean
}

export default function AppShell({ children, fullHeight = false }: AppShellProps) {
  return (
    <div className={`min-h-screen flex flex-col bg-white ${fullHeight ? 'h-screen overflow-hidden' : ''}`}>
      <Navbar />
      <main className={`flex-1 ${fullHeight ? 'overflow-hidden' : ''}`}>
        {children}
      </main>
      {!fullHeight && <Footer />}
    </div>
  )
}
