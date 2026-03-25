from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps

bp_auth = Blueprint('auth', __name__)

# ─── Utilisateurs fictifs avec rôles (pas de base de données) ────────────────
UTILISATEURS = {
    'admin':    {'mot_de_passe': 'admin123',  'role': 'admin'},
    'etudiant': {'mot_de_passe': 'etudiant123', 'role': 'utilisateur'},
}


# ─── Décorateur : connexion obligatoire ──────────────────────────────────────
def connexion_requise(fonction):
    """Protège une route : redirige vers /auth/connexion si non connecté."""
    @wraps(fonction)
    def fonction_decoree(*args, **kwargs):
        if 'utilisateur' not in session:
            flash('Vous devez être connecté pour accéder à cette page.', 'attention')
            return redirect(url_for('auth.connexion'))
        return fonction(*args, **kwargs)
    return fonction_decoree


# ─── Décorateur : rôle admin obligatoire ─────────────────────────────────────
def admin_requis(fonction):
    """Protège une route : réservée aux administrateurs uniquement."""
    @wraps(fonction)
    def fonction_decoree(*args, **kwargs):
        if session.get('role') != 'admin':
            flash('Accès refusé — droits administrateur requis.', 'danger')
            return redirect(url_for('tableau_de_bord.index'))
        return fonction(*args, **kwargs)
    return fonction_decoree


# ─── Route : connexion ────────────────────────────────────────────────────────
@bp_auth.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if 'utilisateur' in session:
        return redirect(url_for('tableau_de_bord.index'))

    if request.method == 'POST':
        nom_utilisateur = request.form.get('nom_utilisateur', '').strip()
        mot_de_passe    = request.form.get('mot_de_passe', '').strip()

        utilisateur = UTILISATEURS.get(nom_utilisateur)
        if utilisateur and utilisateur['mot_de_passe'] == mot_de_passe:
            session['utilisateur'] = nom_utilisateur
            session['role']        = utilisateur['role']
            flash(f'Bienvenue, {nom_utilisateur} ! 👋', 'succes')
            return redirect(url_for('tableau_de_bord.index'))
        else:
            flash('Identifiants incorrects. Veuillez réessayer.', 'danger')

    return render_template('auth/connexion.html')


# ─── Route : déconnexion ──────────────────────────────────────────────────────
@bp_auth.route('/deconnexion')
def deconnexion():
    session.clear()
    flash('Vous avez été déconnecté avec succès.', 'info')
    return redirect(url_for('auth.connexion'))
