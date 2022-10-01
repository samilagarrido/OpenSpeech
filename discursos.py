from collections import defaultdict

class DiscursosPartido:
    def __init__(self, partido, termos, total_termos = 0, soma_relativa = defaultdict(int), coordenada = ('right', 'up')):
        self.partido = partido
        self.termos = termos
        self.total_termos = total_termos
        self.coordenada = coordenada

    def soma_termos(self):
        self.total_termos = 0
        for k,v in self.termos.items():
            self.total_termos += v
        return self.total_termos

    def soma_relativa(self):
        self.soma_relativa = defaultdict(int)
        for k,v in self.termos.items():
            self.soma_relativa[k] = (v/self.total_termos)

        return self.soma_relativa
    


