import operator  # Operações matemáticas úteis (ex: comparação, soma)
from tkinter import *  # Interface gráfica
from time import sleep  # Pausa na execução
from random import shuffle  # Embaralhar listas (ex: cartas)
from threading import Thread  # Executar funções em paralelo (threads)

Adjust = "Auto"  # Ajuste automático da resolução

# Tela principal
rootCol = "lightgoldenrodyellow"  # Cor de fundo
root = Tk()  # Cria a janela

# Define resolução da janela conforme a tela do usuário
windowWidth = (
    (Adjust == "Auto" and root.winfo_screenwidth() >= 1350 and root.winfo_screenheight() >= 850 and [1280, 1300])
    or (Adjust == "Auto" and [1126, 1150])
    or [1280, 1300]
)
windowHeight = (
    (Adjust == "Auto" and windowWidth[0] == 1280 and [720, 800])
    or (Adjust == "Auto" and [634, 660])
    or [720, 800]
)

# Aplica configurações da janela
root.geometry(f"{windowWidth[1]}x{windowHeight[1]}")
root.title("Uno")
root.resizable(False, False)
root.configure(bg=rootCol)

# Variáveis ajustáveis
computerDelay = 1  # Tempo de "raciocínio" do computador
drawInterval = 0.1  # Intervalo visual entre ações
fontSize = (windowWidth[0] == 1280 and 20) or 12  # Tamanho da fonte baseado na resolução
fontType = "Arial"
backgroundImage = (windowWidth[0] == 1280 and "Blue") or "S_Blue"
folder = "Uno_Assets"  # Pasta com os arquivos

# Estrutura com todas as cartas do jogo
cardsInDeck = {
    "Wilds": {"Wild": 4, "Wild_Draw": 4},
    "Normal": {
        "Blue":   {"0": 1, "1": 2, "2": 2, "3": 2, "4": 2, "5": 2, "6": 2, "7": 2, "8": 2, "9": 2, "Skip": 2, "Draw": 2, "Reverse": 2},
        "Green":  {"0": 1, "1": 2, "2": 2, "3": 2, "4": 2, "5": 2, "6": 2, "7": 2, "8": 2, "9": 2, "Skip": 2, "Draw": 2, "Reverse": 2},
        "Red":    {"0": 1, "1": 2, "2": 2, "3": 2, "4": 2, "5": 2, "6": 2, "7": 2, "8": 2, "9": 2, "Skip": 2, "Draw": 2, "Reverse": 2},
        "Yellow": {"0": 1, "1": 2, "2": 2, "3": 2, "4": 2, "5": 2, "6": 2, "7": 2, "8": 2, "9": 2, "Skip": 2, "Draw": 2, "Reverse": 2}
    }
}

# Variáveis de imagem e estado inicial do jogo
cardsRemaining = []  # Cartas ainda disponíveis
fontInfo = (fontType, fontSize)  # Fonte padrão
canvas = Canvas(root, width=windowWidth[0], height=windowHeight[0])  # Área principal de desenho
canvas.place(relx=0.5, rely=0.5, anchor=CENTER)  # Centraliza o canvas

deck = None  # Referência ao monte de cartas
lastPlayed = None  # Última carta jogada
uno = False  # Flag se alguém declarou "UNO"
reverse = False  # Direção do jogo (normal ou reversa)
Colour = "Red"  # Cor inicial da rodada
oldDiscardPile = []  # Cartas já descartadas
playerCount = StringVar()  # Quantidade de jogadores (ligado ao tkinter)
players = []  # Lista de jogadores

# Carrega imagens do jogo
images = {
    "Blue": PhotoImage(file=f"{folder}/Table_3.png"),  # Tabuleiro de fundo
    "Back": PhotoImage(file=f"{folder}/Back.png"),  # Verso das cartas
    "Deck": PhotoImage(file=f"{folder}/Deck.png"),  # Monte de compra
    "UNO": PhotoImage(file=f"{folder}/Logo.png"),  # Logo do UNO
    "UNO_Button": PhotoImage(file=f"{folder}/UnoButton.png"),  # Botão de UNO
    "Red_Color": PhotoImage(file=f"{folder}/red_color.png"),  # Indicadores de cor
    "Blue_Color": PhotoImage(file=f"{folder}/blue_color.png"),
    "Green_Color": PhotoImage(file=f"{folder}/green_color.png"),
    "Yellow_Color": PhotoImage(file=f"{folder}/yellow_color.png"),
    "AvatarPlayer": PhotoImage(file="Uno_Assets/AvatarPlayer.png"),  # Avatares
    "AvatarPlayer02": PhotoImage(file="Uno_Assets/AvatarPlayer02.png"),
    "AvatarPlayer03": PhotoImage(file="Uno_Assets/AvatarPlayer03.png"),
    "AvatarPlayer04": PhotoImage(file="Uno_Assets/AvatarPlayer04.png"),
}

# Cores de fundo que simulam transparência
pseudoBackground = "#1b1e24"
darkPseudoBack = "#1b1e24"

# Monte de compra desenhado na tela
drawDeck = Label(canvas, image=images["Deck"], bg=pseudoBackground)

class Player():            
    def __init__(self, name, anch, x, y, isTurn, bot, scoreLabelPos):
        self.name = name  # Nome do jogador
        self.hand = []  # Cartas na mão
        self.score = 0  # Pontuação (vence com 500)
        
        # Frame visual onde as cartas são exibidas
        self.frame = Frame(canvas, width=109, height=158, bg=darkPseudoBack)
        
        # Label que mostra o placar do jogador
        self.ScoreLabel = Label(root, text=f"{name}: 0", font=fontInfo, bg=rootCol)
        self.ScoreLabel.place(relx=scoreLabelPos, anchor="n")
        
        self.frame.place(relx=x, rely=y, anchor=anch)  # Posiciona o frame das cartas
        self.objects = []  # Objetos visuais das cartas
        self.bot = bot  # Define se é bot ou jogador
        self.turn = isTurn  # Se é o turno atual
        self.drawn = False  # Controle de "já comprou carta?"
        self.lastDrawn = None  # Última carta comprada
        players.append(self)  # Adiciona o jogador à lista geral
        
        # Define orientação do frame: horizontal ou vertical
        self.side = "H" if anch in ["s", "n"] else "V"
        
        self.draw(7)  # Compra 7 cartas iniciais
        
    def restart(self, isTurn):
        for i in self.objects:
            i.destroy()  # Remove cartas visuais antigas

        self.hand = []  # Esvazia a mão
        self.objects = []  # Esvazia os objetos visuais
        self.turn = isTurn  # Atualiza o turno
        self.ScoreLabel["fg"] = "Black"  # Reset da cor do placar
        self.drawn = False
        self.LastDrawn = None
        self.draw(7)  # Recomeça com 7 cartas
        
    def useCard(self, event, card):
        global lastPlayed, Colour, uno

        # Validação básica: só joga se for sua vez, tiver cor ativa e a carta for válida
        if not self.turn or not Colour or not isValidCard(card):
            return

        # Remove a carta visualmente e da mão do jogador
        self.objects[self.hand.index(card)].destroy()
        self.objects.pop(self.hand.index(card))
        self.hand.remove(card)

        # Adiciona a carta à pilha de descarte e atualiza a interface
        oldDiscardPile.append(card)
        self.updateHand()
        usedPileCard = Label(canvas, image=images[card], bg=pseudoBackground)
        usedPileCard.place(relx=0.5, rely=0.5, anchor=CENTER)
        ColourChosen.place_forget()

        viableWild = True  # Assume que Wild_Draw é válida até provar o contrário

        # === Carta é coringa (Wild ou Wild_Draw) ===
        if card.find("Wild") != -1:
            # Verifica se o Wild_Draw foi jogado corretamente (sem cor disponível)
            if card.find("Draw") != -1 and lastPlayed[:lastPlayed.find("_")] in ''.join(self.hand):
                viableWild = False

            if not self.bot:
                changeColour(None)  # Jogador escolhe cor manualmente
            else:
                # Bot escolhe a cor com base nas cartas que mais tem
                string = ''.join(self.hand)
                appearances = {
                    "Green": string.count("Green"),
                    "Blue": string.count("Blue"),
                    "Red": string.count("Red"),
                    "Yellow": string.count("Yellow")
                }
                changeColour(max(appearances.items(), key=operator.itemgetter(1))[0])
        else:
            lastPlayed = card  # Carta comum, apenas atualiza o histórico

        # === Verifica se acabou as cartas (venceu) ===
        if len(self.hand) == 0:
            gameOver(self)
            return
        # === Só uma carta na mão: precisa ter declarado "UNO" ===
        elif len(self.hand) == 1:
            if uno:
                UnoSign.place(relx=0.5, rely=0.5, anchor=CENTER)
                root.after(500, lambda: UnoSign.place_forget())
            else:
                self.draw(2)  # Punição por não declarar UNO

        uno = False  # Reseta a flag de UNO

        # === Executa ações conforme tipo da carta ===
        if card.find("Reverse") != -1 or card.find("Skip") != -1:
            self.endTurn(card[card.find("_") + 1:])
        elif card == "Wild_Draw" != -1:
            if viableWild:
                self.endTurn("Draw_4")
            else:
                self.draw(4)
                self.endTurn(None)
        elif card.find("Draw") != -1:
            self.endTurn("Draw_2")
        else:
            self.endTurn(None)

    def updateHand(self):
    # Atualiza visualmente a mão do jogador

        if self.side == "H":  # Mão na horizontal (jogador em cima ou embaixo)
            self.frame["width"] = len(self.objects) * 109
        else:  # Mão na vertical (jogador nos lados)
            self.frame["height"] = (len(self.objects) + 2) * (158 // 2.5)

        # Posiciona cada carta dentro do frame
        for i, obj in enumerate(self.objects, 1):
            if self.side == "H":
                obj.place(relx=i / len(self.objects), rely=0, anchor="ne")
            else:
                i -= 1
                obj.place(relx=0, rely=i / len(self.objects), anchor="nw")

            root.update()  # Atualiza a interface após reposicionar
            
    def add(self, card):
        # Adiciona a carta à mão (visual)
        self.objects.append(Label(self.frame, anchor="nw", image=images[card], bg=darkPseudoBack))
    
        # Se for jogador humano, permite clicar na carta para jogar
        if not self.bot:
            self.objects[-1].bind("<Button-1>", lambda e: self.useCard(e, card))

        self.updateHand()  # Atualiza a interface da mão
            
    def draw(self, amount):
        global deck, oldDiscardPile

        try:
            # Compra 'amount' cartas do baralho
            for i in range(amount):
                self.hand.append(deck[0])  # Adiciona à mão (lógica)
                self.lastDrawn = deck[0]  # Armazena a última carta comprada

                # Se for bot, mostra carta virada. Se for jogador, mostra real
                if self.bot:
                    self.add("Back")
                else:
                    self.add(deck[0])

                deck.pop(0)  # Remove a carta do topo do baralho
                sleep(drawInterval)  # Pausa para efeito visual
        except Exception as e:
            # Se acabar o baralho, embaralha o descarte e continua a compra
            deck = oldDiscardPile
            shuffle(deck)
            oldDiscardPile = []
            self.draw(amount)  # Tenta comprar novamente

    def handWorth(self):
        # Calcula a pontuação da mão ao final do jogo
        points = 0
        for card in self.hand:
            if card.find("Wild") > -1:
                points += 50  # Coringas valem 50 pontos
            elif len(card[card.find("_") + 1:]) > 1:
                points += 20  # Ações (Draw, Reverse, Skip) valem 20
            else:
                points += int(card[card.find("_") + 1:])  # Números valem seu valor
        return points

    def endTurn(self, special):
        global reverse

        # Remove o aviso de "verificação" se estiver na tela
        try:
            CheckSide.place_forget()
        except:
            pass

        # Configura efeitos especiais
        increment = 1  # Quantos jogadores avançar no turno
        drawAmt = False  # Quantidade de cartas a serem compradas pelo próximo jogador

        if special == "Skip":
            increment = 2  # Pula o próximo jogador
        elif special == "Reverse":
            if len(players) > 2:
                reverse = not reverse  # Inverte o sentido do jogo
            else:
                increment = 2  # Em 2 jogadores, "Reverse" age como "Skip"
        elif special == "Draw_2":
            drawAmt = 2
        elif special == "Draw_4":
            drawAmt = 4

        # Finaliza o turno do jogador atual
        self.turn = False
        self.drawn = False
        self.ScoreLabel["fg"] = "Black"  # Remove destaque visual

        # Calcula o próximo jogador com base na direção do jogo
        n = players.index(self)
        if reverse:
            n -= increment
        else:
            n += increment

        # Corrige se passou dos limites da lista
        if n > len(players) - 1:
            n -= len(players)
        elif n < 0:
            n += len(players)

        plr = players[n]  # Próximo jogador

        if drawAmt > 0:
            plr.draw(drawAmt)  # Faz o jogador comprar
            plr.endTurn(None)  # Pula o turno dele
        else:
            plr.turn = True  # Ativa o turno do próximo
            plr.ScoreLabel["fg"] = "Red"  # Destaca quem está jogando
            
                      
    def drawFromDeck(self):
        # Só permite comprar se for a vez do jogador e ele ainda não comprou
        if self.turn and not self.drawn:
            self.drawn = True  # Marca que o jogador já comprou
            self.draw(1)  # Compra uma carta
            card = self.lastDrawn

            # Se a carta comprada não for válida, encerra o turno
            if not isValidCard(card):
                self.endTurn(None)
            else:
                # Caso a carta seja jogável, exibe a opção de usá-la
                CheckSide.place(relx=0.35, rely=0.5, anchor="w")
                checkImage["image"] = images[card]

    def botPlay(self):
        usableCards = []  # Lista de cartas que o bot pode jogar

        # Verifica todas as cartas da mão e adiciona as jogáveis
        for card in self.hand:
            if isValidCard(card):
                usableCards.append(card)
                
        if len(usableCards) == 0:
            # Nenhuma carta jogável → compra uma
            self.draw(1)
            if isValidCard(self.hand[-1]):
                self.useCard(None, card)  # Se a carta comprada for jogável, joga
            else:
                self.endTurn(None)  # Se não for, passa a vez
        else:
            # Há cartas jogáveis
            
             # Remove Wild_Draw caso não seja permitido jogar
            if lastPlayed[:lastPlayed.find("_")] in usableCards:
                while "Wild_Draw" in usableCards:
                    usableCards.remove("Wild_Draw")

            # Conta quantas vezes cada cor aparece nas cartas jogáveis
            string = ''.join(usableCards)
            appearances = {
                "Green": string.count("Green"),
                "Blue": string.count("Blue"),
                "Red": string.count("Red"),
                "Yellow": string.count("Yellow"),
                "Wild": string.count("Wild")
            }

            # Escolhe a cor mais frequente
            mostAppeared = max(appearances.items(), key=operator.itemgetter(1))[0]

            # Escolhe a primeira carta daquela cor (ou Wild)
            card = [obj for obj in usableCards if mostAppeared in obj][0]
            self.useCard(None, card)  # Joga a carta escolhida
            
def generateDeck(dictionary):
    unshuffledDeck = []  # Baralho ainda não embaralhado

    for i, value in enumerate(cardsInDeck):  # 'Wilds' ou 'Normal'
        mainDictionary = cardsInDeck[value]

        for j, v in enumerate(mainDictionary):  # Cor (se for Normal) ou tipo (se for Wilds)
            if i == 0:
                # Adiciona cartas coringas (sem cor definida)
                for n in range(mainDictionary[v]):
                    unshuffledDeck.append(v)
            else:
                # Adiciona cartas normais com cor + valor (ex: Red_3, Blue_Skip)
                for k, v2 in enumerate(mainDictionary[v]):
                    unshuffledDeck.append(f"{v}_{v2}")

    shuffle(unshuffledDeck)  # Embaralha o baralho
    return unshuffledDeck

def gameOver(winner):
    global players

    # Adiciona 1 ponto ao vencedor da rodada
    winner.score += 1

    # Atualiza o placar na interface
    winner.ScoreLabel["text"] = f"{winner.name}: {winner.score}"

    # Verifica se o jogador venceu 3 partidas (fim do jogo)
    if winner.score >= 3:
        victoryScreen = Toplevel(root)  # Cria uma nova janela
        victoryScreen.title("Fim de Jogo")
        victoryScreen.geometry("400x200")
        victoryScreen.configure(bg=rootCol)

        # Exibe mensagem de vitória
        Label(victoryScreen, text=f"{winner.name} venceu o jogo!", font=("Arial", 20), bg=rootCol).pack(expand=True)
        Button(victoryScreen, text="Fechar", command=root.destroy, font=("Arial", 14)).pack(pady=20)

        root.update()  # Atualiza a interface
        return

    # Se ainda não ganhou o jogo, reinicia para nova rodada
    for plr in players:
        plr.restart(False)  # Reseta todos os jogadores

    # Jogador 1 começa
    players[0].turn = True
    players[0].ScoreLabel["fg"] = "Red"  # Destaca o jogador da vez

def changeColour(col):
    global Colour, lastPlayed
    Colour = col

    if not Colour:
        ColourPicker.place(relx=0.20, rely=0.5, anchor="w")  # Ajuste aqui para mudar posição
        root.update()
        return

    ColourPicker.place_forget()

    # imagem correspondente
    img_key = f"{Colour}_Color"

    # destruir anterior se existir
    for widget in ColourChosen.winfo_children():
        widget.destroy()

    img_label = Label(ColourChosen, image=images[img_key], bg="#1b1e24", bd=0)
    img_label.image = images[img_key]
    img_label.pack()

    ColourChosen.place(relx=0.35, rely=0.5, anchor="w")  # Mesmo ajuste para a exibição da cor escolhida
    lastPlayed = f"{Colour}_Wild"
        
def addColour(color, x, y):
    img_key = f"{color}_Color"

    # Criar um Frame "container" com padding
    wrapper = Frame(ColourPicker, width=100, height=100, bg="#1b1e24", highlightthickness=0, bd=0)
    wrapper.place(relx=x, rely=y, anchor="center")

    label = Label(wrapper, image=images[img_key], bg="#1b1e24", cursor="hand2", bd=0, highlightthickness=0)
    label.image = images[img_key]  # manter referência
    label.pack()  # centraliza dentro do frame
    label.bind("<Button-1>", lambda e: changeColour(color))

def isValidCard(card):
    # Verifica se a carta é jogável:
    if card.find("Wild") == -1 and lastPlayed[:lastPlayed.find("_")] != card[:card.find("_")] and lastPlayed[lastPlayed.find("_")+1:] != card[card.find("_")+1:]:
        return False
    else:
        return True

def unoTrue():
    global uno
    uno = True # Marca que o jogador declarou "UNO"

def makePlayers(n):
    global player
    try: 
        n = int(n.get()) # Tenta converter o valor da entrada
    except: 
        n = 2 # Se falhar, assume 2 jogadores como padrão
        
    # Garante que o número de jogadores esteja entre 2 e 4
    if n <= 2:
        # Cria jogador humano e 1 bot
        player = Player("Player", "s", 0.5, 1, True, False, .35)
        computer1 = Player("User01", "n", 0.5, 0, False, True, .7)
    elif n >= 3: 
        # Cria jogador humano e 2 bots
        player = Player("Player", "s", 0.5, 1, True, False, .2)
        computer1 = Player("User02", "e", 1, 0.5, False, True, .4)
        computer2 = Player("User03", "n", 0.5, 0, False, True, .6)
        if n >= 4:
            # Adiciona o quarto bot se necessário
            computer3 = Player("User04", "w", 0, 0.5, False, True, .8)
    # Destaca o jogador atual com a cor vermelha
    player.ScoreLabel["fg"] = "Red"

# Background
canvas.create_image(0, 0, anchor="nw", image=images[backgroundImage])  # Aplica imagem de fundo

# Interface para escolher o número de jogadores
playerCountLabel = Label(
    canvas, height=3, font=(fontType, 20), bg=pseudoBackground, 
    text="Input how many players you want: (2-4)"
    )

playerCountLabel.place(relx=0.5, rely=0.4, anchor="s")# Posiciona o texto

playerCountInput = Text(
    canvas, font=(fontType, 50), width=10, height=1, wrap=None
    )

playerCountInput.place(relx=0.5, rely=0.5, anchor=CENTER)# Campo de entrada

playerCountButton = Button(
    canvas, text="START", font=fontInfo, command= lambda: playerCount.set(playerCountInput.get("1.0", "end-1c"))
    )
playerCountButton.place(relx=0.5, rely=0.6, anchor="n")# Botão para confirmar

root.update()# Atualiza a interface
playerCountButton.wait_variable(playerCount)# Espera até o valor ser definido

# Limpa a tela (remove input e texto)
playerCountButton.destroy()
playerCountInput.destroy()
playerCountLabel.destroy()

# Exibe o monte de compra e o botão de UNO na tela
drawDeck.place(relx=0.58, rely=0.5, anchor=CENTER)# Mostra imagem do baralho
drawDeck.bind("<Button-1>", lambda e: player.drawFromDeck())# Clica para comprar carta

UnoButton = Label(
    canvas, width=82, height=58, image=images["UNO_Button"], bg=pseudoBackground
    )
UnoButton.place(relx=0.58,rely=0.63, anchor="n")# Mostra botão de UNO
UnoButton.bind("<Button-1>", lambda e: unoTrue())# Clica para declarar UNO

root.update()# Atualiza a interface após posicionar os elementos

# Gera o baralho e carrega imagens das cartas
deck = generateDeck(cardsInDeck)

for i in deck:
    name = f"{folder}/{i}.png"
    try:
        images[i]# Verifica se a imagem já foi carregada
    except:
        images[i] = PhotoImage(file=name)# Carrega imagem da carta se ainda não estiver no dicionário
        
# Frames para escolher e exibir cor ao jogar carta coringa
ColourPicker = Frame(canvas, width=250, height=250, bg="#1b1e24", bd=0, highlightthickness=0)
ColourChosen = Frame(canvas, width=250, height=250, bg="#1b1e24")

# Layout 2x2 para escolha de cor (usado com carta coringa)
addColour("Red", 0.3, 0.3)
addColour("Blue", 0.7, 0.3)
addColour("Green", 0.3, 0.7)
addColour("Yellow", 0.7, 0.7)

# Coloca a primeira carta do baralho na pilha de descarte e atualiza a tela
lastPlayed = deck[0]
deck.pop(0)

usedPileCard = Label(canvas, image=images[lastPlayed], bg=pseudoBackground)
usedPileCard.place(relx=0.5, rely=0.5, anchor=CENTER)

oldDiscardPile.append(lastPlayed)

# Interface para decidir se quer usar a carta comprada ou passar o turno
CheckSide = Frame(canvas, width=100,height=200,bg=pseudoBackground)

checkImage = Label(CheckSide, image = images[lastPlayed])
checkImage.place(relx=0.5,rely=0,anchor="n")

useButton = Button(
    CheckSide, text="Usar Carta", command=lambda: player.useCard(None, player.lastDrawn) # Joga a carta comprada
    )
    
endButton = Button(
    CheckSide, text="Passar a vez", command=lambda: player.endTurn(None)# Passa a vez sem jogar
    )

useButton.place(relx=0.5,rely=0.6, anchor=CENTER)
endButton.place(relx=0.5,rely=0.8, anchor=CENTER)

makePlayers(playerCount)# Cria os jogadores com base na quantidade selecionada

# Verifica o efeito da primeira carta do jogo (já colocada no centro)
if lastPlayed.find("Skip") != -1 or lastPlayed.find("Reverse") != -1:
    # Se for Skip ou Reverse, aplica o efeito diretamente
    player.endTurn(lastPlayed[lastPlayed.find("_")+1:])
elif lastPlayed == "Wild_Draw":
    # Embaralha novamente até que a primeira carta não seja um Wild_Draw (evita início injusto)
    while lastPlayed == "Wild_Draw":
        shuffle(deck)
        lastPlayed = deck[0]
elif lastPlayed.find("Wild") != -1:
     # Se for carta Wild simples, ativa a escolha de cor
    changeColour(None)
elif lastPlayed.find("Draw") != -1:
    # Se for Draw 2 (não Wild), aplica o efeito
    player.draw(2)
    player.endTurn(None)

# Loop principal do jogo
UnoSign = Label(canvas, width=410, height=288, image=images["UNO"], bg=pseudoBackground)
root.update()

# For the computer's moves
while True:
    sleep(0.01) # Pequena pausa para não travar a interface
    root.update() # Mantém a interface gráfica atualizada
    
    # Se não for o turno do jogador, passa a vez para o bot
    if not player.turn:
        sleep(computerDelay) # Simula tempo de "pensar" do computador
        for i in players:
            if i.turn:
                i.botPlay()# Executa jogada do bot
                break