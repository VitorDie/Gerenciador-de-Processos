from control.algoritmos.priority_lock import PriorityLock

def sjf(processos, priority_lock_enable=False):
    tempo_atual = 0
    total_espera = 0
    total_execucao = 0

    # Inicializa o lock se necessário
    lock = PriorityLock() if priority_lock_enable else None

    # Ordena por chegada, depois menor duração
    processos_ordenados = sorted(processos, key=lambda p: (p.chegada, p.duracao))

    while processos_ordenados:
        # Seleciona o processo de menor duração disponível
        processo_atual = processos_ordenados[0]
        for p in processos_ordenados:
            if p.chegada <= tempo_atual and p.duracao < processo_atual.duracao:
                processo_atual = p

        # Avança até a chegada, se necessário
        if processo_atual.chegada > tempo_atual:
            tempo_atual = processo_atual.chegada

        # Acquire do lock antes de executar completamente
        if priority_lock_enable:
            lock.acquire(processo_atual, True)

        # Executa o processo até conclusão
        tempo_atual += processo_atual.adicionar_processamento(
            tempo_atual,
            tempo_atual + processo_atual.duracao
        )
        total_execucao += processo_atual.get_turnaround()
        total_espera += processo_atual.get_espera()

        # Release do lock após término
        if priority_lock_enable:
            lock.release()

        processos_ordenados.remove(processo_atual)

    # Calcula médias
    n = len(processos)
    media_espera = total_espera / n
    media_execucao = total_execucao / n
    return media_espera, media_execucao


# def sjf(processos):
#     tempo_atual = 0
#     total_espera = 0
#     total_execucao = 0
# 
#     processos_ordenados = sorted(processos, key=lambda p: (p.chegada, p.duracao))
# 
#     while processos_ordenados:
#         processo_atual = processos_ordenados[0]
# 
#         if processo_atual.chegada > tempo_atual:
#             tempo_atual += processo_atual.chegada
# 
#         for processo in processos_ordenados:
#             if processo.chegada <= tempo_atual and processo.duracao < processo_atual.duracao:
#                 processo_atual = processo
#         
#         tempo_atual += processo_atual.adicionar_processamento(tempo_atual, tempo_atual + processo_atual.duracao)
#         
#         total_execucao += processo_atual.get_turnaround()
#         total_espera += processo_atual.get_espera()
# 
#         processos_ordenados.remove(processo_atual)
# 
#     media_espera = total_espera / len(processos)
#     media_execucao = total_execucao / len(processos)
#     
#     return media_espera, media_execucao
# 