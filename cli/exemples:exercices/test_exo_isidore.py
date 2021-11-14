import requests
import json

ISIDORE = "https://api.isidore.science/resource/search"

req = requests.get(ISIDORE, params={
    "output":"json", "q":"exposition", "page":"1"
})
json = req.json()

with open ("fichier.json", 'w') as f:
    json.dumps(f, "fichier.json")


