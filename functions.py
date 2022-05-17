import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
import os

#global qpt #quantidade de paginas totais
#qpt = 0
data_inicio = [28, 3, 2022]
data_fim = [28, 4, 2022]
tamanho = 100
current_page = 1
UF = ''
url = f'https://www.camara.leg.br/internet/SitaqWeb/ResultadoPesquisaDiscursos.asp?CurrentPage={current_page}&txIndexacao=&BasePesq=plenario&txOrador=&txPartido=&dtInicio={data_inicio[0]}/{data_inicio[1]}/{data_inicio[2]}&dtFim={data_fim[0]}/{data_fim[1]}/{data_fim[2]}&txUF={UF}&txSessao=&listaTipoSessao=&listaTipoInterv=&inFalaPres=&listaTipoFala=&listaFaseSessao=&txAparteante=&listaEtapa=&CampoOrdenacao=dtSessao&TipoOrdenacao=ASC&PageSize={tamanho}&txTexto=&txSumario='

def qtd_discursos(qpt):
    #>>Retorna quantidade de discursos da busca

    quantidade_de_discursos= []
    qtd_discursos_totais = 0
    soup = UrlToBS(url)
    for links in soup.find_all('span', attrs={'class':"visualStrong"}):
        quantidade_de_discursos.append(links.contents)
    qtd_discursos_totais = int((quantidade_de_discursos[len(quantidade_de_discursos)-1][0]).replace('.',''))
    qpt = int(qtd_discursos_totais/tamanho)  + 1

    return qpt

def SearchSpeech(data_inicio, data_fim, tamanho, qpt, UF= '', current_page = 1):

    #>>Obtenção da url dinâmica

    #formato de data = {dd, mm, aaaa}
    data_inicio = [28, 3, 2022]
    data_fim = [28, 4, 2022]
    #tamanho = quantidade de linhas de informações por página (limite 1788 pq? não sabemos)
    tamanho = 100
    current_page = 1
    #Estado onde será realizada a pesquisa ('' para todos)
    UF = ''
    url = f'https://www.camara.leg.br/internet/SitaqWeb/ResultadoPesquisaDiscursos.asp?CurrentPage={current_page}&txIndexacao=&BasePesq=plenario&txOrador=&txPartido=&dtInicio={data_inicio[0]}/{data_inicio[1]}/{data_inicio[2]}&dtFim={data_fim[0]}/{data_fim[1]}/{data_fim[2]}&txUF={UF}&txSessao=&listaTipoSessao=&listaTipoInterv=&inFalaPres=&listaTipoFala=&listaFaseSessao=&txAparteante=&listaEtapa=&CampoOrdenacao=dtSessao&TipoOrdenacao=ASC&PageSize={tamanho}&txTexto=&txSumario='

    #>>Requisitando o código fonte da url pelo BS

    html = requests.get(url)
    content = html.content
    soup = BeautifulSoup(content, 'html.parser')


    #>>Retorna o dataframe

    data_frame = [None]*qpt
    for i in range(qpt):
        current_page = i+1
        url = f'https://www.camara.leg.br/internet/SitaqWeb/ResultadoPesquisaDiscursos.asp?CurrentPage={current_page}&txIndexacao=&BasePesq=plenario&txOrador=&txPartido=&dtInicio={data_inicio[0]}/{data_inicio[1]}/{data_inicio[2]}&dtFim={data_fim[0]}/{data_fim[1]}/{data_fim[2]}&txUF={UF}&txSessao=&listaTipoSessao=&listaTipoInterv=&inFalaPres=&listaTipoFala=&listaFaseSessao=&txAparteante=&listaEtapa=&CampoOrdenacao=dtSessao&TipoOrdenacao=ASC&PageSize={tamanho}&txTexto=&txSumario='
        data_frame[i] = pd.read_html(url)
    

    return data_frame


def UrlToBS(url):
    html = requests.get(url)
    #content = html.content
    return BeautifulSoup(html.content, 'html.parser')


def SpeechLinks(qpt):

    link_infos= []
    soup = []
    temp = []
    for i in range(qpt):
        current_page = i+1
        url = f'https://www.camara.leg.br/internet/SitaqWeb/ResultadoPesquisaDiscursos.asp?CurrentPage={current_page}&txIndexacao=&BasePesq=plenario&txOrador=&txPartido=&dtInicio={data_inicio[0]}/{data_inicio[1]}/{data_inicio[2]}&dtFim={data_fim[0]}/{data_fim[1]}/{data_fim[2]}&txUF={UF}&txSessao=&listaTipoSessao=&listaTipoInterv=&inFalaPres=&listaTipoFala=&listaFaseSessao=&txAparteante=&listaEtapa=&CampoOrdenacao=dtSessao&TipoOrdenacao=ASC&PageSize={tamanho}&txTexto=&txSumario='
        soup.append(UrlToBS(url))
        for links in soup[i].find_all('a', attrs={'title':"Íntegra do Discurso"}):
            temp.append((links['href']))
        link_infos.append(temp)
        temp = [] #lista temporária que appenda em link_infos

    #>>Limpeza dos links

    linkDiscurso = []
    temp = []
    for i in range(qpt):
        for item in link_infos[i]:
            text = item.replace('\t','').replace('\n','').replace('\r','').replace(' ','')
            temp.append(("https://www.camara.leg.br/internet/SitaqWeb/"+text))
        linkDiscurso.append(temp)
        temp = []


    return linkDiscurso

def SpeechsTxt(qpt = qtd_discursos(0)):
    '''doc'''

    txt = []
    for script in SpeechLinks(qpt)[0]:
        url_script = UrlToBS(url)(script).find_all("font")
        txt.append((str((url_script[0].contents)) + "+" + str((url_script[1].contents))).replace('<br/>','').replace('<b>', '').replace('</b>', '').replace('\'', ''))


    for i in range(len(txt)):
        if not(os.path.exists(f"./discursos/file_{i}.txt")):
            textfile = open(f"./discursos/file_{i}.txt", "x")
            textfile.close()

    for i in range(len(txt)):

        textfile = open(f"./discursos/file_{i}.txt", "w")
        textfile.write(txt[i] + "\n")
        textfile.close()
