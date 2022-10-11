'''Function - é responsável por receber os links dos 
    discursos e transforma-los em arquivo de texto'''

#bibliotecas
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
import os

#declarações

#global qpt #quantidade de paginas totais
#qpt = 0 #quantidade de paginas apresentadas no site

#aqui decidimos as datas que queremos estudar
data_inicio = [28, 3, 2022] 
data_fim = [28, 4, 2022]

#A quantidade de arquivos é o tamanho e a paginas que queremos ler
tamanho = 100
current_page = 1 #quantidade de arrays
UF = ''

#pagina da Web de onde retiramos os links
url = f'https://www.camara.leg.br/internet/SitaqWeb/ResultadoPesquisaDiscursos.asp?CurrentPage={current_page}&txIndexacao=&BasePesq=plenario&txOrador=&txPartido=&dtInicio={data_inicio[0]}/{data_inicio[1]}/{data_inicio[2]}&dtFim={data_fim[0]}/{data_fim[1]}/{data_fim[2]}&txUF={UF}&txSessao=&listaTipoSessao=&listaTipoInterv=&inFalaPres=&listaTipoFala=&listaFaseSessao=&txAparteante=&listaEtapa=&CampoOrdenacao=dtSessao&TipoOrdenacao=ASC&PageSize={tamanho}&txTexto=&txSumario='


def qtd_discursos(qpt):
    # >> Retorna quantidade de discursos da busca

    quantidade_de_discursos= []
    qtd_discursos_totais = 0
    soup = UrlToBS(url)

    for links in soup.find_all('span', attrs={'class':"visualStrong"}):
        quantidade_de_discursos.append(links.contents)

    qtd_discursos_totais = int((quantidade_de_discursos[len(quantidade_de_discursos)-1][0]).replace('.',''))
    qpt = int(qtd_discursos_totais/tamanho)  + 1
    return qpt

def SearchSpeech(data_inicio, data_fim, tamanho, qpt, UF= '', current_page = 1):

    # >> Obtenção da url dinâmica

    #formato de data = {dd, mm, aaaa}
    data_inicio = [28, 3, 2022]
    data_fim = [28, 4, 2022]

    #tamanho = quantidade de linhas de informações por página (limite 1788 pq? não sabemos)
    tamanho = 100
    current_page = 1

    #Estado onde será realizada a pesquisa ('' para todos)
    UF = ''
    url = f'https://www.camara.leg.br/internet/SitaqWeb/ResultadoPesquisaDiscursos.asp?CurrentPage={current_page}&txIndexacao=&BasePesq=plenario&txOrador=&txPartido=&dtInicio={data_inicio[0]}/{data_inicio[1]}/{data_inicio[2]}&dtFim={data_fim[0]}/{data_fim[1]}/{data_fim[2]}&txUF={UF}&txSessao=&listaTipoSessao=&listaTipoInterv=&inFalaPres=&listaTipoFala=&listaFaseSessao=&txAparteante=&listaEtapa=&CampoOrdenacao=dtSessao&TipoOrdenacao=ASC&PageSize={tamanho}&txTexto=&txSumario='

    # >> Requisitando o código fonte da url pelo BS

    html = requests.get(url)
    content = html.content
    soup = BeautifulSoup(content, 'html.parser')

    # >> Retorna o dataframe

    data_frame = [None]*qpt
    for i in range(qpt):
        current_page = i+1
        url = f'https://www.camara.leg.br/internet/SitaqWeb/ResultadoPesquisaDiscursos.asp?CurrentPage={current_page}&txIndexacao=&BasePesq=plenario&txOrador=&txPartido=&dtInicio={data_inicio[0]}/{data_inicio[1]}/{data_inicio[2]}&dtFim={data_fim[0]}/{data_fim[1]}/{data_fim[2]}&txUF={UF}&txSessao=&listaTipoSessao=&listaTipoInterv=&inFalaPres=&listaTipoFala=&listaFaseSessao=&txAparteante=&listaEtapa=&CampoOrdenacao=dtSessao&TipoOrdenacao=ASC&PageSize={tamanho}&txTexto=&txSumario='
        data_frame[i] = pd.read_html(url)
    
    return data_frame


def UrlToBS(url):

    # >> Retira html com beautifulsoup 

    html = requests.get(url)
    #content = html.content
    return BeautifulSoup(html.content, 'html.parser')


def SpeechLinks(qpt):
    
    # >> Retorna os links de acesso para cada discurso

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
        temp = [] #lista temporária que "apenda" em link_infos

    # >> Limpeza dos links

    linkDiscurso = []
    temp = []
    for i in range(qpt):
        for item in link_infos[i]:
            text = item.replace('\t','').replace('\n','').replace('\r','').replace(' ','')
            temp.append(("https://www.camara.leg.br/internet/SitaqWeb/"+text))
        linkDiscurso.append(temp)
        temp = []

    return linkDiscurso

def speechs_txt(qpt = qtd_discursos(0)):
    
    # >> Salva os arquivos do discurso

    txt = []

    #Pegando o html de cada discurso
    for script in SpeechLinks(qpt)[0]:
        url_script = UrlToBS(url)(script).find_all("font")
        txt.append((str((url_script[0].contents)) + "+" + str((url_script[1].contents))).replace('<br/>','').replace('<b>', '').replace('</b>', '').replace('\'', ''))

    #Criando os arquivo de texto
    for i in range(len(txt)):
        if not(os.path.exists(f"./discursos/file_{i}.txt")):
            textfile = open(f"./discursos/file_{i}.txt", "x")
            textfile.close()

    #Escrevendo os discursos nos arquivos de texto
    for i in range(len(txt)):
        textfile = open(f"./discursos/file_{i}.txt", "w")
        textfile.write(txt[i] + "\n")
        textfile.close()
