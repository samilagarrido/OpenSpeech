import requests
from bs4 import BeautifulSoup

response = requests.get("https://www.camara.leg.br/internet/SitaqWeb/ResultadoPesquisaDiscursos.asp?txOrador=&txPartido=&txUF=&dtInicio=28%2F03%2F2022&dtFim=28%2F04%2F2022&txSessao=&listaTipoFala=&listaFaseSessao=&listaTipoInterv=&txAparteante=&txTexto=&txSumario=&txIndexacao=&BasePesq=plenario&CampoOrdenacao=dtSessao&PageSize=20&TipoOrdenacao=ASC&btnPesqAvan=Pesquisar")

content = response.content

site = BeautifulSoup(content, 'html.parser')

# título
title = site.find("h1")
print(title.text)

#colunas
columns = site.find("thead")
print(columns.text)
