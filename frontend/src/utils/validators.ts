export function isValidLatitude(lat: number): boolean {
  return lat >= -90 && lat <= 90
}

export function isValidLongitude(lng: number): boolean {
  return lng >= -180 && lng <= 180
}

export function isValidAccuracy(acc: number): boolean {
  return acc > 0
}

export const MAX_IMAGE_SIZE = 10 * 1024 * 1024  // 10MB
export const MAX_AUDIO_SIZE = 25 * 1024 * 1024  // 25MB
