from flask import Blueprint, render_template
from app.auth.routes import connexion_requise
from app.services import service_etudiants, service_enseignants, service_cours

bp_tableau_de_bord = Blueprint('tableau_de_bord', __name__)


@bp_tableau_de_bord.route('/')
@connexion_requise
def index():
    tous_les_cours       = service_cours.obtenir_tous_les_cours()
    tous_les_etudiants   = service_etudiants.obtenir_tous_les_etudiants()
    tous_les_enseignants = service_enseignants.obtenir_tous_les_enseignants()

    # ── Statistiques avancées ──────────────────────────────────────────────
    statistiques = {
        'nombre_etudiants':   len(tous_les_etudiants),
        'nombre_enseignants': len(tous_les_enseignants),
        'nombre_cours':       len(tous_les_cours),
    }

    # Cours le plus populaire
    cours_populaire_brut = service_cours.cours_le_plus_populaire()
    cours_populaire = None
    if cours_populaire_brut:
        cours_populaire = service_cours.obtenir_details_cours(cours_populaire_brut['id'])

    # Enseignant avec le plus de cours
    enseignant_actif = None
    if tous_les_enseignants and tous_les_cours:
        compteur = {}
        for cours in tous_les_cours:
            eid = cours['identifiant_enseignant']
            compteur[eid] = compteur.get(eid, 0) + 1
        if compteur:
            id_enseignant_actif = max(compteur, key=compteur.get)
            enseignant_actif = service_enseignants.obtenir_enseignant_par_id(id_enseignant_actif)
            if enseignant_actif:
                enseignant_actif = {
                    **enseignant_actif,
                    'nombre_cours': compteur[id_enseignant_actif]
                }

    # Nombre d'étudiants par cours (pour le graphique)
    donnees_graphique = [
        {
            'titre':          c['titre'],
            'nombre_inscrits': len(c['identifiants_etudiants'])
        }
        for c in service_cours.obtenir_tous_les_cours()
    ]

    return render_template(
        'tableau_de_bord/index.html',
        statistiques=statistiques,
        cours_populaire=cours_populaire,
        enseignant_actif=enseignant_actif,
        donnees_graphique=donnees_graphique
    )
