import { v4 as uuidv4 } from 'uuid'

const KEY = 'nadibot_reporter_id'

export function useReporterId(): { reporterId: string } {
  let id = localStorage.getItem(KEY)
  if (!id) {
    id = uuidv4()
    localStorage.setItem(KEY, id)
  }
  return { reporterId: id }
}
