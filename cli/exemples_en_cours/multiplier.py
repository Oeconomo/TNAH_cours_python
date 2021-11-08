import click


# dans le terminal, tout est chaine de caractères : click permet de typer les arguments
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
