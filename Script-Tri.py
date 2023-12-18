import os
import shutil
import click


@click.command()
@click.argument('source', type=click.Path(), metavar='<dossier_source>')
@click.argument('destination', type=click.Path(), metavar='<dossier_destination>')
@click.option('--afficher-contenu', is_flag=True, help='Afficher le contenu du dossier source avant le tri.')
@click.option('--tri-par-extension', is_flag=True, help='Trier les fichiers par extension dans des sous-dossiers.')
@click.option('--renommer-fichiers', is_flag=True, help='Renommer les fichiers avec un nombre devant (nombre croissant)')
@click.option('--supprimer-fichiers', is_flag=True, help='Supprimer les fichiers du dossier source après le tri.')
@click.option('--tri-regroupement', is_flag=True, help='Regroupe les fichiers en fonction de leurs extension')
def trier_fichiers(source, destination, afficher_contenu, tri_par_extension, renommer_fichiers, supprimer_fichiers, tri_regroupement):
    """
    Script pour trier les fichiers d'un dossier source vers un dossier destination.

    PRE : - \n
    POST : Va transporter les fichiers d'une source à une destination en fonction des autres paramètres renseignés\n
    RAISES : FileNotFoundError si le fichier source n'existe pas
    """

    if not os.path.exists(source):
        raise click.ClickException(f"Le fichier source : {source} ,n'existe pas")

    if afficher_contenu:
        click.echo(f"Contenu du dossier source ({source}):")
        for fichier in os.listdir(source):
            click.echo(f"- {fichier}")
    elif tri_par_extension:
        trier_par_extension(source, destination)
    elif renommer_fichiers:
        renommer_avec_prefixe_numerique(source)
    elif supprimer_fichiers:
        supprimer_fichiers_source(source)
    elif tri_regroupement:
        trier_regroupement(source, destination)
    else:
        click.ClickException("la commande renseignée n'existe pas")


def trier_par_extension(source, destination):
    for fichier in os.listdir(source):  # Va passer sur chaque fichier1
        chemin_source = os.path.join(source, fichier)  # Chemin absolu du fichier1 source
        if os.path.isfile(chemin_source):   # Vérifie si c'est un fichier1
            nom_fichier, extension = os.path.splitext(fichier)  # Divise le nom et l'extension du fichier1 source
            if extension != "":  # Si pas d'extension alors pas de tri effectué et reste dans le fichier1 source
                dossier_destination = os.path.join(destination, extension[1:])  # Va creer le repértoire de destination si il n'existe pas et dans un fichier1 au nom de l'extension ([1:] pour pas prendre le .)
                os.makedirs(dossier_destination, exist_ok=True)  # Permet de ne pas écraser si un fichier1 du même nom existe déja dans le répertoire distanation si la valuer du exist_ok est false alors voici l'erreur qui s'affiche en cas de doublon : FileExistsError: [WinError 183] Impossible de créer un fichier1 déjà existant: 'fichier2\\jpg'
                shutil.move(os.path.join(source, fichier), os.path.join(dossier_destination, fichier))
    click.echo("Fichiers triés par extension.")


def renommer_avec_prefixe_numerique(source):

    i = 1
    for fichier in os.listdir(source):
        if os.path.isfile(os.path.join(source, fichier)):
            nouveau_nom = f"{i}_{fichier}"
            os.rename(os.path.join(source, fichier), os.path.join(source, nouveau_nom))
            i += 1
    click.echo("Fichiers renommés avec préfixe numérique.")


def supprimer_fichiers_source(source):
    for fichier in os.listdir(source):
        chemin_fichier = os.path.join(source, fichier)
        if os.path.isfile(chemin_fichier):
            os.remove(chemin_fichier)
    click.echo("Fichiers supprimés du dossier source.")


def trier_regroupement(source,destination):
    if not os.path.exists(destination):
        os.makedirs(destination)

    for fichier in os.listdir(source):
        chemin_fichier = os.path.join(source, fichier)

        if os.path.isfile(chemin_fichier):
            # Obtenir l'extension du fichier1
            _, extension = os.path.splitext(fichier)
            extension = extension.lower()

            # Dossiers de destination pour différents types de fichiers
            dossier_images = os.path.join(destination, 'Images')
            dossier_documents = os.path.join(destination, 'Documents')
            dossier_autres = os.path.join(destination, 'Autres')

            # Créer les dossiers de destination s'ils n'existent pas
            for d in [dossier_images, dossier_documents, dossier_autres]:
                if not os.path.exists(d):
                    os.makedirs(d)

            # Déplacer les fichiers vers les dossiers correspondants
            if extension in ['.jpg', '.png', '.gif']:
                shutil.move(chemin_fichier, os.path.join(dossier_images, fichier))
            elif extension in ['.txt', '.pdf', '.doc']:
                shutil.move(chemin_fichier, os.path.join(dossier_documents, fichier))
            else:
                shutil.move(chemin_fichier, os.path.join(dossier_autres, fichier))

    print("Triage des fichiers terminé.")


if __name__ == '__main__':
    trier_fichiers()