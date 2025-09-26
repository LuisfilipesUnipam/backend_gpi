from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from app.services.company_service import CompanyService

user_bp = Blueprint("user", __name__, url_prefix="/api/users")

# Rotas de Usuário
@user_bp.post("")
def create_user():
    try:
        data = request.get_json(force=True, silent=False)
        user = UserService.create_user(data)
        return jsonify(user), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Erro interno", "details": str(e)}), 500

@user_bp.get("/<string:email>")
def get_user(email: str):
    user = UserService.get_user(email)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200

@user_bp.get("")
def list_users():
    limit = request.args.get("limit", default=25, type=int)
    users = UserService.list_users(limit)
    return jsonify(users), 200

@user_bp.delete("/<string:email>")
def delete_user(email: str):
    ok = UserService.delete_user(email)
    if not ok:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"deleted": True}), 200