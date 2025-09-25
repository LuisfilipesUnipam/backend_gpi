from typing import List, Dict, Any, Optional
from app.repositories.person_repository import PersonRepository

class PersonService:
    @staticmethod
    def create_person(data: Dict[str, Any]) -> Dict[str, Any]:
        name = data.get("name")
        born = data.get("born")
        if not name or born is None:
            raise ValueError("Campos obrigatórios: name (str), born (int)")
        if not isinstance(born, int):
            raise ValueError("born deve ser inteiro")
        return PersonRepository.create_person(name, born)

    @staticmethod
    def get_person(name: str) -> Optional[Dict[str, Any]]:
        return PersonRepository.get_person_by_name(name)

    @staticmethod
    def list_people(limit: int = 25) -> List[Dict[str, Any]]:
        return PersonRepository.list_people(limit)

    @staticmethod
    def delete_person(name: str) -> bool:
        return PersonRepository.delete_person(name)