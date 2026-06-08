import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_BASE_URL

export const publicAxios = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
})

export function adminAxios(adminKey: string) {
  return axios.create({
    baseURL: BASE_URL,
    headers: {
      'Content-Type': 'application/json',
      'X-Admin-Key': adminKey,
    },
  })
}

publicAxios.interceptors.response.use(
  (res) => res,
  (error) => {
    if (
      error.response?.status === 401 ||
      error.response?.status === 403
    ) {
      window.location.href = '/admin'
    }
    return Promise.reject(error)
  }
)
