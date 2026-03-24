# ─────────────────────────────────────────────────────────────
#  Service Étudiants — toute la logique métier ici
#  Stockage en mémoire (listes Python, pas de base de données)
# ─────────────────────────────────────────────────────────────

liste_etudiants = []
_prochain_id = 1


def ajouter_etudiant(nom, email):
    """Crée un nouvel étudiant et l'ajoute en mémoire."""
    global _prochain_id
    nouvel_etudiant = {
        'id':    _prochain_id,
        'nom':   nom,
        'email': email
    }
    liste_etudiants.append(nouvel_etudiant)
    _prochain_id += 1
    return nouvel_etudiant


def supprimer_etudiant(identifiant):
    """Supprime l'étudiant correspondant à l'identifiant donné."""
    global liste_etudiants
    liste_etudiants = [e for e in liste_etudiants if e['id'] != identifiant]


def modifier_etudiant(identifiant, nouveau_nom, nouvel_email):
    """Modifie les informations d'un étudiant existant."""
    for etudiant in liste_etudiants:
        if etudiant['id'] == identifiant:
            etudiant['nom']   = nouveau_nom
            etudiant['email'] = nouvel_email
            return etudiant
    return None


def obtenir_tous_les_etudiants():
    """Retourne la liste complète des étudiants."""
    return liste_etudiants


def obtenir_etudiant_par_id(identifiant):
    """Retourne un étudiant par son identifiant, ou None."""
    for etudiant in liste_etudiants:
        if etudiant['id'] == identifiant:
            return etudiant
    return None


def rechercher_etudiants(mot_cle):
    """Filtre les étudiants dont le nom contient le mot-clé."""
    return [e for e in liste_etudiants if mot_cle.lower() in e['nom'].lower()]
