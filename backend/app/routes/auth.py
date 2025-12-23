from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.extensions import db
from app.models.user import User


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "User already exists"}), 400
    
    user = User(
        email = data["email"],
        password = generate_password_hash(data["password"])
    )


    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "Invalid JSON payload"}), 400


    email = data.get("email")
    password = data.get("password")

    
    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400
    

    user = User.query.filter_by(email=data["email"]).first()

    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401
    
    token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": token}), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 400
    

    return jsonify({
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at.isoformat()
    }), 200