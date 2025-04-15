class Periodo:
    def __init__(self, inicio, fim):
        self.inicio = inicio
        self.fim = fim
    
    def get_duracao(self):
        return self.fim - self.inicio


class Processo:
    def __init__(self, id, chegada, duracao, prioridade):
        self.id = id
        self.chegada = chegada
        self.duracao = duracao
        self.prioridade = prioridade

        self.tempo_restante = duracao
        self.processamentos = []
    
    def adicionar_processamento(self, inicio, fim):
        if self.tempo_restante - fim + inicio < 0:
            fim = inicio + self.tempo_restante

        self.processamentos.append(Periodo(inicio, fim))
        self.tempo_restante -= fim - inicio

        return self.processamentos[-1].get_duracao()

    def get_espera(self):
        espera = 0
        tempo_atual = self.chegada

        for periodo in self.processamentos:
            espera += periodo.inicio - tempo_atual
            tempo_atual = periodo.fim

        return espera

    def get_turnaround(self):
        if(len(self.processamentos) == 0):
            return 0

        return self.processamentos[-1].fim - self.chegada

    def verificar_estado(self, instante):
        if(len(self.processamentos) == 0):
            return "Desconhecido"
        
        if(instante < self.chegada):
            return "Antes da chegada"
        
        if(instante >= self.processamentos[-1].fim):
            return "Após a chegada"

        for periodo in self.processamentos:
            if periodo.inicio <= instante < periodo.fim:
                return "Execução"
            
        return "Espera"
    
    def __str__(self):
        return f'Processo(id={self.id}])'
    