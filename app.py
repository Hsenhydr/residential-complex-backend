from flask import Flask, jsonify
from extensions import db
from routes.admin import admins_bp
from dotenv import load_dotenv
from routes.residential_complex import complexes_bp
load_dotenv()
from routes.auth import auth_bp
from routes.building import buildings_bp
from models.admin import Admin
from models.building import Building
from models.residential_complex import ResidentialComplex
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)

    app.config.from_object("config.Config")
    
    CORS(app, resources={r"/*": {"origins": "*"}})
      
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    

    app.register_blueprint(auth_bp)
    app.register_blueprint(admins_bp)
    app.register_blueprint(complexes_bp)
    app.register_blueprint(buildings_bp)
    

    @app.route("/health")
    def health():
        return jsonify({"msg": "Flask backend running"}), 200
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
