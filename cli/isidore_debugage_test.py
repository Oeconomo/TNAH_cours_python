import click
import requests
import math
import csv
"""
Ce code comporte ma proposition de débugage (voir plus bas). Note : pour les requêtes avec
des miliers de résultats, la commande python3 (erreurs diverses selon la requête) ne marche pas, 
mais la commande python (donc python 2) oui. 
"""

ISIDORE = "https://api.isidore.science/resource/search"


def parser_reponse_isidore(data):
    nb_items = int(data["response"]["replies"]["meta"]["@items"])
    items_per_page = int(data["response"]["replies"]["meta"]["@pageItems"])
    total_page = math.ceil(nb_items / items_per_page)
    items = []
    for item in data["response"]["replies"]["content"]["reply"]:
        items.append({
            "uri": item["@uri"],
            "title": item["isidore"]["title"],
            "date": item["isidore"]["date"].get("normalizedDate", "0000-00-00"),
            "author": []
        })
        '''
        # l'érreur est ici : [enrichedCreators] peut aussi être une liste vide, donc la machine arrête de tourner 
        # dès qu'elle tombe sur une liste ou il n'y a pas de dic ['creator']
        if isinstance(item_creator, list):
            for author in item["isidore"]["enrichedCreators"]["creator"]:
                items[-1]["author"].append(author["@normalizedAuthor"])
        else:
            items[-1]["author"].append(item["isidore"]["enrichedCreators"]["creator"]["@normalizedAuthor"])
        # Je propose le code suivant :
        '''
        # Je m'arrête à [enrichedCreators] car après, le contenu peut être un dic, une liste vide ou une liste pleine
        item_creator = item["isidore"]["enrichedCreators"]
        # Si le contenu est un dictionnaire,
        # et que son élément [creator] est un dictionnaire (pusique des fois, celui-ci aussi est vide) :
        if isinstance(item_creator, dict) and isinstance(item['isidore']['enrichedCreators']['creator'], dict):
            items[-1]["author"].append(item['isidore']['enrichedCreators']['creator']["@normalizedAuthor"])
        # Si le contenu est une liste, et que cette liste contient quelque chose (valeur true) :
        if isinstance(item_creator, list) and item_creator:
            for author in item["isidore"]["enrichedCreators"]["creator"]:
                items[-1]["author"].append(author["@normalizedAuthor"])
        # Si le contenu est une liste, et qu'elle ne contient rien (valeur false):
        if isinstance(item_creator, list) and not item_creator:
            items[-1]["author"].append("auteur non renseigné")
        # Ici fini mon code
        if isinstance(items[-1]["title"], dict):
            items[-1]["title"] = items[-1]["title"]["$"]
        if isinstance(items[-1]["title"], list):
            items[-1]["title"] = items[-1]["title"][0]
            if isinstance(items[-1]["title"], dict):
                items[-1]["title"] = items[-1]["title"]["$"]

    return nb_items, total_page, items, data["response"]["replies"]["page"].get("@next", None)


def cherche_isidore(q, full=False, page=1):
    params = {"output": "json", "q": q, "page": page}
    req = requests.get(ISIDORE, params=params)
    nb_items, total_page, items, next_page = parser_reponse_isidore(req.json())

    # Je rajoute des message de fetch car le programme est lent, pour avoir de l'information sur ce qui prends du temps
    # Cela pourrait permettre de connaitre la page où une exception a lieu
    if full and next_page == '2':
        print("Page 1 : fetched")
    if full and next_page:
        print("Fetching page " + next_page)
        nb_items, total_page, new_items, next_page = cherche_isidore(q=q, full=full, page=next_page)
        items.extend(new_items)
    return nb_items, total_page, items, next_page


@click.command()
@click.argument("query", type=str)
@click.option("-f", "--full",  is_flag=True, default=False,
              help="Browse every page of results")
@click.option("-o", "--output", "output_file", type=click.File(mode="w"), default=None,
              help="File in which to write, in a CSV manner, the results")
def run(query, full, output_file):
    """ Exécute une recherche sur Isidore.science en utilisant [QUERY]
    """
    nb_items, total_page, items, next_page = cherche_isidore(query, full=full)
    print("Nombre de résultats : {}".format(nb_items))
    print("Nombre de résultats affichés : {}".format(len(items)))
    for item in items:
        print("– {}; {}".format(item["title"], "& ".join(item["author"])))

    if output_file:
        writer = csv.writer(output_file)
        writer.writerow(["date", "title", "author", "uri"])
        for item in items:
            writer.writerow([item["date"], item["title"], ", ".join(item["author"]), item["uri"]])


if __name__ == "__main__":
    run()
