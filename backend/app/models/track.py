from datetime import datetime, timezone
from app.extensions import db


class Track(db.Model):
    __tablename__ = "tracks"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    album = db.Column(db.String(255), nullable=True)

    duration_seconds = db.Column(db.Integer, nullable=True)
    cover_image_url = db.Column(db.String(512), nullable=True)

    external_source = db.Column(db.String(50), nullable=False)
    external_id = db.Column(db.String(255), nullable=False)


    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )


    __table_args__ = (
        db.UniqueConstraint(
            "external_source",
            "external_id",
            name="uq_tracks_external_source_external_id"
        ),
    )