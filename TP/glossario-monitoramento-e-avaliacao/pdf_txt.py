import re

def processar_glossario(conteudo):
    """
    Função que:
    1. Remove cabeçalhos, rodapés e formatação indesejada
    2. Normaliza os espaços e quebras de linha
    3. Adiciona marcadores aos conceitos para posterior processamento
    """

    # 1. Limpeza inicial 
    conteudo = re.sub(r'^\d+\s*$', '', conteudo, flags=re.MULTILINE)  # Números de página
    conteudo = re.sub(r'^\f', '', conteudo, flags=re.MULTILINE)       # Caracteres especiais
    conteudo = re.sub(r'^Monitoramento e Avaliação\s*$', '', conteudo, flags=re.MULTILINE) #texto do cabeçalho
    conteudo = re.sub(r'^lossário Temático\s*$', '', conteudo, flags=re.MULTILINE)
    conteudo = re.sub(r'^[A-Za-zÀ-ÿ]\s*$', '', conteudo, flags=re.MULTILINE)  # Letras únicas - de indentificação de nova letra
    conteudo = re.sub(r'^[A-Za-zÀ-ÿ]{3}\s*$', '', conteudo, flags=re.MULTILINE)  # Palavras de 3 letras, do cabeçalho
    conteudo = re.sub(r'^[A-Za-zçãáéíóúâêôûõàèìòùäëïöü ]+ G$', '', conteudo, flags=re.MULTILINE)  # Letras soltas que terminam com " G", há sempre em todas as páginas
    
    # 2. Espaços e quebras de linha
    conteudo = re.sub(r'[ \t]+', ' ', conteudo)  # Múltiplos espaços/tabs -> um espaço
    conteudo = re.sub(r' \n', '\n', conteudo)    # Remove espaços antes de quebras
    conteudo = re.sub(r'\n{3,}', '\n\n', conteudo)  # Reduz múltiplas quebras de linha
    conteudo = conteudo.strip()  # Remove linhas vazias no início/final
    
    # 3. Processamento adicional 
    # Padrão para identificar linhas de conceito 
    padrao_conceito = re.compile(r'^([^,]+),\s(fem\.|masc\.)')
    linhas = conteudo.split('\n')
    texto_marcado = []
    
    for i, linha in enumerate(linhas):
        linha = linha.strip()
        if not linha:
            continue  # Ignorar linhas vazias
            
        if padrao_conceito.match(linha):
            # Adicionar marcador antes de cada novo conceito
            if texto_marcado:  # Se já há conteúdo, adiciona linha a separar
                texto_marcado.append('')
            texto_marcado.append(f"### {linha}")
        else:
            texto_marcado.append(linha)
    
    # 4. Limpeza 
    resultado = '\n'.join(texto_marcado)
    resultado = re.sub(r'[ \t]+', ' ', resultado)  # espaços iguais
    resultado = re.sub(r'\n ', '\n', resultado)    # Remover espaços no início de linhas
    resultado = re.sub(r'\n{3,}', '\n\n', resultado)  # Garantir no máximo 2 quebras seguidas
    
    return resultado

with open('ficheiro.txt', 'r', encoding='utf-8') as file:
    conteudo = file.read()

conteudo_processado = processar_glossario(conteudo)

with open('m_glossario_processado.txt', 'w', encoding='utf-8') as file:
    file.write(conteudo_processado)

