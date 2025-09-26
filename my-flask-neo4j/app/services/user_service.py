from typing import List, Dict, Any, Optional
from app.repositories.user_repository import UserRepository

class UserService:
    @staticmethod
    def create_user(data: Dict[str, Any]) -> Dict[str, Any]:
        required_fields = ["email", "name", "phone", "roles", "password"]
        if not all(field in data for field in required_fields):
            raise ValueError(f"Campos obrigatórios: {', '.join(required_fields)}")
        
        if not isinstance(data["roles"], list):
            raise ValueError("roles deve ser uma lista")
        
        valid_roles = ["producer", "reseller"]
        if not all(role in valid_roles for role in data["roles"]):
            raise ValueError(f"Roles válidos: {', '.join(valid_roles)}")

        if len(data["password"]) < 6:
            raise ValueError("Senha deve ter pelo menos 6 caracteres")

        return UserRepository.create_user(data)

    @staticmethod
    def get_user(email: str) -> Optional[Dict[str, Any]]:
        return UserRepository.get_user_by_email(email)

    @staticmethod
    def list_users(limit: int = 25) -> List[Dict[str, Any]]:
        return UserRepository.list_users(limit)

    @staticmethod
    def delete_user(email: str) -> bool:
        return UserRepository.delete_user(email)