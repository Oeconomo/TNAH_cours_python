import click


@click.command()
@click.argument("phrase", type=str)
def indexer_mots(phrase):
    mots = phrase.lower().split()
    numero = 0
    for index, mot in enumerate(mots):
        numero += 1
        print("Numéro {}: {}".format(numero, mot))git st


indexer_mots()
# pour faire la fonction sur un fichier :
# cat text.txt | xargs -Iboubou python numeroter_mots.py boubou
