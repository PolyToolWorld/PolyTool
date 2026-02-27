<div align="center">
  <br />
  <img src="https://polytool.world/logo.png" width="120" height="120" alt="PolyTool" />
  <br /><br />

  <h1>PolyTool</h1>
  <p><strong>Open-source copy-trading platform for Polymarket</strong></p>

  <a href="https://polytool.world">
    <img src="https://img.shields.io/badge/🌐%20Live%20Site-polytool.world-4c6ef5?style=for-the-badge" alt="Live Site" />
  </a>
  &nbsp;
  <a href="https://builders.polymarket.com">
    <img src="https://img.shields.io/badge/Polymarket%20Builders%20Program-9b59b6?style=for-the-badge" alt="Builders Program" />
  </a>
  &nbsp;
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge" alt="MIT" />
  </a>

  <br /><br />

  <img src="https://img.shields.io/badge/Next.js-13+-000000?style=flat-square&logo=next.js&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/TypeScript-5.0+-3178C6?style=flat-square&logo=typescript&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3.10+-3776ab?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Tailwind-3.0+-38bdf8?style=flat-square&logo=tailwind-css&logoColor=white" />
  <img src="https://img.shields.io/badge/Polygon-137-8247e5?style=flat-square&logo=polygon&logoColor=white" />

  <br /><br />
</div>

---

## What is PolyTool?

**PolyTool** is an open-source copy-trading platform for Polymarket that lets you automatically mirror the trades of top-performing wallets. The platform consists of a web dashboard (Next.js) and a standalone bot (Python) that runs on your server or local machine.

### Key capabilities

- 🔄 **Automatic copy-trading**: track wallets and automatically copy their trades
- 📊 **Analytics**: monitor performance and detailed trading statistics
- 💼 **Portfolio management**: track positions and balances in one place
- 🔑 **API keys & settings**: securely manage credentials and configuration

> **🔒 Security:** Your private key never leaves your machine. It is used only locally to sign orders via `py-clob-client`.

---

## Features

| **Copy Trading** | **Analytics** |
|------------------|---------------|
| Automatically copy trades from tracked wallets | Detailed stats across all trades and overall performance |
| Configurable filters (minimum size, price range, etc.) | P&L charts, win rate, ROI |
| Modes: Auto (auto-execution) and Manual (notifications only) | Full history of copied and detected trades |
| Flexible position sizing (fixed amount, proportional, percentage) | Export data to CSV/JSON |

| **Portfolio** | **API Keys** |
|---------------|--------------|
| Real-time monitoring of all open positions | Encrypted storage of API keys |
| Balance and available funds tracking | Manage multiple keys for different strategies |
| Full history of portfolio changes | Automatic key rotation |
| Integration with Polymarket CLOB API | Audit log of all key operations |

---

## Project architecture

```text
polytool/
├── frontend/                    # Next.js web application
│   ├── app/                     # App Router (Next.js 13+)
│   │   ├── copytrade/           # Copy-trading page
│   │   ├── analytics/           # Analytics page
│   │   ├── portfolio/           # Portfolio page
│   │   └── settings/            # Settings & API keys
│   ├── components/              # React components
│   │   ├── WalletTracker.tsx    # Wallet tracking component
│   │   ├── TradeList.tsx        # Trade list
│   │   └── PortfolioChart.tsx   # Portfolio charts
│   ├── lib/                     # Utilities and API clients
│   │   ├── api.ts               # Backend API client
│   │   └── polymarket.ts        # Polymarket API integration
│   └── package.json             # Next.js, TypeScript, Tailwind deps
│
├── backend/                     # FastAPI backend (separate repo)
│   ├── app/
│   │   ├── api/                 # API endpoints
│   │   │   ├── bot/             # Bot API (config, trade, heartbeat)
│   │   │   ├── wallets/         # Wallet management
│   │   │   └── analytics/       # Analytics endpoints
│   │   ├── models/              # SQLAlchemy models
│   │   └── services/            # Business logic
│   └── requirements.txt         # Python dependencies
│
└── polytool-bot/                # Standalone copy-trading bot (this repo)
    ├── src/polytool_bot/
    │   ├── cli.py               # Click CLI: run / status / configure
    │   ├── config.py            # Pydantic settings (reads .env)
    │   ├── state.py             # Local JSON state for trade deduplication
    │   ├── worker.py            # Main polling loop
    │   ├── api/
    │   │   ├── polytool.py      # PolyTool backend client (X-API-Key auth)
    │   │   └── polymarket.py    # Polymarket Data / CLOB / Gamma APIs
    │   └── engine/
    │       ├── copytrade.py     # Trade detection, filtering, size calculation
    │       ├── executor.py      # Place CLOB orders via py-clob-client
    │       └── signer.py        # HMAC signing for builder attribution
    ├── docker-compose.yml       # Docker Compose configuration
    ├── Dockerfile               # Docker image for the bot
    ├── pyproject.toml           # Python package configuration
    └── .env.example             # Example environment variables
```

---

## How it works

```text
┌─────────────────────────────────────────────────────────────────┐
│                        WALLET CONNECTION                        │
│  User → polytool.world → Connect MetaMask/Wallet                │
│  → Automatic retrieval of CLOB API credentials                  │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      COPY-TRADING SETUP                         │
│  Dashboard → Add wallets to track                               │
│  → Configure filters (min size, price range, copy sells)        │
│  → Choose mode: Auto (auto-execution) or Manual (alerts only)   │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                         STARTING THE BOT                        │
│  polytool-bot run → Load config from .env                       │
│  → Connect to PolyTool API (X-API-Key)                          │
│  → Fetch list of tracked wallets                                │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│               MAIN LOOP (every 15 seconds)                      │
│                                                                 │
│  1. GET /api/bot/config                                         │
│     └─> Get tracked wallets and copy-trading settings           │
│         │                                                       │
│         ▼                                                       │
│  2. Fetch latest trades from Polymarket Data API                │
│     └─> GET /trades?user={wallet_address}&limit=50              │
│         │                                                       │
│         ▼                                                       │
│  3. Filter trades                                               │
│     ├─> Already seen? → Skip                                    │
│     ├─> Below minimum size? → Skip                              │
│     ├─> Outside price range? → Skip                             │
│     └─> Copy sells disabled? → Skip                             │
│         │                                                       │
│         ├─> DO NOT COPY → POST /api/bot/trade (action: DETECTED)│
│         │                                                       │
│         └─> COPY →                                              │
│             │                                                   │
│             ▼                                                   │
│  4. Calculate position size                                     │
│     ├─> fixed: fixed notional size                              │
│     ├─> proportional: original size × multiplier                │
│     └─> percentage: percentage of original size                 │
│             │                                                   │
│             ▼                                                   │
│  5. Fetch orderbook for token                                   │
│     └─> GET /book?token_id={token_id}                           │
│             │                                                   │
│             ▼                                                   │
│  6. Sign and place limit order on CLOB                          │
│     └─> py-clob-client.create_order() → POST /orders            │
│             │                                                   │
│             ▼                                                   │
│  7. POST /api/bot/trade (log in dashboard)                      │
│     └─> Persist result in database                              │
│             │                                                   │
│             ▼                                                   │
│  8. Save trade_id to state.json (deduplication)                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                        DASHBOARD VIEW                           │
│  Frontend → Poll /api/analytics → show stats                    │
│  → P&L charts, trade list, portfolio status                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Tech stack

| Component        | Technology   | Version                            | Purpose                              |
|------------------|-------------|------------------------------------|--------------------------------------|
| **Frontend**     | Next.js     | 13+                                | React framework with App Router      |
|                  | TypeScript  | 5.0+                               | Type safety                          |
|                  | Tailwind CSS| 3.0+                               | Utility-first CSS framework          |
|                  | React Query | 4+                                 | State and data fetching management   |
| **Backend**      | FastAPI     | 0.100+                             | Async Python web framework           |
|                  | Python      | 3.10+                              | Backend language                     |
|                  | SQLAlchemy  | 2.0+                               | ORM for database access              |
|                  | Pydantic    | 2.0+                               | Data validation & settings           |
| **Bot**          | Python      | 3.10+                              | Standalone copy-trading bot          |
|                  | Click       | 8.1+                               | CLI interface                        |
|                  | httpx       | 0.27+                              | Async HTTP client                    |
|                  | py-clob-client | 0.19+                           | Polymarket CLOB client               |
| **Infrastructure**| Docker     | Latest                             | Containerization                     |
|                  | Docker Compose | Latest                          | Container orchestration              |
| **Blockchain**   | Polygon     | 137                                | Network for Polymarket               |
|                  | Web3        | -                                  | Blockchain integration               |

---

## Quick start

### Backend (FastAPI)

```bash
# Clone backend repository
git clone https://github.com/polytool/backend.git
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your DB and API settings

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (Next.js)

```bash
# Clone frontend repository
git clone https://github.com/polytool/frontend.git
cd frontend

# Install dependencies
npm install
# or
yarn install

# Configure environment variables
cp .env.example .env.local
# Edit .env.local with backend API URL

# Start dev server
npm run dev
# or
yarn dev

# Open http://localhost:3000
```

### Bot (Docker)

```bash
# Clone bot repository
git clone https://github.com/polytool/polytool-bot.git
cd polytool-bot

# Create .env file
cp .env.example .env
# Edit .env with your credentials

# Start via Docker Compose
docker compose up -d

# View logs
docker compose logs -f
```

### Bot (Local)

```bash
# Clone repository
git clone https://github.com/polytool/polytool-bot.git
cd polytool-bot

# Install package
pip install -e .

# Configure .env
cp .env.example .env
# Edit .env

# Run bot
polytool-bot run

# Check status
polytool-bot status
```

---

## API reference

### Bot API endpoints

#### `GET /api/bot/config`

Get configuration for tracked wallets and copy-trading settings.

**Headers:**

```text
X-API-Key: plk_your_api_key_here
```

**Response:**

```json
{
  "wallet_address": "0x...",
  "proxy_wallet": "0x...",
  "has_credentials": true,
  "tracked_wallets": [
    {
      "wallet_address": "0x...",
      "label": "Top Trader",
      "is_enabled": true,
      "mode": "auto",
      "min_trade_size": 10.0,
      "copy_sells": true,
      "max_price": 0.95,
      "min_price": 0.01,
      "size_mode": "fixed",
      "fixed_amount": 5.0,
      "proportional_multiplier": 1.0
    }
  ]
}
```

#### `POST /api/bot/trade`

Report an executed or detected trade.

**Headers:**

```text
X-API-Key: plk_your_api_key_here
Content-Type: application/json
```

**Request body:**

```json
{
  "action": "COPY_BUY",
  "market_title": "Will BTC reach $100k by 2025?",
  "token_id": "0x...",
  "outcome": "Yes",
  "side": "BUY",
  "price": 0.65,
  "size": 5.0,
  "total_cost": 3.25,
  "order_id": "0x...",
  "status": "placed",
  "copied_from_wallet": "0x...",
  "error_message": ""
}
```

**Response:**

```json
{
  "success": true,
  "trade_id": 123,
  "message": "Trade logged successfully"
}
```

#### `POST /api/bot/heartbeat`

Send a heartbeat to indicate that the bot is alive.

**Headers:**

```text
X-API-Key: plk_your_api_key_here
```

**Response:**

```json
{
  "user": "user@example.com",
  "server_time": "2024-01-01T00:00:00Z",
  "status": "ok"
}
```

### Polymarket API integration

The bot uses the following Polymarket APIs:

- **Data API** (`https://data-api.polymarket.com`): trades and positions
- **CLOB API** (`https://clob.polymarket.com`): order placement
- **Gamma API** (`https://gamma-api.polymarket.com`): market information

---

## Environment variables

### Backend (`.env`)

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/polytool

# JWT Secret
JWT_SECRET=your_jwt_secret_key_here

# CORS
CORS_ORIGINS=http://localhost:3000,https://polytool.world

# Polymarket API
POLYMARKET_CLOB_URL=https://clob.polymarket.com
POLYMARKET_DATA_URL=https://data-api.polymarket.com
POLYMARKET_GAMMA_URL=https://gamma-api.polymarket.com

# Chain
CHAIN_ID=137

# Environment
ENVIRONMENT=development
```

### Frontend (`.env.local`)

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
# or for production
NEXT_PUBLIC_API_URL=https://api.polytool.world

# Polymarket
NEXT_PUBLIC_POLYMARKET_URL=https://polymarket.com
```

### Bot (`.env`)

```env
# Required
POLYTOOL_API_KEY=plk_your_key_here
PRIVATE_KEY=0x...
CLOB_API_KEY=your_clob_key
CLOB_API_SECRET=your_clob_secret
CLOB_API_PASSPHRASE=your_clob_passphrase

# Optional
PROXY_WALLET=0x...
POLY_BUILDER_API_KEY=your_builder_key
POLY_BUILDER_SECRET=your_builder_secret
POLY_BUILDER_PASSPHRASE=your_builder_passphrase
API_URL=https://polytool.world
POLL_INTERVAL=15
CHAIN_ID=137
CLOB_API_URL=https://clob.polymarket.com
GAMMA_API_URL=https://gamma-api.polymarket.com
DATA_API_URL=https://data-api.polymarket.com
STATE_FILE=state.json
```

---

## Deployment

### Backend (VPS / cloud)

```bash
# On the server
git clone https://github.com/polytool/backend.git
cd backend

# Install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure .env
nano .env

# Run via systemd
sudo nano /etc/systemd/system/polytool-backend.service
```

**systemd service file:**

```ini
[Unit]
Description=PolyTool Backend API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/polytool/backend
Environment="PATH=/opt/polytool/backend/venv/bin"
ExecStart=/opt/polytool/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable polytool-backend
sudo systemctl start polytool-backend
```

### Frontend (Vercel / Netlify)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel

# Or via GitHub Actions (CI-based deploy)
```

**`vercel.json`:**

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "env": {
    "NEXT_PUBLIC_API_URL": "https://api.polytool.world"
  }
}
```

### Bot (Docker on VPS)

```bash
# On the server
git clone https://github.com/polytool/polytool-bot.git
cd polytool-bot

# Create .env
nano .env

# Start via Docker Compose
docker compose up -d

# Enable Docker on boot
sudo systemctl enable docker
```

**`docker-compose.yml`:**

```yaml
services:
  bot:
    build: .
    env_file: .env
    restart: unless-stopped
    volumes:
      - ./state.json:/app/state.json
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

## Builder Program integration

PolyTool integrates with the [Polymarket Builders Program](https://builders.polymarket.com) for trade attribution.

### Setup

1. Register in the [Polymarket Builders Program](https://builders.polymarket.com).
2. Obtain API credentials (API key, secret, passphrase).
3. Add them to the bot `.env` file:

```env
POLY_BUILDER_API_KEY=your_builder_api_key
POLY_BUILDER_SECRET=your_builder_secret
POLY_BUILDER_PASSPHRASE=your_builder_passphrase
```

### How it works

The bot automatically adds builder attribution headers to each order via HMAC signatures:

```python
# engine/signer.py
def get_builder_headers(api_key, secret, passphrase, method, path, body):
    timestamp = str(int(time.time() * 1000))
    signature = build_hmac_signature(secret, timestamp, method, path, body)
    return {
        "POLY_BUILDER_API_KEY": api_key,
        "POLY_BUILDER_TIMESTAMP": timestamp,
        "POLY_BUILDER_PASSPHRASE": passphrase,
        "POLY_BUILDER_SIGNATURE": signature,
    }
```

All trades executed via the bot will be attributed to your builder account.

---

## License

[MIT](LICENSE) © 2024 PolyTool

---

<div align="center">
  <a href="https://polytool.world"><strong>polytool.world</strong></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/polytool">GitHub</a>
  &nbsp;·&nbsp;
  <a href="https://builders.polymarket.com">Polymarket Builders Program</a>
  <br /><br />
  Made with ❤️ for the Polymarket community
</div>

