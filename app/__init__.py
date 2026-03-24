from flask import Flask
from config import Configuration


def creer_application():
    """Application Factory — crée et configure l'application Flask."""
    application = Flask(__name__)
    application.config.from_object(Configuration)

    # --- Enregistrement des blueprints ---
    from app.auth.routes import bp_auth
    from app.etudiants.routes import bp_etudiants
    from app.enseignants.routes import bp_enseignants
    from app.cours.routes import bp_cours
    from app.tableau_de_bord.routes import bp_tableau_de_bord

    application.register_blueprint(bp_auth,            url_prefix='/auth')
    application.register_blueprint(bp_etudiants,       url_prefix='/etudiants')
    application.register_blueprint(bp_enseignants,     url_prefix='/enseignants')
    application.register_blueprint(bp_cours,           url_prefix='/cours')
    application.register_blueprint(bp_tableau_de_bord)

    return application
