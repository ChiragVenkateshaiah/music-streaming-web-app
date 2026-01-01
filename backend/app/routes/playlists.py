from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.playlist import Playlist
from app.models.playlist_track import PlaylistTrack
from app.models.track import Track
from sqlalchemy import and_



playlist_bp = Blueprint("playlists", __name__, url_prefix="/playlists")


# create playlist implementation

@playlist_bp.route("", methods=["POST"])
@jwt_required()
def create_playlist():
    user_id = get_jwt_identity()
    data = request.get_json()


    name = data.get("name")
    if not name:
        abort(400, "Playlist name is required")

    
    playlist = Playlist(
        user_id=user_id,
        name=name
    )

    db.session.add(playlist)
    db.session.commit()


    return {
        "id": playlist.id,
        "name": playlist.name
    }, 201




# add track to playlist

@playlist_bp.route("/<int:playlist_id>/tracks", methods=["POST"])
@jwt_required()
def add_track_to_playlist(playlist_id):
    user_id = get_jwt_identity()
    data = request.get_json()


    track_id = data.get("track_id")
    if not track_id:
        abort(400, "track_id is required")

    
    playlist = Playlist.query.filter_by(
        id=playlist_id,
        user_id=user_id
    ).first()


    if not playlist:
        abort(404, "Playlist not found")


    track = Track.query.get(track_id)
    if not track:
        abort(404, "Track not found")

    
    # Determine next position
    next_position = len(playlist.tracks) + 1

    playlist_track = PlaylistTrack(
        playlist_id=playlist.id,
        track_id=track.id,
        positon=next_position
    )

    db.session.add(playlist_track)
    db.session.commit()


    return {
        "playlist_id": playlist.id,
        "track_id": track.id,
        "position": next_position
    }, 201



# Fetch Playlist with Ordered Tracks

@playlist_bp.route("/<int:playlist_id>", methods=["GET"])
@jwt_required()
def get_playlist(playlist_id):
    user_id = get_jwt_identity()

    playlist = Playlist.query.filter_by(
        id=playlist_id,
        user_id=user_id
    ).first()

    if not playlist:
        abort(404, "Playlist not found")

    
    return {
        "id": playlist.id,
        "name": playlist.name,
        "tracks": [
            {
                "track_id": pt.track.id,
                "title": pt.track.title,
                "artist": pt.track.artist,
                "position": pt.position
            }
            for pt in playlist.tracks
        ]
    }


# Delete Playlist

@playlist_bp.route("/<int:playlist_id>", methods=["DELETE"])
@jwt_required()
def delete_playlist(playlist_id):
    user_id = get_jwt_identity()

    playlist = Playlist.query.filter_by(
        id=playlist_id,
        user_id=user_id
    ).first()

    if not playlist:
        abort(404, "Playlist not found")

    db.session.delete(playlist)
    db.session.commit()

    return {"message": "Playlist deleted"}


# Reorder Playlist

@playlist_bp.route("/<int:playlist_id>/reorder", methods=["PUT"])
@jwt_required()
def reorder_playlist_track(playlist_id):
    user_id = get_jwt_identity()
    data = request.get_json()


    track_id = data.get("track_id")
    new_position = data.get("new_position")


    if not track_id or not new_position:
        abort(400, "track_id and new_position are required")

    playlist = Playlist.query.filter_by(
        id=playlist_id,
        user_id=user_id
    ).first()

    if not playlist:
        abort(404, "Playlist not found")


    playlist_track = PlaylistTrack.query.filter_by(
        playlist_id=playlist.id,
        track_id=track_id
    ).first()


    if not playlist_track:
        abort(404, "Track not in playlist")
    
    old_position = playlist_track.position

    if old_position == new_position:
        return {"message": "No change required"}
    
    try:
        # Atomic reorder
        if new_position < old_position:
            # Move UP: shift others DOWN
            db.session.query(PlaylistTrack).filter(
                and_(
                    PlaylistTrack.playlist_id == playlist.id,
                    PlaylistTrack.position > old_position,
                    PlaylistTrack.position <= new_position
                )
            ).update(
                {PlaylistTrack.position: PlaylistTrack.position - 1},
                synchronize_session=False
            )
    
        else:
            # Move DOWN: Shift others UP
            db.session.query(PlaylistTrack).filter(
                and_(
                    PlaylistTrack.playlist_id == playlist.id,
                    PlaylistTrack.position > old_position,
                    PlaylistTrack.position <= new_position
                )
            ).update(
                {PlaylistTrack.position: PlaylistTrack.position - 1},
                synchronize_session=False
            )

        
        # Set new position
        playlist_track.position = new_position

        db.session.commit()

    except Exception:
        db.session.rollback()
        abort(500, "Failed to reorder playlist")

    
    return {
        "track_id": track_id,
        "old_position": old_position,
        "new_position": new_position
    }


