from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.auth.routes import connexion_requise, admin_requis
from app.services import service_enseignants

bp_enseignants = Blueprint('enseignants', __name__)


@bp_enseignants.route('/')
@connexion_requise
def liste():
    mot_cle = request.args.get('recherche', '').strip()
    if mot_cle:
        tous_les_enseignants = service_enseignants.rechercher_enseignants(mot_cle)
    else:
        tous_les_enseignants = service_enseignants.obtenir_tous_les_enseignants()
    return render_template('enseignants/liste.html',
                           enseignants=tous_les_enseignants,
                           mot_cle=mot_cle)


@bp_enseignants.route('/creer', methods=['GET', 'POST'])
@connexion_requise
@admin_requis
def creer():
    if request.method == 'POST':
        nom       = request.form.get('nom', '').strip()
        email     = request.form.get('email', '').strip()
        specialite = request.form.get('specialite', '').strip()
        if not nom or not email or not specialite:
            flash('Tous les champs sont obligatoires.', 'danger')
        else:
            service_enseignants.ajouter_enseignant(nom, email, specialite)
            flash(f'Enseignant « {nom} » ajouté avec succès.', 'succes')
            return redirect(url_for('enseignants.liste'))
    return render_template('enseignants/formulaire.html', mode='creer', enseignant=None)


@bp_enseignants.route('/modifier/<int:identifiant>', methods=['GET', 'POST'])
@connexion_requise
@admin_requis
def modifier(identifiant):
    enseignant = service_enseignants.obtenir_enseignant_par_id(identifiant)
    if not enseignant:
        flash('Enseignant introuvable.', 'danger')
        return redirect(url_for('enseignants.liste'))

    if request.method == 'POST':
        nouveau_nom        = request.form.get('nom', '').strip()
        nouvel_email       = request.form.get('email', '').strip()
        nouvelle_specialite = request.form.get('specialite', '').strip()
        if not nouveau_nom or not nouvel_email or not nouvelle_specialite:
            flash('Tous les champs sont obligatoires.', 'danger')
        else:
            service_enseignants.modifier_enseignant(
                identifiant, nouveau_nom, nouvel_email, nouvelle_specialite
            )
            flash(f'Enseignant « {nouveau_nom} » modifié avec succès.', 'succes')
            return redirect(url_for('enseignants.liste'))

    return render_template('enseignants/formulaire.html',
                           mode='modifier', enseignant=enseignant)


@bp_enseignants.route('/supprimer/<int:identifiant>')
@connexion_requise
@admin_requis
def supprimer(identifiant):
    enseignant = service_enseignants.obtenir_enseignant_par_id(identifiant)
    if enseignant:
        service_enseignants.supprimer_enseignant(identifiant)
        flash(f'Enseignant « {enseignant["nom"]} » supprimé.', 'info')
    else:
        flash('Enseignant introuvable.', 'danger')
    return redirect(url_for('enseignants.liste'))
