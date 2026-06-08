import { AlertCircle, CheckCircle, Info, XCircle } from 'lucide-react'

type AlertVariant = 'error' | 'success' | 'info' | 'warning'

interface AlertProps {
  variant?: AlertVariant
  message?: string
  children?: React.ReactNode
}

const config: Record<AlertVariant, { cls: string; Icon: React.ElementType }> = {
  error: { cls: 'bg-red-50 border-red-300 text-red-800', Icon: XCircle },
  success: { cls: 'bg-green-50 border-green-300 text-green-800', Icon: CheckCircle },
  info: { cls: 'bg-blue-50 border-blue-300 text-blue-800', Icon: Info },
  warning: { cls: 'bg-yellow-50 border-yellow-300 text-yellow-800', Icon: AlertCircle },
}

export function Alert({ variant = 'error', message, children }: AlertProps) {
  const { cls, Icon } = config[variant]
  return (
    <div className={`flex items-start gap-2 px-4 py-3 rounded border text-sm ${cls}`}>
      <Icon className="h-4 w-4 mt-0.5 flex-shrink-0" />
      <span>{children ?? message}</span>
    </div>
  )
}

export default Alert
