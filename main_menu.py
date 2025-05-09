import tkinter as tk  # Interface gráfica
from PIL import Image, ImageTk  # Imagens no tkinter
import subprocess  # Executar outros scripts
import sys  # Acesso ao interpretador
import os  # Manipular arquivos e pastas


# ===== Ajustes de resolução =====
Adjust = "Auto"  # Define que o ajuste de resolução será automático (pode mudar para valores fixos, se necessário)
root = tk.Tk()  # Cria a janela principal da interface com tkinter
root.title("UNO - Menu Inicial")  # Define o título da janela

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
fundo_pil = Image.open(f"{folder}/HomeBack.png")  # Abre a imagem
fundo_pil = fundo_pil.resize((windowWidth[1], windowHeight[1]), Image.LANCZOS)  # Redimensiona
fundo_img = ImageTk.PhotoImage(fundo_pil)  # Converte para usar no tkinter
fundo_label = tk.Label(root, image=fundo_img)  # Cria label com a imagem
fundo_label.place(x=0, y=0, relwidth=1, relheight=1)  # Preenche a janela

# ===== Funções dos botões =====
# Função que será chamada ao clicar em "Iniciar Jogo"
def iniciar_jogo():
    subprocess.Popen([sys.executable, 'UNO.py'])  # Executa o arquivo 'UNO.py' como um novo processo (abre o jogo)
    root.destroy()  # Fecha a janela atual (menu)

# Função para abrir o arquivo com as regras do jogo
def abrir_regras():
    subprocess.Popen([sys.executable, 'regras.py'])  # Executa o arquivo 'regras.py' (mostra as regras)
    root.destroy()  # Fecha o menu atual

# Função para sair do programa
def sair():
    root.destroy()  # Fecha a janela principal

# ===== Função auxiliar para carregar botões redimensionados com transparência =====

def carregar_botao(caminho, largura, altura):
    # Abre a imagem do botão no modo RGBA (com canal alfa de transparência)
    img = Image.open(caminho).convert("RGBA")
    # Redimensiona a imagem para as dimensões desejadas, usando LANCZOS para manter qualidade
    img = img.resize((largura, altura), Image.LANCZOS)
    # Converte a imagem para o formato compatível com o tkinter (ImageTk.PhotoImage)
    return ImageTk.PhotoImage(img)

# Carrega os botões com o tamanho padronizado
btn_largura, btn_altura = 220, 83 

# Usa a função auxiliar para carregar e redimensionar cada imagem de botão
btn_iniciar_img = carregar_botao(f"{folder}/ButtonJogar.png", btn_largura, btn_altura)
btn_regras_img  = carregar_botao(f"{folder}/ButtonRegras.png", btn_largura, btn_altura)
btn_sair_img    = carregar_botao(f"{folder}/ButtonSair.png", btn_largura, btn_altura)

# Cálculos para centralizar os botões
btn_x = windowWidth[1] // 2 - btn_largura // 2  # Centraliza os botões horizontalmente (posição X = centro da janela - metade da largura do botão)
start_y = windowHeight[1] // 2 - 40  # Define a posição vertical inicial do primeiro botão, ajustado um pouco acima do centro
spacing = 90  # Espaçamento vertical entre os botões

btn_iniciar = tk.Button(
    root, image=btn_iniciar_img, command=iniciar_jogo,
    borderwidth=0, highlightthickness=0, bg=root["bg"]
)
btn_iniciar.place(x=btn_x, y=start_y)  # Primeiro botão (Jogar)

btn_regras = tk.Button(
    root, image=btn_regras_img, command=abrir_regras,
    borderwidth=0, highlightthickness=0, bg=root["bg"]
)
btn_regras.place(x=btn_x, y=start_y + spacing)  # Segundo botão (Regras)

btn_sair = tk.Button(
    root, image=btn_sair_img, command=sair,
    borderwidth=0, highlightthickness=0, bg=root["bg"]
)
btn_sair.place(x=btn_x, y=start_y + spacing * 2)  # Terceiro botão (Sair)

# Inicia o loop principal da interface gráfica, mantendo a janela aberta e responsiva
root.mainloop()

