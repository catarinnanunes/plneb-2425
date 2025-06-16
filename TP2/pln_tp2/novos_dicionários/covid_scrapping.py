# neste caso, o código fonte da página não contém a parte do glossário, porque este é carregado dinamicamente com JavaScript

from bs4 import BeautifulSoup
import requests
import json

# url = "https://www.hospitaldaluz.pt/pt/saude-e-bem-estar/glossario-para-covid-19"
# não dá para ir pelo url do site, tem se ser pela API que tem o JSON com o glossário
url = "https://www.hospitaldaluz.pt/pt/API/Service/Article/SiteArticle?id=glossario-para-covid-19"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": "https://www.hospitaldaluz.pt/pt/saude-e-bem-estar/glossario-para-covid-19",
    "X-Requested-With": "XMLHttpRequest",
    "requestverificationtoken": "v3G7yS3qUyx_2ydXxJhy-GCvMVqkOI3KkS48ZpOcQ18f2KzCxRcAxCnIUjQVj1OcqDJLQg2"
}

cookies = {
    "_gcl_au": "1.1.811502651.1745685244",
    "_hjSessionUser_3458987": "eyJpZCI6IjRkMDA3ZTc3LTY1NTQtNThmOC1hNGZkLTc1NTBkY2Y2OTM1NCIsImNyZWF0ZWQiOjE3NDU2ODUyNDQ0NTcsImV4aXN0aW5nIjp0cnVlfQ==",
    ".ASPXANONYMOUS": "ABSKkSRvRFRtFfbYHdmZZZoPN8KOv3yPS4uy4_e8eS4hkR6DSYpeRs7h32q5Q_7d8xerQtl6s_zO4z3bg-GvcRt-KucpmCcPg-Ph2Xq4SJwM8p5P0",
    "ai_user": "WyfiI8pzxJ8t9Swn2tK8NA|2025-06-12T13:00:46.886Z",
    "_gid": "GA1.2.1289453156.1749733247",
    "ApplicationGatewayAffinityCORS": "41e051abe8e0900f93d1944902d3a691",
    "ApplicationGatewayAffinity": "41e051abe8e0900f93d1944902d3a691",
    "dnn_IsMobile": "False",
    "language": "pt-PT",
    "LSVisitor": "25ea3b9e-5f68-4b0c-a05d-3039009e9336",
    "__RequestVerificationToken": "3tiF6LWKsxWSPjmkqHYEJNydHHzrmHFcqJTL-83w9pvcn-x-E91OVWjva5SUo2LOujlItQ2",
    "_ga": "GA1.1.28380027.1745685244",
    "_hjSession_3458987": "eyJpZCI6IjAzNjk1NDMxLWFjNmItNDRiMC04MjA0LTY5YTg1MDhkZjRmNSIsImMiOjE3NDk4MTY3Njc2MzAsInMiOjEsInIiOjEsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=",
    "_ga_NFC55J900V": "GS2.1.s1749816760$o6$g1$t1749817909$j60$l0$h0",
    "ai_session": "cAYJg7mmzwAlo+IwyDZ13Q|1749816703921|1749817909951"
}


response = requests.get(url, headers=headers, cookies=cookies)
print("Status code:", response.status_code)

if response.status_code == 200:
    try:
        data = response.json()
        print("JSON keys:", data.keys())  # Verifica as chaves do JSON

        # Aceder ao texto do glossário
        modules = data['Result']['Modules']
        glossario_html = ""
        for module in modules:
            for content in module.get('Content', []):
                glossario_html += content.get('Text', '')

        print("HTML content length:", len(glossario_html))
        print("HTML content preview:", glossario_html[:500])

        soup = BeautifulSoup(glossario_html, 'html.parser')
        print("Soup text:", soup.get_text())

        # extrair os termos e definições
        dici = {} 
        termos_definicoes = []
        for li in soup.find_all('li'):
            dici_termo = {}
            strong = li.find('strong')
            if strong:
                termo = strong.text.strip()
                # Remove o termo em <strong> do texto do <li>
                # definicao = li.get_text(separator=" ", strip=True).replace(termo, "", 1).strip(" -–—:;")
                definicao = li.text.replace(termo, "", 1).strip(" - -–—:;").strip()
                termos_definicoes.append((termo, definicao))
                dici_termo["Definição"] = definicao
                dici[termo] = dici_termo

        # Exemplo: imprimir os primeiros 5 termos e definições
        for termo, definicao in termos_definicoes[:5]:
            print(f"Termo: {termo}\nDefinição: {definicao}\n")

        # guardar o dicionário
        f_out = open("dici_covid_hluz.json", "w", encoding="utf-8")
        json.dump(dici, f_out, indent = 4, ensure_ascii = False)
        f_out.close()

    except Exception as e:
        print("Erro ao decodificar JSON:", e)
else:
    print("Erro ao aceder ao recurso.")


