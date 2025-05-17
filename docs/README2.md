# HobbyHosting – Monorepo

Ett modernt DevOps-baserat plattformsprojekt byggt med microservices, Docker, FastAPI och Next.js. Allt hanteras via en central `docker-compose` setup och reverse proxy med Caddy.

---

## 📁 Struktur

```
hobbyhosting/
├── apps/                  # Fristående appar (frontend/adminjs etc)
│   └── hobbyhosting-frontend/
├── services/              # Backend-tjänster
│   ├── auth_service/
│   ├── mail_service/
│   ├── ecom/
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

| Subdomän                  | Beskrivning        |
|--------------------------|--------------------|
| hobbyhosting.org         | Publik sida        |
| auth.hobbyhosting.org    | Autentiseringstjänst |
| admin.hobbyhosting.org   | Adminpanel (Next.js) |
| mail.hobbyhosting.org   | Mail-service |
| ecom.hobbyhosting.org   | E-commerce site |

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

Det använder `pytest` för Python och `jest` för JavaScript.

---

## 🧪 Testanvändare

| Email                    | Lösenord     |
|--------------------------|--------------|
| admin@hobbyhosting.org   | 1337         |
| demo@hobbyhosting.org    | secret123    |

---

## Auth Service API

- `POST /auth/login` – logga in och få JWT-token
- `POST /auth/refresh` – byt ut ett giltigt token mot ett nytt
- `GET /auth/me` – hämta aktuell användare (kräver `Authorization` header)
- `POST /auth/register` – skapa ny användare
- `GET /health` – enkel hälsokoll (alias `/auth/health`)

Alla svar innehåller ett `access_token` som skickas som `Bearer`-token i `Authorization`-headern.

---

## 🛠 TODO (för vidare utveckling)

- Rensa upp gammal kod i hobbyhosting-frontend
- Lägga till CI/CD
- Integrera mailutskick
- Lägg till docs för hur auth fungerar

---

> Senast uppdaterad: 4 maj 2025
