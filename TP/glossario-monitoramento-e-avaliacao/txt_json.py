import re
import json

def clean_text(text):

    if not text:
        return text
    
    # Remove quebras de linha e substitui por espaço
    text = text.replace('\n', ' ')
    
    # Remove espaços múltiplos
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

with open('m_glossario_processado.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# capturar o conceito completo
concepts = re.split(r'^###\s', content, flags=re.MULTILINE)[1:]

glossary = {}

for concept in concepts:

    # Extrair o nome do conceito
    first_line = concept.split('\n')[0].strip()
    name = re.match(r'^([^,]+)', first_line).group(1).strip()
    
    # Extrair gênero e número
    gender_match = re.search(r',\s(fem|masc)(?:\.\spl\.)?', first_line)
    gender = gender_match.group(1) if gender_match else ''
    number = 'pl' if '. pl.' in first_line else ''
    
    # Extrair sinonimos
    synonyms = []
    sin_match = re.search(r'Sin\.\s([^.;]+(?:;\s[^.;]+)*)', concept)
    if sin_match:
        synonyms = [clean_text(s.strip()) for s in re.split(r';\s*', sin_match.group(1))]
    
    # Extrair sigla (se houver ⇒ na definição)
    acronym = ''
    acronym_match = re.search(r'⇒\s([^.,;\n]+)', concept)
    if acronym_match:
        acronym = clean_text(acronym_match.group(1).strip())
    
    # Extrair descrição
    desc_part = re.split(r'(?:Notas?:|Em espanhol:|Em inglês:)', concept, maxsplit=1, flags=re.IGNORECASE)[0]
    desc_part = re.sub(r'^[^,]+,.*?\.\s*', '', desc_part, flags=re.DOTALL)

    if sin_match:
        desc_part = desc_part.replace(sin_match.group(0), '').strip()
    if acronym_match:
        desc_part = desc_part.replace(acronym_match.group(0), '').strip()

    desc_part = re.sub(r'\s*Ver\s+[^.]+\.[\s]*$', '', desc_part)
    desc_part = re.sub(r'\s*Ver sin\.\s+[^.]+\.[\s]*$', '', desc_part)
    desc_part = re.sub(r'^(\s*\.?\s*pl\s*\.?\s*)', '', desc_part, flags=re.IGNORECASE)
    description = clean_text(desc_part)
    description = description.lstrip('. ').strip()
    
    # Extrair notas
    notes = []
    notes_match = re.search(r'Notas?:\s*(.*?)(?=Em espanhol:|Em inglês:|$)', concept, flags=re.DOTALL)
    if notes_match:
        notes_text = notes_match.group(1).strip()
        notes = re.split(r'\s*[ivx]+\)\s*', notes_text)

        #notes = re.split(r'\s*i+\)\s*', notes_text)
        notes = [clean_text(note) for note in notes if clean_text(note)]
        notes = [re.sub(r'\s*Ver\s+[^.]+\.[\s]*$', '', note).strip() for note in notes]
        notes = [re.sub(r'\s*Ver sin\.\s+[^.]+\.[\s]*$', '', note).strip() for note in notes]
    
    # Extrair traduções
    translations = {'es': '', 'en': ''}
    es_match = re.search(r'Em espanhol:\s*(.*?)(?:\n|$)', concept)
    if es_match:
        translations['es'] = clean_text(es_match.group(1).strip().rstrip(';'))
    
    en_match = re.search(r'Em inglês:\s*(.*?)(?:\n|$)', concept)
    if en_match:
        translations['en'] = clean_text(en_match.group(1).strip().rstrip(';'))
    
    #extrair remissivas
    remissivas = []
    concept_one_line = concept.replace('\n', ' ')

    # Para "Ver sin."
    ver_sin_match = re.search(r'Ver sin\.\s*([^.;]+(?:;\s[^.;]+)*)', concept_one_line)
    if ver_sin_match:
        remissivas.extend([clean_text(s.strip()) for s in re.split(r';\s*', ver_sin_match.group(1)) 
                    if s.strip() and s.strip().lower() not in ['sin', 'sin.']])

    # Para "Ver" (exceto "Ver sin.")
    ver_match = re.search(r'Ver\s+(?!sin\.)([^.;]+(?:;\s[^.;]+)*)', concept_one_line)
    if ver_match:
        remissivas.extend([clean_text(s.strip()) for s in re.split(r';\s*', ver_match.group(1)) if s.strip()])

    remissivas = list(dict.fromkeys([r for r in remissivas if r]))

    # Adicionar ao json
    glossary[name] = {
        "Traduções": translations,
        "Descrição": description,
        "Género": gender,
        "Número": number,
        "Sinónimos": synonyms,
        "Notas": notes,
        "Sigla": acronym,
        "Remissivas": remissivas
    }

json_output = json.dumps(glossary, ensure_ascii=False, indent=4)

with open('monitoramento-e-avaliacao-glossario.json', 'w', encoding='utf-8') as f:
    f.write(json_output)

