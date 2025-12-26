# Track Model


> **1. Important Implications**
- It may come from different external APIs
- We do not own the audio file
- We own metadata + relationships

> I am keeping the schema in a way that is:
- Source-agnostic
- Stable
- Minimal

## 2. Track Schema

```text
Track
-----
id                      (PK)
title                   (string, required)
aritst                  (string, required)
album                   (string, required)
duration_seconds        (string, nullable)
cover_image_url         (string, nullable)
external_source         (string, required)
external_id             (string, required)
created_id              (timestamp, UTC)
```

## 3. Why EACH field exists

### id
```text
id (PK)
```
- Internal primary key
- Never exposed to external APIs
- Used for relationships (playlists, history)
> Backend rule: Never rely on third-party IDs as primary keys.

### title
```text
title (string, required)
```
- Core display field
- Always present in external APIs
- Used in UI, search, playlists
> No track exists without a title

### artist
```text
artist (string, required)
```
- Display + grouping
- Search/filter use cases
- Kept as string for simplicity (no artist table yet)
> Industry approach: normalize later, no upfront.

### album
```text
album (string, nullable)
```
- Optional metadata
- Some tracks don't belong to albums
- Useful for UI grouping
> Nullable by design

### duration_seconds
```text
duration_seconds (integer, nullable)
```
- Used for:
    - UI timers
    - playlist duration calculation
- Stored as integer (not time type) for simplicity
Nullable because:
- Not all APIs provide duration
- Some metadata is incomplete

### cover_image_url
```text
cover_image_url (string, nullable)
```
- External reference only
- We do NOT store images
- Can change per provider
Nullable because:
- Some tracks have no artwork

### external_source
```text
external_source (string, required)
```
Examples:
```text
"musicbrainz"
"theaudiodb"
```
Why this exists:
- Some `external_id` can exists across providers
- Enables multi-source ingestion
- Makes debugging easier
> This field is very important for scalability

### external_id
```text
external_id (string, required)
```
- ID provided by the external API
- Used to:
    - avoid duplicates
    - re-sync metadata
    - trace origin

Stored as string because:
- APIs use different ID formats (UUID, numeric, etc)

### created_at
```text
created_at (timestamp, UTC)
```
- Auditability
- Debugging
- Sorting (new arrivals, etc)
> Always UTC, timezone-aware


## 4. Constrints & Implicit rules (backend thinking)
These are not fields, but design decisions

### Unique constraint (Logical)
```text
(external_source, external_id) must be unique
```
- Prevent duplicate tracks
- Same track from same source should exist once
- Should be enforce this later at DB level.

