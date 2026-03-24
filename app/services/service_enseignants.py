# ─────────────────────────────────────────────────────────────
#  Service Enseignants — toute la logique métier ici
#  Stockage en mémoire (listes Python, pas de base de données)
# ─────────────────────────────────────────────────────────────

liste_enseignants = []
_prochain_id = 1


def ajouter_enseignant(nom, email, specialite):
    """Crée un nouvel enseignant et l'ajoute en mémoire."""
    global _prochain_id
    nouvel_enseignant = {
        'id':        _prochain_id,
        'nom':       nom,
        'email':     email,
        'specialite': specialite
    }
    liste_enseignants.append(nouvel_enseignant)
    _prochain_id += 1
    return nouvel_enseignant


def supprimer_enseignant(identifiant):
    """Supprime l'enseignant correspondant à l'identifiant donné."""
    global liste_enseignants
    liste_enseignants = [e for e in liste_enseignants if e['id'] != identifiant]


def modifier_enseignant(identifiant, nouveau_nom, nouvel_email, nouvelle_specialite):
    """Modifie les informations d'un enseignant existant."""
    for enseignant in liste_enseignants:
        if enseignant['id'] == identifiant:
            enseignant['nom']        = nouveau_nom
            enseignant['email']      = nouvel_email
            enseignant['specialite'] = nouvelle_specialite
            return enseignant
    return None


def obtenir_tous_les_enseignants():
    """Retourne la liste complète des enseignants."""
    return liste_enseignants


def obtenir_enseignant_par_id(identifiant):
    """Retourne un enseignant par son identifiant, ou None."""
    for enseignant in liste_enseignants:
        if enseignant['id'] == identifiant:
            return enseignant
    return None


def rechercher_enseignants(mot_cle):
    """Filtre les enseignants dont le nom contient le mot-clé."""
    return [e for e in liste_enseignants if mot_cle.lower() in e['nom'].lower()]
