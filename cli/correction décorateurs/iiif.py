import csv
import requests
import click

def iiif_csv(ark, nom_csv):
    colonnes = ["Numéro", "Nom de Page", "Lien image", "Largeur", "Longueur"]
    rep = requests.get("https://gallica.bnf.fr/iiif/{}/manifest.json".format(
        ark
    ))
    rep = rep.json()
    with open(nom_csv, mode="w") as f:
        # Mes images sont dans\
        writer = csv.writer(f)
        writer.writerow(colonnes)
        for i, image in enumerate(rep["sequences"][0]["canvases"]):
            writer.writerow([
                str(i),
                image["label"],
                image["images"][0]["resource"]["@id"],
                str(image["width"]),
                str(image["height"])
            ])
        # Complétez avec la documentation
    return None


@click.command()
@click.argument("ark", type=str)
@click.argument("fichier", type=str)
def cmd_iiif_csv(ark, fichier):
    """À partir du [ARK] fourni, enregistre l'ensemble des métadonnées pages dans le fichier CSV au chemin [FICHIER]"""
    iiif_csv(ark, fichier)

cmd_iiif_csv()

def get_stats(fichier_csv):
    pages = 0
    with open(fichier_csv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            page += 1
            print(row)
    print("{}pages dans le manifeste".format(pages))