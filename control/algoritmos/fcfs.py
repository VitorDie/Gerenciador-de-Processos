from control.algoritmos.priority_lock import PriorityLock

def fcfs(processos, priority_lock_enable=False):
    tempo_atual = 0
    total_execucao = 0
    total_espera = 0
    lock = PriorityLock() if priority_lock_enable else None

    for p in sorted(processos, key=lambda p: p.chegada):
        # avança até a chegada
        tempo_atual = max(tempo_atual, p.chegada)

        # adquire (e dispara herança, se houvesse disputa)
        if priority_lock_enable:
            lock.acquire(p, True)

        # executa o processo inteiro
        tempo_atual += p.adicionar_processamento(tempo_atual,
                                                 tempo_atual + p.duracao)
        total_execucao += p.get_turnaround()
        total_espera   += p.get_espera()

        # libera o lock imediatamente após terminar
        if priority_lock_enable:
            lock.release()

    n = len(processos)
    return total_espera / n, total_execucao / n



# #from priority_lock import PriorityLock
# from control.algoritmos.priority_lock import PriorityLock
# 
# def fcfs(processos, priority_lock_enable=False):
#     tempo_atual = 0
#     total_execucao = 0
#     total_espera = 0
# 
#     # Cria o lock (já habilitado ou não)
#     lock = PriorityLock() if priority_lock_enable else None
# 
#     # Ordena só pela chegada
#     for processo in sorted(processos, key=lambda p: p.chegada):
#         # Avança até a chegada, se preciso
#         if processo.chegada > tempo_atual:
#             tempo_atual = processo.chegada
# 
#         # Se for usar lock, tenta adquirir; se falhar, espera até liberar
#         if priority_lock_enable:
#             while not lock.acquire(processo, priority_lock_enable):
#                 # simula espera até o dono liberar; aqui você poderia avançar "tempo_atual"
#                 # ou reordenar, dependendo do nível de simulação
#                 lock.release()  # força liberação numa simulação simplificada
# 
#         # Executa
#         tempo_atual += processo.adicionar_processamento(tempo_atual,
#                                                         tempo_atual + processo.duracao)
#         total_execucao += processo.get_turnaround()
#         total_espera   += processo.get_espera()
# 
#         # Libera o lock
#         if priority_lock_enable:
#             lock.release()
# 
#     # Retorna as médias
#     n = len(processos)
#     return total_espera / n, total_execucao / n


# def fcfs(processos):
#     tempo_atual = 0
#     total_execucao = 0
#     total_espera = 0
# 
#     processos_ordenados = sorted(processos, key=lambda p: p.chegada)
#     
#     for processo in processos_ordenados:
#         if processo.chegada > tempo_atual:
#             tempo_atual = processo.chegada
#             
#         tempo_atual += processo.adicionar_processamento(tempo_atual, tempo_atual + processo.duracao)
#         
#         total_execucao += processo.get_turnaround()
#         total_espera += processo.get_espera()
#         
#     media_espera = total_espera / len(processos)
#     media_execucao = total_execucao / len(processos)
#     
#     return media_espera, media_execucao
