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

## Что такое PolyTool?

**PolyTool** — это open-source платформа для копи-трейдинга на Polymarket, которая позволяет автоматически копировать сделки успешных трейдеров. Платформа состоит из веб-дашборда (Next.js) и standalone бота (Python), который работает на вашем сервере или локальной машине.

### Основные возможности:
- 🔄 **Автоматический копи-трейдинг** — следите за кошельками и автоматически копируйте их сделки
- 📊 **Аналитика** — отслеживайте производительность и статистику торговли
- 💼 **Управление портфелем** — мониторинг позиций и балансов
- 🔑 **API Keys** — безопасное управление ключами и настройками

> **🔒 Безопасность:** Ваш приватный ключ никогда не покидает вашу машину. Он используется только локально для подписи ордеров через `py-clob-client`.

---

## Фичи

| **Copy Trading** | **Analytics** |
|------------------|---------------|
| Автоматическое копирование сделок отслеживаемых кошельков | Детальная статистика по всем сделкам и производительности |
| Настраиваемые фильтры (минимальный размер, диапазон цен) | Графики P&L, win rate, ROI |
| Режимы: Auto (автоисполнение) и Manual (только уведомления) | История всех скопированных и обнаруженных сделок |
| Гибкое управление размером позиций (фиксированная сумма, пропорциональная, процентная) | Экспорт данных в CSV/JSON |

| **Portfolio** | **API Keys** |
|---------------|--------------|
| Мониторинг всех открытых позиций в реальном времени | Безопасное хранение API ключей с шифрованием |
| Отслеживание балансов и доступных средств | Управление несколькими ключами для разных стратегий |
| История изменений портфеля | Автоматическая ротация ключей |
| Интеграция с Polymarket CLOB API | Аудит лог всех операций с ключами |

---

## Архитектура проекта

```
polytool/
├── frontend/                    # Next.js веб-приложение
│   ├── app/                     # App Router (Next.js 13+)
│   │   ├── copytrade/          # Страница копи-трейдинга
│   │   ├── analytics/           # Страница аналитики
│   │   ├── portfolio/          # Страница портфеля
│   │   └── settings/           # Настройки и API Keys
│   ├── components/             # React компоненты
│   │   ├── WalletTracker.tsx   # Компонент отслеживания кошельков
│   │   ├── TradeList.tsx       # Список сделок
│   │   └── PortfolioChart.tsx  # Графики портфеля
│   ├── lib/                    # Утилиты и API клиенты
│   │   ├── api.ts              # API клиент для backend
│   │   └── polymarket.ts       # Интеграция с Polymarket API
│   └── package.json            # Зависимости Next.js, TypeScript, Tailwind
│
├── backend/                     # FastAPI backend (отдельный репозиторий)
│   ├── app/
│   │   ├── api/                # API endpoints
│   │   │   ├── bot/           # Bot API (config, trade, heartbeat)
│   │   │   ├── wallets/       # Управление кошельками
│   │   │   └── analytics/     # Аналитика endpoints
│   │   ├── models/            # SQLAlchemy модели
│   │   └── services/          # Бизнес-логика
│   └── requirements.txt       # Python зависимости
│
└── polytool-bot/               # Standalone copy-trading bot (этот репозиторий)
    ├── src/polytool_bot/
    │   ├── cli.py              # Click CLI: run / status / configure
    │   ├── config.py           # Pydantic settings (читает .env)
    │   ├── state.py            # Локальный JSON state — дедупликация сделок
    │   ├── worker.py           # Главный polling loop
    │   ├── api/
    │   │   ├── polytool.py     # PolyTool backend клиент (X-API-Key auth)
    │   │   └── polymarket.py   # Polymarket Data / CLOB / Gamma APIs
    │   └── engine/
    │       ├── copytrade.py    # Детекция сделок, фильтрация, расчет размера
    │       ├── executor.py     # Размещение ордеров на CLOB через py-clob-client
    │       └── signer.py       # HMAC подпись для builder attribution
    ├── docker-compose.yml      # Docker Compose конфигурация
    ├── Dockerfile              # Docker образ для бота
    ├── pyproject.toml           # Python package конфигурация
    └── .env.example            # Пример переменных окружения
```

---

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                    ПОДКЛЮЧЕНИЕ КОШЕЛЬКА                         │
│  Пользователь → polytool.world → Подключение MetaMask/Wallet   │
│  → Автоматическое получение CLOB API credentials                │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    НАСТРОЙКА КОПИ-ТРЕЙДИНГА                      │
│  Dashboard → Добавление кошельков для отслеживания              │
│  → Настройка фильтров (min size, price range, copy sells)       │
│  → Выбор режима: Auto (автоисполнение) или Manual (уведомления) │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ЗАПУСК БОТА                                   │
│  polytool-bot run → Загрузка конфигурации из .env               │
│  → Подключение к PolyTool API (X-API-Key)                        │
│  → Получение списка отслеживаемых кошельков                     │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│              ОСНОВНОЙ ЦИКЛ (каждые 15 секунд)                   │
│                                                                  │
│  1. GET /api/bot/config                                          │
│     └─> Получение списка отслеживаемых кошельков и настроек    │
│         │                                                        │
│         ▼                                                        │
│  2. Fetch latest trades from Polymarket Data API                │
│     └─> GET /trades?user={wallet_address}&limit=50              │
│         │                                                        │
│         ▼                                                        │
│  3. Фильтрация сделок                                           │
│     ├─> Уже видели? → Пропустить                                │
│     ├─> Минимальный размер? → Пропустить                        │
│     ├─> Диапазон цен? → Пропустить                              │
│     └─> Copy sells disabled? → Пропустить                       │
│         │                                                        │
│         ├─> НЕ копировать → POST /api/bot/trade (action: DETECTED)
│         │                                                       │
│         └─> КОПИРОВАТЬ →                                        │
│             │                                                   │
│             ▼                                                   │
│  4. Расчет размера позиции                                      │
│     ├─> fixed: фиксированная сумма                              │
│     ├─> proportional: оригинальный размер × multiplier         │
│     └─> percentage: процент от оригинального размера            │
│             │                                                   │
│             ▼                                                   │
│  5. Получение orderbook для токена                              │
│     └─> GET /book?token_id={token_id}                          │
│             │                                                   │
│             ▼                                                   │
│  6. Подпись и размещение limit order на CLOB                    │
│     └─> py-clob-client.create_order() → POST /orders            │
│             │                                                   │
│             ▼                                                   │
│  7. POST /api/bot/trade (логирование в dashboard)               │
│     └─> Сохранение результата в базу данных                     │
│             │                                                   │
│             ▼                                                   │
│  8. Сохранение trade_id в state.json (дедупликация)            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ОТОБРАЖЕНИЕ В DASHBOARD                       │
│  Frontend → Polling /api/analytics → Отображение статистики    │
│  → Графики P&L, список сделок, статус портфеля                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Компонент | Технология | Версия | Назначение |
|-----------|------------|--------|------------|
| **Frontend** | Next.js | 13+ | React фреймворк с App Router |
| | TypeScript | 5.0+ | Типизация и безопасность кода |
| | Tailwind CSS | 3.0+ | Utility-first CSS фреймворк |
| | React Query | 4+ | Управление состоянием и кеширование |
| **Backend** | FastAPI | 0.100+ | Асинхронный Python веб-фреймворк |
| | Python | 3.10+ | Основной язык бэкенда |
| | SQLAlchemy | 2.0+ | ORM для работы с БД |
| | Pydantic | 2.0+ | Валидация данных и settings |
| **Bot** | Python | 3.10+ | Standalone copy-trading бот |
| | Click | 8.1+ | CLI интерфейс |
| | httpx | 0.27+ | Асинхронный HTTP клиент |
| | py-clob-client | 0.19+ | Клиент для Polymarket CLOB API |
| **Infrastructure** | Docker | Latest | Контейнеризация |
| | Docker Compose | Latest | Оркестрация контейнеров |
| **Blockchain** | Polygon | 137 | Сеть для Polymarket |
| | Web3 | - | Интеграция с блокчейном |

---

## Quick Start

### Backend (FastAPI)

```bash
# Клонировать репозиторий backend
git clone https://github.com/polytool/backend.git
cd backend

# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Установить зависимости
pip install -r requirements.txt

# Настроить переменные окружения
cp .env.example .env
# Отредактировать .env с вашими настройками БД и API ключами

# Запустить миграции
alembic upgrade head

# Запустить сервер
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (Next.js)

```bash
# Клонировать репозиторий frontend
git clone https://github.com/polytool/frontend.git
cd frontend

# Установить зависимости
npm install
# или
yarn install

# Настроить переменные окружения
cp .env.example .env.local
# Отредактировать .env.local с URL backend API

# Запустить dev сервер
npm run dev
# или
yarn dev

# Открыть http://localhost:3000
```

### Bot (Docker)

```bash
# Клонировать репозиторий бота
git clone https://github.com/polytool/polytool-bot.git
cd polytool-bot

# Создать .env файл
cp .env.example .env
# Отредактировать .env с вашими credentials

# Запустить через Docker Compose
docker compose up -d

# Просмотр логов
docker compose logs -f
```

### Bot (Local)

```bash
# Клонировать репозиторий
git clone https://github.com/polytool/polytool-bot.git
cd polytool-bot

# Установить пакет
pip install -e .

# Настроить .env
cp .env.example .env
# Отредактировать .env

# Запустить бота
polytool-bot run

# Проверить статус
polytool-bot status
```

---

## API Reference

### Bot API Endpoints

#### `GET /api/bot/config`
Получить конфигурацию отслеживаемых кошельков и настроек копи-трейдинга.

**Headers:**
```
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
Сообщить о выполненной или обнаруженной сделке.

**Headers:**
```
X-API-Key: plk_your_api_key_here
Content-Type: application/json
```

**Request Body:**
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
Отправить heartbeat для показа, что бот активен.

**Headers:**
```
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

### Polymarket API Integration

Бот использует следующие Polymarket API:

- **Data API** (`https://data-api.polymarket.com`): Получение сделок и позиций
- **CLOB API** (`https://clob.polymarket.com`): Размещение ордеров
- **Gamma API** (`https://gamma-api.polymarket.com`): Информация о рынках

---

## Переменные окружения

### Backend (.env)

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

### Frontend (.env.local)

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
# или для production
NEXT_PUBLIC_API_URL=https://api.polytool.world

# Polymarket
NEXT_PUBLIC_POLYMARKET_URL=https://polymarket.com
```

### Bot (.env)

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

## Деплой

### Backend (VPS / Cloud)

```bash
# На сервере
git clone https://github.com/polytool/backend.git
cd backend

# Установить зависимости
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Настроить .env
nano .env

# Запустить через systemd
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
# Установить Vercel CLI
npm i -g vercel

# Деплой
cd frontend
vercel

# Или через GitHub Actions (автоматический деплой при push)
```

**vercel.json:**
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

### Bot (Docker на VPS)

```bash
# На сервере
git clone https://github.com/polytool/polytool-bot.git
cd polytool-bot

# Создать .env
nano .env

# Запустить через Docker Compose
docker compose up -d

# Автозапуск при перезагрузке
sudo systemctl enable docker
```

**docker-compose.yml:**
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

## Builder Program Integration

PolyTool интегрирован с [Polymarket Builders Program](https://builders.polymarket.com) для атрибуции сделок.

### Настройка

1. Зарегистрируйтесь в [Polymarket Builders Program](https://builders.polymarket.com)
2. Получите API credentials (API Key, Secret, Passphrase)
3. Добавьте их в `.env` файл бота:

```env
POLY_BUILDER_API_KEY=your_builder_api_key
POLY_BUILDER_SECRET=your_builder_secret
POLY_BUILDER_PASSPHRASE=your_builder_passphrase
```

### Как это работает

Бот автоматически добавляет builder attribution headers к каждому ордеру через HMAC подпись:

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

Все сделки, выполненные через бота, будут атрибутированы вашей builder программе.

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
"# PolyTool" 
"# PolyTool" 
