# ─────────────────────────────────────────────────────────────
#  Service Cours — toute la logique métier ici
#  Collabore avec service_etudiants et service_enseignants
#  Stockage en mémoire (listes Python, pas de base de données)
# ─────────────────────────────────────────────────────────────

from app.services import service_etudiants, service_enseignants

liste_cours = []
_prochain_id = 1


def ajouter_cours(titre, identifiant_enseignant):
    """Crée un nouveau cours avec un enseignant responsable."""
    global _prochain_id
    nouveau_cours = {
        'id':                    _prochain_id,
        'titre':                 titre,
        'identifiant_enseignant': identifiant_enseignant,
        'identifiants_etudiants': []
    }
    liste_cours.append(nouveau_cours)
    _prochain_id += 1
    return nouveau_cours


def inscrire_etudiant_au_cours(identifiant_cours, identifiant_etudiant):
    """Inscrit un étudiant à un cours. Retourne False si déjà inscrit."""
    for cours in liste_cours:
        if cours['id'] == identifiant_cours:
            if identifiant_etudiant in cours['identifiants_etudiants']:
                return False  # déjà inscrit
            cours['identifiants_etudiants'].append(identifiant_etudiant)
            return True
    return False


def supprimer_cours(identifiant):
    """Supprime le cours correspondant à l'identifiant donné."""
    global liste_cours
    liste_cours = [c for c in liste_cours if c['id'] != identifiant]


def modifier_cours(identifiant, nouveau_titre, nouvel_identifiant_enseignant):
    """Modifie le titre et l'enseignant d'un cours existant."""
    for cours in liste_cours:
        if cours['id'] == identifiant:
            cours['titre']                  = nouveau_titre
            cours['identifiant_enseignant'] = nouvel_identifiant_enseignant
            return cours
    return None


def obtenir_tous_les_cours():
    """Retourne tous les cours enrichis avec les données liées."""
    resultat = []
    for cours in liste_cours:
        enseignant = service_enseignants.obtenir_enseignant_par_id(
            cours['identifiant_enseignant']
        )
        etudiants_inscrits = [
            service_etudiants.obtenir_etudiant_par_id(eid)
            for eid in cours['identifiants_etudiants']
        ]
        etudiants_inscrits = [e for e in etudiants_inscrits if e is not None]
        resultat.append({
            **cours,
            'nom_enseignant':    enseignant['nom'] if enseignant else 'Inconnu',
            'etudiants_inscrits': etudiants_inscrits
        })
    return resultat


def obtenir_cours_par_id(identifiant):
    """Retourne un cours brut par son identifiant, ou None."""
    for cours in liste_cours:
        if cours['id'] == identifiant:
            return cours
    return None


def obtenir_details_cours(identifiant):
    """Retourne un cours enrichi avec enseignant et étudiants."""
    cours = obtenir_cours_par_id(identifiant)
    if not cours:
        return None
    enseignant = service_enseignants.obtenir_enseignant_par_id(
        cours['identifiant_enseignant']
    )
    etudiants_inscrits = [
        service_etudiants.obtenir_etudiant_par_id(eid)
        for eid in cours['identifiants_etudiants']
    ]
    etudiants_inscrits = [e for e in etudiants_inscrits if e is not None]
    return {
        **cours,
        'enseignant':            enseignant,
        'etudiants_inscrits':    etudiants_inscrits,
        'nombre_inscrits':       len(etudiants_inscrits)
    }


def cours_le_plus_populaire():
    """Retourne le cours avec le plus d'étudiants inscrits."""
    if not liste_cours:
        return None
    return max(liste_cours, key=lambda c: len(c['identifiants_etudiants']))


def filtrer_cours_par_enseignant(identifiant_enseignant):
    """Retourne les cours enrichis d'un enseignant donné."""
    return [c for c in obtenir_tous_les_cours()
            if c['identifiant_enseignant'] == identifiant_enseignant]
