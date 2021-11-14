import click
import requests
import math
import csv

ISIDORE = "https://api.isidore.science/resource/search"


def parser_reponse_isidore(data):
    """ Fait une recherche sur Isidore

    :param data: JSON Parsed Data
    :type data: dict     # code de thibaut appelait ce param "q", ça doit être une erreur
    :returns: Tuple (
        Nombre de Résultats,
        Nombre de Pages,
        Liste de résultat sous forme de dictionnaire {title, desc, author, date}
    )
    """
    # On récupère le nombre de résultats
    nb_items = int(data["response"]["replies"]["meta"]["@items"])
    # On récupère le nombre de résultats par page
    items_per_page = int(data["response"]["replies"]["meta"]["@pageItems"])
    # Le nombre total de pages est l'arrondi supérieur de la division nb_items / items_per_page
    total_page = math.ceil(nb_items / items_per_page)

    # On crée une liste vide dans laquelle on enregistrera les données
    items = []
    # Pour chaque réponse
    for item in data["response"]["replies"]["content"]["reply"]:
        # On ajoute à items un nouvel objet
        items.append({
            "uri": item["@uri"],
            "title": item["isidore"]["title"],
            # dictionnaire.get(cle, valeur-par-defaut) : valeur-par-defaut est utilisée si clé n'est
            # pas présente
            "date": item["isidore"]["date"].get("normalizedDate", "0000-00-00"),
            "author": []
        })
        # Les auteurs peuvent être plusieurs : dans ce cas, on a une liste sur laquelle on bouclera
        # On utilise items[-1] car il s'agit du dernier item ajouté
        if isinstance(item["isidore"]["enrichedCreators"]["creator"], list):
            for author in item["isidore"]["enrichedCreators"]["creator"]:
                items[-1]["author"].append(author["@normalizedAuthor"])
        else:
            items[-1]["author"].append(item["isidore"]["enrichedCreators"]["creator"]["@normalizedAuthor"])

        # Des fois, le titre est un dictionnaire aussi ou une liste
        if isinstance(items[-1]["title"], dict):
            items[-1]["title"] = items[-1]["title"]["$"]
        if isinstance(items[-1]["title"], list):
            items[-1]["title"] = items[-1]["title"][0]
            # Et des fois, dans cette liste de titre, on a aussi des dictionnaires...
            if isinstance(items[-1]["title"], dict):
                items[-1]["title"] = items[-1]["title"]["$"]

    return nb_items, total_page, items, data["response"]["replies"]["page"].get("@next", None)


def cherche_isidore(q, full=False, page=1):
    """ Chercher sur isidore en faisant une requête

    :param q: Chaine de recherche
    :type q: str
    :param full: Recherche complète (itère sur toutes les pages)
    :type full: bool
    :param page: Page à récupérer
    :type page: int
    :returns: Tuple (
        Nombre de Résultats,
        Nombre de Pages,
        Liste de résultat sous forme de dictionnaire {uri, title, desc, author, date}
    )
    """

    # On exécute la requête
    params = {"output": "json", "q": q, "page": page}
    req = requests.get(ISIDORE, params=params)

    # On la parse
    nb_items, total_page, items, next_page = parser_reponse_isidore(req.json())

    if full and next_page:
        # On la parse
        nb_items, total_page, new_items, next_page = cherche_isidore(q=q, full=full, page=next_page)
        # On ajoute chacune des valeurs d'items à total_items
        items.extend(new_items)

    return nb_items, total_page, items, next_page


# moi : mon code pour l'exo chapitre 5
@click.group()
def group():

@group.command()
def run():
    """ Commande que l'on mettra comme commande principale
    """
    print("Commande exécutée !")

# Si ce fichier est le fichier exécuté directement par python
# Alors on exécute la commande
if __name__ == "__main__":
        run()
