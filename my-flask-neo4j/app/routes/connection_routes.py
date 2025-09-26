from flask import Blueprint, request, jsonify
from app.services.connection_service import ConnectionService

connection_bp = Blueprint("connection", __name__, url_prefix="/api/connections")

@connection_bp.post("/request")
def request_connection():
    try:
        data = request.get_json(force=True)
        reseller_email = data.get("reseller_email")
        producer_email = data.get("producer_email")
        
        if not reseller_email or not producer_email:
            return jsonify({"error": "reseller_email e producer_email são obrigatórios"}), 400
            
        connection = ConnectionService.request_connection(reseller_email, producer_email)
        return jsonify(connection), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Erro interno", "details": str(e)}), 500

@connection_bp.post("/accept")
def accept_connection():
    try:
        data = request.get_json(force=True)
        producer_email = data.get("producer_email")
        reseller_email = data.get("reseller_email")
        
        if not producer_email or not reseller_email:
            return jsonify({"error": "producer_email e reseller_email são obrigatórios"}), 400
            
        connection = ConnectionService.accept_connection(producer_email, reseller_email)
        return jsonify(connection), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Erro interno", "details": str(e)}), 500

@connection_bp.post("/reject")
def reject_connection():
    try:
        data = request.get_json(force=True)
        producer_email = data.get("producer_email")
        reseller_email = data.get("reseller_email")
        
        if not producer_email or not reseller_email:
            return jsonify({"error": "producer_email e reseller_email são obrigatórios"}), 400
            
        success = ConnectionService.reject_connection(producer_email, reseller_email)
        if not success:
            return jsonify({"error": "Conexão não encontrada"}), 404
        return jsonify({"rejected": True}), 200
    except Exception as e:
        return jsonify({"error": "Erro interno", "details": str(e)}), 500

@connection_bp.get("/pending/<string:user_email>")
def list_pending_connections(user_email: str):
    try:
        connections = ConnectionService.list_pending_connections(user_email)
        return jsonify(connections), 200
    except Exception as e:
        return jsonify({"error": "Erro interno", "details": str(e)}), 500

@connection_bp.get("/active/<string:user_email>")
def list_active_connections(user_email: str):
    try:
        connections = ConnectionService.list_active_connections(user_email)
        return jsonify(connections), 200
    except Exception as e:
        return jsonify({"error": "Erro interno", "details": str(e)}), 500