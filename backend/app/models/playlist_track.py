from datetime import datetime, timezone
from app.extensions import db




class PlaylistTrack(db.Model):
    __tablename__ = "playlist_tracks"


    id = db.Column(db.Integer, primary_key=True)


    playlist_id = db.Column(
        db.Integer,
        db.ForeignKey("playlists.id", ondelete="CASCADE"),
        nullable=False
    )


    track_id = db.Column(
        db.Integer,
        db.ForeignKey("tracks.id", ondelete="CASCADE"),
        nullable=False
    )


    # Order of the track inside the playlist
    position = db.Column(db.Integer, nullable=False)


    added_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )


    # Relationships
    playlist = db.relationship(
        "Playlist",
        back_populates="tracks"
    )

    track = db.relationship(
        "Track",
        lazy="joined"
    )

    def __repr__(self):
        return f"<PlaylistTrack playlist={self.playlist_id} track={self.track_id} pos={self.position}>"


