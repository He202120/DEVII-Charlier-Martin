import os
import shutil
import click


@click.command()
@click.argument('source', type=click.Path(), metavar='<dossier_source>')
@click.argument('destination', type=click.Path(), metavar='<dossier_destination>')
@click.option('--afficher-contenu', is_flag=True, help='Afficher le contenu du dossier source avant le tri.')
@click.option('--tri-regroupement', is_flag=True, help='Regroupe les fichiers en fonction de leurs extension')
def trier_fichiers(source, destination, afficher_contenu,tri_regroupement):
    """
    Script pour trier les fichiers d'un dossier source vers un dossier destination.

    PRE : - \n
    POST : Va transporter les fichiers d'une source à une destination en fonction des autres paramètres renseignés\n
    RAISES : FileNotFoundError si le fichier source n'existe pas
    """

    if not os.path.exists(source):
        raise click.ClickException("Le fichier1 source n'existe pas")

    if afficher_contenu:
        click.echo(f"Contenu du dossier source ({source}):")
        for fichier in os.listdir(source):
            click.echo(f"- {fichier}")
    elif tri_regroupement:
        trier_regroupement(source, destination)



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
