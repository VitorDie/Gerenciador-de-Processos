from control.algoritmos.priority_lock import PriorityLock

def prioridade_preemptivo(processos, priority_lock_enable=False):
    tempo_atual = 0
    total_espera = 0
    total_execucao = 0

    # Instancia PriorityLock caso habilitado
    lock = PriorityLock() if priority_lock_enable else None
    previous_owner = None

    # Ordena inicialmente por chegada e prioridade (maior prioridade primeiro)
    processos_ordenados = sorted(processos, key=lambda p: (p.chegada, -p.prioridade))

    while processos_ordenados:
        # Verifica se o lock está habilitado e interfere na escolha do processo
        if priority_lock_enable and lock.owner:
            processo_atual = lock.owner
        else:
            processo_atual = None
            for p in processos_ordenados:
                if p.chegada <= tempo_atual:
                    if processo_atual is None or p.prioridade > processo_atual.prioridade:
                        processo_atual = p

        # Avança até a chegada, se necessário
        if processo_atual.chegada > tempo_atual:
            tempo_atual = processo_atual.chegada

        # Caso o lock esteja habilitado, a prioridade é herdada e o processo dono do lock tem maior prioridade
        if priority_lock_enable:
            if previous_owner != processo_atual:
                if previous_owner:
                    lock.release()  # Libera o lock do dono anterior
                lock.acquire(processo_atual, True)  # Adquire o lock para o novo dono
                previous_owner = processo_atual

        # Executa 1 unidade de tempo (preemptivo)
        tempo_atual += processo_atual.adicionar_processamento(
            tempo_atual, tempo_atual + 1
        )

        # Se terminou, registra métricas e remove
        if processo_atual.tempo_restante == 0:
            total_espera += processo_atual.get_espera()
            total_execucao += processo_atual.get_turnaround()
            processos_ordenados.remove(processo_atual)

            # Release do lock quando o dono termina
            if priority_lock_enable:
                lock.release()
                previous_owner = None

    n = len(processos)
    media_espera = total_espera / n
    media_execucao = total_execucao / n
    return media_espera, media_execucao

# from control.algoritmos.priority_lock import PriorityLock
# 
# def prioridade_preemptivo(processos, priority_lock_enable=False):
#     tempo_atual = 0
#     total_espera = 0
#     total_execucao = 0
# 
#     # Instancia PriorityLock caso habilitado
#     lock = PriorityLock() if priority_lock_enable else None
#     previous_owner = None
# 
#     # Ordena inicialmente por chegada e prioridade (maior prioridade primeiro)
#     processos_ordenados = sorted(processos, key=lambda p: (p.chegada, -p.prioridade))
# 
#     while processos_ordenados:
#         # Encontra o próximo processo de maior prioridade disponível
#         processo_atual = processos_ordenados[0]
#         for p in processos_ordenados:
#             if p.chegada <= tempo_atual and p.prioridade > processo_atual.prioridade:
#                 processo_atual = p
# 
#         # Avança até a chegada, se necessário
#         if processo_atual.chegada > tempo_atual:
#             tempo_atual = processo_atual.chegada
# 
#         # Acquire do lock quando mudamos de dono
#         if priority_lock_enable:
#             if previous_owner != processo_atual:
#                 if previous_owner:
#                     lock.release()
#                 lock.acquire(processo_atual, True)
#                 previous_owner = processo_atual
# 
#         # Executa 1 unidade de tempo (preemptivo)
#         tempo_atual += processo_atual.adicionar_processamento(
#             tempo_atual, tempo_atual + 1
#         )
# 
#         # Se terminou, registra métricas e remove
#         if processo_atual.tempo_restante == 0:
#             total_espera += processo_atual.get_espera()
#             total_execucao += processo_atual.get_turnaround()
#             processos_ordenados.remove(processo_atual)
# 
#             # Release do lock quando o dono termina
#             if priority_lock_enable:
#                 lock.release()
#                 previous_owner = None
# 
#     n = len(processos)
#     media_espera = total_espera / n
#     media_execucao = total_execucao / n
#     return media_espera, media_execucao


# def prioridade_preemptivo(processos):
#     tempo_atual = 0
#     total_espera = 0
#     total_execucao = 0
# 
#     processos_ordenados = sorted(processos, key=lambda p: (p.chegada, -p.prioridade))
# 
#     while processos_ordenados:
#         processo_atual = processos_ordenados[0]
# 
#         if processo_atual.chegada > tempo_atual:
#             tempo_atual += processo_atual.chegada
# 
#         for processo in processos_ordenados:
#             if processo.chegada <= tempo_atual and processo.prioridade > processo_atual.prioridade:
#                 processo_atual = processo
#         
#         tempo_atual += processo_atual.adicionar_processamento(tempo_atual, tempo_atual + 1)
#                 
#         if processo_atual.tempo_restante == 0:
#             total_espera += processo_atual.get_espera()
#             total_execucao += processo_atual.get_turnaround()
#             processos_ordenados.remove(processo_atual)
# 
#     media_espera = total_espera / len(processos)
#     media_execucao = total_execucao / len(processos)
#     
#     return media_espera, media_execucao

