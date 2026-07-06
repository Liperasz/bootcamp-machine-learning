import torch
import torch.nn as nn
from torch.nn import functional as F
torch.manual_seed(1337)

# hyper parametros
# quantidade de sequencias para processar em paralelo
batch_size = 32
# quantidade de contexto por predicao
block_size = 8
max_iters = 3000
eval_interval = 300
learning_rate = 1e-2
device = 'cuda' if torch.cuda.is_available() else 'cpu'
eval_iters = 200

# comando para baixar o arquivo de texto
# wget https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt

# lendo o arquivo de texto
with open('input.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# characteres unicos que aparecem no texto
chars = sorted(list(set(text)))
vocab_size = len(chars)

# mapeando os characteres em inteiros
stoi = { ch:i for i,ch in enumerate(chars) }
itos = { i:ch for i,ch in enumerate(chars) }

# encoder pega uma string e transforma em inteiros
encode = lambda s: [stoi[c] for c in s]
# decoder pega uma lista de inteiros e transforma em uma string
decode = lambda l: ''.join([itos[i] for i in l])

# divide os dados em treino e teste
data = torch.tensor(encode(text), dtype=torch.long)
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

# modelo
class BigramLanguageModel(nn.Module):

    def __init__(self, vocab_size):
        super().__init__()
        # lookup table que mapeia cada token para um vetor
        self.token_embedding_table = nn.Embedding(vocab_size, vocab_size)

    def forward(self, idx, targets=None):

        # pega os logits da tabeka
        logits = self.token_embedding_table(idx)

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
        for _ in range(max_new_tokens):
            # pega os logits do contexto inicial
            logits, loss = self(idx)
            # pega o caracter mais recente da sequencia
            # transforma o formato  (B, T, C) para (B, C)
            logits = logits[:, -1, :]
            # aplica a funcao softmax para calcular a probabilidade
            probs = F.softmax(logits, dim=-1)
            # preve o proximo token
            idx_next = torch.multinomial(probs, num_samples=1)
            # adiciona o novo token
            idx = torch.cat((idx, idx_next), dim=1)
        return idx

# instancia o modelo
model = BigramLanguageModel(vocab_size)
m = model.to(device)

# criando um optmizador
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)

# treinando o modelo
for iter in range(max_iters):

    # avalia o loss com os dados de validação
    if iter % eval_interval == 0:
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
context = torch.zeros((1, 1), dtype=torch.long, device=device)
print(decode(m.generate(context, max_new_tokens=500)[0].tolist()))