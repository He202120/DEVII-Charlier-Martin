import os
import shutil
import click
#cc c'est martin

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

    PRE : -

    POST : Va transporter les fichiers d'une source à une destination en fonction des autres paramètres renseignés

    RAISES : FileNotFoundError si le fichier source n'existe pas
    """

    if not os.path.exists(source):
        raise click.ClickException(f"Le dossier source : {source} ,n'existe pas")

    if afficher_contenu:
        click.echo(f"Contenu du dossier source ({source}):")
        for fichier in os.listdir(source):
            click.echo(f"- {fichier}")
    elif tri_par_extension:
        trier_par_extension(source, destination)
    elif renommer_fichiers:
        renommer_avec_numéro_Croiss(source)
    elif supprimer_fichiers:
        supprimer_fichiers_source(source)
    elif tri_regroupement:
        trier_regroupement(source, destination)
    else:
        click.ClickException("la commande renseignée n'existe pas")


def trier_par_extension(source, destination):
    """
    Fonction pour trier des fichiers dans des dossiers portant le nom de leurs extensions

    PRE : -
    POST : Va transporter les fichiers du dossier source dans des dossiers portant le nom des extensions des fichiers
    source se trouvant dans le dossier destination et va demander si l'utilisateur souhaite écraser les fichiers déjà
    existant dans le fichier destination et va créer le fichier destination s'il n'existe pas.
    RAISES : FileNotFoundError si le fichier source n'existe pas
    """
    for fichier in os.listdir(source):
        chemin_source = os.path.join(source, fichier)
        if os.path.isfile(chemin_source):
            nom_fichier, extension = os.path.splitext(fichier)
            if extension != "":
                dossier_destination = os.path.join(destination, extension[1:])
                os.makedirs(dossier_destination, exist_ok=True)

                chemin_destination = os.path.join(dossier_destination, fichier)

                if os.path.exists(chemin_destination):
                    confirmer = click.confirm(
                        f"Le fichier '{fichier}' existe déjà dans le dossier destination. Voulez-vous l'écraser?")
                    if not confirmer:
                        click.echo(f"Le fichier '{fichier}' n'a pas été trié.")
                        continue

                shutil.move(chemin_source, chemin_destination)
    click.echo("Fichiers triés par extension.")


def renommer_avec_numéro_Croiss(source):
    """
    Fonction qui va renommer les fichiers se trouvant dans le dossier source en y ajoutant un chiffre devant dans
    l'ordre croissant

    PRE : -
    POST : Va modifier le nom des fichiers se trouvant dans le dossier source en y ajoutant un numéro
    RAISES : FileNotFoundError si le fichier source n'existe pas
    """

    i = 1
    for fichier in os.listdir(source):
        if os.path.isfile(os.path.join(source, fichier)):
            nouveau_nom = f"{i}_{fichier}"
            os.rename(os.path.join(source, fichier), os.path.join(source, nouveau_nom))
            i += 1
    click.echo("Fichiers renommés avec préfixe numérique.")


def supprimer_fichiers_source(source):
    """
    Fonction qui va supprimer tous les fichiers se trouvant dans le dossier source

    PRE : -
    POST : Va supprimer les fichiers se trouvant dans le dossier source
    RAISES : FileNotFoundError si le fichier source n'existe pas
    """
    for fichier in os.listdir(source):
        chemin_fichier = os.path.join(source, fichier)
        if os.path.isfile(chemin_fichier):
            os.remove(chemin_fichier)
    click.echo("Fichiers supprimés du dossier source.")


def trier_regroupement(source, destination):
    """
    Fonction qui va regrouper les fichiers sources dans des dossiers dans le dossier destination

    PRE : -
    POST : Va déplacer les fichiers du dossier sources dans leurs dossiers respectif en fonction dans leurs extensions
    se trouvant dans le dossier destination et va créer le fichier destination s'il n'existe pas
    RAISES : FileNotFoundError si le fichier source n'existe pas
    """
    if not os.path.exists(destination):
        os.makedirs(destination)

    for fichier in os.listdir(source):
        chemin_fichier = os.path.join(source, fichier)

        if os.path.isfile(chemin_fichier):
            _, extension = os.path.splitext(fichier)
            extension = extension.lower()
            dossier_images = os.path.join(destination, 'Images')
            dossier_documents = os.path.join(destination, 'Documents')
            dossier_autres = os.path.join(destination, 'Autres')

            for d in [dossier_images, dossier_documents, dossier_autres]:
                if not os.path.exists(d):
                    os.makedirs(d)

            if extension in ['.jpg', '.png', '.gif']:
                shutil.move(chemin_fichier, os.path.join(dossier_images, fichier))
            elif extension in ['.txt', '.pdf', '.doc']:
                shutil.move(chemin_fichier, os.path.join(dossier_documents, fichier))
            else:
                shutil.move(chemin_fichier, os.path.join(dossier_autres, fichier))

    print("Triage des fichiers terminé.")


if __name__ == '__main__':
    trier_fichiers()

