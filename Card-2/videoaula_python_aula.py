#Comando para selecionar qual versão do python usar.
#!python3

#printa uma mensagem no terminal
print("Bem vindo")

#printa o nome do módulo
print(__name__)
#printa o pacote a qual o arquivo executado pertence
print(__package__)

#Variáveis
print('\n\n\n')
print('Variáveis')
print('\n\n\n')

#atribui um valor a uma variável
a = 3
b = 4.4

print(a+b)

texto = 'Sua idade é...'
idade = 23

#str() transforma uma variável de outro tipo para String
print(texto + ' ' + str(idade))

#FString, que funciona para referenciar outros tipos de valores no Print
print(f'{texto} {idade}')
print(f'{texto} {15+12}')

#Vai mostrar o texto 3 vezes
saudacao = 'Bom dia! '
print(3 * saudacao)

#Conversão de que constantes usam letras maiúsculas
PI = 3.14

#Pede uma entrada para o usuário via o terminal
raio = float(input('Informe o raio da circunferência: '))
#A função float converte o input para o tipo float
area = PI * pow(raio, 2)
#Pow é uma função para calcular potencias

#Mostra o tipo da variável
print(type(raio))

print(f'A área da circunferência é {area}')


print('\n\n\n')

#Tipos básicos do python
print('#Tipos básicos do python')
print('\n\n\n')

print(type(1))
print(type(1.1))
print(type('texto'))
print(type(True))
print(type(False))


print('\n\n\n')

#Lista
print('Lista')
print('\n\n\n')

nums = [1, 2, 3]
print(type(nums))

#append() adiciona valores na lista
nums.append(3) #Listas podem possuir valores repetidos
nums.append(4)
nums.append(5)

#len() mostra o tamanho da lista
print(len(nums))

#Altera o valor do elemento da lista no indice selecionado
nums[3] = 100
print(nums)

#insert() adiciona um elemento na posição da lista que é desejado e reposiciona o resto
nums.insert(0, -200)
print(nums)
#printa o elemento do index na lista
print(nums[5])
#printa o elemento no index na lista contando de frente pra tras
print(nums[-1])

print(2 in nums) #Mostra se o 2 está na lista

print('\n\n\n')

# Tupla
print('Tupla')
print('\n\n\n')

nomes = ('Ana', 'Bia', 'Gui', 'Leo','Ana')
print(type(nomes))
print(nomes)

print('bia' in nomes) #Mostra se o valor está presente na tupla

print(nomes[0])
print(nomes[1:3])
print(nomes[1:-1])
print(nomes[2:])
print(nomes[:-2])
#Serve para printar de um ponto da tupla (funciona nas listas) até outro

print('\n\n\n')

# Conjunto
print('Conjunto')
print('\n\n\n')

print({1,2,3})
print(type({1,2,3}))
conj = {1,2,3,3,3,3,3,3,3,3} #Conjuntos não aceitam valores repetidos

# print(conj[0]) #conjuntos não suportam index

print(conj)
print(len(conj))

print('\n\n\n')

# Dicionarios
print('Dicionarios')
print('\n\n\n')

aluno = {
    'nome': 'Pedro Henrique',
    'nota': 9.2,
    'ativo': True
}

print(type(aluno))

# Acessar pela chave
print(aluno['nome'])
print(aluno['nota'])
print(aluno['ativo'])

print(len(aluno))

print('\n\n\n')


# Operadores Unarios
print('Operadores Unarios')
print('\n\n\n')

# Operador de negação
print(not True)
print(not False)

y = 4

# Operador Menos
print(-y)
print(--y)

# Operador mais
print(+y)

# Não existe operador de incremento ou decremento no python
# y++

print('\n\n\n')

# Operadores Aritmeticos
print('Operadores Aritmeticos')
print('\n\n\n')

x = 10
y = 3

print(x + y)
print(x - y)
print(x * y) #Multiplicação
print(x / y)
print(x // y) # no vídeo nao é citado pois ele utiliza a versão 2 do python, mas esse operador mostra apenas
              # o resultado inteiro da divisão
print(x % y) #resto da divisão

par = 34
impar = 33

#Comparação
print(par % 2 == 0)
print(impar % 2 == 1)

print('\n\n\n')

# Operadores relacionais
print('Operadores relacionais')
print('\n\n\n')

x = 7
y = 5

# Comparações que retornam verdadeiro ou falso
print(x > y)
print(x >= y)
print(x < y)
print(x <= y)
print(x == y)
print(x != y)

# Compara os tipos também
print('5' != 5)

print('\n\n\n')

# Operadores de atribuicao
print('Operadores de atribuicao')
print('\n\n\n')

resultado = 2
print(resultado)

# Atribuições com operações aritméticas
resultado += resultado
resultado += 3
resultado -= 1
resultado *= 4
resultado /= 2
resultado %= 6

print(resultado)

# Fazendo uma nova atribuição a mesma variável
resultado = 'texto'
print(resultado)

# Python possui tipos dinamicos


print('\n\n\n')

# Operadores logicos
print('Operadores logicos')
print('\n\n\n')

b1 = True
b2 = False
b3 = True

# Operador lógico binário
print(b1 and b2 and b3)
print(b1 or b2 or b3)
print(b1 != b2) #xor
print(not b1)
print(not b2)

print(b1 and not b2 and b3)

x = 3
y = 4

print(b1 and not b2 and x < y) # Usando operador relacional com operador lógico

print('\n\n\n')


# Operadores ternarios
print('Operadores ternarios')
print('\n\n\n')

lockdown = False
grana = 30
status = 'Em casa' if lockdown or grana <= 100 else 'Uhuuuuuuuu!'
#If ternário que faz algo se for verdadeiro ou faz outra coisa caso seja falso dada uma condição
print(f'O status é : {status}')

print('\n\n\n')


# If
print('If')
print('\n\n\n')

nota = float(input('Informe a nota do aluno: '))
comportado = True if input('é comportado? (s/n): ') == 's' else False

# Verificação para as notas
if nota >= 9:
    print('Duas palavras: para bens! :P')
    print('Quadro de Honra')
elif nota >= 7:
    print('Aprovado')
elif nota >= 5.5:
    print('Recuperação')
elif nota >= 3.5:
    print('Recuperação + Trabalho')
else:
    print('Reprovado')

print(nota)

#Python utiliza de blocos para saber o que executar

# Usando If para verificar se uma variável existe
a = 'valor' # True
a = 0 # False
a = -0.000001 # True
a = '' # False
a = ' ' # True
a = [] # False


if a:
    print('Existe')
else:
    print('Não existe ou zero ou vazio')

print('\n\n\n')

# For
print('For')
print('\n\n\n')

# De 0 a 9
for i in range (10):
    print(i)

print('\n')

# De 1 a 10
for i in range (1, 11): # '1' define o começo
    print(i)

print('\n')

for i in range (1, 100, 7): # '7' define o passo
    print(i)

print('\n')

for i in range (20, 0, -3): # De frente pra trás
    print(i)

print('\n')

nums = [2, 4, 6, 8]
for n in nums: # Acessando todos os números da lista
    print(n, end=' ') # end é uma atribuição para o final do print

print('\n')

texto = 'Python é muito massa!'
for letra in texto: # Printando as letras da String
    print(letra, end=' ')

print('\n')

for n in {1, 2, 3, 4, 4, 4, 4, 4}: # Printando os elementos de um conjunto
    print(n, end=' ')

print('\n')

produto = {
    'nome': 'Caneta',
    'preco': 8.80,
    'desc': 0.5
}

for atrib in produto: # Pegando os atributos do produto
    print(atrib, '==>', produto[atrib]) # produto[atrib] pega os valores dos atributos

print('\n')


for atrib, valor in produto.items(): # Mesma coisa mas mais simples
    print(atrib, '==>', valor)

print('\n')


for valor in produto.values(): # Percorre apenas os valores
    print(valor, end=' ')

print('\n')

for atrib in produto.keys(): # Percorre apenas as chaves
    print(atrib, end=' ')


print('\n\n\n')

# While
print('While')
print('\n\n\n')

x = 10

# Enquanto X for verdadeiro, executa o loop
while x:
    print(x)
    x -= 1
print('Fim')
# Não recomendado, melhor utilizar o For

total = 0
qtde = 0
nota = 0

# Executa enquanto nota for diferente de -1
while nota != -1:
    nota = float(input('Informe a nota ou -1 para sair: '))
    if nota != -1:
        qtde += 1
        total += nota

print(f'A média da turma é {total / qtde}')

print('\n\n\n')


# Outros exemplos
print('Outros exemplos')
print('\n\n\n')

pessoas = ['Gui', 'Rebeca']
adj = ['Sapeca', 'Inteligente']

for p in pessoas:
    for a in adj:
        print(f'{p} é {a}!')

for i in [1, 2, 3]:
    pass
# Usa-se pass quando quer deixar um laço vazio

for i in range(1, 11):
    if i % 2:
        continue # Quebra o laço e continua, ou seja, pula para o próximo loop e não executa o print que está na próxima linha
    print(i, end=' ')

for i in range(1, 11):
    if i == 5:
        break # Para o laço for inteiro
    print(i, end=' ')
print('Fim')

print('\n\n\n')


# Funções
print('Funções')
print('\n\n\n')

# Toda função tem um bloco com o algoritmo associado a ela.
def saudacao_pela_manha():
    print('Bom dia')

saudacao_pela_manha()

def saudacao(nome = 'Pessoa', idade = 20): # Parametro padrão
    print(f'Bom dia, {nome}! Você nem parece ter {idade} anos.')

# def saudacao():
#     print('Bom dia')
# Não é utilizado dessa forma em python

saudacao('Maria', 15)
saudacao('Carlos')
saudacao(idade=33)

if __name__ == '__main__': # Verifica se esse arquivo é o que começou a execução, se é o principal
    saudacao('Ana', 30)

def soma_e_multi(a, b, x):
    return (a + b) * x

a = soma_e_multi(10, 2, 3)
print(a)

print('\n\n\n')


# Packing
print('Packing')
print('\n\n\n')

def soma(*nums): # O parametro é uma Tupla
    total = 0
    for n in nums:
        total += n
    return total

s = soma(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 10)
print(s)

def resultado_final(**kwargs):
    status = 'aprovado(a)' if kwargs['nota'] >= 7 else 'reprovado(a)'
    print(kwargs['nome'])
    print(kwargs['nota'])
    return f'{kwargs["nome"]} foi {status} '

resultado = resultado_final(nome='Pedro', nota= 6.3)
print(resultado)

print('\n\n\n')

# Retornando funções
print('Retornando funções')
print('\n\n\n')

def soma(a, b):
    return a + b

def sub(a, b):
    return a - b

somar = soma
print(somar(3, 4))

def operacao_aritmetica(fn, op1, op2): # Passar uma função como parâmetro
    return fn(op1, op2)

resultado = operacao_aritmetica(soma, 13, 48)
print(resultado)

resultado = operacao_aritmetica(sub, 13, 48)
print(resultado)

def soma_parcial(a): # Da para definir uma função dentro da outra
    def concluir_soma(b):
        return a + b
    return concluir_soma

# Fn recebe uma função e não a soma direto
fn = soma_parcial(10)
resultado_final = fn(12)
print(resultado_final)

resultado_final = soma_parcial(10)(12) # Forma direta de executar a função logo após ter recebido
print(resultado_final)

print('\n\n\n')

# Map Reduce
from functools import reduce

print('Map Reduce')
print('\n\n\n')

def somar_nota(delta):
    def somar(nota):
        return nota + delta
    return somar

notas = [6.4, 7.2, 5.8, 8.4]
notas_finais_1 = map(somar_nota(1.5), notas) # Usando map para criar uma nova lista a partir de uma lista
notas_finais_2 = map(somar_nota(2), notas)

#Esse bloco serve para transformar o map em uma lista de fato, pois o map nao funciona como mostrado no vídeo, porque
#estou utilizando o python 3 e não o python 2. Por isso, foi necessário a adição da função list()
notas_finais_1 = list(notas_finais_1)
notas_finais_2 = list(notas_finais_2)

print(notas)
print(notas_finais_1)
print(notas_finais_2)

def somar(a, b):
    return a + b

total = reduce(somar, notas, 0) # Soma das notas
print(total)

# Método nao muito recomendado
# for i, nota in enumerate(notas): # Enumerate para conseguir pegar o índice
#     notas[i] = nota + 1.5
#
# for i in range(len(notas)):
#     notas[i] = notas[i] + 1.5


print('\n\n\n')

# Lambda
from functools import reduce

print('Lambda')
print('\n\n\n')

alunos = [
    {'nome': 'Ana', 'nota': 7.2},
    {'nome': 'Breno', 'nota': 8.1},
    {'nome': 'Claudia', 'nota': 8.7},
    {'nome': 'Pedro', 'nota': 6.4},
    {'nome': 'Rafael', 'nota': 6.7},
]

aluno_aprovado = lambda aluno: aluno['nota'] >= 7 # Recebe um aluno como parametro, retorna verdadeiro ou falso
alunos_aprovados = list(filter(aluno_aprovado, alunos)) # Cria uma nova lista filtrando conforme a outra função retorna
                                                        # verdadeiro/falso

# Pega as notas dos alunos aprovados e adiciona em uma nova lista
obter_nota = lambda aluno: aluno['nota']
notas_alunos_aprovados = list(map(obter_nota, alunos_aprovados))

somar = lambda a, b: a + b
total = reduce(somar, notas_alunos_aprovados, 0) # Somando as notas

print(total / len(notas_alunos_aprovados))

print('\n\n\n')

# Classes
print('Classes')
print('\n\n\n')

class Produto:
    def __init__(self, nome, preco = 1.99, desc = 0.0): # Método construtor do python
        # Atributos da classe
        self.__nome = nome # Colocar 2 underlines para definir o atributo como privado (Existe como burlar mas é uma convenção)
        self.__preco = preco
        self.desc = desc

    @property # Criando uma nova função para utilizar o nome
    def nome(self):
        return self.__nome

    @property
    def preco(self):
        return self.__preco

    @preco.setter # Criando um setter com condição, para que não seja manipulado diretamente
    def preco(self, novo_preco):
        if novo_preco > 0:
            self.__preco = novo_preco

    # Função própria da classe
    @property # Decorator que faz chamar a função como se fosse um atributo
    def preco_final(self):
        return (1 - self.desc) * self.__preco

p1 = Produto('Caneta', 5.99, 0.1)
p2 = Produto('Caderno', 12.99, 0.2)

print(p1.nome, p1.preco, p1.desc, p1.preco_final)
print(p2.nome, p2.preco, p2.desc, p2.preco_final)

print('\n\n\n')

# Herança
print('Herança')
print('\n\n\n')

class Carro:
    def __init__(self):
        self.__velocidade = 0

    @property
    def velocidade(self):
        return self.__velocidade

    def acelerar(self):
        self.__velocidade += 5
        return self.__velocidade

    def frear(self):
        self.__velocidade -= 5
        if self.__velocidade <= 0:
            self.__velocidade = 0
        return self.__velocidade

# Criando subclasses de carro
class Uno(Carro):
    pass

class Ferrari(Carro):
    #Sobrescrevedo a função acelerar
    def acelerar(self):
        super().acelerar()
        return super().acelerar()

c1 = Ferrari()
print(c1.acelerar())
print(c1.acelerar())
print(c1.acelerar())
print(c1.frear())
print(c1.frear())
print(c1.frear())

class Contador:
    contador = 0 # Atributo de classe

    def inst(self):
        return 'Estou bem!'

    @classmethod
    def inc(cls):
        cls.contador += 1
        return cls.contador

    @classmethod
    def dec(cls):
        cls.contador -= 1
        return cls.contador

    # Método estático, caso nao precise acessar nada que precise a classe (também nao precisa de um objeto (instancia))
    @staticmethod
    def mais_um(n):
        return n + 1

# Não é preciso criar uma instancia, pois utilizamos métodos de classes e um atributo de classe.
print(Contador.inc())
print(Contador.inc())
print(Contador.inc())
print(Contador.dec())
print(Contador.dec())
print(Contador.dec())

# Esse vai dar erro, pois precisa de um objeto
# print(Contador.inst())

# Agora vai funcionar
c1 = Contador()
print(c1.inst())

print(Contador.mais_um(2))

print('\n\n\n')