from datetime import datetime, timezone
from app.extensions import db


class Playlist(db.Model):
    __tablename__ = "playlists"


    id = db.Column(db.Integer, primary_key=True)


    # Owner of the playlist
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )


    name = db.Column(db.String(255), nullable=False)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )


    # Relationship to playlist_tracks
    tracks = db.relationship(
        "PlaylistTrack",
        back_populates="playlist",
        cascade="all, delete-orphan",
        order_by="PlaylistTrack.position"
    )

    def __repr__(self):
        return f"<Playlist {self.id} - {self.name}>"