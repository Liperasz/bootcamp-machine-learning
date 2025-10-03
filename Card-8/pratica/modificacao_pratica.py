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

# função para achar os empregos
def find_jobs(soup):

    job_list = []

    # Achando todos os "cards" de emprego
    jobs = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')

    for job in jobs:

        # achando o nome da compania desse primeiro emprego. 
        # Utilizei agora a funcão join para fazer a limpeza correta e separar corretamente o nome da empresa.
        company_name = ' '.join(job.find('h3', class_ = 'joblist-comp-name').text.split())

        # achando as skills desse emprego.
        # Arrumei aqui também o espaçamento com a mesma função.
        skills = ' '.join(job.find('div', class_ = 'more-skills-sections').text.split())

        # pegando o link de mais informações
        more_info = job.header.h2.a['href']

        # salvando em um dicionário agora
        job_dic = {
            'name': company_name,
            'skills': skills,
            'info': more_info

        }

        job_list.append(job_dic)
        save_file(job_dic)

    return job_list

    
# função que monta a interface inicial
def interface(jobs):

    clear()

    print('What filter do you want to use?\n\n')
    print('0 - exit program')
    print('1 - familiar skills')
    print('2 - unfamiliar skill')
    
    r = int(input(' > '))

    # escolhe uma opção
    match r:
        case 0:

            print('Exiting program...')
            return 0
        
        case 1:

            print('Enter a familiar skill')
            skill = input(' > ')
            filter(jobs, 1, skill)
            return 1
            
        
        case 2: 

            print('Enter a unfamiliar skill')
            skill = input(' > ')
            filter(jobs, 2, skill)

            return 2
        
        case _:
            print('Invalid value')
            return -1
        
# Limpa o terminal
def clear():

    system = platform.system()
    if system == "Windows":
        os.system('cls')
    else:
        os.system('clear')

# função que busca com filtro na skill
def filter(jobs, filter, skill):

    # para cada emprego
    for job in jobs:

        # verifica o tipo do filtro

        if filter == 1:  # familiar skills

            # verifica se emprego bate com o filtro
            if skill.lower() in job['skills'].lower(): # lower para melhor verificação

                print(f"Company name: {job['name']}")
                print(f"Required Skills: {job['skills']}")
                print(f"More info: {job['info']}\n")

        elif filter == 2:  # unfamiliar skill

            if skill.lower() not in job['skills'].lower():

                print(f"Company name: {job['name']}")
                print(f"Required Skills: {job['skills']}")
                print(f"More info: {job['info']}\n")

    input('Aperte alguma tecla para continuar...')


# função para salvar os dados em um arquivo
def save_file(job):

    with open(f'posts/jobs.txt', 'a') as f:

        f.write(f"Company name: {job['name'].strip()} \n")
        f.write(f"Required Skills: {job['skills'].strip()} \n")
        f.write(f'More info: {job['info']}\n')

        f.write('\n')

        print("Saving to:", os.path.abspath("posts/jobs.txt"))



# Se esse foi o arquivo main na abertura do programa
if __name__ == '__main__':

    # url para buscar
    url = 'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=ft&searchTextText=Python&txtKeywords=Python%2C&txtLocation='
    
    # chama as funções
    soup = get_html(url)
    jobs = find_jobs(soup)

    while True:

        # só fecha se o usuário quiser fechar o programa
        r = interface(jobs)
        if r == 0:
            break