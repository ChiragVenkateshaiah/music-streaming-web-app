# DB-Backed Streaming
## Objective
Convert filename-based streaming into database-driven streaming and integrate Supabase Storage as the audio source

## What Changed
### Before:
```bash
/stream/<filename>
```
### After:
```bash
/stream/tracks/<track_id>
```
Streaming is now based on track records, not filenames.

### Architecture Overview
```java
Client
 -> Flask API (JWT protected)
 -> PostgreSQL (track metadata)
 -> Supabase Storage (audio files)
 -> Flask streaming service
```

---

### Database Design
The `tracks` table stores metadata only:
- `id`
- `title`
- `artist`
- `audio_file` (logical filename, e.g. `test.mp3`)

Binary audio files are never stored in PostgreSQL

---

### Supabase Storage Integration
- Audio files are uploaded to a private Supabase Storage bucket
- Backend fetches files using a service role key
- Files are cached locally for performance
- Streaming logic remains unchanged

This separation keeps the system scalable and cloud-ready

---

### Caching Behavior
- Audio files are downloaded once from Supabase
- Subsequent requests stream from local cache
- Reduces latency and storage API calls

This mirrors real-world CDN/cache behavior.

---



