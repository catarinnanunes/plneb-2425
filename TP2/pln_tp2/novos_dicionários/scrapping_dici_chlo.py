from bs4 import BeautifulSoup
import requests
import json


def get_info(num):
    url = "https://www.chlo.min-saude.pt/index.php/component/seoglossary/1-glossario?start=" + str(num)

    # sem os headers dá Forbidden
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }   

    response = requests.get(url, headers=headers)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    #print(soup)
    dici = {}

    tabela_termos = soup.find("table", class_ = "glossaryclear table")

    for entrada in tabela_termos.find_all("tr", class_=["row0", "row1"]):
        termo = entrada.td.a.text.strip()
        # definicao = entrada.td.div.p.text.strip()
        if entrada.find("p"):
            definicao = entrada.find("p").text.strip().replace(" ", " ")
        else: # caso excecão do termo "Optocinético"
            div = entrada.find("div", class_ = "dolAcepsRightCell")
            definicao = div.span.span.span.text.strip()
        print(termo, definicao)

        dici[termo] = {"Definição": definicao}
    return dici


dici_total = {}
# tem 15 entradas por página, portanto começa no 0, 15, 30, etc até 375
for num in range(0, 376, 15):
    # print(num)
    termos = get_info(num)
    dici_total = dici_total | termos  # junta os dicionários


f_out = open("dici_chlo.json", "w", encoding="utf-8")
json.dump(dici_total, f_out, indent = 4, ensure_ascii = False)
f_out.close()
