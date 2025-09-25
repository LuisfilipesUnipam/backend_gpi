from flask import Blueprint, request, jsonify
from app.services.person_service import PersonService

person_bp = Blueprint("person", __name__, url_prefix="/api/persons")

@person_bp.post("")
def create_person():
    try:
        data = request.get_json(force=True, silent=False)
        person = PersonService.create_person(data)
        return jsonify(person), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Erro interno", "details": str(e)}), 500

@person_bp.get("/<string:name>")
def get_person(name: str):
    person = PersonService.get_person(name)
    if not person:
        return jsonify({"error": "Person not found"}), 404
    return jsonify(person), 200

@person_bp.get("")
def list_people():
    limit = request.args.get("limit", default=25, type=int)
    people = PersonService.list_people(limit)
    return jsonify(people), 200

@person_bp.delete("/<string:name>")
def delete_person(name: str):
    ok = PersonService.delete_person(name)
    if not ok:
        return jsonify({"error": "Person not found"}), 404
    return jsonify({"deleted": True}), 200