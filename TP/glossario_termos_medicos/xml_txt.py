import re

with open('glossario_termos.xml', 'r', encoding='utf-8') as f:
    xml_content = f.read()

# 1. Remove todo o cabeçalho até a primeira letra do alfabeto
xml_content = re.sub(r'^.*?<text top="\d+" left="\d+" width="\d+" height="\d+" font="\d+"><b>[A-Z]<\/b><\/text>', '', xml_content, flags=re.DOTALL)

# 2. Remove as letras do alfabeto (A, B, C...)
xml_content = re.sub(r'<text[^>]*font="\d+"[^>]*><b>[A-Z]<\/b><\/text>', '', xml_content)

# 3. Remove todas as tags <i> e </i> (itálico)
xml_content = re.sub(r'</?i>', '', xml_content)

# 4. Remove as tags <text>
xml_content = re.sub(r'</?text[^>]*>', '', xml_content)

# 5. Remove todas as tags <page> e </page>
xml_content = re.sub(r'</?page[^>]*>', '', xml_content)

# 6. Remove linhas vazias e espaços extras
xml_content = re.sub(r'\n\s*\n', '\n', xml_content).strip()

with open('termos_medicos_populares.txt', 'w', encoding='utf-8') as f:
    f.write(xml_content)