
import re
import json

def parse_dictionary(file_content):
    entries = file_content.split('@\n')
    dictionary = {}
    print(len(entries))
    #print(entries)
    
    for entry in entries[1:]:  # Ignorar o primeiro split vazio
        if not entry.strip():
            continue

        # Deteção do conceito (pode estar dividido em múltiplas linhas)
        concept_match = re.search(
            r'<height="\d+" font="\d+"><b>\s*(.*)\s*</b>(\n<.*><b>(.*)</b>)?',
            entry
        )
        if not concept_match:
            continue

        # marcas para conseguir extrair as traduções árabes que têm números/letras pelo meio, porque não dá para distinguir de outra maneira
        # à frente ou tem a categoria, o CAS ou nc
        entry = re.sub(r'<(.*)><i>\s*CAS\s*</i>', r'€\n<\1><i>CAS</i>', entry)
        entry = re.sub(r'<(.*)>([A-ZÀ-Ú\s]+)\.([^\.]*)', r'€\n<\1>\2.\3', entry)
        entry = re.sub(r'<(.*)><i>(nc|sbl)', r'€\n<\1><i>\2', entry)
        

        # Processar o conceito (pode conter múltiplas partes)
        concept = concept_match.group(1).strip()
        if concept_match.group(2):
            concept = concept + " " + concept_match.group(3).strip() 
            # para ficar um espaço entre as palavras independentemente dos espaços que possam estar no xml
        #print(concept)



        entry_data = {}  # Inicializamos sem campos vazios

        
        # Categoria Lexical
        lexical_category_match = re.search(r'<height="16" font="12"><i>(.*?)</i>', entry)
        if lexical_category_match and lexical_category_match.group(1).strip():
            entry_data["Categoria Lexical"] = lexical_category_match.group(1).strip()
        
        

        # Traduções 
        translations = {}
        current_lang = None
        current_translation = []
        collecting = False

        # Dividir o conteúdo por linhas para processar sequencialmente
        lines = entry.split('\n')
        for line in lines:
            lang_match = re.search(r'<i>(oc|eu|gl|es|en|fr|pt|nl|ar)\s*\[?(PT|BR)?\]?\s*</i>', line)
            if lang_match:
                if current_lang and current_translation:
                    joined_translation = ' '.join(current_translation).strip()
                    if joined_translation:
                        if current_lang not in translations:
                            translations[current_lang] = []
                        translations[current_lang].append(joined_translation)
                
                # Reiniciar para a nova língua
                lang = lang_match.group(1)
                if lang_match.group(2):  # Se tem variante (PT/BR)
                # AMY-101 -> único caso em que a variante [PT] ou [BR] aparece na linha da tradução e não à frente de pt -> mudar à mão
                    lang = f"{lang}_{lang_match.group(2)}"
                current_lang = lang
                current_translation = []
                collecting = True
                continue
            
            if collecting and current_lang and current_lang != "ar":
                text_match = re.search(r'>(.*?)(?:<|$)', line)
                if text_match:
                    text = text_match.group(1).strip()
                    
                    # Se a linha começa com ";", é uma nova tradução
                    if text.startswith(';'):
                        # Adicionar a tradução atual se existir
                        if current_translation:
                            joined_translation = ' '.join(current_translation).strip()
                            if joined_translation:
                                if current_lang not in translations:
                                    translations[current_lang] = []
                                translations[current_lang].append(joined_translation)
                        
                        # Começar nova tradução com o texto após o ";"
                        current_translation = [text[1:].strip()]
                    else:
                        # Adicionar à tradução atual
                        if text:
                            current_translation.append(text)
            
            elif current_lang and current_lang == "ar":
                if "€" in line:
                    current_translation = False
                    current_lang = False
                else:
                    text_match = re.search(r'<height="1[69]" font="(11|26)">(.*?)(?:<height|$)', line)
                    if text_match:
                        text = text_match.group(2).strip()
                        if current_lang not in translations:
                            translations[current_lang] = []
                        translations[current_lang].append(text.strip().replace("&#34;","'"))

        # Adicionar a última tradução se existir
        if current_lang and current_translation:
            joined_translation = ' '.join(current_translation).strip()
            if joined_translation:
                if current_lang not in translations:
                    translations[current_lang] = []
                translations[current_lang].append(joined_translation)

        # para as traduções árabes que têm números e letras pelo meio
        if "ar" in translations.keys():
            for t in translations["ar"]:
                if re.search(r'[0-9]', t) and len(translations["ar"]) > 1:
                    translations["ar"] = [translations["ar"][0] + translations["ar"][1]]

        # Processar casos especiais como o holandês com "a" em linha separada
        for lang in translations:
            # Juntar partes que foram separadas indevidamente
            new_translations = []
            i = 0
            while i < len(translations[lang]):
                trans = translations[lang][i]
                if len(trans) < 3 and i+1 < len(translations[lang]):
                    new_trans = trans + translations[lang][i+1]
                    new_translations.append(new_trans)
                    i += 2
                else:
                    new_translations.append(trans)
                    i += 1
            translations[lang] = new_translations

        # Remover línguas vazias e formatar
        translations = {k: [t for t in v if t] for k, v in translations.items() if v}
        if translations:
            entry_data["Traduções"] = translations

        # -----------------------------------------------------------------------------------------------
               
        
        # Categoria (ex: ETIOPATOGÈNIA, CLÍNICA, etc.)
        category_match = re.search(r'<height="16" font="11">([A-ZÀ-Ú\s]+)\.([^\.]*)\.', entry, re.DOTALL)
        if category_match:
            entry_data["Categoria"] = category_match.group(1).strip()
            description = category_match.group(2).strip()
            # Limpar tags HTML e normalizar espaços/quebras de linha
            description = re.sub(r'<[^>]+>', '', description)  
            description = re.sub(r'\s+', ' ', description)
            if description:
                entry_data["Descrição"] = description.strip()
        
        # Notas 
        notes = []
        note_blocks = re.findall(r'<height="14" font="27">(Nota:)?\s*(\d+\.)?\s*(.*?)(?=<height="14" font="27">|\Z)', entry, re.DOTALL)
        current_note = ""
        for _, num, text in note_blocks:
            #text = re.sub(r'<i>(\w+)</i>', r'"\1"', text) 
            text = re.sub(r'<[^>]+>', '', text)  # Remove tags
            text = re.sub(r'•', '', text) # remover bullet point (ex: anticòs)
            text = re.sub(r'\s+', ' ', text).strip()  # Normaliza espaços
            if num:  # Nova nota (ex: "1.", "2.")
                if current_note:  # Salva a nota anterior
                    notes.append(current_note)
                current_note = text
            else:  # Continuação da nota atual
                current_note += " " + text if current_note else text
        if current_note: 
            notes.append(current_note)
        if notes:
            entry_data["Notas"] = notes
        
        # Sigla
        # pode ter várias linhas
        siglas = []
        sigla_match = re.search(r'<height="16" font="11">\s?sigla\s*\n<height="16" font="25"><b>(.*?)</b>\n(<.*><b>(.*)</b>)?', entry)
        if sigla_match and sigla_match.group(1).strip():
            sigla = sigla_match.group(1).strip()
            if sigla_match.group(2):
                sigla = sigla + sigla_match.group(3).strip()
            siglas.append(sigla)
        
        # Verifica se há siglas após a primeira (separadas por ";")
        additional_siglas = re.findall(r'<height="16" font="11">;\s*\n<height="16" font="25"><b>(m?[A-Z]*?)</b>', entry)
        # m para além das maiúsculas para apanhar o mRNA também
        for match in additional_siglas:
            if match.strip() != "UVI": # exceção em que apanha isto, mas não está dentro da categoria de siglas
                siglas.append(match.strip())
        
        if siglas:
            entry_data["Sigla"] = siglas
        
        # Símbolo
        simbolo_match = re.search(r'<height="16" font="12"><i>sbl\s*</i>\n<.*>(.*?)\n(<height="(15|9)" font="[13]9">(.*)\n)?', entry)
        if simbolo_match and simbolo_match.group(1).strip():
            entry_data["Símbolo"] = simbolo_match.group(1).strip()
            if simbolo_match.group(2):
                entry_data["Símbolo"] = entry_data["Símbolo"] + simbolo_match.group(4).strip()


        # Nome Científico
        # pode ter várias linhas
        nome_cientifico_match = re.search(r'<height="16" font="12"><i>nc\s*(.*)\s*</i>\n(<.*><i>(.*)</i>)?', entry)
        if nome_cientifico_match and nome_cientifico_match.group(1).strip():
            entry_data["Nome Científico"] = nome_cientifico_match.group(1).strip()
            if nome_cientifico_match.group(2):
                entry_data["Nome Científico"] = entry_data["Nome Científico"] + " "  + nome_cientifico_match.group(3).strip()
    
        
        # Entrada Principal
        # pode ter várias linhas (ex:  veg. coronavirus 2 de la síndrome respiratòria aguda greu)
        entrada_principal_match = re.search(r'<height="16" font="11">\s*veg\.\s*\n<.*><b>(.*?)</b>\n(<.*><b>(.*)</b>)?', entry)
        if entrada_principal_match and entrada_principal_match.group(1).strip():
            entry_data["Entrada Principal"] = entrada_principal_match.group(1).strip()
            if entrada_principal_match.group(2):
                entry_data["Entrada Principal"] = entry_data["Entrada Principal"] + " "  + entrada_principal_match.group(3).strip()
    

        # Sinónimo
        sinonimo_match = re.search(r'<height="16" font="11">\s*sin\.\s*\n<height="16" font="25"><b>(.*?)</b>', entry)
        if sinonimo_match and sinonimo_match.group(1).strip():
            entry_data["Sinónimo"] = sinonimo_match.group(1).strip()
        

        # caso excecional - taxa de mortalitat - não está em bold -> corrigir à mão
        # Sinónimo Complementar 
        sinonimos_compl = []
        sinonimo_compl_match = re.search(r'<height="16" font="11">sin\. compl\.\s*<height="16" font="25"><b>(.*?)</b>\n(<.*><b>(.*?)</b>)?', entry)
        if sinonimo_compl_match and sinonimo_compl_match.group(1).strip():
            sinonimo = sinonimo_compl_match.group(1).strip()
            if sinonimo_compl_match.group(2):
                sinonimo = sinonimo + " " + sinonimo_compl_match.group(3).strip()
            sinonimos_compl.append(sinonimo)
            

            # Verificar sinónimos adicionais (separados por ";")
            additional_sinonimos = re.findall(r'<height="16" font="11">;\s*\n<height="16" font="25"><b>([^A-Z]{2}.*)</b>\n(<.*><b>(.*)</b>)?', entry) # para não captar siglas
            #print(additional_sinonimos)
            for match in additional_sinonimos:
                sinonimo = match[0] + match[2]
                sinonimos_compl.append(sinonimo)
            
            if sinonimos_compl:
                entry_data["Sinónimo Complementar"] = sinonimos_compl
        
        # Número CAS
        cas = []
        cas_match = re.search(r'<height="16" font="12"><i>\s*CAS\s*</i>\n<height="16" font="11">(.*?)\n(<.*>([0-9].*))?', entry)
        if cas_match and cas_match.group(1).strip():
            cas.append(cas_match.group(1).strip().replace(";", ""))
            if cas_match.group(2):
                cas.append(cas_match.group(3).strip())
            if cas:
                entry_data["Número CAS"] = cas

        # Denominação Comercial
        den_com_match = re.search(r'<height="16" font="11">den\. com\.\s*<.*><b>(.*?)</b>', entry)
        if den_com_match and den_com_match.group(1).strip():
            entry_data["Denominação Comercial"] = den_com_match.group(1).strip()
       
        if concept not in dictionary.keys():
            dictionary[concept] = entry_data
        else: 
            dictionary[concept] = dictionary[concept] | entry_data

    return dictionary


# Carregar o conteúdo do ficheiro
with open('doc1_organizado_v6_processado.xml', 'r', encoding='utf-8') as file:
    content = file.read()

# Processar o conteúdo
parsed_data = parse_dictionary(content)


numero_de_chaves = len(parsed_data)
print(numero_de_chaves) # 739
# não dá 743 porque o dicionário original em pdf contém entradas iguais
# nos casos que são exatamente iguais (termo e infos) a segunda foi ignorada
# nos casos em que os termos são iguais, mas as infos diferentes, as infos foram concatenadas
# casos: mascareta, immunològic -a, immune, careta

# Salvar como JSON
with open('dicionario_medico.json', 'w', encoding='utf-8') as json_file:
    json.dump(parsed_data, json_file, indent = 4, ensure_ascii = False)

print("Conversão concluída. O ficheiro JSON foi gerado.")
