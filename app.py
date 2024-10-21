import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__)

def dados_personagens():
    lista_personagens = []
    url = 'https://rickandmortyapi.com/api/character'

    while url:
        response = requests.get(url)

        if response.status_code == 200:
            personagens = response.json()

            for personagem in personagens["results"]:
                data = {
                    "id": personagem["id"],
                    "nome": personagem["name"],
                    "status": personagem["status"],
                    "especies": personagem["species"],
                    "genero": personagem["gender"],
                    "origem": {"nome": personagem["origin"]["name"], "url": personagem["origin"]["url"]},
                    "localizacao": personagem["location"]["name"],
                    "imagem": personagem["image"],
                    "quant_ep": len(personagem["episode"])
                }
                lista_personagens.append(data)

            url = personagens["info"]["next"]
        else:
            break

    return lista_personagens

@app.route("/")
def index():
    personagens = dados_personagens()
    return render_template('index.html', personagens=personagens)

@app.route("/characters")
def characters():
    personagens = dados_personagens()
    return jsonify(personagens)

if __name__ == "__main__":
    app.run()