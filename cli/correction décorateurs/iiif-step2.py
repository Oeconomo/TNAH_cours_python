import csv
import requests
import click
import csv

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

# cmd_iiif_csv = click.argument("ark", click.command(cmd_iiif_csv))


def get_stats(fichier_csv, get_height=False, get_width=False, dpi=300):
    pages = 0
    heights = []
    widths = []
    with open(fichier_csv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            pages += 1
            # Si je récupère la hauteur, j'ajoute la longueur transformée en entier dans la liste heights
            if get_height:
                heights.append(int(row["Longueur"]))
            if get_width:
                widths.append(int(row["Largeur"]))
    print("{} pages dans le manifest IIIF".format(pages))
    if get_height and heights:
        heights = sum(heights) / len(heights)
        # {:.2f} permet d'avoir uniquement deux chiffres après la virgule
        print("Hauteur moyenne: {:.2f}".format(heights))
        if dpi:
            print("Hauteur moyenne: {:.2f} en pouces".format(heights/dpi))
    if get_width:
        widths = sum(widths) / len(widths)
        print("Largeur moyenne: {:.2f}".format(widths))
        if dpi:
            print("Largeur moyenne: {:.2f} en pouces".format(widths/dpi))


@click.command()
@click.argument("FICHIER-CSV")
@click.option("-H", "--height", is_flag=True, default=False,
              help="Récupère la hauteur moyenne des pages")
@click.option("-W", "--width", is_flag=True, default=False,
              help="Récupère la largeur moyenne des pages")
@click.option("-D", "--dpi", type=int, default=300,
              help="DPI des images pour calculer la taille en pouces")
def cmd_get_stats(fichier_csv, height, width, dpi):
    """ Récupère des statistiques sur un dump de manifest IIIF stocké dans un [FICHIER-CSV]"""
    get_stats(fichier_csv, get_height=height, get_width=width, dpi=dpi)

cmd_get_stats()