from flask import Flask, jsonify
from app.config import Config
from app.extensions import db, jwt, cors



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app import models

    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "OK"}), 200
    
    # Import blueprints INSIDE functions
    from app.routes.auth import auth_bp
    from app.routes.stream import stream_bp


    app.register_blueprint(auth_bp)
    app.register_blueprint(stream_bp)

    
    return app

app = create_app()
