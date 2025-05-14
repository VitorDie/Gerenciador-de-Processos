from control.algoritmos.priority_lock import PriorityLock

def srtf(processos, priority_lock_enable=False):
    tempo_atual = 0
    total_espera = 0
    total_execucao = 0
    # Instancia PriorityLock caso habilitado
    lock = PriorityLock() if priority_lock_enable else None
    previous_owner = None
    
    processos_restantes = sorted(processos, key=lambda p: p.chegada)
    processos_concluidos = []
    
    while processos_restantes or previous_owner:
        # Identifica processos disponíveis no momento atual
        disponiveis = [p for p in processos_restantes if p.chegada <= tempo_atual]
        
        # Verifica se o lock está habilitado e interfere na escolha do processo
        if priority_lock_enable and lock.owner and lock.owner in disponiveis:
            processo_atual = lock.owner
        else:
            # Se não há processo com lock ou o dono do lock não está disponível
            if not disponiveis:
                # Avança o tempo até a próxima chegada
                if processos_restantes:
                    tempo_atual = processos_restantes[0].chegada
                    continue
                else:
                    break
                    
            # Escolhe o processo com menor tempo restante
            processo_atual = min(disponiveis, key=lambda p: p.tempo_restante)
        
        # Caso o lock esteja habilitado, verifica se há troca de processo
        if priority_lock_enable:
            if previous_owner != processo_atual:
                if previous_owner:
                    lock.release()  # Libera o lock do dono anterior
                lock.acquire(processo_atual, True)  # Adquire o lock para o novo dono
                previous_owner = processo_atual
        
        # Determina por quanto tempo este processo vai executar
        # No SRTF, executa até a próxima chegada ou até o fim do processo
        proxima_chegada = float('inf')
        for p in processos_restantes:
            if p.chegada > tempo_atual and p.chegada < proxima_chegada:
                proxima_chegada = p.chegada
        
        tempo_execucao = min(processo_atual.tempo_restante, proxima_chegada - tempo_atual)
        tempo_atual += processo_atual.adicionar_processamento(tempo_atual, tempo_atual + tempo_execucao)
        
        # Se o processo terminou, registra métricas e remove
        if processo_atual.tempo_restante == 0:
            total_espera += processo_atual.get_espera()
            total_execucao += processo_atual.get_turnaround()
            processos_restantes.remove(processo_atual)
            processos_concluidos.append(processo_atual)
            
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
# def srtf(processos, priority_lock_enable=False):
#     tempo_atual = 0
#     total_espera = 0
#     total_execucao = 0
# 
#     # Inicializa PriorityLock se habilitado
#     lock = PriorityLock() if priority_lock_enable else None
#     previous_owner = None
# 
#     # Ordena por chegada e tempo restante
#     processos_ordenados = sorted(processos, key=lambda p: (p.chegada, p.tempo_restante))
# 
#     while processos_ordenados:
#         # Seleção do processo de menor tempo restante disponível
#         processo_atual = processos_ordenados[0]
#         for p in processos_ordenados:
#             if p.chegada <= tempo_atual and p.tempo_restante < processo_atual.tempo_restante:
#                 processo_atual = p
# 
#         # Avança até a chegada, se necessário
#         if processo_atual.chegada > tempo_atual:
#             tempo_atual = processo_atual.chegada
# 
#         # Acquire do lock ao mudar de dono
#         if priority_lock_enable and processo_atual != previous_owner:
#             if previous_owner:
#                 lock.release()
#             lock.acquire(processo_atual, True)
#             previous_owner = processo_atual
# 
#         # Executa por 1 unidade de tempo
#         tempo_atual += processo_atual.adicionar_processamento(
#             tempo_atual,
#             tempo_atual + 1
#         )
# 
#         # Se terminou, coleta métricas e remove
#         if processo_atual.tempo_restante == 0:
#             total_execucao += processo_atual.get_turnaround()
#             total_espera += processo_atual.get_espera()
#             processos_ordenados.remove(processo_atual)
# 
#             # Release do lock
#             if priority_lock_enable:
#                 lock.release()
#                 previous_owner = None
# 
#     # Cálculo de médias
#     n = len(processos)
#     media_espera = total_espera / n
#     media_execucao = total_execucao / n
#     return media_espera, media_execucao


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