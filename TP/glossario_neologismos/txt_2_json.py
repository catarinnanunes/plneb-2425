import re
import json

with open("glossario.txt", "r", encoding="utf-8") as f:
    content = f.read()
    
content = content.replace('\f', '')

# Separar os termos com quebra de página ou espaços grandes
termos_brutos = re.split(r'\n(?=\S.*\s+s\.(?:f|m)\.)', content.strip())
# print(termos_brutos[8]) - desde o nome do termo até o fim da citação

termos_dict={}

for termo_bruto in termos_brutos:
    bloco = termo_bruto.strip().split('\n')
    
    termo_entrada = bloco[0].strip() # Nome do termo + categoria lexical
    
    termo = re.sub(r"\s(s\.f\.|s\.m\.)$", "", termo_entrada).strip()
    categoria_lexical = re.search(r"\s(s\.f\.|s\.m\.)$", termo_entrada).group(1)
    
    traducao_linhas = []
    for linha in bloco[1:]:
        if '[ing]' in linha or '[esp]' in linha:
            traducao_linhas.append(linha)
        else:
            break  # parou de apanhar traduções

    traducoes_texto = ' '.join(traducao_linhas).strip()
    
    # print(f"Termo: {termo}")
    # print(f"Categoria lexical: {categoria_lexical}")
    # print(f"Traduções: {traducoes_texto}")
    # print(f"-------------")
    
    
    termo_info = {
        # "categoria_lexical": re.search(r"(s\.f\.|s\.m\.)$", termo_entrada).group(1),
        "categoria_lexical": re.search(r"\s(s\.f\.|s\.m\.)$", termo_entrada).group(1),
        "traducoes": {},
        "descricao": "",
        "sigla": "",
        "inf_encicl": "",
        "citacoes": []
    }
    
    # Trad: "xxx [ing]; xxx[esp]]"
    trad_match = re.match(r"^(.*?)\s*\[ing\];\s*(.*?)\s*\[esp\]$", traducoes_texto)
    if trad_match:
        termo_info["traducoes"]["en"] = trad_match.group(1).strip()
        termo_info["traducoes"]["es"] = trad_match.group(2).strip()
    
    # print(f"Termo: {termo_info['termo']}")
    # print(f"Categoria lexical: {termo_info['categoria_lexical']}")  
    # print(f"Traduções: {termo_info['traducoes']}")
    # print(f"-------------")
    
    resto_linhas = bloco[len(traducao_linhas) + 1:]  # tudo depois da tradução
    resto_texto = '\n'.join(resto_linhas)
    # print(f"Resto texto: {resto_texto}")
    # print("-------------------------")
    
    # --- SIGLA ---
    sigla_match = re.search(r"Sigla:\s*(.*)", resto_texto)
    if sigla_match:
        termo_info["sigla"] = sigla_match.group(1).strip()
        # print(f"Sigla: {sigla_match.group(1).strip()}")
        # até aqui ta a dar certo!!
        
    # --- INF. ENCICL. ---
    inf_encicl_match = re.search(r"Inf\. encicl\.:([\s\S]+?)(?=“)", resto_texto)
    if inf_encicl_match:
        termo_info["inf_encicl"] = inf_encicl_match.group(1).replace('\n',' ').strip()
        
        # print(f"Termo: {termo}\nInf. encicl.: {inf_encicl_match.group(1).strip()}")
        # print("-------------")

    # --- CITAÇÕES ---
    citacoes = re.findall(r'“([^”]+)”\s*\(([\d,]+)\)', resto_texto)
    for citacao, numeros in citacoes:
        citacao = citacao.replace('\n', ' ')
        termo_info["citacoes"].append(citacao.strip())
        # print(f"Termo: {termo}\nCitação: {citacao.strip()}")
        
    
    # --- DESCRIÇÃO ---
    # Descrição é o texto entre as traduções e o início da sigla ou 'Inf. encicl.'
    # Exclui citações e sigla
    descricao_linhas = []
    for linha in resto_linhas:
        if linha.startswith("Sigla:") or linha.startswith("Inf. encicl.:") or '“' in linha:
            break
        descricao_linhas.append(linha)

    termo_info["descricao"] = ' '.join(descricao_linhas).strip()
    # print(f"Termo: {termo}\n-----\n Descrição: {descricao_linhas}\n-----------------")

    termos_dict[termo]=termo_info

# Guardar em JSON
with open("glossario.json", "w", encoding="utf-8") as f:
    json.dump(termos_dict, f, ensure_ascii=False, indent=2)