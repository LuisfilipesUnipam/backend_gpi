from typing import List, Dict, Any, Optional
from app.repositories.user_repository import UserRepository
from app.repositories.company_repository import CompanyRepository

class CompanyService:
    @staticmethod
    def create_company(data: Dict[str, Any]) -> Dict[str, Any]:
        required_fields = ["cnpj", "name", "type", "address", "owner_email"]
        if not all(field in data for field in required_fields):
            raise ValueError(f"Campos obrigatórios: {', '.join(required_fields)}")
        
        valid_types = ["producer", "reseller"]
        if data["type"] not in valid_types:
            raise ValueError(f"Tipo deve ser: {' ou '.join(valid_types)}")

        user = UserRepository.get_user_by_email(data["owner_email"])
        if not user:
            raise ValueError("Usuário proprietário não encontrado")

        return CompanyRepository.create_company(data)

    @staticmethod
    def get_company(cnpj: str) -> Optional[Dict[str, Any]]:
        return CompanyRepository.get_company_by_cnpj(cnpj)

    @staticmethod
    def list_companies(limit: int = 25) -> List[Dict[str, Any]]:
        return CompanyRepository.list_companies(limit)

    @staticmethod
    def delete_company(cnpj: str) -> bool:
        return CompanyRepository.delete_company(cnpj)