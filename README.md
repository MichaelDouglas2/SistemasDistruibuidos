UNIVERSIDADE CATÓLICA DE SANTOS - SISTEMAS DISTRIBUÍDOS (CO.N1.17)
SANTOS, SP - 2025

Adrielle Valascvijus Fernandes | RA: 9333671
Alec Emil Meier | RA: 1420906
Lavínia Lopes de Lana | RA: 1373644
Matheus Moledo Fonseca Vasconcelos | RA: 6225772
Michael Douglas Santos Costa | RA: 9683205
Raquel Nazaré Belfort Costa | RA: 1016513


# UNO Pokémon - Jogo Multiplayer em Python

Este é um jogo de UNO inspirado no universo Pokémon, desenvolvido em Python com interface gráfica usando *Tkinter* e manipulação de imagens com *Pillow (PIL)*.

---

# Descrição dos arquivos

- Uno.py - Arquivo principal do jogo. Contém toda a lógica de funcionamento do UNO, controle de turnos, jogadas, pontuação e regras.
- main_menu.py - Interface inicial com botões para Jogar, Ver Regras e Sair. É o ponto de entrada visual do jogo.
- regras.py - Tela com as regras básicas do UNO. Exibida ao clicar em "Regras" no menu.
- Uno_Assets/ - Pasta com todas as imagens usadas no jogo: cartas, tabuleiro, botões, avatares e ícones.

---

# Pré-requisitos:

- Python 3.x instalado  
- Pillow (PIL) instalado:  
  ```bash
  pip install pillow

---

# Funcionalidades

- Interface gráfica completa em Tkinter
- Até *4 jogadores* (1 humano + até 3 bots)
- Cartas de ação: *Pular*, *Inverter*, *+2*, *Coringa*, *+4*
- Detecção de "UNO" (última carta)
- Escolha de cor ao jogar cartas coringas
- Vence quem ganhar 3 rodadas

---

# Como executar e jogar

- Faça o *download* ou clone o repositório: 
   git clone https://github.com/seu-usuario/uno-pokemon.git
   cd uno-pokemon
- Execute o arquivo inicial: 
   python main_menu.py
- Escolha o número de *jogadores (2 a 4)*.
- Clique no baralho para comprar carta.
- Clique no botão *UNO* quando tiver uma carta só.
- Ao comprar uma carta jogável, escolha entre usá-la ou passar.
- Bots jogam automaticamente após seu turno.
- O jogo termina quando alguém vencer *3 partidas*.

---