from bs4 import BeautifulSoup
import requests

# Requisitando o html do site 
html_Text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=ft&searchTextText=Python&txtKeywords=Python%2C&txtLocation=').text

# Utilizando o soup para ler o html
soup = BeautifulSoup(html_Text, 'lxml')

# Achando todos os "cards" de emprego
jobs = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')

for job in jobs:
    # Aqui eu também substitui pelo get_text para arrumar a formatação.
    published_date = job.find('span', class_ = 'sim-posted').span.get_text(strip=True)
    if 'few' in published_date:


        # achando o nome da compania desse primeiro emprego. Tive que alterar o método replace pelo get_text(strip=True) para correta formatação
        company_name = job.find('h3', class_ = 'joblist-comp-name').get_text(strip=True)

        # achando as skills desse emprego. OBS: diferente da aula, o site nao utiliza mais span, e sim div para guardar as skils, e o nome também está diferente.
        skills = job.find('div', class_ = 'more-skills-sections').text.replace(' ', '')



        print(f'''

        Company name: {company_name}
        Required skills: {skills}

        ''')

        print('')