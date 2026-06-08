import React from 'react'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
  children: React.ReactNode
}

export function Button({
  variant = 'primary',
  size = 'md',
  loading = false,
  children,
  className = '',
  disabled,
  ...props
}: ButtonProps) {
  const base =
    'inline-flex items-center justify-center font-medium rounded border transition-colors focus:outline-none focus:ring-2 focus:ring-offset-1'

  const variants = {
    primary:
      'bg-[#1a56db] text-white border-[#1a56db] hover:bg-[#1648c0] focus:ring-[#1a56db] disabled:bg-slate-400 disabled:border-slate-400',
    secondary:
      'bg-white text-[#1a56db] border-[#1a56db] hover:bg-blue-50 focus:ring-[#1a56db] disabled:text-slate-400 disabled:border-slate-300',
    ghost:
      'bg-transparent text-[#1a56db] border-transparent hover:bg-blue-50 focus:ring-[#1a56db] disabled:text-slate-400',
    danger:
      'bg-red-600 text-white border-red-600 hover:bg-red-700 focus:ring-red-500 disabled:bg-slate-400',
  }

  const sizes = {
    sm: 'px-3 py-1.5 text-sm gap-1.5',
    md: 'px-4 py-2 text-sm gap-2',
    lg: 'px-6 py-3 text-base gap-2',
  }

  return (
    <button
      className={`${base} ${variants[variant]} ${sizes[size]} ${className}`}
      disabled={disabled || loading}
      {...props}
    >
      {loading && (
        <svg
          className="animate-spin h-4 w-4"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8v8H4z"
          />
        </svg>
      )}
      {children}
    </button>
  )
}
