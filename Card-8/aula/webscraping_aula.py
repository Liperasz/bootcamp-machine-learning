from bs4 import BeautifulSoup
import requests
import time
import os

# Pedindo uma skill para o usuário
print("Put some skill that you are not familiar with")

# Pega o valor que o usuário desseja passar como skill
unfamiliar_skill = input('>')

print(f"Filtering out {unfamiliar_skill}")

def find_jobs():

    # Requisitando o html do site 
    html_Text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=ft&searchTextText=Python&txtKeywords=Python%2C&txtLocation=').text

    # Utilizando o soup para ler o html
    soup = BeautifulSoup(html_Text, 'lxml')

    # Achando todos os "cards" de emprego
    jobs = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')

    for index, job in enumerate(jobs):

        # pegando a data de publicação do span
        published_date = job.find('span', class_ = 'sim-posted').span.text.replace(' ','')
        if 'few' in published_date:


            # achando o nome da compania desse primeiro emprego.
            company_name = job.find('h3', class_ = 'joblist-comp-name').text.replace(' ','')

            # achando as skills desse emprego. OBS: diferente da aula, o site nao utiliza mais span, e sim div para guardar as skils, e o nome também está diferente.
            skills = job.find('div', class_ = 'more-skills-sections').text.replace(' ','')

            # pegando o link de mais informações
            more_info = job.header.h2.a['href']

            # se a skill que não é familiar para o usuário, não está no emprego, ela não aparece
            if unfamiliar_skill not in skills:

                with open(f'posts/{index}.txt', 'w') as f:


                    f.write(f"Company name: {company_name.strip()} \n")
                    f.write(f"Required Skills: {skills.strip()} \n")
                    f.write(f'More info: {more_info}\n')

                print("File saved: {index}")

if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait = 10
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait * 60)
