import click


@click.command()     #on vient de transformer notre fonction en commande
@click.argument("prenom")     #on colle les decorateurs au nom de la fonction pour savoir à quoi il correspond
def dire_bonjour(prenom):
    print("Bonjour "+prenom)

dire_bonjour()
# dire_bonjour("TNAH")    lancera une erreur dans le terminal




#dnans le terminal, tout est chaine de caractères : click permet de typer les arguments
@click.command()
@click.argument("a", type=int)
@click.argument("b", type=int)
@click.option("--c", default=None, type=int)
def multiplier(a, b, c):
    r = a * b
    if c is not None:
        r *= c
    print(r)

multiplier()   
