import click


@click.command()
@click.argument("phrase", type=str)
def numeroter_mots(phrase):
    """Fait un décompte des mots et les retourne numérotés.

    :param phrase: texte à numéroter
    :type phrase: str
    :return: none
    """
    mots = phrase.lower().replace(".", " ").replace(",", " ").replace("-", " ").split()
    numero = 0
    for index, mot in enumerate(mots):
        numero += 1
        print("Numéro {}: {}".format(numero, mot))
        return None


numeroter_mots()
# pour faire la fonction sur un fichier :
# cat text.txt | xargs -Iboubou python numeroter_mots.py boubou
