
GitHub repo for HNG Stage 2 backend track

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.2-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)
![Railway](https://img.shields.io/badge/Deployed-Railway-blueviolet.svg)

## Country Currency & Exchange API

A production-grade RESTful API built with **FastAPI** that:

- Fetches country data from `https://restcountries.com`
- Fetches exchange rates from `https://open.er-api.com`
- Computes `estimated_gdp = population × random(1000–2000) ÷ exchange_rate`
- Caches everything in **MySQL**
- Supports **CRUD**, **filters**, **sorting**, **image generation**, and **robust error handling**

Fully persistent — data survives restarts (SQLite locally, MySQL in prod)
Case-insensitive name matching
Exact 400/404/503 JSON formats

---

## Features

| Feature | Endpoint | Description |
|---------|----------|-------------|
| **Refresh Cache** | `POST /countries/refresh` | Fetch + store all countries + rates |
| **List Countries** | `GET /countries` | Filter by `region`, `currency`, sort by `gdp_desc` |
| **Get One Country** | `GET /countries/{name}` | Case-insensitive |
| **Delete Country** | `DELETE /countries/{name}` | Case-insensitive |
| **Status** | `GET /status` | Total + last refresh timestamp |
| **Summary Image** | `GET /countries/image` | PNG with top 5 GDP + total |
| **Interactive Docs** | `/docs`, `/redoc` | Swagger + ReDoc |
| **CORS** | `*` | Enabled for cross-origin access |
| **Error Handling** | 400, 404, 503 | Exact JSON format |

---

## Project Structure

```
country-exchange-api/
├── main.py              # FastAPI app, routes, background tasks
├── database.py          # Async SQLAlchemy + MySQL setup
├── models/
│   └── country.py       # SQLAlchemy Country model
├── schemas/
│   └── country.py       # Pydantic models (input/output)
├── crud/
│   └── country.py       # Upsert logic + GDP calculation
├── services/
│   ├── fetch.py         # External API calls
│   └── image.py         # Matplotlib + PIL image generation
├── utils/
│   └── errors.py        # 404 JSON helper
├── cache/
│   └── summary.png      # Generated image
├── .env                 # DB + API config
├── requirements.txt     # Dependencies
└── README.md            # This file
```

---

## Prerequisites

- Python 3.12
- SQLite (bundled with Python) for local quick start
- MySQL 8.0+ for production (optional)
- Git
- Virtual Environment (`venv`)
- Railway/Aiven/RDS account (optional for hosted MySQL)

---

## Quick Start (SQLite - no DB setup)

This project now supports SQLite out of the box for the easiest local run.

1) Create and activate a virtual environment
```powershell
python -m venv venv
./venv/Scripts/activate
```

2) Install dependencies
```powershell
pip install -r country-exchange-api/requirements.txt
```

3) Create `.env` (inside `country-exchange-api/`)
```env
DATABASE_URL=sqlite+aiosqlite:///./countries.db
ALLOWED_ORIGINS=*
COUNTRIES_API=https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies
EXCHANGE_API=https://open.er-api.com/v6/latest/USD
```

4) Run the API
```powershell
cd country-exchange-api
python -m uvicorn main:app --reload --port 8000 --env-file .env
```

5) Populate cache (in a new terminal while server runs)
```powershell
Invoke-RestMethod -Method Post http://127.0.0.1:8000/countries/refresh
```

6) Test endpoints
```powershell
Invoke-RestMethod http://127.0.0.1:8000/countries
Invoke-RestMethod http://127.0.0.1:8000/status
Invoke-RestMethod http://127.0.0.1:8000/countries/image -OutFile summary.png
```

---

## Setup Instructions (MySQL option)

### 1. Fork and Clone the Repository

```bash
git clone https://github.com/your-username/country-exchange-api.git
cd country-exchange-api
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

* **Windows**: `venv\Scripts\activate`  
* **Mac/Linux**: `source venv/bin/activate`

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` File (MySQL)

Use a single `DATABASE_URL` variable. Examples:

Local MySQL (installed on Windows):
```env
DATABASE_URL=mysql+aiomysql://root:your_password@127.0.0.1:3306/countries_db
ALLOWED_ORIGINS=*
COUNTRIES_API=https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies
EXCHANGE_API=https://open.er-api.com/v6/latest/USD
```

Railway/Aiven/RDS (managed):
```env
DATABASE_URL=mysql+aiomysql://USER:PASSWORD@HOST:PORT/DBNAME
ALLOWED_ORIGINS=*
COUNTRIES_API=https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies
EXCHANGE_API=https://open.er-api.com/v6/latest/USD
```

### 5. Start MySQL (optional)

If you use local MySQL, ensure the server is running and the `countries_db` database exists. On managed services, copy the connection details from the dashboard.

---

## Running Locally

```powershell
python -m uvicorn main:app --reload --port 8000 --env-file .env
```

* **URL**: http://127.0.0.1:8000
* **Swagger UI**: http://127.0.0.1:8000/docs
* **ReDoc**: http://127.0.0.1:8000/redoc

> **First run**: Call `POST /countries/refresh` to populate the database

---

## API Usage

### 1. Refresh Data

```bash
curl -X POST http://127.0.0.1:8000/countries/refresh
```

### 2. Get All Countries

```bash
curl http://127.0.0.1:8000/countries
```

### 3. Filter + Sort

```bash
curl "http://127.0.0.1:8000/countries?region=Africa&sort=gdp_desc"
```

### 4. Get One Country

```bash
curl http://127.0.0.1:8000/countries/nigeria
```

### 5. Delete Country

```bash
curl -X DELETE http://127.0.0.1:8000/countries/Nigeria
```

### 6. Status

```bash
curl http://127.0.0.1:8000/status
```

### 7. Download Image

```bash
curl http://127.0.0.1:8000/countries/image --output summary.png
```

---

## Deployment on Railway

### Prerequisites

* Push to GitHub
* Railway account

### Steps

#### 1. Push to GitHub

```bash
git add .
git commit -m "Deploy to Railway"
git push origin main
```

#### 2. Deploy on Railway

* Go to [railway.app](https://railway.app)
* New Project → Deploy from GitHub
* Select your repo

#### 3. Add MySQL Plugin

* Click `+ New` → Database → MySQL
* Railway auto-generates credentials

#### 4. Set Environment Variables

Set a single `DATABASE_URL` using variables provided by Railway’s MySQL plugin:

```env
DATABASE_URL=mysql+aiomysql://${{MySQL.MYSQLUSER}}:${{MySQL.MYSQLPASSWORD}}@${{MySQL.MYSQLHOST}}:${{MySQL.MYSQLPORT}}/${{MySQL.MYSQLDATABASE}}
ALLOWED_ORIGINS=*
COUNTRIES_API=https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies
EXCHANGE_API=https://open.er-api.com/v6/latest/USD
```

#### 5. Start Command

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

#### 6. Deploy

Your API will be live at: `https://your-app.up.railway.app`

---

## Deployment on PXXL App

### Prerequisites

* Push code to GitHub
* A PXXL account and an app created

### Steps

1) Connect repository

* In PXXL, create a new app and connect your GitHub repo

2) Set environment variables

Set a single `DATABASE_URL` (recommended: managed MySQL). Example:

```env
DATABASE_URL=mysql+aiomysql://USER:PASSWORD@HOST:PORT/DBNAME
ALLOWED_ORIGINS=*
COUNTRIES_API=https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies
EXCHANGE_API=https://open.er-api.com/v6/latest/USD
```

If you insist on SQLite for a demo, it will work but may be ephemeral depending on PXXL’s filesystem policy:

```env
DATABASE_URL=sqlite+aiosqlite:///./countries.db
```

3) Start command

Configure the start command (in PXXL dashboard) to:

```bash
python -m uvicorn main:app --host 0.0.0.0 --port $PORT
```

4) Build/runtime settings

* Runtime: Python 3.12
* Workdir: `country-exchange-api`

5) Deploy

* Trigger a deployment. After it’s live, visit:
  - `https://your-pxxl-app.domain/countries/refresh` (POST) to populate
  - `https://your-pxxl-app.domain/docs` for Swagger

> Note: For production, prefer a managed MySQL over SQLite so data persists across restarts.

---

## Production Considerations

* **MySQL** → Persistent storage
* **Async SQLAlchemy** → High performance
* **Background Tasks** → Non-blocking image generation
* **Case-Insensitive Matching** → Robust name lookup
* **Exact JSON Errors** → Consistent responses
* **Image Generation** → Matplotlib + PIL
* **No `--reload` in production**

---

## Troubleshooting

| Issue | Fix |
|------|-----|
| 404 on `/` | Root path not defined; use `/docs` or API routes |
| 503 on refresh | Check external APIs or network |
| `.env` parse warning | Recreate `.env` with exactly 4 lines as shown |
| `uvicorn` not found | Use `python -m uvicorn ...` inside the venv |
| DB connection error | Verify `DATABASE_URL` and DB availability |
| Windows PowerShell curl | Prefer `Invoke-RestMethod` for JSON |
| Matplotlib GUI warning | Harmless; generation runs headless and saves PNG |

---

## Contributing

1. Fork the repo
2. Create branch: `git checkout -b feature/xyz`
3. Commit: `git commit -m "Add feature"`
4. Push & open PR
```
```