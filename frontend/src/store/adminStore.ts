import { create } from 'zustand'

interface AdminState {
  adminKey: string | null
  setAdminKey: (key: string) => void
  clearAdminKey: () => void
}

export const useAdminStore = create<AdminState>((set) => ({
  adminKey: null,
  setAdminKey: (key) => set({ adminKey: key }),
  clearAdminKey: () => set({ adminKey: null }),
}))
