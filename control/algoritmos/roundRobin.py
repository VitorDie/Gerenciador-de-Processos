from control.algoritmos.priority_lock import PriorityLock

def round_robin(processos, quantum=2, priority_lock_enable=False):
    tempo_atual = 0
    total_espera = 0
    total_execucao = 0

    # Inicializa lock e controle de dono anterior
    lock = PriorityLock() if priority_lock_enable else None
    previous_owner = None

    processos_ordenados = sorted(processos, key=lambda p: p.chegada)
    fila = []

    while processos_ordenados or fila:
        # Adiciona processos recém-chegados à fila
        for p in list(processos_ordenados):
            if p.chegada <= tempo_atual:
                fila.append(p)
                processos_ordenados.remove(p)

        if not fila:
            tempo_atual += 1
            continue

        processo_atual = fila.pop(0)

        # Acquire do lock ao mudar de dono
        if priority_lock_enable and processo_atual != previous_owner:
            if previous_owner:
                lock.release()
            lock.acquire(processo_atual, True)
            previous_owner = processo_atual

        # Executa por quantum ou até terminar
        tempo_exec = min(quantum, processo_atual.tempo_restante)
        tempo_atual += processo_atual.adicionar_processamento(
            tempo_atual,
            tempo_atual + tempo_exec
        )

        # Se terminou completamente
        if processo_atual.tempo_restante == 0:
            total_execucao += processo_atual.get_turnaround()
            total_espera += processo_atual.get_espera()
            # release do lock quando finaliza
            if priority_lock_enable:
                lock.release()
                previous_owner = None
        else:
            # Reinsere no fim da fila
            fila.append(processo_atual)

    n = len(processos)
    media_espera = total_espera / n
    media_execucao = total_execucao / n
    return media_espera, media_execucao


# def round_robin(processos, quantum=2):
#     tempo_atual = 0
#     total_espera = 0
#     total_execucao = 0
# 
#     processos_ordenados = sorted(processos, key=lambda p: p.chegada)
#     fila = []
# 
#     while processos_ordenados:
#         for processo in processos_ordenados:
#             if(processo.chegada <= tempo_atual and processo not in fila):
#                 fila.append(processo)
# 
#         if not fila:
#             tempo_atual += 1
#             continue
# 
#         processo_atual = fila.pop(0)
#         processos_ordenados.remove(processo_atual)
# 
#         tempo_atual += processo_atual.adicionar_processamento(tempo_atual, tempo_atual + quantum)
# 
#         if processo_atual.tempo_restante == 0:
#             total_execucao += processo_atual.get_turnaround()
#             total_espera += processo_atual.get_espera()
#         else:
#             processos_ordenados.append(processo_atual)
#         
# 
#     media_espera = total_espera / len(processos)
#     media_execucao = total_execucao / len(processos)
#     
#     return media_espera, media_execucao
