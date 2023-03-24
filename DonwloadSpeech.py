import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
import os

class FileNumber:
    def __init__(self, count_file = 0):
        self.count_file = count_file

    def next(self):
        self.count_file += 1


first_day = [28, 3, 2022] #dd/mm/yyyy
last_day = [28, 4, 2022]  #dd/mm/yyyy
size_speechs = 100 # Number of speeches per dataframe
current_page = 1
UF = ''
url = f'https://www.camara.leg.br/internet/SitaqWeb/ResultadoPesquisaDiscursos.asp?CurrentPage={current_page}&txIndexacao=&BasePesq=plenario&txOrador=&txPartido=&dtInicio={first_day[0]}/{first_day[1]}/{first_day[2]}&dtFim={last_day[0]}/{last_day[1]}/{last_day[2]}&txUF={UF}&txSessao=&listaTipoSessao=&listaTipoInterv=&inFalaPres=&listaTipoFala=&listaFaseSessao=&txAparteante=&listaEtapa=&CampoOrdenacao=dtSessao&TipoOrdenacao=ASC&PageSize={size_speechs}&txTexto=&txSumario='

def UrlToBS(url):
    '''Return a beautifulsoup object'''
    html = requests.get(url)
    #content = html.content
    return BeautifulSoup(html.content, 'html.parser')

def count_speechs():
    '''Returns the Amount of Speech's Dataframes - ASD'''

    count_of_speechs= []
    count_of_speechs_value = 0
    soup = UrlToBS(url)
    for links in soup.find_all('span', attrs={'class':"visualStrong"}):
        count_of_speechs.append(links.contents)
    count_of_speechs_value = int((count_of_speechs[len(count_of_speechs)-1][0]).replace('.',''))
    asd = int(count_of_speechs_value/size_speechs)  + 1

    return asd

def SpeechLinks(asd):
    '''Return a list with links per speech'''

    link_infos= []
    soup = []
    temp = []
    for i in range(asd):
        current_page = i+1
        url = f'https://www.camara.leg.br/internet/SitaqWeb/ResultadoPesquisaDiscursos.asp?CurrentPage={current_page}&txIndexacao=&BasePesq=plenario&txOrador=&txPartido=&dtInicio={first_day[0]}/{first_day[1]}/{first_day[2]}&dtFim={last_day[0]}/{last_day[1]}/{last_day[2]}&txUF={UF}&txSessao=&listaTipoSessao=&listaTipoInterv=&inFalaPres=&listaTipoFala=&listaFaseSessao=&txAparteante=&listaEtapa=&CampoOrdenacao=dtSessao&TipoOrdenacao=ASC&PageSize={size_speechs}&txTexto=&txSumario='
        soup.append(UrlToBS(url))
        for links in soup[i].find_all('a', attrs={'title':"Íntegra do Discurso"}):
            temp.append((links['href']))
        link_infos.append(temp)
        temp = []

    #>>Cleaning links to access a speech

    linkDiscurso = []
    temp = []
    for i in range(asd):
        for item in link_infos[i]:
            text = item.replace('\t','').replace('\n','').replace('\r','').replace(' ','')
            temp.append(("https://www.camara.leg.br/internet/SitaqWeb/"+text))
        linkDiscurso.append(temp)
        
        temp = []

    return linkDiscurso

def speechs_txt(link_list):
    '''create speechs in doc file'''

    file_number = FileNumber(len(os.listdir('speechs')))

    txt = []
    for script in link_list:
        url_script_html = UrlToBS(script)
        url_script = url_script_html.find_all("font")
        if (len(url_script) < 2):
            print(file_number.count_file)
            print(url_script_html)
            print(script)
            print(url_script)
            print("É menor que 2")
            continue
        txt.append((str((url_script[0].contents)) + "+" + str((url_script[1].contents))).replace('<br/>','').replace('<b>', '').replace('</b>', '').replace('\'', ''))
    for i in txt:
        textfile = open(f"./speechs/file_{file_number.count_file}.txt", "w")
        textfile.write(i + "\n")
        textfile.close()
        file_number.next()

link_list = SpeechLinks(count_speechs())

if not('speechs' in os.listdir()):
    os.mkdir('speechs/')
    for i in range(count_speechs()-1):
        print(i)
        speechs_txt(link_list[i])
else:
    for i in range(int(len(os.listdir('speechs/'))/100),count_speechs()-1):
        print(i)
        speechs_txt(link_list[i])