from flask import Flask, request, render_template
import json
import re

app= Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("home.html")

# O que for json metemos a rota com /api/

# é melhor usar json para comunicaçao das maquinas web
# dbFile = open("conceitos.json", encoding="utf-8") # copiei o ficheiro da pasta aula4 para a pasta aula5
dbFile = open("conceitos_.json", encoding="utf-8") # ficheiro que vai ser atualizado (cópia do ficheiro original com alterações)
db = json.load(dbFile)
dbFile.close()

@app.get("/conceitos/<designacao>") 
def conceito(designacao):
    if designacao in db:
        return render_template("conceito.html", designacao=designacao,descricao=db[designacao])
    else: 
        return render_template("conceito.html", designacao="ERRO",descricao="Descricao nao encontrada")


@app.route("/api/conceitos")
def conceitos_api():
    return db

@app.route("/conceitos")
def conceitos():
    designacoes = list(db.keys())
    return render_template("conceitos.html", designacoes=designacoes, title = "Lista de conceitos") # o html tem de estar na pasta templates

@app.post("/conceitos")
def adicionar_conceito(): # espera por receber dados vindos de um formulário
    descricao=request.form.get("descricao") # é assim que obtemos os dados de um formulario
    designacao=request.form.get("designacao") 
    
    db[designacao]=descricao
    f_out = open("conceitos_.json", "w", encoding="utf-8") # para não sobrescrever o ficheiro original
    json.dump(db, f_out, ensure_ascii=False, indent=4)
    f_out.close()
    
    designacoes=list(db.keys())
    
    return render_template("conceitos.html",designacoes=designacoes,title="Lista de Conceitos")

@app.post("/api/conceitos")
def adicionar_conceito_api(): # aqui espera receber um json!!
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


def find_conceito(db,query,word_bound,case_sensitive, use_regex):
    res = []
    flags = 0
    
    if use_regex == 'on':
        pattern = r"(" + query + r")"
        
    else:  
        if word_bound == "on":
            pattern = r"\b(" + query + r")\b"
        else:
            pattern = r"(" + query + r")"
    
    if case_sensitive != "on":
        flags = re.IGNORECASE

    for designacao, descricao in db.items():
        if re.search(pattern, designacao,flags) or re.search(pattern, descricao,flags):
            
            bold_designacao = re.sub(pattern,r"<strong>\1</strong>",designacao, flags)
            bold_descricao = re.sub(pattern,r"<strong>\1</strong>",descricao, flags)
            res.append((designacao, bold_designacao, bold_descricao))   
    return res

@app.get("/pesquisa")
def pesquisa():
    query = request.args.get("query")
    word_bound = request.args.get("word_bound")
    case_sensitive = request.args.get("case_sensitive")
    use_regex = request.args.get("use_regex")

    if not query:
        return render_template("pesquisa.html", title="Pesquisa")
    
    res = find_conceito(db,query,word_bound,case_sensitive,use_regex)
    return render_template("pesquisa.html", conceitos=res, query=query, word_bound=word_bound, case_sensitive=case_sensitive, use_regex=use_regex, title="Pesquisa")



@app.delete("/conceitos/<designacao>")
def delete_conceito(designacao):
    if designacao in db:
        f_out=open("conceitos_.json","w")
        del db[designacao]
        json.dump(db,f_out,indent=4,ensure_ascii=False, encoding='utf-8')
        f_out.close
        return{"success": True,
            "message":"Conceito apagado",
            "redirect_url":"/conceitos",
            "data":designacao}
    return {"success":False, "message":"O conceito nao ta na bd", "data":designacao}
        


@app.get("/conceitos/tabela")
def conceitos_tabela():
    conceitos = [{"designacao": k, "descricao": v} for k, v in db.items()]
    return render_template("tabela.html", conceitos=conceitos)

app.run(host="localhost", port=4002, debug=True)

