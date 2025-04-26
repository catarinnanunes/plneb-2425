import json

# Função para carregar ficheiros
def load_json(caminho):
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)

# Função básica para fundir dois valores
def merge(v1, v2):
    if type(v1) == dict and type(v2) == dict:
        resultado = {}
        for chave in set(list(v1.keys()) + list(v2.keys())):
            if chave in v1 and chave in v2:
                resultado[chave] = merge(v1[chave], v2[chave])
            elif chave in v1:
                resultado[chave] = v1[chave]
            else:
                resultado[chave] = v2[chave]
        return resultado
    
    elif type(v1) == list and type(v2) == list:
        return list(set(v1 + v2))
    
    elif type(v1) == str and type(v2) == str:
        if v1 == v2:
            return v1
        else:
            return list(set([v1, v2]))
    
    elif type(v1) == list:
        return list(set(v1 + [v2]))
    
    elif type(v2) == list:
        return list(set([v1] + v2))
    
    else:
        return list(set([v1, v2]))

# Carregamento dos dicionários
d1 = load_json("diccionari-multilinguee-de-la-covid-19/dicionario_medico.json")
d2 = load_json("glossario_neologismos/glossario.json")
d3 = load_json("glossario_termos_medicos/termos_medicos_populares.json")
d4 = load_json("glossario-monitoramento-e-avaliacao/monitoramento-e-avaliacao-glossario.json")

# Lista com todos os dicionários
todos = [d1, d2, d3, d4]

# Dicionário final
unificado = {}

for dicionario in todos:
    for termo in dicionario:
        if termo not in unificado:
            unificado[termo] = dicionario[termo]
        else:
            unificado[termo] = merge(unificado[termo], dicionario[termo])

# Guardar o resultado final
with open("dicionario_final.json", "w", encoding="utf-8") as f_out:
    json.dump(unificado, f_out, ensure_ascii=False, indent=2)
