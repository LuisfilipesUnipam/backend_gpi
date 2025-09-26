from flask import Flask, jsonify
from app.routes.user_routes import user_bp
from app.routes.company_routes import company_bp
from app.config.neo4j_client import Neo4jClient
from app.config import settings
from app.utils.json_encoder import CustomJSONProvider
from app.routes.connection_routes import connection_bp

def create_app() -> Flask:
    app = Flask(__name__)
    
    # Configure custom JSON encoder
    app.json = CustomJSONProvider(app)

    # Blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(connection_bp)

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