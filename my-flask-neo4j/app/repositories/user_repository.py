from typing import List, Dict, Any, Optional
from app.config.neo4j_client import run_read, run_write
from werkzeug.security import generate_password_hash
from datetime import datetime

class UserRepository:
    @staticmethod
    def create_user(data: Dict[str, Any]) -> Dict[str, Any]:
        # Gerar hash da senha
        password_hash = generate_password_hash(data['password'])
        
        query = """
        MERGE (u:User {email: $email})
        ON CREATE SET 
            u.name = $name,
            u.phone = $phone,
            u.password_hash = $password_hash,
            u.created_at = datetime(),
            u.roles = $roles
        ON MATCH SET 
            u.name = $name,
            u.phone = $phone,
            u.password_hash = $password_hash,
            u.roles = $roles
        RETURN u {
            .email,
            .name,
            .phone,
            .roles,
            created_at: toString(u.created_at)
        } AS user
        """
        params = {
            "email": data["email"],
            "name": data["name"],
            "phone": data["phone"],
            "password_hash": password_hash,
            "roles": data["roles"]
        }
        
        result = run_write(query, params)
        record = result[0] if result else None
        return record["user"] if record else {}

    @staticmethod
    def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        query = """
        MATCH (u:User {email: $email})
        RETURN u {
            .email,
            .name,
            .phone,
            .roles,
            created_at: toString(u.created_at)
        } AS user
        """
        result = run_read(query, {"email": email})
        return result[0]["user"] if result else None

    @staticmethod
    def list_users(limit: int = 25) -> List[Dict[str, Any]]:
        query = """
        MATCH (u:User)
        RETURN u {
            .email,
            .name,
            .phone,
            .roles,
            created_at: toString(u.created_at)
        } AS user
        ORDER BY u.name
        LIMIT $limit
        """
        result = run_read(query, {"limit": limit})
        return [rec["user"] for rec in result]

    @staticmethod
    def delete_user(email: str) -> bool:
        query = """
        MATCH (u:User {email: $email})
        DETACH DELETE u
        RETURN count(*) AS deleted
        """
        result = run_write(query, {"email": email})
        return result[0]["deleted"] > 0