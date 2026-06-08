import { useRef } from 'react'
import { ImageIcon, X } from 'lucide-react'

interface ImageUploadProps {
  file: File | null
  onChange: (file: File | null) => void
  error?: string
}

export default function ImageUpload({ file, onChange, error }: ImageUploadProps) {
  const inputRef = useRef<HTMLInputElement>(null)
  const MAX_MB = 10

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const selected = e.target.files?.[0] ?? null
    if (!selected) return
    if (selected.size > MAX_MB * 1024 * 1024) {
      alert(`Image must be under ${MAX_MB}MB.`)
      return
    }
    onChange(selected)
  }

  function handleRemove() {
    onChange(null)
    if (inputRef.current) inputRef.current.value = ''
  }

  return (
    <div>
      {!file ? (
        <button
          type="button"
          onClick={() => inputRef.current?.click()}
          className="flex items-center gap-2 px-4 py-2 border border-dashed border-slate-300 rounded text-sm text-slate-600 hover:bg-slate-50"
        >
          <ImageIcon size={16} />
          Attach Image (optional, max 10MB)
        </button>
      ) : (
        <div className="flex items-center gap-3 p-3 border border-slate-200 rounded bg-slate-50">
          <img
            src={URL.createObjectURL(file)}
            alt="preview"
            className="w-14 h-14 object-cover rounded border border-slate-200"
          />
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-slate-700 truncate">{file.name}</p>
            <p className="text-xs text-slate-500">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
          </div>
          <button type="button" onClick={handleRemove} className="p-1 rounded hover:bg-slate-200 text-slate-500">
            <X size={16} />
          </button>
        </div>
      )}
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        className="hidden"
        onChange={handleChange}
      />
      {error && <p className="mt-1 text-xs text-red-600">{error}</p>}
    </div>
  )
}
