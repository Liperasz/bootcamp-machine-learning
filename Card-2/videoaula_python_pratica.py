import random
import time
import os


class Personagem:

    # Método construtor do personagem
    def __init__(self, nome = 'NPC', vida = 0, mana = 0, ataque = 0, defesa = 0):

        self.nome = nome
        self.vida = vida
        self.mana = mana
        self.ataque = ataque # Status de ataque do personagem
        self.defesa = defesa # Status de defesa (status definem o quão forte o personagem é)
        self.ataques = [] # Lista de ataques (será preenchido com dicionários)
        self.vivo = True # Status se o personagem está vivo

    # Função para mostrar os ataques do personagem
    def mostrar_ataques(self):
        if not self.ataques:
            print("Sem ataques")

        else:
            for i, ataque in enumerate(self.ataques):
                print(f'{i + 1} - {ataque["nome"]} - Dano: {ataque['dano']} - Mana: {ataque['mana']}')

    # Função para selecionar o ataque
    def selecionar_ataque(self):
        if not self.vivo:
            return 0

        print("Ataques: \n\n")
        self.mostrar_ataques()

        escolha = int(input("Selecione um ataque: "))
        while escolha <= 0 or escolha > len(self.ataques): # verifica escolha invalida
            escolha = int(input("Escolha invalida, escolha um ataque disponível: "))
        return self.ataques[escolha - 1]

    # Função para atacar outro personagem
    def atacar(self, alvo, ataque_utilizado):
        if not self.vivo:
            return 0

        if ataque_utilizado['mana'] > self.mana: # Verifica se o personagem tem mana suficiente para utilizar o ataque
            print('Mana insuficiente')
            return -1

        self.reduzir_mana(ataque_utilizado['mana'])
        dano_total = ataque_utilizado['dano'] * self.ataque / alvo.defesa
        print(f'{self.nome} causou {dano_total} de dano!')
        alvo.reduzir_vida(dano_total)
        return dano_total

    # Funcão que reduz mana
    def reduzir_mana(self, mana):
        self.mana -= mana
        return self.mana

    # Função que reduz vida
    def reduzir_vida(self, vida):
        self.vida -= vida
        print(f'A vida de {self.nome} abaixou para {self.vida}')
        if self.vida < 0:
            self.vida = 0
            self.morreu()
        return self.vida

    # Mostra mensagem de morte e define o personagem como morto
    def morreu(self):
        print(f'{self.nome} está morto')
        self.vivo = False

#Ataques que eu criei (nao sei como organizar isso de forma legivel)
luffy_ataque_1 = {
    'nome': 'Gomu Gomu no Pistol',
    'dano': 40,
    'mana': 0
}
luffy_ataque_2 = {
    'nome': 'Gomu Gomu no Gatling Gun',
    'dano': 55,
    'mana': 0
}
luffy_ataque_3 = {
    'nome': 'Gomu Gomu no Red Hawk',
    'dano': 80,
    'mana': 40
}
luffy_ataque_4 = {
    'nome': 'Gomu Gomu no Elephant Gun',
    'dano': 115,
    'mana': 65
}
teach_ataque_1 = {
    'nome': 'Soco Sísmico',
    'dano': 45,
    'mana': 0
}
teach_ataque_2 = {
    'nome': 'Liberation',
    'dano': 50,
    'mana': 0
}
teach_ataque_3 = {
    'nome': 'Kurouzu',
    'dano': 75,
    'mana': 35
}
teach_ataque_4 = {
    'nome': 'Shima Yurashi',
    'dano': 120,
    'mana': 70
}

# Atribuindo os ataques a lista de ataques
ataques_luffy = [luffy_ataque_1, luffy_ataque_2, luffy_ataque_3, luffy_ataque_4]
ataques_teach = [teach_ataque_1, teach_ataque_2, teach_ataque_3, teach_ataque_4]

# Criando os personagens
luffy = Personagem(nome = 'Luffy', vida = 150, mana = 100, ataque = 120, defesa = 80)
teach = Personagem(nome = 'Teach', vida = 250, mana = 200, ataque = 90, defesa = 100)

# Adicionando os ataques
luffy.ataques = ataques_luffy
teach.ataques = ataques_teach

# Função para escolher o personagem para jogar
def escolher_personagem():
    print('Escolha seu personagem!!!\n\n\n')
    print('1- Luffy')
    print('2- Teach')
    escolha = int(input('Escolha: '))
    while escolha != 1 and escolha != 2: # Verifica escolha inválida
        escolha = int(input("Escolha invalida, escolha um ataque disponível: "))
    return escolha

# Atribui o seu personagem e o personagem da cpu
player = luffy if escolher_personagem() == 1 else teach
computador = luffy if player == teach else teach

# Gameplay
while player.vivo and computador.vivo:

    os.system('cls') # Limpa a tela no windows, caso esteja no mac/linux troque por clear

    print('\n\n\n')
    print("Sua vez!\n")
    print(f'Vida: {player.vida} | Mana: {player.mana}')
    print(f'Vida do Oponente: {computador.vida} | Mana do Oponente: {computador.mana}')
    print('\n\n')

    # Loop while caso o jogador tenha escolhido um ataque que nao tenha mana suficiente para utilizar, nesse caso ele
    # apenas tem que escolher outro ataque
    while True:
        ataque = player.selecionar_ataque()
        time.sleep(1.5)
        dano = player.atacar(computador, ataque)
        time.sleep(2)
        if dano != -1:
            break


    # Verifica se o computador morreu
    if not computador.vivo:
        break

    time.sleep(3)

    print('\n\n\n')
    print(f'Vez do computador\n')
    print('\n\n')

    time.sleep(3)

    # Mesma coisa, mas agora para o computador
    while True:
        # Biblioteca random para escolha aleatória do ataque
        ataque = random.choice(computador.ataques)
        time.sleep(1.5)
        dano = computador.atacar(player, ataque)
        time.sleep(2)
        if dano != -1:
            break

    print(f"{computador.nome} vai usar '{ataque['nome']}'!")

    time.sleep(3)

print('\n\n\n')

if player.vivo:
    print(f"O grande vencedor é {player.nome}!")
else:
    print(f"O grande vencedor é {computador.nome}!")