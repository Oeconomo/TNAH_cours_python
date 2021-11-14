import csv
import requests
import click


@click.command()
@click.argument("ark", type=str)
@click.argument("nom_csv", type=str)
def iiif_csv(ark, nom_csv):
    """À partir d'un identifiant ark de la BnF, affiche en json les métadonnées associées à l'objet décrit,
    puis génère un fichier CSV qui consiste en un tableau listant les images iiif associées à  cet objet,
    avec les colonnes suivantes : Numéro, Nom de Page, Lien image, Largeur, Longueur.

    :param ark: identifiant ark complet
    :type ark: str
    :param nom_csv: nom souhaité pour le fichier csv à produire
    :type nom_csv: str
    :return: none
    """
    # A. Afficher Json
    rep = requests.get("https://gallica.bnf.fr/iiif/{}/manifest.json".format(ark))
    rep = rep.json()
    print(rep["metadata"])
    #B. générer csv
    colonnes = ["Numéro", "Nom de Page", "Lien image", "Largeur","Longueur"]
    with open(nom_csv, mode="w") as f:
        writer = csv.writer(f)
        writer.writerow(colonnes)
        for i, image in enumerate(rep["sequences"][0]["canvases"]):
            writer.writerow([
            str(i+1),    # +1 ajouter pour harmoniser numérotation avec numéro folio sur le lien
            image["label"],
            image["images"][0]["resource"]["@id"],
            str(image["width"]),
            str(image["height"])
             ])
    return None


iiif_csv()
# commande souhaitée :
# python iiif_to_csv.py ark:/12148/btv1b84259980


