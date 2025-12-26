import os
from flask import Blueprint, abort
from flask_jwt_extended import jwt_required
from app.services.audio_service import stream_audio
from app.models.track import Track
from app.extensions import db


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




# Give this a headline

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
