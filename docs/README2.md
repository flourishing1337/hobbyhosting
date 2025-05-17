# HobbyHosting – Monorepo

Ett modernt DevOps-baserat plattformsprojekt byggt med microservices, Docker, FastAPI och Next.js. Allt hanteras via en central `docker-compose` setup och reverse proxy med Caddy.

---

## 📁 Struktur

```
hobbyhosting/
├── apps/                  # Fristående appar (frontend/adminjs etc)
│   ├── public_site/
│   └── admin_panel/
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

### Mail Service

- `RESEND_API_KEY` – API-nyckel för utskick via Resend
- `MAIL_FROM` – standardavsändare
- `JWT_SECRET` – hemlighet för verifiering av tokens
- `JWT_ALGO` – algoritm för signering (default HS256)

---

## 🌐 Subdomäner

| Subdomän               | Beskrivning           |
| ---------------------- | --------------------- |
| hobbyhosting.org       | Publik sida           |
| auth.hobbyhosting.org  | Autentiseringstjänst  |
| admin.hobbyhosting.org | Admin Panel (Next.js) |
| mail.hobbyhosting.org  | Mail-service          |
| ecom.hobbyhosting.org  | E-commerce site       |

---

## 🐳 Docker

- Allt byggs och körs genom `config/docker-compose.yml`
- Caddy hanterar HTTPS + domäner automatiskt
- Alla tjänster körs via interna nätverk (`backend`)

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

---

## 🛠 TODO (för vidare utveckling)

- Rensa upp gammal kod i public_site
- Lägga till CI/CD
- Integrera mailutskick
- Lägg till docs för hur auth fungerar

---

> Senast uppdaterad: 4 maj 2025
