from flask import Blueprint, request, jsonify
from app.services.company_service import CompanyService

company_bp = Blueprint("company", __name__, url_prefix="/api/companies")

# Rotas de Empresa
@company_bp.post("")
def create_company():
    try:
        data = request.get_json(force=True, silent=False)
        company = CompanyService.create_company(data)
        return jsonify(company), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Erro interno", "details": str(e)}), 500

@company_bp.get("/<string:cnpj>")
def get_company(cnpj: str):
    company = CompanyService.get_company(cnpj)
    if not company:
        return jsonify({"error": "Company not found"}), 404
    return jsonify(company), 200

@company_bp.get("")
def list_companies():
    limit = request.args.get("limit", default=25, type=int)
    companies = CompanyService.list_companies(limit)
    return jsonify(companies), 200

@company_bp.delete("/<string:cnpj>")
def delete_company(cnpj: str):
    ok = CompanyService.delete_company(cnpj)
    if not ok:
        return jsonify({"error": "Company not found"}), 404
    return jsonify({"deleted": True}), 200