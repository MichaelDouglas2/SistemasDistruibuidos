import tkinter as tk  # Interface gráfica
from PIL import Image, ImageTk  # Imagens no tkinter
import subprocess  # Executar outros scripts
import sys  # Acesso ao interpretador
import os  # Manipular arquivos e pastas

# === Ajustes de resolução da janela ===
Adjust = "Auto"  # Define que o tamanho da janela será ajustado automaticamente conforme a resolução da tela
root = tk.Tk()  # Cria a janela principal da interface
root.title("UNO - Menu Inicial")  # Define o título que aparece na barra superior da janela

# Define a largura da janela dependendo da resolução da tela e da configuração "Auto"
windowWidth = (
    (Adjust == "Auto" and root.winfo_screenwidth() >= 1350 and root.winfo_screenheight() >= 850 and [1280, 1300])
    or (Adjust == "Auto" and [1126, 1150])
    or [1280, 1300]
)
# Define a altura da janela de forma semelhante, com base na largura escolhida
windowHeight = (
    (Adjust == "Auto" and windowWidth[0] == 1280 and [720, 800])
    or (Adjust == "Auto" and [634, 660])
    or [720, 800]
)
# Aplica a resolução escolhida à janela principal no formato "largura x altura"
root.geometry(f"{windowWidth[1]}x{windowHeight[1]}")
# Impede que o usuário redimensione a janela manualmente
root.resizable(False, False)

# Define a pasta onde estão os arquivos de imagem e outros recursos gráficos do jogo
folder = "Uno_Assets"

# ===== Imagem de fundo redimensionada com Pillow =====
fundo_pil = Image.open(f"{folder}/RegrasBack.png")  # Abre a imagem
fundo_pil = fundo_pil.resize((windowWidth[1], windowHeight[1]), Image.LANCZOS)  # Redimensiona
fundo_img = ImageTk.PhotoImage(fundo_pil)  # Converte para uso no tkinter
fundo_label = tk.Label(root, image=fundo_img)  # Cria label com a imagem
fundo_label.place(x=0, y=0, relwidth=1, relheight=1)  # Preenche a janela

# ===== Funções dos botões =====
def voltar():
    subprocess.Popen([sys.executable, 'main_menu.py'])  # Abre o menu principal
    root.destroy()  # Fecha a janela atual

# ===== Função auxiliar para carregar botões redimensionados com transparência =====
def carregar_botao(caminho, largura, altura):
    img = Image.open(caminho).convert("RGBA")  # Abre a imagem com transparência
    img = img.resize((largura, altura), Image.LANCZOS)  # Redimensiona
    return ImageTk.PhotoImage(img)  # Converte para uso no tkinter

# Carrega os botões
btn_largura, btn_altura = 220, 83  # Tamanho do botão
btn_regras_img = carregar_botao(f"{folder}/ButtonVoltar.png", btn_largura, btn_altura)  # Imagem do botão "Voltar"

# Cálculos para posicionar o botão
btn_x = int(windowWidth[1] * 0.70)  # Posição horizontal (70% da largura)
btn_y = int(windowHeight[1] * 0.78)  # Posição vertical (78% da altura)

# Cria botão com imagem, sem borda, e fundo transparente
btn_regras = tk.Button(root, image=btn_regras_img, command=voltar,
                       borderwidth=0, highlightthickness=0, bg=root["bg"])
btn_regras.place(x=btn_x, y=btn_y)  # Posiciona o botão

# Inicia a interface
root.mainloop()

