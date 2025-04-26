import re
import json

#no txt, foram alterados à mão casos específicos  

#Nas linhas 255 e 256 ------------------------------
# <b>pré-</b>
# <b>medicação</b>

# Para:
#<b>pré-medicação</b>


#Nas linhas 2423 e 2424 -------------------------
#disto:
# <b>infecção </b>
# <b>cruzada </b>

#Para isto:
#  <b>infecção cruzada </b>

#Nas linhas 12348 e 12349 ----------------------------------
# <b>tremor</b>
# <b>intencional</b>

#Para isto:
# <b>tremor intencional</b>




with open('termos_medicos_populares.txt', 'r', encoding='utf-8') as f:
    content = f.read()


pattern = re.compile(
    r'(?P<popular>(?:[^<(]|\((?!(?:pop\))))*?)\s*\(pop\)\s*,\s*<b>(?P<tecnico>(?:.|\n)+?)</b>|'
    r'<b>(?P<tecnico2>(?:.|\n)+?)</b>\s*,\s*(?P<popular2>(?:[^<(]|\((?!(?:pop\))))*?)\s*\(pop\)',
    re.DOTALL
)

result = {}


for match in pattern.finditer(content):
    if match.group('tecnico'):
        tecnico = match.group('tecnico').strip().strip("'")  # Remove aspas simples
        popular = match.group('popular').strip()
    else:
        tecnico = match.group('tecnico2').strip().strip("'")  # Remove aspas simples
        popular = match.group('popular2').strip()
        

    tecnico = re.sub(r'\s*\n\s*', '', tecnico)

    popular = re.sub(r'\s+', ' ', popular)  # Normaliza espaços
    popular = popular.replace('\n', ' ')    # Remove quebras de linha
    popular = popular.strip(' ,')

    popular_terms = [term.strip() for term in re.split(r'[,;]', popular) if term.strip()]
    

    # Condição especial para pré-medicação que tem erro de ortografia
    if tecnico.lower() == "pré-medicação":
        popular_terms = [term for term in popular_terms if term.endswith('geral')]


    if tecnico not in result:
        result[tecnico] = {"termo_popular": []}
    
    for term in popular_terms:
        if term not in result[tecnico]["termo_popular"]:
            result[tecnico]["termo_popular"].append(term)

sorted_result = {k: result[k] for k in sorted(result)}

with open('termos_medicos_populares.json', 'w', encoding='utf-8') as f:
    json.dump(sorted_result, f, ensure_ascii=False, indent=4, sort_keys=True)

print("JSON consolidado criado com sucesso!")
