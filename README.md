# Vikas Gupta — Software Developer Portfolio & FastAPI Backend

A modern, high-performance personal portfolio website for **Vikas Gupta**, positioning his career as a **Backend / Full-Stack Developer transitioning from PHP/Laravel toward Python backend engineering**.

Designed with clean typography, dark theme aesthetics, responsive grid architecture, and a production-ready **Python FastAPI** REST backend.

---

## 🏗️ Technology Stack

### Frontend
- **HTML5 & Semantic Markup**: SEO-optimized with OpenGraph tags, JSON schemas, and structured metadata.
- **CSS3 & Custom Design System**: Responsive dark mode styling, custom scrollbars, glassmorphism (`backdrop-filter`), micro-interactions, and neon accent glows.
- **Bootstrap 5 & Bootstrap Icons**: Grid framework and modern developer icons.
- **JavaScript (ES6+)**: Dynamic project rendering, category filter tabs, modal dialogs, and asynchronous `fetch()` communication with the FastAPI backend.

### Backend
- **Python 3.10+ / 3.13**: Asynchronous backend service.
- **FastAPI**: Modern, fast web framework for building RESTful APIs.
- **Pydantic v2**: Strong type validation, input sanitization, and response serialization.
- **SQLAlchemy 2.0**: Relational ORM supporting both **MySQL** (via `pymysql`) and local **SQLite** resilience fallback.
- **Uvicorn**: High-throughput ASGI server.

### Database
- **MySQL**: Relational database for production deployment (schema provided in `backend/schema.sql`).
- **SQLite (Local Fallback)**: Built-in zero-configuration local fallback if MySQL is offline during local development.

---

## 📁 Project Directory Structure

```text
portfolio/
├── backend/
│   ├── app/
│   │   ├── __init__.py           # Package initializer
│   │   ├── config.py             # Environment configuration & DB URL resolver
│   │   ├── database.py           # SQLAlchemy engine & session factory with MySQL/SQLite fallback
│   │   ├── main.py               # FastAPI application, CORS middleware & static file mounting
│   │   ├── models/               # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   ├── contact.py        # Contacts table definition
│   │   │   └── project.py        # Projects table definition
│   │   ├── schemas/              # Pydantic v2 validation models
│   │   │   ├── __init__.py
│   │   │   ├── contact.py        # Contact form validation & sanitization
│   │   │   └── project.py        # Project responses
│   │   ├── routers/              # API Route controllers
│   │   │   ├── __init__.py
│   │   │   ├── contact.py        # POST /api/contact
│   │   │   ├── projects.py       # GET /api/projects
│   │   │   └── health.py         # GET /api/health
│   │   └── services/             # Business logic layer
│   │       ├── __init__.py
│   │       ├── contact_service.py # Message persistence logic
│   │       └── project_service.py # Project retrieval & initial seed logic
│   ├── .env                      # Active environment settings
│   ├── .env.example              # Template environment configuration
│   ├── requirements.txt          # Python dependencies
│   └── schema.sql                # Complete MySQL DDL & seed records
├── frontend/
│   ├── index.html                # Main semantic single-page portfolio
│   ├── css/
│   │   └── style.css             # Tailored styling, animations, and responsiveness
│   ├── js/
│   │   └── main.js               # Client controller & API integration
│   ├── images/                   # High-resolution project mockup assets
│   │   ├── project-product-mgmt.jpg
│   │   ├── project-hrms.jpg
│   │   ├── project-student-mgmt.jpg
│   │   └── project-fastapi-api.jpg
│   └── assets/                   # Additional downloadable documents
├── run_backend.py                # Convenience launcher for FastAPI backend
└── README.md                     # Documentation and setup guide
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Python 3.10+** (Tested on Python 3.13)
- **Git**
- *(Optional for MySQL)* **XAMPP / MySQL Server** running on port 3306.

---

### 2. Install Backend Dependencies

Navigate to the project root:
```bash
cd C:\Users\vikas\.gemini\antigravity-ide\scratch\portfolio
```

Install the required Python packages:
```bash
python -m pip install -r backend/requirements.txt
```

---

### 3. Database Configuration

#### Option A: MySQL (Recommended for Production / XAMPP)
1. Start Apache & MySQL in **XAMPP Control Panel** (or start your MySQL service).
2. Open **phpMyAdmin** (`http://localhost/phpmyadmin`) or MySQL CLI.
3. Import or execute the queries in `backend/schema.sql`. It will create the `vikas_portfolio_db` database, tables, and seed projects.
4. Verify your credentials in `backend/.env`:
   ```env
   DB_USER=root
   DB_PASSWORD=
   DB_HOST=127.0.0.1
   DB_PORT=3306
   DB_NAME=vikas_portfolio_db
   ```

#### Option B: Automatic SQLite Fallback (Zero Config)
If MySQL is not currently running, the application **automatically detects it and uses a local SQLite database** (`portfolio_local.db`). It automatically creates all tables and seeds the project catalog so you can test all features without any setup.

---

### 4. Running the Application

Launch the FastAPI application:
```bash
python run_backend.py
```

Or run via Uvicorn:
```bash
python -m uvicorn app.main:app --app-dir backend --reload --port 8000
```

Once running:
- **Portfolio Website**: Open your browser at [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative ReDoc API Docs**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **Health Check Endpoint**: [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)

---

## 📡 REST API Specifications

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Returns service health, uptime, and active database driver |
| `GET` | `/api/projects` | Returns list of featured portfolio projects |
| `POST` | `/api/contact` | Validates & saves incoming contact inquiries into the database |
| `GET` | `/docs` | Interactive Swagger UI API playground |
| `GET` | `/redoc` | OpenAPI specifications document |

### Sample Contact Request Body (`POST /api/contact`):
```json
{
  "name": "Jane Recruiter",
  "email": "jane@techcorp.com",
  "subject": "Interview Opportunity for Backend Developer Role",
  "message": "Hi Vikas, we were impressed by your background in PHP/Laravel and your transition into Python/FastAPI."
}
```

### Sample Successful Response (`201 Created`):
```json
{
  "success": true,
  "message": "Thank you! Your message has been sent successfully. Vikas will get back to you soon.",
  "contact_id": 1,
  "created_at": "2026-10-02T19:25:00.000000"
}
```

---

## 🎨 Design & Accessibility Features
- **Mobile-First & Responsive**: Fluid layout across phones (375px+), tablets (768px+), and high-res desktops.
- **Micro-Interactions**: Hover elevation, subtle neon glow on code cards, and responsive navigation links.
- **Recruiter-Focused**: Clear, honest positioning detailing real professional experience at **Parasight Solutions** alongside active problem-solving practice in **DSA & Python**.
- **No Inaccurate Claims**: No subjective percentage bars; all skills and DSA topics are honestly categorized as production experience or active daily practice.

---

## 📄 License & Attribution
Crafted with pride for **Vikas Gupta**.
