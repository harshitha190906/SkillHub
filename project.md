# 🏆 SkillHub — Technical Architecture & Project Specification

## 1. Executive Summary & Project Overview

**SkillHub** is a modern, full-stack web application developed using **Python (Flask)** and **MySQL**. It provides a centralized platform for students, developers, and professionals to track technical competencies, organize skill sets by proficiency level, upload proof certificates, monitor skill analytics, and manage personal profile portfolios.

The platform emphasizes clean separation of concerns, robust security mechanisms (PBKDF2 password hashing, secure file sanitization, parameterized SQL queries), responsive visualization via Chart.js, and multi-environment deployment compatibility (local development and cloud platforms like Railway).

---

## 2. Problem Statement & Solution

### Problem Statement
Students and professionals frequently acquire technical skills and certifications across multiple platforms (Coursera, Udemy, college courses, hackathons), leading to fragmented records, lack of visual skill distribution tracking, and difficulty in presenting proof of certification during resume building or job applications.

### The SkillHub Solution
- **Centralized Dashboard**: Consolidates skill counts, certificate metrics, and skill-level breakdown analytics into a single visual view.
- **Skill Proficiency Tracking**: Categorizes skills by difficulty levels (*Beginner*, *Intermediate*, *Advanced*) and provides live DOM-based search filtering.
- **Certificate Management**: Securely handles PDF and image uploads with UUID prefixing to prevent name collisions.
- **User Portfolio & Profile**: Manages user profiles, custom bios, avatar pictures, and user settings (dark mode persistence, password updates, account teardown).

---

## 3. System Architecture Specification

SkillHub is structured according to the **Model-View-Controller (MVC)** design pattern, implemented using Flask Blueprints and Jinja2 server-side rendering (SSR).

```text
+-----------------------------------------------------------------------------------+
|                                 CLIENT LAYER                                      |
|                                                                                   |
|   Web Browser (Desktop / Mobile Client)                                           |
|   ├── Layout Engine: Bootstrap 5 (Responsive CSS Grid & Controls)                 |
|   ├── Client Interactivity: Vanilla JS (static/js/script.js)                      |
|   │   ├── Live Table Search Filter                                                |
|   │   ├── Dark Mode Theme Switcher (localStorage persistence)                     |
|   │   └── Auto-hiding Alert Notifications                                         |
|   └── Analytics Engine: Chart.js (HTML5 Canvas Visualizations)                    |
+----------------------------------------+------------------------------------------+
                                         |
                                   HTTP / HTTPS
                                         |
+----------------------------------------v------------------------------------------+
|                             WSGI & WEB SERVER LAYER                               |
|                                                                                   |
|   Gunicorn WSGI Server (v23.0.0)                                                  |
|   ├── Process Model: Multi-worker pre-fork (2 Workers)                            |
|   └── Host/Port Binding: 0.0.0.0:8080 (Configured via nixpacks.toml)              |
+----------------------------------------+------------------------------------------+
                                         |
                                   Python WSGI API
                                         |
+----------------------------------------v------------------------------------------+
|                             APPLICATION LAYER (FLASK)                             |
|                                                                                   |
|   Core Controller Entrypoint: app.py                                              |
|   ├── Database Connection & Auto-table Verifier (init_tables)                     |
|   ├── Environment Config Manager (config.py)                                      |
|   │                                                                               |
|   ├── Modular Flask Blueprints:                                                   |
|   │   ├── auth Blueprint (routes/auth.py)        -> Auth & Session Management     |
|   │   ├── skills Blueprint (routes/skills.py)    -> Skill CRUD Operations         |
|   │   └── certificate Blueprint (routes/cert.py) -> Document Upload Management   |
|   │                                                                               |
|   └── View Compiler: Jinja2 Templating Engine (HTML5 Views)                       |
+-------------------+-----------------------------------+---------------------------+
                    |                                   |
           Parameterized SQL Queries                  File I/O
                    |                                   |
+-------------------v-------------------+   +-----------v---------------------------+
|         DATABASE LAYER (MYSQL)        |   |       LOCAL FILE STORAGE              |
|                                       |   |                                       |
|   MySQL RDBMS (v8.0+) / MariaDB       |   |   Static Asset Directories            |
|   ├── Connection Driver: Flask-MySQLdb|   |   ├── static/uploads/profiles/        |
|   │   (PyMySQL compatibility wrapper) |   |   │   (Profile Avatars)               |
|   └── Schema Tables:                  |   |   └── static/uploads/                 |
|       ├── users (Auth & Profile Data) |   |       (UUID Certificate Files)        |
|       ├── skills (FK: users.id)       |   +---------------------------------------+
|       └── certificates (FK: users.id) |
+---------------------------------------+
```

---

## 4. Technology Stack & Technical Rationale

### Backend Runtime & Framework
- **Python (v3.10+)**: Core runtime offering clean syntax, rapid development speed, and broad WSGI ecosystem integration.
- **Flask (v3.1.0)**: Lightweight WSGI micro-framework selected for low overhead, flexible routing, modular **Blueprints**, and Jinja2 templating support.
- **Gunicorn (v23.0.0)**: Production-grade Web Server Gateway Interface (WSGI) server running a multi-worker pre-fork architecture to handle concurrent client requests efficiently.

### Database & Connectors
- **MySQL (v8.0+)**: Relational Database Management System (RDBMS) offering ACID compliance, foreign key enforcement, and automatic cascade deletion.
- **Flask-MySQLdb (v2.0.0) & PyMySQL (v1.1.1)**: Database connector interface for executing parameterized SQL queries, with `pymysql.install_as_MySQLdb()` providing cross-platform execution fallback.

### Security Primitives
- **Werkzeug (v3.1.3)**: Provides security utilities including `generate_password_hash` (PBKDF2 hashing algorithm), `check_password_hash`, and `secure_filename` path injection prevention.

### Frontend & UI Technologies
- **HTML5 & Jinja2 (v3.1.6)**: Server-Side Rendering (SSR) template hierarchy utilizing base template inheritance (`{% extends "layout.html" %}`).
- **Bootstrap 5**: Mobile-responsive CSS framework for grid layouts, cards, buttons, badges, and modals.
- **Vanilla JavaScript (`static/js/script.js`)**: Client-side scripting for DOM live search filtering, dark mode toggle state, and auto-fading alerts.
- **Chart.js**: HTML5 Canvas graphing library used to display skill level distributions on the dashboard.

---

## 5. Database Schema & Data Models

### Entity Relationship Diagram (Textual Representation)

```text
+-----------------------+           +-----------------------+
|         users         | 1       * |        skills         |
+-----------------------+-----------+-----------------------+
| PK  id (INT AUTO_INC) |           | PK  id (INT AUTO_INC) |
|     fullname (VARCHAR)|           | FK  user_id (INT)     |
| UK  email (VARCHAR)   |           |     skill_name(VARCHAR|
|     password (VARCHAR)|           |     skill_level(VRCHR)|
|     bio (TEXT)        |           |     description (TEXT)|
|     profile_img(VRCHR)|           +-----------------------+
+-----------+-----------+
            | 1
            |
            | *
+-----------v-----------+
|     certificates      |
+-----------------------+
| PK  id (INT AUTO_INC) |
| FK  user_id (INT)     |
|     title (VARCHAR)   |
|     file_name(VARCHAR)|
+-----------------------+
```

### DDL Schema Definitions

```sql
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fullname VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    bio TEXT,
    profile_image VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    skill_name VARCHAR(255) NOT NULL,
    skill_level VARCHAR(50) NOT NULL,
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS certificates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

---

## 6. Key Application Workflows

### A. Authentication & Session Management
1. User submits registration details -> Email converted to lowercase -> Username/Email uniqueness checked against MySQL -> Password hashed via Werkzeug PBKDF2 -> Record created in `users` table.
2. User logs in -> Password hash verified -> `session["user_id"]`, `session["fullname"]`, and `session["email"]` stored in server-side encrypted cookies.
3. Protected routes verify `session["user_id"]` presence; unauthorized requests redirect to `/login`.

### B. Skill CRUD & Analytics Flow
1. User creates or updates a skill record -> Data validated -> Persisted to `skills` table under logged-in `user_id`.
2. Dashboard route `/dashboard` executes SQL aggregate queries (`COUNT(*)`, `GROUP BY skill_level`) -> Aggregated arrays (`labels`, `values`) passed to Jinja2 template -> Rendered dynamically by Chart.js.

### C. Certificate File Processing
1. User uploads a file (PDF, PNG, JPG, JPEG) -> File extension checked against whitelist -> Sanitized via `secure_filename()` -> Prepended with `uuid.uuid4()` -> Saved to `static/uploads/` -> File path saved in `certificates` table.

---

## 7. Security Architecture

1. **Password Protection**: Passwords are never stored in plain text; Werkzeug PBKDF2 hashing protects against hash collision and dictionary attacks.
2. **SQL Injection Prevention**: All queries across `models/` use parameterized tuples (`cursor.execute(sql, (params,))`).
3. **Upload File Validation**: Extensions restricted to `{"pdf", "png", "jpg", "jpeg"}`. UUID prefixing prevents path collision and overwriting.
4. **Referential Integrity**: Cascading deletes (`ON DELETE CASCADE`) guarantee orphan records are purged if a user account is deleted.

---

## 8. Directory & File Structure

```text
SkillHub/
│
├── app.py                  # Core application initialization, error handlers & primary routes
├── config.py               # Environment & configuration management
├── init_db.py              # Standalone DB table creation script
├── test_db.py              # Connectivity verification script
├── schema.sql              # Database DDL schema specification
├── requirements.txt        # Python dependency manifest
├── nixpacks.toml           # Deployment build & process configuration
├── Procfile                # WSGI process command entrypoint
├── README.md               # User guide & project manual
├── project.md              # Technical architecture specification
│
├── models/                 # Data access objects (DAO)
│   ├── database.py         # DB execution helper routines
│   ├── user.py             # User queries & password verification
│   ├── skill.py            # Skill CRUD query operations
│   └── certificate.py      # Certificate database queries
│
├── routes/                 # Modular Flask Blueprints
│   ├── auth.py             # User registration, login & logout routes
│   ├── skills.py           # Skill management routes
│   └── certificate.py      # Document upload & deletion routes
│
├── static/                 # Static web assets
│   ├── css/                # Stylesheets
│   ├── js/script.js        # Client-side DOM filtering & theme toggling
│   └── uploads/            # Uploaded avatars and certificates
│
├── templates/              # Jinja2 HTML View templates
│   ├── layout.html         # Base template layout with navigation
│   ├── dashboard.html      # Analytics dashboard with Chart.js
│   ├── skills.html         # Skill list with live DOM search
│   ├── certificates.html   # Certificate gallery
│   └── profile.html        # User profile view
│
└── utils/                  # Helper utilities
    └── helpers.py          # Badge styling and file upload helpers
```

---

## 9. Deployment & Environment Setup

### Environment Variables (`.env`)
```env
SECRET_KEY=your_secret_key
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=skillhub
UPLOAD_FOLDER=static/uploads
```

### Running Locally
```bash
# 1. Clone repository & set up virtual environment
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch Flask server
python app.py
```

### Production Deployment (Railway / Containerized)
Build configuration defined in [nixpacks.toml](file:///c:/Users/Harshitha/Downloads/SkillHub-main/nixpacks.toml):
```toml
[pkgs]
apt = ["mariadb-client", "libmariadb-dev", "gcc", "pkg-config"]

[start]
cmd = "gunicorn app:app --bind 0.0.0.0:8080 --workers 2"
```
