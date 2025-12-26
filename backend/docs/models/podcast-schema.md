# Podcast Schema

## 1. Important Implications:
- A podcast is a container(episodes may come later)
- We don't own audio
- We store **stable metadata**
- Schema must support **future expansion**

## 2. Podcast Schema
```text
Podcast
-------
id                  (PK)
title               (string, required)
publisher           (string, nullable)
description         (text, nullable)
image_url           (string, nullable)
language            (string, nullable)
external_source     (string, required)
external_id         (string, required)
created_at          (timestamp, UTC)
```
## Why EACH field exists (this is the key part)

### id
```text
id (PK)
```
- Internal primary key
- Used for relationship later (episode, subscriptions, history)
- Never tied to external systems
Same rule as Track.

### title
```text
title (string, required)
```
- Core identity of the podcast
- Used everywhere (UI, search, playlist)
- Always available from external APIs
No podcast exists without a title

### publisher
```text
publisher (string, nullable)
```
Why nullable:
- Some APIs don't provide this
- Some podcasts are self-published

Useful for:
- Display
- Credibility
- Filtering

### description
```text
description (text, nullable)
```
- Long-form content
- Used for detail pages
- Stored as text (not string) due to length

Nullable because:
- Some APIs provide poor or empty descriptions

---

### image_url
```text
image_url (string, nullable)
```
- External reference only
- Used for UI thumbnails
- Not stored locally
Nullable by design

---

### language
```text
language (string, nullable)
```
Examples:
```text
"en"
"en-US"
"hi"
```
Why include this now:
- Podcasts are language-sensitive
- Enables filtering later
- Very hard to retrofit cleanly later

Still nullable:
- Not all APIs provide it reliably

---

## external_source
```text
external_source (string, required)
```

Same purpose as Track:
- Multi-provider support
- Debugging
- Data lineage

---

### external_id
```text
external_id (string, required)
```
- Unique ID from the external provider
- Used for de-duplication and syncing
Stored as string for flexibility.

---

### created_at
```text
created_at (timestamp, UTC)
```
- Audit trail
- Sorting
- Debugging ingestion issues
Timezone-aware, UTC

---

## Constraint & implicit rules
### Unique constraint (logical)
```text
(external_source, external_id) must be unique
```

Same logic as Track:
- Prevent duplicate podcasts from same provider
