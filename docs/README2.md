# HobbyHosting – Monorepo

Ett modernt DevOps-baserat plattformsprojekt byggt med microservices, Docker, FastAPI och Next.js. Allt hanteras via en central `docker-compose` setup och reverse proxy med Caddy.

---

## 📁 Struktur

```
hobbyhosting/
├── apps/                  # Fristående frontends
│   ├── public_site/       # Enkel statisk sida
│   ├── admin_panel/       # Minimal adminpanel
│   └── hobbyhosting-frontend/  # Legacy Next.js-projekt (tomt)
├── packages/
│   └── ui/                # Återanvändbara React-komponenter
├── services/              # Backend-tjänster
│   ├── auth_service/
│   ├── mail_service/
│   ├── ecommerce/
│   ├── database_service/
│   └── shared/            # Delad kod mellan tjänster
├── config/                # DevOps, Caddy, docker-compose
├── Makefile               # Kommandon för bygg, deploy, loggar
└── README.md
```

---

## 🚀 Kom igång

```bash
# Starta allt
make rebuild

# Starta en tjänst på nytt (t.ex. auth)
make restart-auth_service

# Kolla loggar
make logs-auth_service

# Kontrollera hälsa
make health-auth
```

---

## 🔑 Miljövariabler

Exempel finns i `.env.example`.
Development and production configs are generated with `./scripts/setup_env.sh`, creating `.env.dev` and `.env.prod`.

### Mail Service

- `RESEND_API_KEY` – API-nyckel för utskick via Resend
- `MAIL_FROM` – standardavsändare
- `JWT_SECRET` – hemlighet för verifiering av tokens
- `JWT_ALGO` – algoritm för signering (default HS256)

---

## 🌐 Subdomäner

| Subdomän               | Beskrivning          |
| ---------------------- | -------------------- |
| hobbyhosting.org       | Publik sida          |
| auth.hobbyhosting.org  | Autentiseringstjänst |
| admin.hobbyhosting.org | Adminpanel (Next.js) |
| mail.hobbyhosting.org  | Mail-service         |
| ecom.hobbyhosting.org  | E-commerce site      |

---

## 🐳 Docker

- Allt byggs och körs genom `config/docker-compose.yml`
- Caddy hanterar HTTPS + domäner automatiskt
- Alla tjänster körs via interna nätverk (`backend`)

---

## 🎨 Frontend & UI

Det finns ett separat paket `packages/ui` som innehåller återanvändbara
React-komponenter. Installera beroenden och bygg paketet via:

```bash
cd packages/ui
npm install
npm run build
```

Dessa komponenter kan sedan importeras i admin-frontenden för en enhetlig
design.

Frontend-apparna ligger under `apps/` och består av rena statiska filer:

- `public_site/` – enkel publiksida
- `admin_panel/` – lättviktigt admin-gränssnitt

Starta dem genom att öppna `index.html` direkt eller kör en simpel HTTP-server:

```bash
cd apps/public_site
python3 -m http.server
```

Surfa sedan till `http://localhost:8000` och API:et fungerar som vanligt via
Docker Compose.

---

## 🧪 Tester

Kör alla enhetstester och frontendtester med:

```bash
make test
```

In a fresh environment install the development dependencies first:

```bash
pip install -r requirements-dev.txt
npm install
```

Det använder `pytest` för Python och `jest` för JavaScript.

---

## 🧪 Testanvändare

| Email                  | Lösenord  |
| ---------------------- | --------- |
| admin@hobbyhosting.org | 1337      |
| demo@hobbyhosting.org  | secret123 |

Kör skriptet nedan för att skapa admins användare lokalt:

```bash
python services/auth_service/app/create_admin.py
```

---

## Auth Service API

- `POST /auth/login` – logga in och få JWT-token. Accepterar både `application/x-www-form-urlencoded` och `application/json` payloads
- `POST /auth/refresh` – byt ut ett giltigt token mot ett nytt
- `GET /auth/me` – hämta aktuell användare (kräver `Authorization` header)
- `POST /auth/register` – skapa ny användare
- `GET /auth/health` – hälsokontroll för tjänsten (finns även som `GET /health`)

Alla svar innehåller ett `access_token` som skickas som `Bearer`-token i `Authorization`-headern.

### Felsökning av inloggning

Om svaret du får tillbaka innehåller HTML (t.ex. `<!DOCTYPE html>`)
beror det oftast på att anropet går till fel domän eller port.
Se till att auth-tjänsten körs och att du anropar rätt adress,
exempelvis:

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "demo@hobbyhosting.org", "password": "secret123"}'
```

Svaret ska vara JSON med ett `access_token`. Ett HTML-svar innebär
vanligtvis en 404- eller proxy-felkod.

## Använda enkla inloggningssidor

Det finns statiska filer i `apps/public_site` som visar hur du kan logga in
och registrera dig utan ett fullständigt frontendbygge. Öppna `login.html`
eller `register.html` i webbläsaren medan auth-tjänsten kör lokalt på
`http://localhost:8000`. Vid lyckad inloggning sparas `access_token` i
`localStorage` och du skickas vidare till `welcome.html`. Markerar du rutan
"Log in after registration" sker inloggningen automatiskt efter lyckad
registrering.

---

## 🛠 TODO (för vidare utveckling)

- Lägga till CI/CD
- Integrera mailutskick
- Lägg till docs för hur auth fungerar
- Bygg vidare på `packages/ui` för delad design

---

> Senast uppdaterad: 4 maj 2025
