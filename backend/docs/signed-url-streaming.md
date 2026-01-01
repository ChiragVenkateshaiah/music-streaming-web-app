# Signed URL Based AUdio Streaming

## Objective
Enable secure, scalable audio streaming using Supabase Storage signed URLs, allowing browsers to stream audio files directly without proxing bytes through the backend.

This approach mirrors production architectures used by media platforms

---

## Why Signed URLs are Needed
HTML `<audio>` elements cannot send Authorization headers.

Problems with diret backend streaming:
- Backend must handle Range requests
- High memory & bandwidth usage
- Poor scalability
Signed URLs solve this by:
- Allowing temporary, secure access to private storage objects
- Letting the browser handle streaming natively
- Reducing backend load

---

## Architecture Overview
```text
Client
  │
  │  (JWT)
  ▼
Flask Backend
  │
  │  (Service Role Key)
  ▼
Supabase Storage (Private Bucket)
  │
  │  (Signed URL)
  ▼
Browser <audio> streaming
```
---

## Storage Setup
- Bucket name: `audio`
- Bucket visibility: PRIVATE
- Object key example: `test.mp3`
Only the backend can generate access using the **Service Role Key**

---

## Backend Flow
### 1. Client requests signed URL
```bash
GET /stream/tracks/<track_id>/signed-url
Authorization: Bearer <JWT>
```

### 2. Backend validates user
- JWT authentication
- Track lookup from database
- Fetch `audio_file` path

### 3. Backend generates signed URL
Uses Supabase Storage API:
```bash
POST /storage/v1/object/sign/<bucket>
```
payload:
```json
{
    "paths": ["test.mp3"]
    "expiresIn": 300
}
```

## Important Supabase Detail
Supabase returns a **relative signed path**:
```swift
/object/sign/audio/test.mp3?token=...
```
To access the file, it must be served via the storage gateway:
```swift
/storage/v1/object/sign/audio/test.mp3?token=...
```

Final backend response:
```json
{
    "stream_url": "https://<project>.supabase.co/storage/v1/object/sign/audio/test.mp3?token=...",
    "expires_in": 300
}
```

## Security Considerations
- Bucket remains private
- URLs expire automatically
- Service Role Key is never exposed to frontend
- Users cannot access files without backend authorization


## Outcome
- Native browser streaming
- Seek forward/backward works
- Backend is lighweight and scalable
- Matches real-world cloud storage patterns

## Key Learnings
- Signed URLs are required for private media access
- Storage APIs have **control plane vs data plane**
- `/object/sign` generates tokens
- `/storage/v1` serves actual files
- Backend authorization != file streaming