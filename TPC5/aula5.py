from flask import Flask, request, render_template
import json

app= Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!<p>"

# O que for json metemos a rota com /api/

# é melhor usar json para comunicaçao das maquinas web
# dbFile = open("conceitos.json", encoding="utf-8") # copiei o ficheiro da pasta aula4 para a pasta aula5
dbFile = open("conceitos_.json", encoding="utf-8") # ficheiro que vai ser atualizado (cópia do ficheiro original com alterações)
db = json.load(dbFile)
dbFile.close()

@app.route("/api/conceitos")
def conceitos_api():
    return db

@app.route("/conceitos")
def conceitos():
    designacoes = list(db.keys())
    return render_template("conceitos.html", designacoes=designacoes, title = "Lista de conceitos") # o html tem de estar na pasta templates


@app.post("/api/conceitos")
def adicionar_conceito():
    #json
    data=request.get_json()
    # {"designacao"="vida", "descricao"="a vida é..."}

    db[data["designacao"]]=data["descricao"]
    f_out = open("conceitos_.json", "w", encoding="utf-8") # para não sobrescrever o ficheiro original
    json.dump(db, f_out, ensure_ascii=False, indent=4)
    f_out.close()
    
    #form data
    # designacao = request.form.get("designacao")
    # descricao = request.form.get("descricao")
    # ...
    
    return data

@app.route("/api/conceitos/<designacao>")
def get_conceito(designacao):
    return {"designacao":designacao, "descricao":db[designacao]}



app.run(host="localhost", port=4002, debug=True)

