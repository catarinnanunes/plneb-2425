import re
 
def ordenar_colunas(nome_ficheiro_entrada, nome_ficheiro_saida):
    try:
        with open(nome_ficheiro_entrada, 'r', encoding='utf-8') as f:
            xml_content = f.read()
    except FileNotFoundError:
        print(f"Erro: Ficheiro não encontrado: {nome_ficheiro_entrada}")
        return []

    paginas = re.findall(r'(<page.*?>(?:.|\n)*?</page>)', xml_content, re.IGNORECASE)

    novo_xml = '<document>\n'
    for pagina in paginas:
        novo_xml += f'<page>\n'
        novo_xml += '<coluna_esquerda>\n'
        coluna_esquerda_texto = []
        coluna_direita_texto = []

        # Extrair todos os elementos text com atributos
        elementos_texto = re.findall(
        r'<text.*?top="(\d+\.?\d*)".*?left="(\d+\.?\d*)".*?width="(\d+\.?\d*)".*?height="(\d+\.?\d*)".*?font="(\d+\.?\d*)".*?>(.*?)</text>',
        pagina, re.DOTALL | re.IGNORECASE
        )


        for top, left, width, height, font, texto in elementos_texto:
            criterio1 = re.search(r'[0-9]{1,3}', texto)
            criterio2 = re.search(r'(?!(675|271)")\d+', left)
            criterio3 = re.search(r'(?!(23|16)")\d+', width) 
            criterio4 = re.search(r'veg\.', texto) 
            criterio5 = re.search(r'sigla', texto) 
            criterio6 = re.search(r'sin\.', texto) 

            if criterio1 and criterio2 and criterio3 or criterio4 or criterio5 or criterio6: # número da entrada ou veg.
                limite_coluna = 440
            else:
                limite_coluna = 468
            left_valor = float(left)
            atributos_texto = f' top="{top}" left="{left}" width="{width}" height="{height}" font="{font}"'
            if left_valor < limite_coluna:
                coluna_esquerda_texto.append(f'<text{atributos_texto}>{texto}</text>')
            elif left_valor > limite_coluna:
                coluna_direita_texto.append(f'<text{atributos_texto}>{texto}</text>')

        novo_xml += '\n'.join(coluna_esquerda_texto) + '\n'
        novo_xml += '</coluna_esquerda>\n'
        novo_xml += '<coluna_direita>\n'
        novo_xml += '\n'.join(coluna_direita_texto) + '\n'
        novo_xml += '</coluna_direita>\n'
        novo_xml += f'</page>\n'
        novo_xml += '</document>\n'

    try:
        with open(nome_ficheiro_saida, 'w', encoding='utf-8') as f:
            f.write(novo_xml)
    except IOError:
        print(f"Erro: Não foi possível escrever no ficheiro: {nome_ficheiro_saida}")

nome_ficheiro_xml_entrada = "doc1.xml"
nome_ficheiro_xml_saida = "doc1_organizado_v6.xml"
ordenar_colunas(nome_ficheiro_xml_entrada, nome_ficheiro_xml_saida)

print(f"Ficheiro XML organizado criado: {nome_ficheiro_xml_saida}")
