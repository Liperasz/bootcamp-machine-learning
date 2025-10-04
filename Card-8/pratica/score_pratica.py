from bs4 import BeautifulSoup
import requests
import os
import platform

# função para puxar o html
def get_html(url):

    # Requisitando o html do site 
    html_Text = requests.get(url).text

    # Utilizando o soup para ler o html
    soup = BeautifulSoup(html_Text, 'lxml')

    return soup

# Limpa o terminal
def clear():

    system = platform.system()
    if system == "Windows":
        os.system('cls')
    else:
        os.system('clear')

# pega as seções do site
def get_sections(soup):

    # acha todas as sections
    sections = soup.find_all('section')

    # lista para as sections que eu quero
    section_list = []

    for section in sections:

        # pegar o valor da variável aria labelledby
        aria = section.get('aria-labelledby')

        # se a seção possue esse atributo e nele contém a palavra collection ou feed, então ele é uma seção de notícias
        if aria and ('collection' in aria or 'feed' in aria):

            # adiciona a lista seções
            section_list.append(section)

    return section_list

# pega as noticias de uma seção
def get_news(section):

    # pega as noticias
    news = section.find('li')

    # lista com o dicionário de cada noticia
    news_list = []

    for n in news:

        # acha primeiro o link e o título da notícia
        a = n.find('a')

        if a:
            title = a.text
            link = a['href']

        # tratamento
        else:
            title = None
            link = None


        # acha o parágrafo
        p = n.find('p')

        if p:
            paragraph = p.text

        # tratamento  
        else:
            paragraph = None

        # acha o timestamp da postagem
        d = n.find('time')

        if d:
            datetime = d.get('datetime')
            moment = d.text

        # tratamento
        else:
            datetime = None
            moment = None

        # dicionário da notícia
        news_dicionary = {
            'title': title,
            'link': link,
            'paragraph': paragraph,
            'datetime': datetime,
            'moment': moment
        }

        # adiciona o dicionário a lista
        news_list.append(news_dicionary)

    return news_list




if __name__ == '__main__':

    # url para buscar o site da bbc
    url = 'https://www.bbc.com/portuguese'
    

    soup = get_html(url)
    sections = get_sections(soup)

    for section in sections:

        print(get_news(section))