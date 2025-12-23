# JWT Authenctication Flow

This backend uses stateless JWT authentication.

---

## Flow Overview

1. User registers
2. User logs in
3. JWT token is issues
4. Client stores token
5. Client sends token in Authorization header
6. Protected routes validate token

---

## Token Creation

```python
create_access_token(identity=str(user.id))
> JWT subject (`sub`) must be a string per JWT specification.
```

## Token Validation
Protected routes use:
```python
@jwt_required()
```
## This middleware:
- Validates token
- Checks expiry
- Extracts identity

## Stateless Design
- No server-side sessions
- Scales horizontally
- Suitable for microservices