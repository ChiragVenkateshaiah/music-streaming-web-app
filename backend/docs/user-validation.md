```markdown
# User Insert & Read Validation

This document validates that the `users` table is correctly wired to SQLAlchemy ORM by inserting and reading data using Flask shell.

```
---

## Purpose

The goal of this validation is to confirm:

- Database connectivity
- ORM model correctness
- Insert and query operations
- Timezone-aware timestamp handling

---

## User Model (Reference)

```python
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

```

## Insert User Record
### Using Flask shell:
```bash
flask shell
```

```python
from app.main import app
from app.extensions import db
from app.models.user import User

with app.app_context():
    user = User(email="testuser@example.com")
    db.session.add(user)
    db.session.commit()

    print("Inserted user ID:", user.id)

```
### Expected output:
```sql
Inserted user ID: 1
```

## Read User Records
```python
with app.app_context():
    users = User.query.all()
    for u in users:
        print(u.id, u.email, u.created_at)
```

### Expected output:
```css
1 testuser@example.com 2025-01-10 2025-12-22 13:36:14.694884+05:30
```

## Validation Result
- Insert operation successful
- Query operation successful
- ORM mapping confirmed
- PostgreSQL integration verified
