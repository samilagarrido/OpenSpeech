import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
import os
from tqdm import tqdm

first_day = [28, 3, 2022] #dd/mm/yyyy
last_day = [29, 5, 2022]  #dd/mm/yyyy
size_speechs = 500 # Number of speeches per dataframe
current_page = 1
UF = ''
url = f'https://www.camara.leg.br/internet/SitaqWeb/ResultadoPesquisaDiscursos.asp?CurrentPage={current_page}&txIndexacao=&BasePesq=plenario&txOrador=&txPartido=&dtInicio={first_day[0]}/{first_day[1]}/{first_day[2]}&dtFim={last_day[0]}/{last_day[1]}/{last_day[2]}&txUF={UF}&txSessao=&listaTipoSessao=&listaTipoInterv=&inFalaPres=&listaTipoFala=&listaFaseSessao=&txAparteante=&listaEtapa=&CampoOrdenacao=dtSessao&TipoOrdenacao=ASC&PageSize={size_speechs}&txTexto=&txSumario='

class Counter_save():
    def __init__(self):
        self.count = 0
    
    def next(self):
        self.count += 1
        return self.count
        
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
    print('oi')

    link_infos= []
    link_list = []
    soup = []
    temp = []
    data_frame_list = []
    text = ''
    for i in range(asd):
        current_page = i+1
        url = f'https://www.camara.leg.br/internet/SitaqWeb/ResultadoPesquisaDiscursos.asp?CurrentPage={current_page}&txIndexacao=&BasePesq=plenario&txOrador=&txPartido=&dtInicio={first_day[0]}/{first_day[1]}/{first_day[2]}&dtFim={last_day[0]}/{last_day[1]}/{last_day[2]}&txUF={UF}&txSessao=&listaTipoSessao=&listaTipoInterv=&inFalaPres=&listaTipoFala=&listaFaseSessao=&txAparteante=&listaEtapa=&CampoOrdenacao=dtSessao&TipoOrdenacao=ASC&PageSize={size_speechs}&txTexto=&txSumario='
        soup.append(UrlToBS(url))

        for links in soup[i].find_all('a', attrs={'title':"Íntegra do Discurso"}):
            temp = (links['href'])
            for item in temp:
                text += item.replace('\t','').replace('\n','').replace('\r','').replace(' ','')
            link_list.append("https://www.camara.leg.br/internet/SitaqWeb/"+text)
            text = ''

        #link_list ta ok
        #dataframe ta ok
        dataframe = pd.read_html(url)

        save_speechs_df(link_list, dataframe[0])
        link_list = []

def get_id(link):
    id = []
    id.append('nI')
    id.append((re.findall(r'(?<=nuInsercao=)\d+', link))[0])
    id.append("nQ")
    id.append((re.findall(r'(?<=nuQuarto=)\d+', link))[0])
    id.append("nS")
    id.append((re.findall(r'(?<=nuSessao=)\d+', link))[0])
    id.append("nO")
    id.append((re.findall(r'(?<=nuOrador=)\d+', link))[0])
    return "".join(id)

def speechs_txt(link_list):
    '''create speechs in doc file'''

    txt = []
    id = []
    counter = 0
    drop = []
    
    for script in tqdm(link_list):
        # print(counter)
        url_script_html = UrlToBS(script)
        url_script = url_script_html.find_all("font")
        if (len(url_script) < 2):
            drop.append(counter)
            counter += 1
            continue

        txt.append((str((url_script[0].contents)) + "+" + str((url_script[1].contents))).replace('<br/>','').replace('<b>', '').replace('</b>', '').replace('\'', ''))
        id.append(get_id(script))
        counter += 1

    drop_return = (len(drop), drop)
    txt_return = txt
    print(len(txt))
    id_return = id

    txt = []
    id = []
    counter = 0
    drop = []
    

    return txt_return, id_return, drop_return

def save_speechs_df(links_speech, dataframe):
    '''Save speechs in a dataframe'''

    txt, id, drops = speechs_txt(links_speech)
    print(drops)
    if(drops[0] > 0):
        dataframe = dataframe.drop(drops[1])
        dataframe.reset_index(drop=True)
    print(len(txt))
    print(type(txt))
    dataframe['speechs'] = txt
    dataframe['id'] = id
    
    dataframe.to_csv(f'/home/xonas/UFPB/OpenSpeech/speech_datasets/speechs_{first_day[0]}_{first_day[1]}_{first_day[2]}_to_{last_day[0]}_{last_day[1]}_{last_day[2]}_{object.count}.csv', index=False)
    object.next()

object = Counter_save()

SpeechLinks(count_speechs())