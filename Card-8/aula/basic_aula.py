from bs4 import BeautifulSoup

# abrindo o arquivo html com a função "read"
with open('home.html', 'r') as html_file:

    "função que lê o html"
    content = html_file.read()

    # lendo o arquivo html como lxml agora, através da beautifulsoup, que organiza melhor a leitura
    soup = BeautifulSoup(content, 'lxml')
     
    # achando todos os cards
    course_cards = soup.find_all('div', class_='card')

    for course in course_cards:
        # printando o nome do curso e o preço
        course_name = course.h5.text
        course_price = course.a.text.split()[-1]

        print(f'{course_name} costs {course_price}')