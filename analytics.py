import pandas as pd
import numpy as np
from collections import defaultdict
from discursos import DiscursosPartido





def speech_dict():
    discursos = pd.read_csv('datasets/df_discursos.csv')
    data = pd.read_csv('datasets/data.csv')



    dataset_geral = pd.merge(data, discursos, on="Id", how="left")



    dataset_geral = dataset_geral.drop(columns ="Discurso")



    aux = {'SOLIDARIEDAD': 'SOLIDARIEDADE', 'DEM':'UNIÃO', 'REPUBLICANOS': 'PRB'}
    dataset_geral['Partido'].replace(aux, inplace=True)



    partidos = dataset_geral['Partido'].unique()
    len(partidos)


    dicio=eval(dataset_geral['qtd_termos'][0])

    discursos_partidos = []
    for i in partidos:
        discursos_partidos.append(dataset_geral[dataset_geral['Partido'] == i])


    discursos_dicionarios = []
    for i in range(len((discursos_partidos))):
        discursos_por_partido = []
        
        for j in discursos_partidos[i]['qtd_termos']:
            discursos_por_partido.append(eval(j))
        discursos_dicionarios.append(discursos_por_partido)

    a = []

    for i in range(len(discursos_dicionarios)):
        b = []
        dicio = defaultdict(int)
        for j in range(len(discursos_dicionarios[i])):
            for k, v in discursos_dicionarios[i][j].items():
                dicio[k]+=v
            b.append(dicio)
        a.append(b)

    #uniao = psl + dem
    #solidariedade = solidariedad
    #prb = republicanos


    pt = DiscursosPartido(partidos[0], a[0][0], total_termos=0, coordenada=('left','down'))
    pp = DiscursosPartido(partidos[1], a[1][0], total_termos=0, coordenada=('right','up'))
    psd = DiscursosPartido(partidos[2], a[2][0], total_termos=0, coordenada=('right','up'))
    psb = DiscursosPartido(partidos[3], a[3][0], total_termos=0, coordenada=('left','down'))
    cidadania = DiscursosPartido(partidos[4], a[4][0], total_termos=0, coordenada=('right','down'))
    pl = DiscursosPartido(partidos[5], a[5][0], total_termos=0, coordenada=('right','up'))
    uniao = DiscursosPartido(partidos[6], a[6][0], total_termos=0, coordenada=('right','up'))
    psol = DiscursosPartido(partidos[7], a[7][0], total_termos=0, coordenada=('left','down'))
    pdt = DiscursosPartido(partidos[8], a[8][0], total_termos=0, coordenada=('left','up'))
    solidariedade = DiscursosPartido(partidos[9], a[9][0], total_termos=0, coordenada=('left','down'))
    novo = DiscursosPartido(partidos[10], a[10][0], total_termos=0, coordenada=('right','up'))
    #mdb = DiscursosPartido(partidos[11], a[11][0], total_termos=0, coordenada=('right','up'))
    prb = DiscursosPartido(partidos[12], a[12][0], total_termos=0, coordenada=('right','up'))
    #pros = DiscursosPartido(partidos[13], a[13][0], total_termos=0, coordenada=('right','up'))
    pv = DiscursosPartido(partidos[14], a[14][0], total_termos=0, coordenada=('right','down'))
    psc = DiscursosPartido(partidos[15], a[15][0], total_termos=0, coordenada=('right','up'))
    psdb = DiscursosPartido(partidos[16], a[16][0], total_termos=0, coordenada=('right','up'))


    left = [pt, psb, psol, pdt, solidariedade]
    soma_total_left = 0
    for i in left:
        soma_total_left += (i.soma_termos())
    soma_total_left


    right = [pp, psd, cidadania, pl, uniao, novo, pv, psc, psdb]
    soma_total_right = 0
    for i in right:
        soma_total_right += (i.soma_termos())
    soma_total_right



    dict_right = defaultdict(int)
    for i in right:
        for k,v in i.termos.items():
            dict_right[k] += v
    dict_right


    dict_left = defaultdict(int)
    for i in left:
        for k,v in i.termos.items():
            dict_left[k] += v
    dict_left


    score_left = {}
    for k,v in dict_left.items():
        score_left[k] = v/soma_total_left

    score_right = {}
    for k,v in dict_right.items():
        score_right[k] = v/soma_total_right


def word_score(word):
    return (score_right[word] - score_left[word]) / (score_right[word] + score_left[word])
    
print(word_score['MORTE'])


