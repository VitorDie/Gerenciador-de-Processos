def prioridade_preemptivo(processos):
    tempo_atual = 0
    total_espera = 0
    total_execucao = 0

    processos_ordenados = sorted(processos, key=lambda p: (p.chegada, -p.prioridade))

    while processos_ordenados:
        processo_atual = processos_ordenados[0]

        if processo_atual.chegada > tempo_atual:
            tempo_atual += processo_atual.chegada

        for processo in processos_ordenados:
            if processo.chegada <= tempo_atual and processo.prioridade > processo_atual.prioridade:
                processo_atual = processo
        
        tempo_atual += processo_atual.adicionar_processamento(tempo_atual, tempo_atual + 1)
                
        if processo_atual.tempo_restante == 0:
            total_espera += processo_atual.get_espera()
            total_execucao += processo_atual.get_turnaround()
            processos_ordenados.remove(processo_atual)

    media_espera = total_espera / len(processos)
    media_execucao = total_execucao / len(processos)
    
    return media_espera, media_execucao

