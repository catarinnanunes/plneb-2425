import re
import json

# ler o ficheiro xml
file = open("doc1_organizado_v6.xml", encoding="utf8")
texto = file.read()
file.close()

# tirar à mão a parte inicial e final que não interessam, deixar só o glossário

dici_medico = {}

# --------------------------------------------------------------------------------

# remover as páginas

texto = re.sub(r'</?[cd][\n\S]*>','', texto)

# --------------------------------------------------------------------------------

# remover cabeçalhos (letra e nome dicionário)

texto = re.sub(r'<text[^>]*height="(19|72)" font="(14|15|16)">.*</text>', "", texto)
texto = re.sub(r'<[^>]*font="3[68]".*>[A-Z]<.*>', "", texto) # colocar a fonte para diferenciar dos R0 e Rt

# --------------------------------------------------------------------------------

# remover os números de página
texto = re.sub(r'<text top="1149" left="\d+" width="\d+" height="25" font="6">\d+</text>', "", texto)

# --------------------------------------------------------------------------------

# remover linhas vazias (ex: <text top="705" left="123" width="3" height="16" font="11"> </text>)

texto = re.sub(r'<.*>(<[ib]>)?\s+(</[ib]>)?</text>', '', texto)


# --------------------------------------------------------------------------------

# remover espaços entre páginas
texto = re.sub(r'</text>\n{2,}<text', "</text>\n<text", texto)


# --------------------------------------------------------------------------------

# separar cada nova entrada por @
texto = re.sub(r'<text top="\d+" left="(?!(675|271)")\d+" width="(?!(23|16)")\d+" height="\d+" font="11">\d+\s{0,2}</text>', "@", texto)


# --------------------------------------------------------------------------------

# remove os text todos menos a parte da height e font para diferenciar (os outros parâmetros são muito aleatórios)
texto = re.sub(
    r'<text[^>]*height="(\d+)"[^>]*font="(\d+)"[^>]*>(.*?)</text>',
    r'<height="\1" font="\2">\3',
    texto
)


# --------------------------------------------------------------------------------

# guardar em ficheiro json
f_out = open("doc1_organizado_v6_processado.xml", "w", encoding="utf-8")
f_out.write(texto)
f_out.close()
