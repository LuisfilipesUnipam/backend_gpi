from typing import List, Dict, Any, Optional
from app.config.neo4j_client import run_read, run_write

class PersonRepository:
    @staticmethod
    def create_person(name: str, born: int) -> Dict[str, Any]:
        query = """
        MERGE (p:Person {name: $name})
        ON CREATE SET p.born = $born
        ON MATCH SET p.born = coalesce(p.born, $born)
        RETURN p { .name, .born } AS person
        """
        result = run_write(query, {"name": name, "born": born})
        record = result[0] if result else None
        return record["person"] if record else {}

    @staticmethod
    def get_person_by_name(name: str) -> Optional[Dict[str, Any]]:
        query = """
        MATCH (p:Person {name: $name})
        RETURN p { .name, .born } AS person
        """
        result = run_read(query, {"name": name})
        if not result:
            return None
        return result[0]["person"]

    @staticmethod
    def list_people(limit: int = 25) -> List[Dict[str, Any]]:
        query = """
        MATCH (p:Person)
        RETURN p { .name, .born } AS person
        ORDER BY p.name
        LIMIT $limit
        """
        result = run_read(query, {"limit": limit})
        return [rec["person"] for rec in result]

    @staticmethod
    def delete_person(name: str) -> bool:
        query = """
        MATCH (p:Person {name: $name})
        DETACH DELETE p
        RETURN count(*) AS deleted
        """
        result = run_write(query, {"name": name})
        count = result[0]["deleted"] if result else 0
        return count > 0