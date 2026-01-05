# 🎵 Music Streaming Web App
### Backend-driven Audio Streaming with Beat-Synced Sonic Visualizer

---

## 📌 Project Overview
This project is a **full-stack music streaming web application** built as part of an internship assignment

The goal was to design and implement:
- Secure backend APIs for music and podcast streaming
- Cloud-based storage and database integration
- Efficient audio straming with byte-range support
- A **real-time**, **beat-synced sonic wave visualizer** on the frontend

The system is designed with **real-world media streaming principles**, focusing on performance, security, and extensibility

---

## 🧠 Key Features
###🔐 Authentication & Security
- JWT-based authentication for protected APIs
- Secure access to music metadata and streaming endpoints
- Time-limited signed URLs for private audio files

## 🎧 Audio Streaming
- Supports **HTTP Range requests**
- Enables seeking, partial loading, and efficient playback
- Handles large audio files without full downloads

## ☁ Cloud Integration (Supabase)
- PostgreSQL database for metadata (tracks, playlists, podcasts)
- Supabase Storage for audio files
- Signed URLs for controlled access to music files

## 🌊 Sonic Wave / Beat-Synced Visualizer
- Built using the **Web Audio API**
- Real-time frequency analysis using `AnalyserMode`
- Canvas-based rendering
- **Layered 3D parallex effect** for depth and visual impact

## 🎙Podcast Integration
- External podcast metadata fetched via Listen Notes API
- Backend proxy streaming for podcast audio (handles CDN restrictions)

---

## 🏗 High-Level Architecture
```css
Frontend (HTML + Canvas + Web Audio API)
        ↓
Flask Backend (APIs, Auth, Streaming)
        ↓
Supabase (PostgreSQL + Storage)
```
### Responsibilities
| Layer    | Responsibility                                  |
| -------- | ----------------------------------------------- |
| Frontend | Audio playback, visualization, user interaction |
| Backend  | Auth, metadata APIs, streaming logic            |
| Database | Tracks, playlists, podcasts metadata            |
| Storage  | Music files, accessed via signed URLs           |

---

## 📂Project Structure
```bash
music-streaming-web-app/
│
├── backend/
│   ├── app/
│   │   ├── main.py            # App entry point
│   │   ├── extensions.py      # DB, JWT initialization
│   │   ├── models/            # SQLAlchemy models
│   │   ├── routes/            # API routes
│   │   └── services/          # Streaming & storage logic
│   │
│   ├── migrations/            # Alembic migrations
│   ├── docs/                  # Technical documentation
│   └── README.md
│
├── frontend/
│   ├── supabase-visualizer.html
│   ├── visualizer.js
│   └── test files
│
└── README.md
```
---

## 🧩 Backend Implementation Details
### Audio Streaming
- Implements `206 Partial Content` responses
- Handles `Range` headers for smooth seeking
- Prevents path traversal attacks
- Designed for large audio files

### Database Models
- Tracks
- Podcasts
- Playlists & playlist reordering
- Managed using SQLAlchemy + Alembic

### Supabase Storage
- Audio files stored privately
- Backend generates signed URLs with expiration
- Avoids exposing storage credentials to frontend

---

## 🌊 Sonic Wave Visualizer (Core Highlight)
The sonic wave visualizer is implemented using:
- `AudioContext`
- `AnalyserNode`
- Canvas rendering

### Visualization Strategy
- Frequency data extracted in real time
- Multiple visual layers rendered with:
    - Different depths
    - Different opacity
    - Temporal smoothing
- Creates a **3D parallex illusion** without WebGL

### Why Canvas Instead of WebGL?
- Faster iteration
- Lower risk
- High performance
- Easier to maintain
- Still visually impressive

This approach was choosen to meet tight deadlines while delivering a professional visual effect.

---

## 🎥 Demo Flow (What to Expect)
1. User plays music from Supabase
2. Audio streams instantly with seeking enabled
3. Sonic waves react in real time to beats and frequency changes
4. Visual depth gives a 3D-like experience
5. Podcasts can be searched and streamed via backend APIs

---

## 🧪 Testing Strategy
- Manual browser testing
- Network inspection for `206 Partial Content`
- Audio seek & reload validation
- Visualizer synchronization tests
- Signed URLs expiry validation

---

## 📚 Key Learnings
- Media streaming is different from file downloads
- Proper handling of HTTP Range requests is critical
- Browser audio security requires user interaction
- External CDNs may restrict embedded playback
- Backend proxying is sometimes necessary
- Real-Time visualization requires careful performance considerations

---

## 🚀 Future Imporvements
- User playlists UI
- WebGL-based advanced visualizations
- Mobile-optimized frontend
- Caching strategies for audio metadata
- User personalization features

---
## Author
### **Chirag Venkateshaiah**
 Music Streaming Web App -- Internship Project