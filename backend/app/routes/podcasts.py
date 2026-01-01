from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required
from app.services.podcast_service import (
    search_podcasts,
    get_podcast_episodes
)


podcast_bp = Blueprint(
    "podcasts",
    __name__,
    url_prefix="/podcasts"
)


@podcast_bp.route("/search", methods=["GET"])
@jwt_required()
def search():
    query = request.args.get("q")
    if not query:
        abort(400, "Search query required")
    
    results = search_podcasts(query)


    return [
        {
            "id": p["id"],
            "title": p["title_original"]
            "publisher": p["publisher_original"],
            "thumbnail": p["thumbnail"]
        }
        for p in results
    ]


@podcast_bp.route("/<podcast_id>/episodes", methods=["GET"])
@jwt_required()
def episodes(podcast_id):
    episodes = get_podcast_episodes(podcast_id)


    return [
        {
            "id": e["id"],
            "title": e["title"],
            "audio_url": e["audio_url"],
            "duration_sec": e["duration_sec"],
            "published_at": e["pub_date_ms"]
        }
        for e in episodes
    ]