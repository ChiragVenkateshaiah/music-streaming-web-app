# Audio Streaming Backend

## Objective
Implement secure, efficient audio streaming in the backend using proper HTTP semantics so that clients can play, pause, seek, and resume audio files.

---

## Key Features Implemented
- JWT-protected audio streaming endpoints
- HTTP Range request handling
- `206 Partial Content` responses for streaming
- Efficient memory usage (chuck-based reads)
- Path traversal protection for file access
- Browser-compatible streaming behavior

---

## Why Streaming (Not File Download)
| **File Download** | **Streaming** |
| ---               |   ---         |
| Entire file sent  |    Only requested bytes sent|
| No seeking        |    Seeking supported|
| High memory usage |    Efficient memory usage|
| Poor scalability  |    Production-ready|

**Streaming is required for real-world media applications**

---

## Core Streaming Logic
- Browser sends `Range` headers (e.g. `bytes=500000-1000000`)
- Backend parses the range
- Reads only the requested byte segment
- Returns `206 Partial Content` with corret headers

### Key headers:
- `Accept-Ranges: bytes`
- `Content-Range`
- `Content-Length`

---

## Security Considerations
- All streaming routes are protected with JWT
- File paths are validated to prevent path traversal attacks
- Clients never provide direct filesystem paths

