import os
from flask import Blueprint, abort
from flask_jwt_extended import jwt_required
from app.services.audio_service import stream_audio


stream_bp = Blueprint("stream", __name__, url_prefix="/stream")


AUDIO_DIR = os.path.join(os.getcwd(), "media", "audio")


@stream_bp.route("/<string:filename>")
@jwt_required()
def stream(filename):
    file_path = os.path.join(AUDIO_DIR, filename)


    if not os.path.exists(file_path):
        abort(404, "Audio file not found")

    
    return stream_audio(file_path)

