# Fingerprint Scanner AI frontend

Next.js App Router client for the local FastAPI service.

```bash
npm install
copy .env.example .env.local
npm run dev
```

Set `NEXT_PUBLIC_API_URL` to the backend origin (default `http://localhost:8000`). Camera capture requires browser permission and localhost or HTTPS. Production output can be checked with `npm run build`.
