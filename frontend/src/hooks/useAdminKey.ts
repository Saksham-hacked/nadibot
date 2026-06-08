import { useAdminStore } from '../store/adminStore'

const STORAGE_KEY = 'nadibot_admin_key'

export function useAdminKey() {
  const { adminKey, setAdminKey: storeSet, clearAdminKey: storeClear } = useAdminStore()

  // Hydrate from sessionStorage if store is empty (page reload)
  if (!adminKey) {
    const stored = sessionStorage.getItem(STORAGE_KEY)
    if (stored) {
      storeSet(stored)
    }
  }

  function setKey(key: string) {
    sessionStorage.setItem(STORAGE_KEY, key)
    storeSet(key)
  }

  function clearKey() {
    sessionStorage.removeItem(STORAGE_KEY)
    storeClear()
  }

  return {
    adminKey: adminKey ?? sessionStorage.getItem(STORAGE_KEY),
    setKey,
    clearKey,
  }
}
