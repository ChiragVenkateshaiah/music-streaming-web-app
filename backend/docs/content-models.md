# Content Models (Tracks & Podcasts)

This document describes the core content models used in the backend.
These models represent externally sourced media metadata and are designed to be source-agnostic, minimal, and scalable.

---

## Design Philosophy

- Store only metadata owned by the applicaton
- Do not mirror external APIs directly
- Support multiple external content providers
- Keep schemas stable and extensible

---

## Track Model

Represent a single music track sourced from an external provider.

### Fields

| Field | Type | Description |
|---|---|---|
| id | Integer (PK) | Internal primary key |
| title | String | Track title |
| artist | String | Artist name |
| album | String (nullable) | Album name |
| duration_seconds | Integer (nullable) | Track duration |
| cover_image_url | String (nullable) | Artwork URL |
| external_source | String | Source provider (e.g. MusicBrainz) |
| external_id | String | Provider-specific ID |
| created_at | Timestamp (UTC) | Record creation time |


### Constraints

- Unique constraint on (`external_source`, `external_id`)
- Prevents duplicate ingestion from the same provider

---

## Podcast Model

Represent a podcast show or series (not episodes).

### Fields

| Field | Type | Description |
|---|---|---|
| id | Integer (PK) | Internal primary key |
| title | String | Podcast title |
| publisher | String (nullable) | Publisher or creator |
| description | Text (nullable) | Podcast description |
| image_url | String (nullable) | Artwork URL |
| language | String (nullable) | Podcast language |
| external_source | String | Source provider |
| external_id | String | Provider-specific ID |
| created_at | Timestamp (UTC) | Record creation time |

### Constraints

- Unique constraint on (`external_source`, `external_id`)
- Ensures uniqueness per provider

---

## Notes

- Audio files are not stored or streamed by the backend
- Episodes and playlists are modeled separately
- External IDs are stored only for synchronization and traceability

