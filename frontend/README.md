# Fingerprint Scanner AI frontend

Next.js App Router client for the local FastAPI service.

```bash
npm install
cp .env.example .env.local
npm run dev
```

Set `NEXT_PUBLIC_API_URL` in `.env.local` to `http://localhost:8000` for local development, or to the Render service URL for deployment. The `.env.example` uses a production placeholder; replace it before running locally. Camera capture requires browser permission and localhost or HTTPS. Production output can be checked with `npm run build`.
