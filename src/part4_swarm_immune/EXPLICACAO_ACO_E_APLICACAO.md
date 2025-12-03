# Explicação: Ant Colony Optimization (ACO) e Aplicação ao Problema de Montagem de Provas

## 1. O que é Ant Colony Optimization (ACO)?

### 1.1 Inspiração Biológica

O ACO é inspirado no comportamento de formigas reais ao procurar comida. Quando formigas saem do formigueiro:

1. **Exploração inicial**: Andam aleatoriamente procurando comida
2. **Descoberta**: Quando encontram comida, voltam ao formigueiro deixando um rastro de **feromônio**
3. **Comunicação**: Outras formigas seguem o rastro de feromônio (quanto mais forte, mais atraente)
4. **Reinforcement**: Formigas que encontram caminhos mais curtos reforçam o feromônio mais rápido
5. **Convergência**: Com o tempo, o caminho mais curto fica com muito feromônio e é preferido

### 1.2 Princípios Fundamentais

- **Feromônio (τ)**: Substância química que marca caminhos bons
  - Quanto mais feromônio, mais atraente o caminho
  - Evapora com o tempo (exploração contínua)
  
- **Heurística (η)**: Informação local sobre a qualidade de uma escolha
  - Não depende de experiência passada
  - Exemplo: distância até o objetivo
  
- **Probabilidade de Escolha**: Combina feromônio + heurística
  - Formigas escolhem probabilísticamente
  - Boas escolhas têm maior probabilidade, mas não são garantidas

---

## 2. Componentes do Algoritmo ACO

### 2.1 Representação do Problema como Grafo

O ACO requer que o problema seja representado como um **grafo** onde:
- **Nós/Vértices**: Estados ou componentes da solução
- **Arestas**: Transições possíveis entre estados
- **Caminho**: Sequência de arestas que forma uma solução completa

### 2.2 Construção de Soluções (Ant Construction)

Cada formiga constrói uma solução passo a passo:

```
1. Formiga começa em um nó inicial (ou aleatório)
2. Enquanto solução não está completa:
   a) Calcula probabilidades de escolha para próximos nós
   b) Escolhe próximo nó probabilísticamente
   c) Adiciona à solução parcial
3. Avalia solução completa
4. Deposita feromônio proporcional à qualidade
```

### 2.3 Regra de Transição (Probabilidade de Escolha)

A probabilidade de uma formiga escolher o nó `j` a partir do nó `i`:

```
P(i→j) = [τ(i,j)^α × η(i,j)^β] / Σ[τ(i,k)^α × η(i,k)^β]
```

Onde:
- **τ(i,j)**: Quantidade de feromônio na aresta (i→j)
- **η(i,j)**: Valor heurístico da aresta (i→j)
- **α**: Peso do feromônio (exploração de conhecimento)
- **β**: Peso da heurística (exploração local)
- **Σ**: Soma sobre todos os nós candidatos `k`

**Interpretação:**
- `α` alto: Formigas confiam mais no feromônio (exploração de conhecimento)
- `β` alto: Formigas confiam mais na heurística (exploração local)
- `α=0`: Ignora feromônio (busca aleatória)
- `β=0`: Ignora heurística (só segue feromônio)

### 2.4 Atualização de Feromônio

Após todas as formigas construírem soluções:

**1. Evaporação (Global)**:
```
τ(i,j) = (1 - ρ) × τ(i,j)
```
- `ρ` (rho): Taxa de evaporação (0 < ρ < 1)
- Remove feromônio antigo (exploração contínua)

**2. Deposição (Local ou Global)**:
```
τ(i,j) = τ(i,j) + Δτ(i,j)
```

Onde `Δτ(i,j)` depende da qualidade da solução:
- **AS (Ant System)**: Todas as formigas depositam
  ```
  Δτ(i,j) = Q / L_k  (se aresta (i,j) está na solução k)
  Δτ(i,j) = 0        (caso contrário)
  ```
  - `Q`: Constante
  - `L_k`: Custo/comprimento da solução k
  - Quanto melhor a solução, mais feromônio depositado

- **AS-Elite (Elitist Ant System)**: Melhor formiga deposita extra
  ```
  Δτ(i,j) = Q / L_k + (e × Q / L_best)  (se (i,j) está na melhor solução)
  ```
  - `e`: Peso da elite
  - `L_best`: Custo da melhor solução encontrada

---

## 3. Adaptação do Problema de Montagem de Provas para ACO

### 3.1 Desafio: Representação como Grafo

O problema original:
- **Entrada**: Banco com N questões (ex: 200 questões de Física/Dinâmica)
- **Saída**: Lista de 10 questões únicas
- **Restrições**: 
  - Sem duplicatas (hard constraint)
  - Tempo total: 50-60 min (soft constraint)
  - Dificuldade média: ~4.0 (soft constraint)

### 3.2 Modelagem do Grafo

**Opção 1: Grafo de Seleção Sequencial (Recomendada)**

Representação:
- **Nós**: Posições na prova (1, 2, 3, ..., 10)
- **Arestas**: Transições de uma posição para a próxima
- **Estado**: Prova parcial construída até o momento

```
Nó 0 (Início) → [Escolhe Q1] → Nó 1 → [Escolhe Q2] → Nó 2 → ... → Nó 10 (Fim)
```

**Estrutura:**
- Cada nó `i` representa "já escolhi i questões"
- Aresta de `i` para `i+1` representa escolher uma questão para a posição `i+1`
- Feromônio `τ(i, q)`: Quão bom é escolher questão `q` na posição `i`

**Vantagens:**
- Natural para problemas de seleção
- Fácil garantir restrições (sem duplicatas)
- Permite heurística baseada em estado parcial

**Desvantagens:**
- Feromônio depende da posição (mais complexo)

---

**Opção 2: Grafo de Questões (Alternativa)**

Representação:
- **Nós**: Questões do banco
- **Arestas**: Transições entre questões
- **Caminho**: Sequência de 10 questões

```
Q1 → Q2 → Q3 → ... → Q10
```

**Estrutura:**
- Feromônio `τ(q1, q2)`: Quão bom é escolher Q2 após Q1
- Heurística `η(q1, q2)`: Quão bom é essa combinação localmente

**Vantagens:**
- Simples de implementar
- Feromônio direto entre questões

**Desvantagens:**
- Não considera ordem (problema é conjunto, não sequência)
- Mais difícil incorporar restrições de tempo/dificuldade acumulada

---

### 3.3 Escolha da Modelagem: Grafo de Seleção Sequencial

**Vamos usar a Opção 1** porque:
1. Permite considerar estado parcial (tempo e dificuldade acumulados)
2. Facilita garantir restrições (sem duplicatas)
3. Heurística pode ser mais informativa

---

## 4. Detalhamento da Aplicação

### 4.1 Estrutura de Dados

**Feromônio:**
```python
pheromone[i][q] = quantidade de feromônio para escolher questão q na posição i
```
- `i`: Posição na prova (0 a 9)
- `q`: Questão do banco
- Matriz de tamanho: `10 × N_questoes`

**Estado da Formiga:**
```python
ant_state = {
    'prova': [q1, q2, ..., qk],  # Questões já escolhidas (k <= 10)
    'tempo_total': soma dos tempos,
    'dificuldades': [d1, d2, ..., dk],
    'posicao_atual': k  # Quantas questões já escolheu
}
```

### 4.2 Função Heurística η(i, q)

A heurística deve indicar quão "bom" é escolher questão `q` na posição `i`, considerando:
- Estado parcial atual (tempo e dificuldade acumulados)
- Meta final (tempo 50-60 min, dificuldade média 4.0)

**Proposta de Heurística:**

```python
def heuristica(posicao, questao, estado_parcial):
    """
    Calcula atratividade de escolher 'questao' na 'posicao' atual.
    Retorna valor maior para escolhas mais promissoras.
    """
    # 1. Penalidade por duplicata (hard constraint)
    if questao.id in [q.id for q in estado_parcial['prova']]:
        return 0.0  # Não pode escolher
    
    # 2. Cálculo de métricas projetadas
    tempo_projetado = estado_parcial['tempo_total'] + questao.tempo
    dificuldades_projetadas = estado_parcial['dificuldades'] + [questao.dificuldade]
    dificuldade_media_projetada = np.mean(dificuldades_projetadas)
    
    # 3. Questões restantes
    questoes_restantes = 10 - (posicao + 1)
    
    # 4. Heurística baseada em quão próximo está das metas
    score = 1.0  # Base
    
    # 4a. Tempo: penaliza se já passou do limite ou está muito abaixo
    if tempo_projetado > ALVO_TEMPO_MAX:
        # Já passou do máximo, muito ruim
        score *= 0.1
    elif tempo_projetado < ALVO_TEMPO_MIN:
        # Ainda abaixo, mas precisa considerar questões restantes
        tempo_medio_necessario = (ALVO_TEMPO_MIN - tempo_projetado) / questoes_restantes
        if questao.tempo < tempo_medio_necessario * 0.5:
            # Questão muito rápida, pode não conseguir atingir meta
            score *= 0.5
    else:
        # Dentro do intervalo, bom!
        score *= 1.5
    
    # 4b. Dificuldade: penaliza desvios da meta
    erro_dificuldade = abs(dificuldade_media_projetada - ALVO_DIFICULDADE)
    if erro_dificuldade < 0.5:
        score *= 1.2  # Muito próximo da meta
    elif erro_dificuldade > 1.0:
        score *= 0.7  # Muito longe da meta
    
    # 4c. Balanceamento: questões muito extremas são menos desejáveis
    if questao.dificuldade < 2.0 or questao.dificuldade > 4.5:
        score *= 0.8
    
    return score
```

**Características:**
- Retorna 0 para escolhas inválidas (duplicatas)
- Considera estado parcial (tempo e dificuldade acumulados)
- Projeta resultado final
- Penaliza escolhas que levam longe das metas

### 4.3 Construção de Solução por uma Formiga

```python
def construir_solucao(formiga, questoes_candidatas, feromonio, alpha, beta):
    """
    Uma formiga constrói uma prova completa.
    """
    solucao = []
    tempo_total = 0
    dificuldades = []
    
    # Para cada posição na prova (0 a 9)
    for posicao in range(10):
        # 1. Calcula probabilidades para todas as questões candidatas
        probabilidades = []
        denominador = 0.0
        
        for questao in questoes_candidatas:
            # Verifica se já está na solução (hard constraint)
            if questao.id in [q.id for q in solucao]:
                continue  # Pula duplicatas
            
            # Calcula heurística
            estado_parcial = {
                'prova': solucao,
                'tempo_total': tempo_total,
                'dificuldades': dificuldades
            }
            eta = heuristica(posicao, questao, estado_parcial)
            
            if eta == 0.0:  # Inválida
                continue
            
            # Calcula numerador: τ^α × η^β
            tau = feromonio[posicao][questao.id]
            numerador = (tau ** alpha) * (eta ** beta)
            probabilidades.append((questao, numerador))
            denominador += numerador
        
        # 2. Normaliza probabilidades
        if denominador == 0:
            # Nenhuma escolha válida (não deveria acontecer se há questões suficientes)
            # Escolhe aleatoriamente entre não usadas
            disponiveis = [q for q in questoes_candidatas 
                          if q.id not in [q2.id for q2 in solucao]]
            if disponiveis:
                questao_escolhida = random.choice(disponiveis)
            else:
                break  # Não há mais questões
        else:
            # Escolhe probabilísticamente (roleta)
            probabilidades = [(q, p/denominador) for q, p in probabilidades]
            questao_escolhida = escolher_roleta(probabilidades)
        
        # 3. Adiciona à solução
        solucao.append(questao_escolhida)
        tempo_total += questao_escolhida.tempo
        dificuldades.append(questao_escolhida.dificuldade)
    
    return solucao
```

**Características:**
- Constrói solução passo a passo
- Usa probabilidade baseada em feromônio + heurística
- Garante restrições (sem duplicatas)
- Considera estado parcial em cada decisão

### 4.4 Atualização de Feromônio

**Após todas as formigas construírem soluções:**

```python
def atualizar_feromonio(feromonio, solucoes, fitness_solucoes, rho, Q):
    """
    Atualiza feromônio: evaporação + deposição
    """
    n_formigas = len(solucoes)
    
    # 1. Evaporação global
    for i in range(10):  # Para cada posição
        for q_id in range(n_questoes):
            feromonio[i][q_id] *= (1 - rho)
    
    # 2. Deposição (cada formiga deposita)
    for k in range(n_formigas):
        solucao = solucoes[k]
        fitness = fitness_solucoes[k]
        
        # Quantidade de feromônio a depositar
        # Quanto melhor o fitness, mais feromônio
        delta_tau = Q / (1000 - fitness)  # Ajustar conforme função fitness
        
        # Deposita em todas as arestas usadas
        for posicao, questao in enumerate(solucao):
            feromonio[posicao][questao.id] += delta_tau
    
    # 3. (Opcional) Deposição extra da melhor formiga
    melhor_idx = np.argmax(fitness_solucoes)
    melhor_solucao = solucoes[melhor_idx]
    melhor_fitness = fitness_solucoes[melhor_idx]
    
    delta_tau_elite = (e * Q) / (1000 - melhor_fitness)  # e = peso elite
    
    for posicao, questao in enumerate(melhor_solucao):
        feromonio[posicao][questao.id] += delta_tau_elite
```

**Características:**
- Evaporação remove feromônio antigo
- Deposição proporcional à qualidade
- Elite deposita extra (AS-Elite)

### 4.5 Função de Fitness

Pode reutilizar a mesma função do AG:

```python
def fitness(prova):
    # Hard constraint: duplicatas
    if len(set([q.id for q in prova])) < len(prova):
        return -1000.0
    
    # Soft constraints: tempo e dificuldade
    tempo_total = sum(q.tempo for q in prova)
    dificuldade_media = np.mean([q.dificuldade for q in prova])
    
    score = 1000.0
    
    # Penalidade de tempo
    if not (ALVO_TEMPO_MIN <= tempo_total <= ALVO_TEMPO_MAX):
        distancia = min(abs(tempo_total - ALVO_TEMPO_MIN), 
                       abs(tempo_total - ALVO_TEMPO_MAX))
        score -= distancia * 10
    
    # Penalidade de dificuldade
    erro_dif = abs(dificuldade_media - ALVO_DIFICULDADE)
    score -= erro_dif * 200
    
    return score
```

---

## 5. Fluxo Completo do Algoritmo ACO

```
1. INICIALIZAÇÃO
   ├─> Cria matriz de feromônio (10 × N_questoes)
   ├─> Inicializa feromônio com valor pequeno (τ₀)
   └─> Define parâmetros (α, β, ρ, Q, n_formigas)

2. LOOP (por N iterações):
   
   a) CONSTRUÇÃO DE SOLUÇÕES
      └─> Para cada formiga:
          └─> Constrói prova completa usando regra de transição
   
   b) AVALIAÇÃO
      └─> Calcula fitness de cada solução
      └─> Identifica melhor solução
   
   c) ATUALIZAÇÃO DE FEROMÔNIO
      ├─> Evaporação: τ = (1-ρ) × τ
      ├─> Deposição: τ = τ + Δτ (proporcional ao fitness)
      └─> Deposição Elite: τ = τ + e×Δτ (melhor formiga)
   
   d) LOGGING
      └─> Registra melhor solução da iteração

3. RETORNO
   └─> Melhor solução encontrada em todas as iterações
```

---

## 6. Parâmetros do ACO

### 6.1 Parâmetros Principais

- **n_formigas**: Número de formigas por iteração
  - Mais formigas: mais exploração, mais lento
  - Típico: 10-50 formigas
  
- **α (alpha)**: Peso do feromônio
  - Alto (ex: 2.0): Confia mais em conhecimento acumulado
  - Baixo (ex: 0.5): Mais exploração
  
- **β (beta)**: Peso da heurística
  - Alto (ex: 5.0): Confia mais em informação local
  - Baixo (ex: 1.0): Menos influência da heurística
  
- **ρ (rho)**: Taxa de evaporação
  - Alto (ex: 0.5): Evapora rápido, mais exploração
  - Baixo (ex: 0.1): Evapora devagar, mais exploração de conhecimento
  
- **Q**: Constante de deposição
  - Controla quantidade de feromônio depositado
  - Típico: 1.0 a 100.0
  
- **τ₀ (tau_zero)**: Feromônio inicial
  - Valor inicial em todas as arestas
  - Típico: 0.1 a 1.0
  
- **e (elite)**: Peso da formiga elite
  - Quanto extra a melhor formiga deposita
  - Típico: 1 a 10

### 6.2 Valores Sugeridos para o Problema

```python
n_formigas = 20
alpha = 1.0      # Peso do feromônio
beta = 2.0       # Peso da heurística (maior, pois heurística é informativa)
rho = 0.1        # Evaporação (baixa, para manter conhecimento)
Q = 10.0         # Constante de deposição
tau_zero = 1.0   # Feromônio inicial
e = 5            # Peso da elite
n_iteracoes = 50
```

---

## 7. Diferenças entre ACO e Algoritmo Genético

| Aspecto | Algoritmo Genético | Ant Colony Optimization |
|---------|-------------------|------------------------|
| **Representação** | População de soluções completas | Feromônio em arestas do grafo |
| **Construção** | Gera população inicial aleatória | Formigas constroem passo a passo |
| **Seleção** | Torneio, roleta, etc. | Probabilística baseada em feromônio+heurística |
| **Operadores** | Crossover + Mutação | Construção guiada + Atualização de feromônio |
| **Memória** | Melhor indivíduo (elitismo) | Feromônio em todas as arestas |
| **Exploração** | Mutação aleatória | Evaporação + construção probabilística |
| **Adequado para** | Problemas com representação direta | Problemas de caminho/sequência/grafo |

**Vantagens do ACO para este problema:**
- Considera estado parcial durante construção
- Heurística pode guiar melhor a busca
- Feromônio captura padrões de boas combinações

**Desvantagens:**
- Mais complexo de implementar
- Mais parâmetros para ajustar
- Pode ser mais lento (construção passo a passo)

---

## 8. Estrutura de Código Proposta

```
aco.py
├── class ACO
│   ├── __init__(n_formigas, alpha, beta, rho, Q, tau_zero, ...)
│   ├── inicializar_feromonio()
│   ├── construir_solucao(formiga) -> prova
│   ├── atualizar_feromonio(solucoes, fitnesses)
│   └── run(n_iteracoes) -> melhor_solucao
│
└── class ExamProblemACO
    ├── __init__(banco, materia, topico)
    ├── heuristica(posicao, questao, estado_parcial) -> float
    ├── fitness(prova) -> float  # Reutiliza do AG
    └── validar_solucao(prova) -> bool
```

---

## 9. Considerações de Implementação

### 9.1 Inicialização do Feromônio

```python
# Matriz 10 × N_questoes
feromonio = [[tau_zero] * n_questoes for _ in range(10)]
```

### 9.2 Escolha Probabilística (Roleta)

```python
def escolher_roleta(probabilidades):
    """
    probabilidades: [(questao, prob), ...]
    Retorna questão escolhida
    """
    r = random.random()
    acumulado = 0.0
    for questao, prob in probabilidades:
        acumulado += prob
        if r <= acumulado:
            return questao
    return probabilidades[-1][0]  # Fallback
```

### 9.3 Tratamento de Casos Especiais

- **Sem questões válidas**: Escolhe aleatoriamente entre não usadas
- **Feromônio zero**: Usa apenas heurística
- **Heurística zero**: Evita escolha (hard constraint violada)

### 9.4 Otimizações

- **Cache de heurísticas**: Reutilizar cálculos quando possível
- **Estruturas de dados eficientes**: Sets para verificar duplicatas
- **Normalização**: Evitar overflow em probabilidades

---

## 10. Resumo da Lógica de Aplicação

1. **Modelagem**: Problema como grafo de seleção sequencial
   - Posições (0-9) são nós
   - Escolher questão `q` na posição `i` é aresta
   - Feromônio `τ(i,q)` guia escolhas

2. **Construção**: Formigas constroem provas passo a passo
   - Cada passo: escolhe questão baseado em feromônio + heurística
   - Heurística considera estado parcial (tempo/dificuldade acumulados)
   - Garante restrições (sem duplicatas)

3. **Aprendizado**: Feromônio é atualizado após cada iteração
   - Evaporação remove conhecimento antigo
   - Deposição reforça boas escolhas
   - Elite deposita extra

4. **Convergência**: Com o tempo, formigas preferem questões que aparecem em boas soluções
   - Feromônio se concentra em arestas boas
   - Soluções melhoram iterativamente

---

Esta é a lógica completa para aplicar ACO ao problema de montagem de provas. O algoritmo será implementado seguindo esta estrutura e raciocínio.

