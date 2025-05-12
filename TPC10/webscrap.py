import requests
from bs4 import BeautifulSoup
import json
import time

# url da página com os artigos do volume
volume_url = "https://revista.spmi.pt/index.php/rpmi/issue/view/135"

# Função para limpar texto
def clean_text(text):
    return ' '.join(text.strip().split())

# Função para extrair informações do artigo
def extract_article_data(article_url):
    response = requests.get(article_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = {}

    # Título
    title_tag = soup.find('h1', class_='page_title')
    
    if title_tag:
        data['title'] = clean_text(title_tag.text)

    # DOI
    doi_section = soup.find('section', class_='item doi')
    if doi_section and doi_section.a:
        data['doi'] = doi_section.a['href'] 

    # Keywords
    keywords_section = soup.find('section', class_='item keywords')
    if keywords_section:
        data['keywords'] = []
        for k in keywords_section.text.replace("Keywords:", "").split(","):
            keyword = clean_text(k) 
            if keyword:
                data['keywords'].append(keyword)
        
    # Abstract
    abstract_section = soup.find('section', class_='item abstract')
    if abstract_section:
        data['abstract'] = clean_text(abstract_section.text.replace("Abstract", ""))

    # Data de publicação
    published_section = soup.find('div', class_='item published')
    if published_section:
        data['date_published'] = clean_text(published_section.text.replace("Published", "")) 

    return data

# todos os links dos artigos da página do volume
response = requests.get(volume_url)
soup = BeautifulSoup(response.text, 'html.parser')

articles = []

article_list = soup.find_all('div', class_='obj_article_summary')

for article_div in article_list:
    link_tag = article_div.find('h3', class_='title').a
    # print(link_tag) 
    # <a href="https://revista.spmi.pt/index.php/rpmi/article/view/2723" id="article-2723">
    # Revisão pelos Pares e Cidadania Científica
    # </a>
    article_url = link_tag['href']
    # print(article_url)
    # https://revista.spmi.pt/index.php/rpmi/article/view/2723 
    article_data = extract_article_data(article_url)
    articles.append(article_data)

# guardar em json
with open('artigos_rpmi.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=4)

print("Dados guardados em 'artigos_rpmi.json'")
