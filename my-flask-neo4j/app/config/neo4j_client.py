from neo4j import GraphDatabase, basic_auth
from .settings import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

class Neo4jClient:
    _driver = None

    @classmethod
    def get_driver(cls):
        if cls._driver is None:
            cls._driver = GraphDatabase.driver(
                NEO4J_URI,
                auth=basic_auth(NEO4J_USER, NEO4J_PASSWORD)
            )
        return cls._driver

    @classmethod
    def close(cls):
        if cls._driver is not None:
            cls._driver.close()
            cls._driver = None

def run_read(query: str, params: dict | None = None):
    driver = Neo4jClient.get_driver()
    with driver.session() as session:
        return session.read_transaction(lambda tx: list(tx.run(query, params or {})))

def run_write(query: str, params: dict | None = None):
    driver = Neo4jClient.get_driver()
    with driver.session() as session:
        return session.write_transaction(lambda tx: list(tx.run(query, params or {})))