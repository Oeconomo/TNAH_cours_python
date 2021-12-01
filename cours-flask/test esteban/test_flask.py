from flask import Flask, render_template

app = Flask('AppSteban')

chiens = [{"nom": "boubou",
           "nationalité": "Mexicaine",
           "couleurs": ["noir", "blanc", "marron"]
           },
          {"nom": "maxou",
           "nationalité": "française",
           "couleurs": ["blanc", "marron"]},
          {"nom": "kida",
           "nationalité": "Mexicaine",
           "couleurs": ["blanc", "noir"]
           },
          {"nom": "bro",
           "nationalité": "Mexicaine",
           "couleurs": ["noir", "blanc", "marron"]
           },
          {"nom": "athena",
           "nationalité": "Mexicaine",
           "couleurs": ["marron", "noir"]},
          {"nom": "Nikita",
           "nationalité": "Mexicaine",
           "couleurs": "marron"}]


@app.route("/")
def acceuil():
    return render_template("template1.html",
                           nom_site="boubou",
                           page="Acceuil",
                           prenom="Esteban",
                           chien="boubou",
                           chiens=chiens)


@app.route("/chiens/<int:chien_id>")
def chemin_place(chien_id):
    return render_template("template_chiens.html",
                           nom_site="chiens",
                           chien=chiens[chien_id])

# continuer chapitre 6 dans "boucles dans les templates et liens"


app.run()    # ceci sert à lancer un serveur de test
