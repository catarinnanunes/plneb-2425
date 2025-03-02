import re

def limpa_descricao(descricao):
    descricao=descricao.strip() # remove espaços no inicio e no fim
    descricao=re.sub(r'\n', ' ',descricao) # substitui quebras de linha por espaços
    return descricao


file = open("dicionario_medico.txt", encoding="utf-8")
texto = file.read()

# LIMPEZA
# em vez de fazer: texto = re.sub(r'\f', '', texto)
texto = re.sub(r"[^\f]\n\f", r"\n", texto)  # qualquer caracter (exceto \f) seguido de \n\f

# MARCAR com @
texto = re.sub(r'\n\n', r'\n\n@', texto)
# texto = re.sub(r'\n\n+', '\n\n@', texto)  # Marcar conceitos com "@"


# EXTRAIR CONCEITOS
# em vez de: conceitos_raw =re.findall(r'@(.*)\n([^@]*)',texto)
conceitos_raw = re.findall(r"@(.+)\n([^@]+)",texto)
conceitos = [(designacao.strip(),limpa_descricao(descricao)) for designacao, descricao in conceitos_raw]
print(conceitos[0:40])

# gerar HTML
def gera_ftml(conceitos):
    html_header = """
        <!DOCTYPE html>
            <head>
            <meta charset="UTF-8">
            </head>
            <body>
            <h3>Dicionario de conceitos medicos</h3>
            <p>Dicionario para a aula de PLNEB 2024/2025</p>"""
    html_conceitos = ""
               
    for designacao, descricao in conceitos:
        html_conceitos += f"""
                    <div>
                        <p><b>{designacao}</b></p>
                        <p>{descricao}</p>                
                    </div>
                    <hr/>
                """
        html_footer = """
                </body>
            </html>
        """
        
    return html_header + html_conceitos + html_footer

html = gera_ftml(conceitos)
f_out = open("dicionario_medico.html", "w", encoding="utf-8")
f_out.write(html)
f_out.close()

file.close()