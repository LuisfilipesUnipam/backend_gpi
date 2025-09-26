from typing import List, Dict, Any, Optional
from app.config.neo4j_client import run_read, run_write

class CompanyRepository:
    @staticmethod
    def create_company(data: Dict[str, Any]) -> Dict[str, Any]:
        query = """
        MERGE (c:Company {cnpj: $cnpj})
        ON CREATE SET 
            c.name = $name,
            c.type = $type,
            c.address = $address,
            c.created_at = datetime()
        ON MATCH SET 
            c.name = $name,
            c.type = $type,
            c.address = $address
        WITH c
        MATCH (u:User {email: $owner_email})
        MERGE (u)-[:OWNS]->(c)
        RETURN c {
            .cnpj,
            .name,
            .type,
            .address,
            created_at: toString(c.created_at)
        } AS company
        """
        result = run_write(query, data)
        record = result[0] if result else None
        return record["company"] if record else {}

    @staticmethod
    def get_company_by_cnpj(cnpj: str) -> Optional[Dict[str, Any]]:
        query = """
        MATCH (c:Company {cnpj: $cnpj})
        RETURN c {
            .cnpj,
            .name,
            .type,
            .address,
            created_at: toString(c.created_at)
        } AS company
        """
        result = run_read(query, {"cnpj": cnpj})
        return result[0]["company"] if result else None

    @staticmethod
    def list_companies(limit: int = 25) -> List[Dict[str, Any]]:
        query = """
        MATCH (c:Company)
        RETURN c {
            .cnpj,
            .name,
            .type,
            .address,
            created_at: toString(c.created_at)
        } AS company
        ORDER BY c.name
        LIMIT $limit
        """
        result = run_read(query, {"limit": limit})
        return [rec["company"] for rec in result]

    @staticmethod
    def delete_company(cnpj: str) -> bool:
        query = """
        MATCH (c:Company {cnpj: $cnpj})
        DETACH DELETE c
        RETURN count(*) AS deleted
        """
        result = run_write(query, {"cnpj": cnpj})
        return result[0]["deleted"] > 0