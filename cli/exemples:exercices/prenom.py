import click


@click.command()     # on vient de transformer notre fonction en commande
@click.argument("prenom")     # on colle les decorateurs au nom de la fonction pour savoir à quoi il correspond
def dire_bonjour(prenom):
    print("Bonjour "+prenom)


dire_bonjour()
# dire_bonjour("TNAH")    lancera une erreur dans le terminal



