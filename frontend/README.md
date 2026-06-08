# NadiBot — Frontend

AI-powered water governance platform. Citizens report water issues; authorities manage them via a dashboard.

## Setup

1. **Install dependencies**
   ```
   npm install
   ```

2. **Configure environment**
   ```
   copy .env.example .env
   ```
   The default `.env` points to `http://localhost:8000` — no changes needed if the backend runs there.

3. **Start the backend** (must be running before the frontend)
   ```
   # From the backend directory:
   uvicorn main:app --reload --port 8000
   ```

4. **Start the frontend**
   ```
   npm run dev
   ```

5. Open [http://localhost:5173](http://localhost:5173)

## Routes

| Path | Description |
|------|-------------|
| `/` | Home — live incident counts, CTAs |
| `/report` | 3-step complaint form (GPS → content → submit) |
| `/report/success` | Confirmation after submission |
| `/map` | Leaflet map of all incidents with filters |
| `/track` | Track your complaints by Reporter ID |
| `/admin` | Admin key login |
| `/admin/dashboard` | Analytics overview, charts, recent incidents |
| `/admin/incidents` | Full incident table with status management |

## Notes

- Reporter ID is auto-generated (UUID) and stored in `localStorage`. It persists across reloads.
- Admin key is stored in `sessionStorage` and cleared on tab close.
- The map uses OpenStreetMap tiles — no API key required.
- All API calls read `VITE_API_BASE_URL` from the `.env` file. Never hardcoded.
