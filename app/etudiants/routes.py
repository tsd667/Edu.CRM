from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.auth.routes import connexion_requise, admin_requis
from app.services import service_etudiants

bp_etudiants = Blueprint('etudiants', __name__)


@bp_etudiants.route('/')
@connexion_requise
def liste():
    mot_cle = request.args.get('recherche', '').strip()
    if mot_cle:
        tous_les_etudiants = service_etudiants.rechercher_etudiants(mot_cle)
    else:
        tous_les_etudiants = service_etudiants.obtenir_tous_les_etudiants()
    return render_template('etudiants/liste.html',
                           etudiants=tous_les_etudiants,
                           mot_cle=mot_cle)


@bp_etudiants.route('/creer', methods=['GET', 'POST'])
@connexion_requise
@admin_requis
def creer():
    if request.method == 'POST':
        nom   = request.form.get('nom', '').strip()
        email = request.form.get('email', '').strip()
        if not nom or not email:
            flash('Le nom et l\'email sont obligatoires.', 'danger')
        else:
            service_etudiants.ajouter_etudiant(nom, email)
            flash(f'Étudiant « {nom} » ajouté avec succès.', 'succes')
            return redirect(url_for('etudiants.liste'))
    return render_template('etudiants/formulaire.html', mode='creer', etudiant=None)


@bp_etudiants.route('/modifier/<int:identifiant>', methods=['GET', 'POST'])
@connexion_requise
@admin_requis
def modifier(identifiant):
    etudiant = service_etudiants.obtenir_etudiant_par_id(identifiant)
    if not etudiant:
        flash('Étudiant introuvable.', 'danger')
        return redirect(url_for('etudiants.liste'))

    if request.method == 'POST':
        nouveau_nom   = request.form.get('nom', '').strip()
        nouvel_email  = request.form.get('email', '').strip()
        if not nouveau_nom or not nouvel_email:
            flash('Le nom et l\'email sont obligatoires.', 'danger')
        else:
            service_etudiants.modifier_etudiant(identifiant, nouveau_nom, nouvel_email)
            flash(f'Étudiant « {nouveau_nom} » modifié avec succès.', 'succes')
            return redirect(url_for('etudiants.liste'))

    return render_template('etudiants/formulaire.html', mode='modifier', etudiant=etudiant)


@bp_etudiants.route('/supprimer/<int:identifiant>')
@connexion_requise
@admin_requis
def supprimer(identifiant):
    etudiant = service_etudiants.obtenir_etudiant_par_id(identifiant)
    if etudiant:
        service_etudiants.supprimer_etudiant(identifiant)
        flash(f'Étudiant « {etudiant["nom"]} » supprimé.', 'info')
    else:
        flash('Étudiant introuvable.', 'danger')
    return redirect(url_for('etudiants.liste'))
