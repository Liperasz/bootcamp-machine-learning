# Nesse código prático meu objetivo foi tentar melhorar o codigo v2 feito na aula, utilizando o tiktoken
# para fazer a tokenização do input inves de fazer caractere por caractere, o resultado é que agora os tokens
# sao subwords e nao um caractere apenas

import torch
import torch.nn as nn
from torch.nn import functional as F
import tiktoken

# hyper parametros
# quantidade de sequencias para processar em paralelo
batch_size = 16
# quantidade de contexto por predicao
block_size = 128
max_iters = 5000
eval_interval = 100
learning_rate = 1e-3
device = 'cuda' if torch.cuda.is_available() else 'cpu'
eval_iters = 200
n_embd = 64
n_head = 4
n_layer = 4
dropout = 0.0

torch.manual_seed(1337)

# comando para baixar o arquivo de texto
# wget https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt

# lendo o arquivo de texto
with open('input.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# usando o tokenizador BPE do GPT-2 (via tiktoken) no lugar de caracteres individuais
enc = tiktoken.get_encoding("gpt2")

# tamanho do vocabulário
vocab_size = enc.n_vocab

# encoder pega uma string e transforma em inteiros 
encode = lambda s: enc.encode(s)
# decoder pega uma lista de inteiros e transforma em uma string
decode = lambda l: enc.decode(l)

# divide os dados em treino e teste
data = torch.tensor(encode(text), dtype=torch.long)
# os primeiros 90% serao para treino, o resto para validacao
n = int(0.9*len(data))
train_data = data[:n]
val_data = data[n:]

# carrega os dados
def get_batch(split):
    # gera um pequeno lote de dados de treino e teste
    data = train_data if split == 'train' else val_data
    ix = torch.randint(len(data) - block_size, (batch_size,))
    x = torch.stack([data[i:i+block_size] for i in ix])
    y = torch.stack([data[i+1:i+block_size+1] for i in ix])
    x, y = x.to(device), y.to(device)
    return x, y

# função para calcular a loss do modelo e treinar ele
@torch.no_grad()
def estimate_loss():
    out = {}
    model.eval()
    for split in ['train', 'val']:
        losses = torch.zeros(eval_iters)
        for k in range(eval_iters):
            X, Y = get_batch(split)
            logits, loss = model(X, Y)
            losses[k] = loss.item()
        out[split] = losses.mean()
    model.train()
    return out

class Head(nn.Module):
    # um unico head de auto attention

    def __init__(self, head_size):
        super().__init__()
        self.key = nn.Linear(n_embd, head_size, bias=False)
        self.query = nn.Linear(n_embd, head_size, bias=False)
        self.value = nn.Linear(n_embd, head_size, bias=False)
        self.register_buffer('tril', torch.tril(torch.ones(block_size, block_size)))

        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        B,T,C = x.shape
        k = self.key(x)   # (B,T,C)
        q = self.query(x) # (B,T,C)
        # calcula os scores de atencao ("afinidades")
        wei = q @ k.transpose(-2,-1) * C**-0.5 # (B, T, C) @ (B, C, T) -> (B, T, T)
        wei = wei.masked_fill(self.tril[:T, :T] == 0, float('-inf')) # (B, T, T)
        wei = F.softmax(wei, dim=-1) # (B, T, T)
        wei = self.dropout(wei)
        # realiza a agregacao ponderada dos valores
        v = self.value(x) # (B,T,C)
        out = wei @ v # (B, T, T) @ (B, T, C) -> (B, T, C)
        return out

class MultiHeadAttention(nn.Module):
    # multiplas head attentions em paralelo

    def __init__(self, num_heads, head_size):
        super().__init__()
        self.heads = nn.ModuleList([Head(head_size) for _ in range(num_heads)])
        self.proj = nn.Linear(n_embd, n_embd)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        out = torch.cat([h(x) for h in self.heads], dim=-1)
        out = self.dropout(self.proj(out))
        return out

class FeedFoward(nn.Module):
    # uma camada linear seguida de uma nao linearidade

    def __init__(self, n_embd):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_embd, 4 * n_embd),
            nn.ReLU(),
            nn.Linear(4 * n_embd, n_embd),
            nn.Dropout(dropout),
        )

    def forward(self, x):
        return self.net(x)

class Block(nn.Module):
    # um bloco de transformer: comunicacao seguida de computacao

    def __init__(self, n_embd, n_head):
        # n_embd: dimensao do embedding, n_head: numero de heads desejadas
        super().__init__()
        head_size = n_embd // n_head
        self.sa = MultiHeadAttention(n_head, head_size)
        self.ffwd = FeedFoward(n_embd)
        self.ln1 = nn.LayerNorm(n_embd)
        self.ln2 = nn.LayerNorm(n_embd)

    def forward(self, x):
        x = x + self.sa(self.ln1(x))
        x = x + self.ffwd(self.ln2(x))
        return x

# modelo
class GPTLanguageModel(nn.Module):

    def __init__(self):
        super().__init__()
        # lookup table que mapeia cada token BPE para um vetor de embedding
        self.token_embedding_table = nn.Embedding(vocab_size, n_embd)
        self.position_embedding_table = nn.Embedding(block_size, n_embd)
        self.blocks = nn.Sequential(*[Block(n_embd, n_head=n_head) for _ in range(n_layer)])
        # normalizacao da camada final
        self.ln_f = nn.LayerNorm(n_embd)
        self.lm_head = nn.Linear(n_embd, vocab_size)

    def forward(self, idx, targets=None):
        B, T = idx.shape

        # idx e targets sao tensores (B,T) de inteiros representando tokens BPE
        tok_emb = self.token_embedding_table(idx) # (B,T,C)
        pos_emb = self.position_embedding_table(torch.arange(T, device=device)) # (T,C)
        x = tok_emb + pos_emb # (B,T,C)
        x = self.blocks(x) # (B,T,C)
        x = self.ln_f(x) # (B,T,C)
        # pega os logits da tabela
        logits = self.lm_head(x) # (B,T,vocab_size)

        if targets is None:
            loss = None
        else:
            # pega as dimensoes do logit
            B, T, C = logits.shape

            # achatando em uma dimensao
            logits = logits.view(B*T, C)
            targets = targets.view(B*T)

            # calcula a loss
            loss = F.cross_entropy(logits, targets)

        return logits, loss

    def generate(self, idx, max_new_tokens):
        # idx é um array (B, T) de indices de tokens BPE no contexto atual
        for _ in range(max_new_tokens):
            # recorta o idx para os ultimos block_size tokens
            idx_cond = idx[:, -block_size:]
            # pega os logits do contexto inicial
            logits, loss = self(idx_cond)
            # pega o token mais recente da sequencia
            # transforma o formato (B, T, C) para (B, C)
            logits = logits[:, -1, :]
            # aplica a funcao softmax para calcular a probabilidade
            probs = F.softmax(logits, dim=-1) # (B, C)
            # preve o proximo token BPE
            idx_next = torch.multinomial(probs, num_samples=1) # (B, 1)
            # adiciona o novo token
            idx = torch.cat((idx, idx_next), dim=1) # (B, T+1)
        return idx

# instancia o modelo
model = GPTLanguageModel()
m = model.to(device)

# exibe o numero de parametros no modelo
print(sum(p.numel() for p in m.parameters())/1e6, 'M parameters')

# criando um optmizador
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)

# treinando o modelo
for iter in range(max_iters):

    # avalia o loss com os dados de validação
    if iter % eval_interval == 0 or iter == max_iters - 1:
        losses = estimate_loss()
        print(f"step {iter}: train loss {losses['train']:.4f}, val loss {losses['val']:.4f}")

    # batch de dados
    xb, yb = get_batch('train')

    # avaliação do modelo
    logits, loss = model(xb, yb)
    optimizer.zero_grad(set_to_none=True)
    loss.backward()
    optimizer.step()

# criando texto com o modelo
# o contexto inicial é o token de inicio de sequencia do GPT-2
context = torch.zeros((1, 1), dtype=torch.long, device=device)
print(decode(m.generate(context, max_new_tokens=500)[0].tolist()))
