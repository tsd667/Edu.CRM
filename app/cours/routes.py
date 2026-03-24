from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.auth.routes import connexion_requise, admin_requis
from app.services import service_cours, service_enseignants, service_etudiants

bp_cours = Blueprint('cours', __name__)


@bp_cours.route('/')
@connexion_requise
def liste():
    identifiant_filtre = request.args.get('enseignant', '').strip()
    if identifiant_filtre:
        tous_les_cours = service_cours.filtrer_cours_par_enseignant(int(identifiant_filtre))
    else:
        tous_les_cours = service_cours.obtenir_tous_les_cours()
    tous_les_enseignants = service_enseignants.obtenir_tous_les_enseignants()
    return render_template('cours/liste.html',
                           cours=tous_les_cours,
                           enseignants=tous_les_enseignants,
                           filtre_enseignant=identifiant_filtre)


@bp_cours.route('/details/<int:identifiant>')
@connexion_requise
def details(identifiant):
    details_cours = service_cours.obtenir_details_cours(identifiant)
    if not details_cours:
        flash('Cours introuvable.', 'danger')
        return redirect(url_for('cours.liste'))
    return render_template('cours/details.html', cours=details_cours)


@bp_cours.route('/creer', methods=['GET', 'POST'])
@connexion_requise
@admin_requis
def creer():
    tous_les_enseignants = service_enseignants.obtenir_tous_les_enseignants()
    if request.method == 'POST':
        titre                    = request.form.get('titre', '').strip()
        identifiant_enseignant   = request.form.get('identifiant_enseignant', '').strip()
        if not titre or not identifiant_enseignant:
            flash('Le titre et l\'enseignant sont obligatoires.', 'danger')
        else:
            service_cours.ajouter_cours(titre, int(identifiant_enseignant))
            flash(f'Cours « {titre} » créé avec succès.', 'succes')
            return redirect(url_for('cours.liste'))
    return render_template('cours/formulaire.html',
                           mode='creer',
                           cours=None,
                           enseignants=tous_les_enseignants)


@bp_cours.route('/modifier/<int:identifiant>', methods=['GET', 'POST'])
@connexion_requise
@admin_requis
def modifier(identifiant):
    cours_actuel         = service_cours.obtenir_cours_par_id(identifiant)
    tous_les_enseignants = service_enseignants.obtenir_tous_les_enseignants()
    if not cours_actuel:
        flash('Cours introuvable.', 'danger')
        return redirect(url_for('cours.liste'))

    if request.method == 'POST':
        nouveau_titre              = request.form.get('titre', '').strip()
        nouvel_identifiant_ens     = request.form.get('identifiant_enseignant', '').strip()
        if not nouveau_titre or not nouvel_identifiant_ens:
            flash('Tous les champs sont obligatoires.', 'danger')
        else:
            service_cours.modifier_cours(identifiant, nouveau_titre, int(nouvel_identifiant_ens))
            flash(f'Cours « {nouveau_titre} » modifié avec succès.', 'succes')
            return redirect(url_for('cours.liste'))

    return render_template('cours/formulaire.html',
                           mode='modifier',
                           cours=cours_actuel,
                           enseignants=tous_les_enseignants)


@bp_cours.route('/supprimer/<int:identifiant>')
@connexion_requise
@admin_requis
def supprimer(identifiant):
    cours_actuel = service_cours.obtenir_cours_par_id(identifiant)
    if cours_actuel:
        service_cours.supprimer_cours(identifiant)
        flash(f'Cours « {cours_actuel["titre"]} » supprimé.', 'info')
    else:
        flash('Cours introuvable.', 'danger')
    return redirect(url_for('cours.liste'))


@bp_cours.route('/inscrire/<int:identifiant_cours>', methods=['GET', 'POST'])
@connexion_requise
@admin_requis
def inscrire(identifiant_cours):
    cours_actuel      = service_cours.obtenir_cours_par_id(identifiant_cours)
    tous_les_etudiants = service_etudiants.obtenir_tous_les_etudiants()
    if not cours_actuel:
        flash('Cours introuvable.', 'danger')
        return redirect(url_for('cours.liste'))

    if request.method == 'POST':
        identifiant_etudiant = request.form.get('identifiant_etudiant', '').strip()
        if not identifiant_etudiant:
            flash('Veuillez sélectionner un étudiant.', 'danger')
        else:
            resultat = service_cours.inscrire_etudiant_au_cours(
                identifiant_cours, int(identifiant_etudiant)
            )
            if resultat:
                flash('Étudiant inscrit au cours avec succès.', 'succes')
            else:
                flash('Erreur : cet étudiant est déjà inscrit à ce cours.', 'danger')
            return redirect(url_for('cours.details', identifiant=identifiant_cours))

    return render_template('cours/inscrire.html',
                           cours=cours_actuel,
                           etudiants=tous_les_etudiants)
