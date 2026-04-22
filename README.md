# ShopSense — E-Commerce Client Assistance System

> A Flask web application that tracks purchase behaviour and delivers personalised product recommendations through rule-based analytics. Built across two Scrum sprints.

---

## Project Objective

ShopSense helps e-commerce customers discover relevant products by analysing their purchase history. The system exposes purchase analytics (category breakdown, frequency, spending) and generates a **Top 5 personalised recommendation list** per user, ranking candidates by category affinity and global popularity.

---

## Technology Stack

| Layer | Technology |
|---|---|
| Web framework | Flask 3.x |
| ORM / Database | Flask-SQLAlchemy + SQLite |
| Authentication | Flask-Login + Flask-Bcrypt |
| Templating | Jinja2 (HTML5 + CSS3) |
| Language | Python 3.10+ |

---

## Folder Structure

```
project/
├── app/
│   ├── __init__.py           # App factory — initialises Flask, DB, auth
│   ├── models.py             # SQLAlchemy models: User, Purchase, Product, Recommendation
│   ├── routes.py             # All HTTP routes (auth, history, dashboard, recommendations)
│   ├── services/
│   │   ├── analytics.py      # Sprint 2: purchase metrics
│   │   └── recommender.py    # Sprint 2: Top-5 recommendation engine
│   ├── templates/
│   │   ├── base.html         # Shared layout (nav, flash messages, footer)
│   │   ├── index.html        # Landing / hero page
│   │   ├── register.html     # User registration
│   │   ├── login.html        # User login
│   │   ├── history.html      # Protected purchase history (Sprint 1)
│   │   ├── dashboard.html    # Analytics dashboard (Sprint 2)
│   │   └── recommendations.html  # Top 5 recommendations (Sprint 2)
│   └── static/
│       └── styles.css        # Custom dark-mode CSS (no framework)
├── run.py                    # Entry point + demo data seeder
├── requirements.txt          # Python dependencies
└── README.md
```

---

## Database Design

### `users`
| Column | Type | Notes |
|---|---|---|
| id | INTEGER | Primary key |
| name | VARCHAR(120) | Full name |
| email | VARCHAR(150) | Unique |
| password_hash | VARCHAR(256) | Bcrypt hash |
| created_at | DATETIME | Auto |

### `purchases`
| Column | Type | Notes |
|---|---|---|
| id | INTEGER | Primary key |
| user_id | INTEGER | FK → users.id |
| product_name | VARCHAR(200) | Product name |
| category | VARCHAR(100) | e.g. Electronics |
| price | FLOAT | EUR |
| date | DATETIME | Purchase date |

### `products`
| Column | Type | Notes |
|---|---|---|
| id | INTEGER | Primary key |
| name | VARCHAR(200) | Product name |
| category | VARCHAR(100) | Category tag |
| price | FLOAT | Listed price |
| popularity_score | FLOAT | 0–100 |
| description | TEXT | Optional |

### `recommendations`
| Column | Type | Notes |
|---|---|---|
| id | INTEGER | Primary key |
| user_id | INTEGER | FK → users.id |
| product_id | INTEGER | FK → products.id |
| reason | VARCHAR(300) | Human-readable reason |
| score | FLOAT | Ranking score |
| created_at | DATETIME | Auto |

---

## Sprint Goals

### Sprint 1 — Foundation
> **Goal:** Deliver a working vertical slice with authentication and purchase history.

**User stories delivered:**
- As a visitor, I can register a new account.
- As a user, I can log in and log out securely.
- As a user, I can view my full purchase history in a protected page.
- As a developer, the database is seeded with demo data for testing.

**Modules:** `models.py`, `routes.py`, auth templates, `history.html`, `run.py`

---

### Sprint 2 — Intelligence Layer
> **Goal:** Add analytics and rule-based recommendation engine on top of Sprint 1.

**User stories delivered:**
- As a user, I can see my spending broken down by category.
- As a user, I can see how often I buy each product (purchase frequency).
- As a user, I receive a Top 5 personalised product list.
- As a user, I can see globally popular products.

**Modules:** `services/analytics.py`, `services/recommender.py`, `dashboard.html`, `recommendations.html`

---

## How the Recommendation Logic Works

The recommender uses a **rule-based ranking pipeline** (no machine learning required):

```
1. Identify the user's top 3 most-purchased categories
        ↓
2. Query all Products in those categories
        ↓
3. Sort by popularity_score (descending)
        ↓
4. Exclude products the user has already purchased
        ↓
5. Backfill with globally popular products if < 5 candidates remain
        ↓
6. Return the Top 5 with a human-readable reason string
```

This covers two recommendation strategies simultaneously:
- **Similarity-based:** recommends within the user's preferred categories.
- **Popularity-based:** backfills with trending products for cold-start users.

---

## Setup Instructions

### 1. Clone / Navigate to the project

```bash
cd "Projet federe"
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python run.py
```

The first run will:
- Create `app.db` (SQLite database) automatically.
- Seed 12 products and 2 demo users with purchase histories.
- Start the development server on **http://127.0.0.1:5000**.

---

## How to Test the App

### Demo accounts (pre-seeded)

| Email | Password | Profile |
|---|---|---|
| alice@demo.com | password123 | Electronics + Books buyer |
| bob@demo.com | password123 | Gaming + Fashion buyer |

### Manual test checklist

| Step | Expected result |
|---|---|
| Visit `/` | Hero landing page visible |
| Register a new account | Redirected to login with success flash |
| Login with wrong password | Error flash shown |
| Login as `alice@demo.com` | Redirected to `/history` |
| Visit `/history` without login | Redirected to `/login` |
| Visit `/dashboard` as Alice | Electronics + Books bars highest |
| Visit `/recommendations` as Alice | Top 5 Electronics/Books products |
| Visit `/recommendations` as Bob | Top 5 Gaming/Fashion products |
| Logout | Session cleared, back to `/login` |

---

## Scrum Artefacts

### Product Backlog (prioritised)

| Priority | User Story |
|---|---|
| 1 | Register / Login / Logout |
| 2 | View purchase history |
| 3 | Category spending breakdown |
| 4 | Purchase frequency analysis |
| 5 | Similarity-based recommendations |
| 6 | Popularity-based recommendations |
| 7 | Top 5 personalised output |

### Sprint 1 Backlog

| Task | Status |
|---|---|
| User model + password hashing | ✅ Done |
| Register / Login / Logout routes | ✅ Done |
| Purchase model + history route | ✅ Done |
| Auth templates (login, register) | ✅ Done |
| History template with stat cards | ✅ Done |
| DB seed with demo data | ✅ Done |

### Sprint 2 Backlog

| Task | Status |
|---|---|
| `analytics.py` — frequency, categories, spending | ✅ Done |
| `recommender.py` — Top 5 pipeline | ✅ Done |
| Dashboard route + template | ✅ Done |
| Recommendations route + template | ✅ Done |
| Popularity product grid | ✅ Done |

---

## License

Academic project — TD / Scrum sprint exercise.
