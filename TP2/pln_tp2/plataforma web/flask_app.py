from flask import Flask, request, render_template
import unicodedata
import json
import re

app = Flask(__name__)

file = open("dicionario_final_com_tudo.json", encoding = "utf-8")
bd = json.load(file)
file.close()

lookup_traducao_para_termo = {}

# Primeiro, mapear traduções em catalão para termos principais
for termo, info in bd.items():
    traducoes = info.get("Traduções", {})
    lista_ca = traducoes.get("ca", [])
    
    if isinstance(lista_ca, list):
        for traducao in lista_ca:
            lookup_traducao_para_termo[traducao.lower()] = termo
    elif isinstance(lista_ca, str):
        lookup_traducao_para_termo[lista_ca.lower()] = termo

# Depois, mapear sinónimos, mas manter mapeamentos de traduções
for termo, info in bd.items():
    for sinonimo in info.get("Sinónimos", []):
        # Só mapear se não houver um mapeamento de tradução em catalão
        if sinonimo.lower() not in lookup_traducao_para_termo:
            lookup_traducao_para_termo[sinonimo.lower()] = termo


# gerar dinamicamente o dicionário das categorias por causa de adicionar/editar/apagar termos
def dici_categ_dinamico():
    dici_categorias = {}

    for termo, info in bd.items():
        categoria = info["Categoria"] # todos os termos têm uma categoria atribuída
        if categoria not in dici_categorias:
            dici_categorias[categoria] = {}
        dici_categorias[categoria][termo] = info

    # para poder ver o que ele está a fazer
    f_out_cat = open("dici_dinamico_categorias.json", "w", encoding = "utf-8")
    json.dump(dici_categorias, f_out_cat, indent = 4, ensure_ascii = False)
    f_out_cat.close()

    return dici_categorias

dici_categorias = dici_categ_dinamico() 


# file_cat = open("dici_dinamico_categorias.json", encoding = "utf-8")
# bd_categorias = json.load(file_cat)
# file_cat.close()

@app.route("/")
def index():
    return render_template("home.html")


def remover_acentos(letra):
    return unicodedata.normalize('NFD', letra)[0].upper()

def letra_base(termo):
    # Remove acentos
    termo_sem_acentos = unicodedata.normalize('NFD', termo)
    termo_sem_acentos = ''.join([c for c in termo_sem_acentos if unicodedata.category(c) != 'Mn'])
    # Procura a primeira letra alfabética
    m = re.search(r'[A-Za-z]', termo_sem_acentos)
    if m:
        return m.group(0).upper()
    return termo[0].upper()  # fallback


@app.route("/termos")
def listar_termos():
    letra = request.args.get("letra")
    termos = sorted(bd.keys())
    letras = sorted({letra_base(t) for t in termos if t}) # conjunto de letras iniciais - só as que efetivamente existem no dici
    if letra:
        termos = [t for t in termos if letra_base(t) == letra.upper()]
    return render_template("termos.html", termos=termos, letras=letras, letra_selecionada=letra, title = "Lista de Termos Médicos")


@app.route("/termos/<termo>")
def termo_individual(termo):
    termo_key = termo.lower()

    if termo_key in (t.lower() for t in bd):
        # encontra o termo correto com capitalização original
        termo_real = next(t for t in bd if t.lower() == termo_key)
        info = bd[termo_real]

        sinonimos_links = []
        for s in info.get("Sinónimos", []):
            s_key = s.lower()

            if s_key == termo_key:
                target = None  # não cria link para si próprio
            elif s_key in (t.lower() for t in bd):
                target = next(t for t in bd if t.lower() == s_key)
            elif s_key in lookup_traducao_para_termo:
                target_raw = lookup_traducao_para_termo[s_key]
                target = (
                    target_raw if target_raw.lower() != termo_key else None
                )
            else:
                target = None

            sinonimos_links.append((s, target))  # mantém forma original para display
        
        # Processar Entrada Principal
        entrada_principal = info.get("Entrada Principal")
        entrada_principal_target = None
        if entrada_principal:
            ep_key = entrada_principal.lower()
            if ep_key == termo_key:
                entrada_principal_target = None  # Não cria link para si próprio
            elif ep_key in (t.lower() for t in bd):
                entrada_principal_target = next(t for t in bd if t.lower() == ep_key)
            elif ep_key in lookup_traducao_para_termo:
                target_raw = lookup_traducao_para_termo[ep_key]
                entrada_principal_target = (
                    target_raw if target_raw.lower() != termo_key else None
                )

        # Processar Remissivas
        remissivas_links = []
        for r in info.get("Remissivas", []):
            r_key = r.lower()
            if r_key == termo_key:
                target = None  # Não cria link para si próprio
            elif r_key in (t.lower() for t in bd):
                target = next(t for t in bd if t.lower() == r_key)
            elif r_key in lookup_traducao_para_termo:
                target_raw = lookup_traducao_para_termo[r_key]
                target = (
                    target_raw if target_raw.lower() != termo_key else None
                )
            else:
                target = None
            remissivas_links.append((r, target))

        return render_template(
            "termo_individual_bonito.html",
            termo=termo_real,
            info=info,
            sinonimos_links=sinonimos_links,
            entrada_principal=(entrada_principal, entrada_principal_target),
            remissivas_links=remissivas_links,
            title=termo_real,
        )
    else:
        return render_template(
            "termo_individual_bonito.html",
            termo="Erro",
            info="Descrição não encontrada",
            title=termo,
        )


@app.route("/categorias")
def listar_categorias():
    dici_categorias = dici_categ_dinamico() # para atualizar categorias quando de adiciona, edita, elimina termos
    categorias = sorted(dici_categorias.keys())
    return render_template("categorias.html", categorias=categorias, title = "Lista de Categorias")


@app.route("/categorias/<categoria>")
def listar_termos_categoria(categoria):
    dici_categorias = dici_categ_dinamico() # para atualizar categorias quando de adiciona, edita, elimina termos
    if categoria in dici_categorias.keys():
        termos = dici_categorias[categoria]
        return render_template("termos_categoria.html", termos=termos, categoria=categoria, title=f"Termos da Categoria: {categoria}")
    else:
        return render_template("termos_categoria.html", termos=[], categoria=categoria, title="Categoria não encontrada")


@app.route("/pesquisa")
def pesquisa():
    dici_categorias = dici_categ_dinamico() # para atualizar categorias quando de adiciona, edita, elimina termos
    termo_pesquisa = request.args.get("pesquisa")
    search_area = request.args.get("search_area")
    word_boundary = request.args.get("word_boundary")
    categoria = request.args.get("categoria")
    #print(termo_pesquisa)
    categorias =  list(dici_categorias.keys())

    if not termo_pesquisa:
        return render_template("menu_pesquisa.html", categorias = categorias, title="Pesquisa")
    
    if word_boundary == "on": # só palavras completas
        padrao = rf"\b{re.escape(termo_pesquisa)}\b" # para só selecionar palavras completas
    else:
        padrao = rf"{re.escape(termo_pesquisa)}"
    
    resultados = {}
    
    if not categoria:
        bd_cat = bd
    else:
        bd_cat = dici_categorias[categoria]

    if search_area == "on": # pesquisar só nos termos em si
        for termo, info in bd_cat.items():
            if re.search(padrao, termo, flags = re.IGNORECASE):
                bold_termo = re.sub(padrao, r"<strong>\g<0></strong>", termo, flags = re.IGNORECASE)
                if "termo_popular" in info:
                    resultados[bold_termo] = info["termo_popular"]
                elif "Descrição" in info:
                    resultados[bold_termo] = info["Descrição"]
                
   
    else: # pesquisar também nas descrições ou termos populares
        for termo, info in bd_cat.items():
            if re.search(padrao, termo, flags = re.IGNORECASE): # pesquisar no termo em si
                bold_termo = re.sub(padrao, r"<strong>\g<0></strong>", termo, flags = re.IGNORECASE)
                if "termo_popular" in info:
                    resultados[bold_termo] = info["termo_popular"]
                elif "Descrição" in info:
                    resultados[bold_termo] = info["Descrição"]

            for desc in info["Descrição"]: # pesquisar na descrição -> é uma lista
                if re.search(padrao, desc, flags = re.IGNORECASE):
                    bold_termo = re.sub(padrao, r"<strong>\g<0></strong>", termo, flags = re.IGNORECASE)
                    bold_desc = re.sub(padrao, r"<strong>\g<0></strong>", desc, flags = re.IGNORECASE)
                    resultados[bold_termo] = [bold_desc]
                    break # basta um match

            if "termo_popular" in info.keys():
                for termo_pop in info["termo_popular"]: # pesquisar no termo_popular -> é uma lista
                    if re.search(padrao, termo_pop, flags = re.IGNORECASE):
                        bold_termo = re.sub(padrao, r"<strong>\g<0></strong>", termo, flags = re.IGNORECASE)
                        bold_termo_pop = re.sub(padrao, r"<strong>\g<0></strong>", termo_pop, flags = re.IGNORECASE)
                        resultados[bold_termo] = [bold_termo_pop]
                        break # basta um match

    #print(resultados)
    return render_template("menu_pesquisa.html",  categorias = categorias, resultados=resultados, pesquisa=termo_pesquisa, search_area=search_area, word_boundary=word_boundary, categoria=categoria, title="Resultados da Pesquisa")


@app.route("/novo_termo")
def menu_adicao():
    return render_template("adicionar_termo.html", title="Adicionar Termo")

# adicionar informação pelo form
@app.post("/novo_termo") 
def adicionar_termo(): # não deixar adicionar termos já existentes, porque aí estaria a editá-los
    termo = request.form.get("termo")
    descricao = request.form.get("descricao")
    categoria = request.form.get("categoria")

    if termo and descricao and categoria:
        if termo not in bd: # só deixa adicionar se não existir 
            bd[termo] = {}
            bd[termo]["Descrição"] = [descricao]
            bd[termo]["Categoria"] = categoria

            # f_out = open("dici_teste_adicao.json", "w", encoding = "utf-8") # depois tem que se mudar para o próprio ficheiro
            f_out = open("dicionario_final_com_tudo.json", "w", encoding = "utf-8")
            json.dump(bd, f_out, indent = 4, ensure_ascii = False)
            f_out.close()

            return render_template("adicionar_termo.html", termo = termo, descricao=descricao, categoria=categoria, title="Adicionar Termo")
        
    return render_template("adicionar_termo.html", termo = termo, title="Adicionar Termo")

# se adicionarmos um termo que já existe, ele altera a sua descrição 

@app.route("/editar/<termo>")
def menu_edicao(termo):
    info = bd[termo]
    return render_template("editar_termo.html", termo = termo, info = info, title="Editar Termo")

@app.post("/editar/<termo>") 
def editar_conceito(termo): # só para termos que já existam
    descricao = request.form.get("descricao")
    categoria = request.form.get("categoria")
    info = bd[termo]

    if termo in bd.keys(): # só atualiza se o termo já existir
        if descricao:
            bd[termo]["Descrição"] = [descricao]
        if categoria:
            bd[termo]["Categoria"] = categoria 

        # f_out = open("dici_teste_adicao.json", "w", encoding = "utf-8") 
        f_out = open("dicionario_final_com_tudo.json", "w", encoding = "utf-8")
        json.dump(bd, f_out, indent = 4, ensure_ascii = False)
        f_out.close()

        return render_template("editar_termo.html", info = info, termo=termo, descricao=descricao, categoria=categoria, title="Editar Termo")
    
    return render_template("editar_termo.html", termo = termo, title="Editar Termo")


@app.delete("/termos/<termo>")
def delete_termo(termo): # aqui também tem que se apagar no dici das categorias, senão vai aparecer lá na mesma
    if termo in bd:
        # f_out = open("dici_teste_adicao.json", "w", encoding = "utf-8")
        f_out = open("dicionario_final_com_tudo.json", "w", encoding = "utf-8")
        print(termo)
        del bd[termo]
        json.dump(bd, f_out, indent = 4, ensure_ascii = False)
        f_out.close()
        return {"success": True, "message": "Termo apagado com sucesso", "redirect_url": "/termos", "data": termo}
    return {"success": False, "message": "O termo não existe", "data": termo}


app.run(host="localhost", port = 40002, debug = True)
