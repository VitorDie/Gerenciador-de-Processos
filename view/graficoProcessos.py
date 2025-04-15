import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import tkinter as tk

def centralizar_grafico(fig):
    janela_temporaria = tk.Tk()
    janela_temporaria.withdraw()

    largura_tela = janela_temporaria.winfo_screenwidth()
    altura_tela = janela_temporaria.winfo_screenheight()

    largura_janela = fig.canvas.manager.window.winfo_width()
    altura_janela = fig.canvas.manager.window.winfo_height()

    pos_x = (largura_tela // 2) - int(1.5 * largura_janela)
    pos_y = (altura_tela // 2) - int(1.5 * altura_janela)

    fig.canvas.manager.window.wm_geometry(f"+{pos_x}+{pos_y}")

    janela_temporaria.destroy()

def grafico_processos(processos, media_execucao, media_espera):
    fig, ax = plt.subplots()
    
    fig.canvas.manager.set_window_title('Gráfico de Escalonamento')
    tempo_maximo = max([max([p.fim for p in processo.processamentos]) for processo in processos if processo.processamentos]) + 1
    ax.set_xlim(0, tempo_maximo)

    for processo in processos:
        for instante in range(tempo_maximo):
            estado = processo.verificar_estado(instante)

            if estado == "Execução":
                ax.barh(processo.id, 1, left=instante, color='#1E90FF', edgecolor='#1E90FF')
            elif estado == "Espera":
                ax.barh(processo.id, 1, left=instante, color='#FF6347', edgecolor='#FF6347')

        espera = processo.get_espera()
        turnaround = processo.get_turnaround()
        ax.text(tempo_maximo + 0.5, processo.id, f"Execução: {turnaround}\nEspera: {espera}", va='center')

    ax.set_xlabel('Tempo')
    ax.set_ylabel('Processo')
    ax.set_title('Escalonamento de Processos')

    execucao_patch = mpatches.Patch(color='#1E90FF', label=f'Execução: Média Execução = {media_execucao:.2f}')
    espera_patch = mpatches.Patch(color='#FF6347', label=f'Espera: Média Espera = {media_espera:.2f}')
    ax.legend(handles=[execucao_patch, espera_patch], loc='lower right', bbox_to_anchor=(1, -0.35))

    #fig.canvas.manager.window.wm_iconbitmap("assets/icon.ico")

    plt.tight_layout()
    plt.draw()
    
    centralizar_grafico(fig)
    plt.show()
