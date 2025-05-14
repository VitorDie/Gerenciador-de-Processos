from control.algoritmos.priority_lock import PriorityLock

def srtf(processos, priority_lock_enable=False):
    tempo_atual = 0
    total_espera = 0
    total_execucao = 0

    # Inicializa PriorityLock se habilitado
    lock = PriorityLock() if priority_lock_enable else None
    previous_owner = None

    # Ordena por chegada e tempo restante
    processos_ordenados = sorted(processos, key=lambda p: (p.chegada, p.tempo_restante))

    while processos_ordenados:
        # Seleção do processo de menor tempo restante disponível
        processo_atual = processos_ordenados[0]
        for p in processos_ordenados:
            if p.chegada <= tempo_atual and p.tempo_restante < processo_atual.tempo_restante:
                processo_atual = p

        # Avança até a chegada, se necessário
        if processo_atual.chegada > tempo_atual:
            tempo_atual = processo_atual.chegada

        # Acquire do lock ao mudar de dono
        if priority_lock_enable and processo_atual != previous_owner:
            if previous_owner:
                lock.release()
            lock.acquire(processo_atual, True)
            previous_owner = processo_atual

        # Executa por 1 unidade de tempo
        tempo_atual += processo_atual.adicionar_processamento(
            tempo_atual,
            tempo_atual + 1
        )

        # Se terminou, coleta métricas e remove
        if processo_atual.tempo_restante == 0:
            total_execucao += processo_atual.get_turnaround()
            total_espera += processo_atual.get_espera()
            processos_ordenados.remove(processo_atual)

            # Release do lock
            if priority_lock_enable:
                lock.release()
                previous_owner = None

    # Cálculo de médias
    n = len(processos)
    media_espera = total_espera / n
    media_execucao = total_execucao / n
    return media_espera, media_execucao


# def srtf(processos):
#     tempo_atual = 0
#     total_espera = 0
#     total_execucao = 0
# 
#     processos_ordenados = sorted(processos, key=lambda p: (p.chegada, p.tempo_restante))
# 
#     while processos_ordenados:
#         processo_atual = processos_ordenados[0]
# 
#         if processo_atual.chegada > tempo_atual:
#             tempo_atual += processo_atual.chegada
# 
#         for processo in processos_ordenados:
#             if processo.chegada <= tempo_atual and processo.tempo_restante < processo_atual.tempo_restante:
#                 processo_atual = processo
# 
#         tempo_atual += processo_atual.adicionar_processamento(tempo_atual, tempo_atual + 1)
# 
#         if processo_atual.tempo_restante == 0:
#             total_execucao += processo_atual.get_turnaround()
#             total_espera += processo_atual.get_espera()
#             processos_ordenados.remove(processo_atual)
# 
#     media_espera = total_espera / len(processos)
#     media_execucao = total_execucao / len(processos)
#     
#     return media_espera, media_execucao
# 