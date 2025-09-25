from flask import Flask, jsonify
from app.routes.person_routes import person_bp
from app.config.neo4j_client import Neo4jClient
from app.config import settings

def create_app() -> Flask:
    app = Flask(__name__)

    # Blueprints
    app.register_blueprint(person_bp)

    # Healthcheck
    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    # Fechar driver ao encerrar
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        Neo4jClient.close()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host=settings.HOST, port=settings.PORT, debug=(settings.FLASK_ENV == "development"))