import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
import os

class DownloadSpeech():
    def __init__(self, first_day, last_day, size_speechs = 100, current_page = 1, UF = ""):

        '''obejct to download speechs
        first_day and last_day = [DD,MM,YYYY]
        size_speech < 1800
        uf = AM, RN, MT...
        '''
        self.first_day = first_day
        self.last_day = last_day
        self.size_speechs = size_speechs
        self.current_page = current_page
        self.UF = UF
        self.url = f'https://www.camara.leg.br/internet/SitaqWeb/ResultadoPesquisaDiscursos.asp?CurrentPage={self.current_page}&txIndexacao=&BasePesq=plenario&txOrador=&txPartido=&dtInicio={self.first_day[0]}/{self.first_day[1]}/{self.first_day[2]}&dtFim={self.last_day[0]}/{self.last_day[1]}/{self.last_day[2]}&txUF={self.UF}&txSessao=&listaTipoSessao=&listaTipoInterv=&inFalaPres=&listaTipoFala=&listaFaseSessao=&txAparteante=&listaEtapa=&CampoOrdenacao=dtSessao&TipoOrdenacao=ASC&PageSize={self.size_speechs}&txTexto=&txSumario='

    def UrlToBS(url):
        '''Return a beautifulsoup object'''
        html = requests.get(url)
        #content = html.content
        return BeautifulSoup(html.content, 'html.parser')
    
    


    