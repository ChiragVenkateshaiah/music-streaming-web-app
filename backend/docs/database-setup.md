# Database Setup (PostgreSQL + Flask-SQLALchemy)

This document describes how the PostgreSQL database was configured and how tables were created during local development using SQLAlchemy ORM.

> Note: This approach is used only for development and learning purposes.
> Production systems should use schema migrations (Alembic).

---

## Prerequisites

- PostgreSQL installed and running
- Database created: `music-app`
- Python virtual environment activated
- Required dependencies installed via `requirements.txt`

---

## Environment Configuration

Create a `.env` file at the backend root with the following variables:

```env
FLASK_ENV=development
SECRET_KEY=super-secret-key
JWT_SECRET_KEY=jwt-secret-key
DATABASE_URL=postgresql://postgres:<password>@localhost:5432/music_app
```

.env is excluded from version control
A .env.example file is provided for reference


## Model Registration
All SQLAlchemy models are defined under:
```bash
app/models/
```
Models are imported in app/models/__init__.py to ensure they are registered with SQLAlchemy at runtime.

Example:
```bash
from .user import User
```

This guarantees that SQLAlchemy is aware of all models before table creation

## Table Creation (Development Only)
Tables were created using SQLAlchemy metadata inside an application context.
```python
from app.main import app
from app.extensions import db

with app.app_context():
    db.metadata.create_all(bind=db.engine)
```

This method ensures:
- Correct database connection
- All registered models are detected
- Deterministic table creation

## Verification
Table creation was verified using pgAdmin:
```pgsql
Server -> Databases -> music_app -> Schemas -> public -> Tables
```
```bash
users
```

## Developer Notes
- Tables are introduced incrementally based on feature development.
- This mirrors real-world backend engineering practices.
- Bulk upfront schema creation is intentionally avoided.