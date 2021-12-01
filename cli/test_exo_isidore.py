import click
import requests


@click.command()
@click.argument('mot', type=str)
def rechercher_mot(mot):
    ''' Fait une recherche foireuse sur l'api isidore et génére un document contenant la réponse json.
    Le nom du document est le texte rechercé.
    C'est mon premier script dans une api : on a accès qu'à la première page, c'est pas très intéressant.
    Mais mon code à marché !

    :param mot: texte à chercher sur Isidore
    :type mot: str
    :return: none
    '''
    isidore = "https://api.isidore.science/resource/search"
    req = requests.get(isidore, params={
        "output": "json", "q": mot, "page": "1"
    })
    with open('{}_test.json'.format(mot), 'w') as f:
        f.write(req.text)
    return None


rechercher_mot()
