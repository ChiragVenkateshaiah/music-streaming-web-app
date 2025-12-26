from app.extensions import db, migrate
from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:music-streaming-app@db.cteoorioifetpeiidxuq.supabase.co:5432/postgres"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)

    # 🔥 IMPORTANT: import models so Alembic can see them
    from app import models

    return app