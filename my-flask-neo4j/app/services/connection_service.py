from typing import List, Dict, Any, Optional
from app.repositories.connection_repository import ConnectionRepository
from app.repositories.user_repository import UserRepository

class ConnectionService:
    @staticmethod
    def request_connection(reseller_email: str, producer_email: str) -> Dict[str, Any]:
        # Verificar se os usuários existem
        reseller = UserRepository.get_user_by_email(reseller_email)
        producer = UserRepository.get_user_by_email(producer_email)
        
        if not reseller or not producer:
            raise ValueError("Usuário não encontrado")
        
        if "reseller" not in reseller["roles"]:
            raise ValueError("Usuário solicitante deve ser um reseller")
            
        if "producer" not in producer["roles"]:
            raise ValueError("Usuário alvo deve ser um producer")
            
        if reseller_email == producer_email:
            raise ValueError("Não é possível conectar-se consigo mesmo")
            
        connection = ConnectionRepository.request_connection(reseller_email, producer_email)
        if not connection:
            raise ValueError("Conexão já existe ou não pode ser criada")
            
        return connection

    @staticmethod
    def accept_connection(producer_email: str, reseller_email: str) -> Dict[str, Any]:
        connection = ConnectionRepository.accept_connection(producer_email, reseller_email)
        if not connection:
            raise ValueError("Solicitação de conexão não encontrada")
        return connection

    @staticmethod
    def reject_connection(producer_email: str, reseller_email: str) -> bool:
        return ConnectionRepository.reject_connection(producer_email, reseller_email)

    @staticmethod
    def list_pending_connections(user_email: str) -> List[Dict[str, Any]]:
        return ConnectionRepository.list_pending_connections(user_email)

    @staticmethod
    def list_active_connections(user_email: str) -> List[Dict[str, Any]]:
        return ConnectionRepository.list_active_connections(user_email)