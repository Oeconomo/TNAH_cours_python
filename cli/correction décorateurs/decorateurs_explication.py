
def decorateur(fonction):
    def fonction2(parametre: int):
        print(str(parametre) + " a été utilisé")
        return fonction(parametre)
    return fonction2


def carre(nombre: int):
    print(nombre**2)

carre(2)

carre_augmente = decorateur(carre)
carre_augmente(2)


@decorateur
def carre_decore(nombre):
    print(nombre**2)

# Equivalent de
# carre_decore = decorateur(carre_decore)

carre_decore(3)
decorateur(carre_decore(2))

