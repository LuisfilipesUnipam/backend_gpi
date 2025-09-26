from typing import List, Dict, Any, Optional
from app.config.neo4j_client import run_read, run_write
from datetime import datetime

class ConnectionRepository:
    @staticmethod
    def request_connection(reseller_email: str, producer_email: str) -> Dict[str, Any]:
        query = """
        MATCH (reseller:User {email: $reseller_email})
        MATCH (producer:User {email: $producer_email})
        WHERE 'reseller' IN reseller.roles AND 'producer' IN producer.roles
        AND NOT EXISTS((reseller)-[:CONNECTED|PENDING_CONNECTION]->(producer))
        CREATE (reseller)-[r:PENDING_CONNECTION {
            requested_at: datetime(),
            status: 'pending'
        }]->(producer)
        RETURN {
            reseller: reseller.email,
            producer: producer.email,
            status: r.status,
            requested_at: toString(r.requested_at)
        } AS connection
        """
        result = run_write(query, {
            "reseller_email": reseller_email,
            "producer_email": producer_email
        })
        if not result:
            return {}
        return result[0]["connection"]

    @staticmethod
    def accept_connection(producer_email: str, reseller_email: str) -> Dict[str, Any]:
        query = """
        MATCH (reseller:User {email: $reseller_email})-[r:PENDING_CONNECTION]->(producer:User {email: $producer_email})
        DELETE r
        CREATE (reseller)-[new_r:CONNECTED {
            connected_at: datetime(),
            status: 'active'
        }]->(producer)
        RETURN {
            reseller: reseller.email,
            producer: producer.email,
            status: new_r.status,
            connected_at: toString(new_r.connected_at)
        } AS connection
        """
        result = run_write(query, {
            "producer_email": producer_email,
            "reseller_email": reseller_email
        })
        if not result:
            return {}
        return result[0]["connection"]

    @staticmethod
    def reject_connection(producer_email: str, reseller_email: str) -> bool:
        query = """
        MATCH (reseller:User {email: $reseller_email})-[r:PENDING_CONNECTION]->(producer:User {email: $producer_email})
        DELETE r
        RETURN count(*) as deleted
        """
        result = run_write(query, {
            "producer_email": producer_email,
            "reseller_email": reseller_email
        })
        return result[0]["deleted"] > 0

    @staticmethod
    def list_pending_connections(user_email: str) -> List[Dict[str, Any]]:
        query = """
        MATCH (reseller:User)-[r:PENDING_CONNECTION]->(producer:User {email: $user_email})
        RETURN {
            reseller: reseller { .email, .name },
            requested_at: toString(r.requested_at),
            status: r.status
        } AS connection
        """
        result = run_read(query, {"user_email": user_email})
        return [rec["connection"] for rec in result]

    @staticmethod
    def list_active_connections(user_email: str) -> List[Dict[str, Any]]:
        query = """
        MATCH (user:User {email: $user_email})
        OPTIONAL MATCH (user)-[r1:CONNECTED]->(producer:User)
        OPTIONAL MATCH (reseller:User)-[r2:CONNECTED]->(user)
        RETURN {
            as_reseller: COLLECT(DISTINCT {
                producer: producer { .email, .name },
                connected_at: toString(r1.connected_at)
            }),
            as_producer: COLLECT(DISTINCT {
                reseller: reseller { .email, .name },
                connected_at: toString(r2.connected_at)
            })
        } AS connections
        """
        result = run_read(query, {"user_email": user_email})
        return result[0]["connections"] if result else {"as_reseller": [], "as_producer": []}