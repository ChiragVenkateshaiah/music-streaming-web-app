import os
from flask import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.audio_service import stream_audio
from app.models.track import Track
from app.extensions import db
from app.services.storage_service import generate_signed_url



stream_bp = Blueprint("stream", __name__, url_prefix="/stream")


BASE_AUDIO_DIR = os.path.abspath(
    os.path.join(os.getcwd(), "media", "audio")
)


# 🎧 GET - actual audio streaming
@stream_bp.route("/<string:filename>")
@jwt_required()
def stream(filename):
    requested_path = os.path.abspath(
        os.path.join(BASE_AUDIO_DIR, filename)
    )

    # 🔐 Path traversal protection
    if not requested_path.startswith(BASE_AUDIO_DIR):
        abort(403, "Access denied")

    if not os.path.exists(requested_path):
        abort(404, "Audio file not found")

    
    return stream_audio(requested_path)


# 🧠 HEAD - metadata only (browser optimization)
@stream_bp.route("/<string:filename>", methods=["HEAD"])
@jwt_required()
def stream_head(filename):
    requested_path = os.path.abspath(
        os.path.join(BASE_AUDIO_DIR, filename)
    )

    if not requested_path.startswith(BASE_AUDIO_DIR):
        abort(403)

    
    if not os.path.exists(requested_path):
        abort(404)

    size = os.path.getsize(requested_path)

    return "", 200, {
        "Content-Length": str(size),
        "Accept-Ranges": "bytes"
    }




# TrackID

@stream_bp.route("/tracks/<int:track_id>", methods=["GET"])
@jwt_required()
def stream_track(track_id):
    # adding for testing
    print("STREAM TRACK HIT:", track_id)


    track = Track.query.get(track_id)
    # adding for testing
    print("TRACK:", track)
    print("AUDIO_FILE:", track.audio_file)



    if not track:
        abort(404, "Track not found")

    
    requested_path = os.path.abspath(
        os.path.join(BASE_AUDIO_DIR, track.audio_file)
    )

    # 🔒 Path traversal protection
    if not requested_path.startswith(BASE_AUDIO_DIR):
        abort(403, "Access denied")

    if not os.path.exists(requested_path):
        abort(404, "Audio file not found on server")

    return stream_audio(requested_path)


# signed URL
@stream_bp.route("/tracks/<int:track_id>/signed-url", methods=["GET"])
@jwt_required()
def get_signed_stream_url(track_id):
    track = Track.query.get(track_id)
    if not track:
        abort(404, "Track not found")

    print(f"[DEBUG] Track audio_file value: '{track.audio_file}'")
    print(f"[DEBUG] Type of audio_file: {type(track.audio_file)}")

    # Also check if the file exists locally (for debugging)
    local_path = os.path.join(BASE_AUDIO_DIR, track.audio_file)
    print(f"[DEBUG] Local path would be: {local_path}")
    print(f"[DEBUG] Local file exists: {os.path.exists(local_path)}")


    # track.audio_file should be like "test.mp3"
    signed_url = generate_signed_url(
        bucket="audio",
        file_path=track.audio_file, # Hardcoded a known file
        expires_in=300 # 5 minutes
    )

    return {
        "stream_url": signed_url,
        "expires_in": 300
    }

