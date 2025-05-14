from control import fcfs, sjf, round_robin, srtf, prioridade_cooperativo, prioridade_preemptivo

def simular_escalonamento(processos, algoritmo, quantum_entry=0, priority_lock_enabled=False):
    if not processos:
        raise Exception("Nenhum processo foi adicionado.")

    if algoritmo == 1:
        media_espera, media_execucao = fcfs(processos, priority_lock_enabled)
    elif algoritmo == 2:
        media_espera, media_execucao = sjf(processos, priority_lock_enabled)
    elif algoritmo == 3:
        quantum = int(quantum_entry)
        media_espera, media_execucao = round_robin(processos, quantum, priority_lock_enabled)
    elif algoritmo == 4:
        media_espera, media_execucao = srtf(processos,priority_lock_enabled)
    elif algoritmo == 5:
        media_espera, media_execucao = prioridade_cooperativo(processos, priority_lock_enabled)
    elif algoritmo == 6:
        media_espera, media_execucao = prioridade_preemptivo(processos, priority_lock_enabled)
    else:
        raise Exception("Selecione um algoritmo válido.")
    
    return media_execucao, media_espera
       
    
