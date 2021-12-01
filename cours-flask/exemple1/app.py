from flask import Flask

app = Flask("Application")


@app.route("/©")      # / est la racine de mon application web. Je connecte une fonction à ce chemin
def index():
    return "Hello world !"     # pas du HTML, rien : du texte brut


app.run()                     # Je lance mon application

# app pourrait s'appeler boubou