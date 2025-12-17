# Explicação: Clonal Selection Algorithm (CLONALG) e Aplicação ao Problema de Montagem de Provas

## 1. O que é Clonal Selection Algorithm (CLONALG)?

### 1.1 Inspiração Biológica

O CLONALG é inspirado no **sistema imunológico adaptativo** dos vertebrados, especificamente no processo de **seleção clonal**:

1. **Reconhecimento de Antígenos**: Quando o corpo detecta um patógeno (antígeno), células B específicas são ativadas
2. **Clonagem**: Células B ativadas se multiplicam (clonagem), gerando muitas cópias
3. **Hipermutação**: Durante a clonagem, ocorrem mutações (hipermutação somática) que geram variações
4. **Seleção**: Células com maior afinidade (que se ligam melhor ao antígeno) são selecionadas
5. **Memória**: Células de memória são criadas para resposta futura mais rápida
6. **Maturidade**: Células maduras produzem anticorpos que combatem o patígeno

### 1.2 Analogia Computacional

No CLONALG:
- **Antígeno**: Problema a ser resolvido (função objetivo)
- **Anticorpo**: Solução candidata
- **Afinidade**: Qualidade da solução (fitness)
- **Clonagem**: Duplicação das melhores soluções
- **Hipermutação**: Modificação das soluções clonadas
- **Seleção**: Manter apenas as melhores soluções após mutação
- **Memória**: Manter um conjunto de melhores soluções encontradas

### 1.3 Princípios Fundamentais

- **Seleção Clonal**: Melhores soluções são clonadas proporcionalmente à sua qualidade
- **Hipermutação Inversa**: Quanto melhor a solução, menos mutação (preserva boas características)
- **Diversidade**: Manter população diversa para explorar o espaço de busca
- **Memória**: Armazenar melhores soluções encontradas

---

## 2. Componentes do Algoritmo CLONALG

### 2.1 Estrutura Básica

```
População de Anticorpos (Ab)
├─> Cada anticorpo = uma solução candidata
├─> Afinidade = fitness da solução
└─> Clones = cópias modificadas dos melhores
```

### 2.2 Operadores Principais

#### **1. Seleção e Clonagem**
- Seleciona os N melhores anticorpos (baseado em afinidade)
- Clona cada um proporcionalmente à sua afinidade
- Número de clones: `N_clones = round(β × N × (afinidade_normalizada))`
  - `β`: Fator de clonagem (ex: 10)
  - `N`: Tamanho da população
  - Quanto melhor a afinidade, mais clones

#### **2. Hipermutação Inversa**
- Aplica mutação nos clones
- **Taxa de mutação inversa**: Quanto melhor a afinidade, MENOS mutação
- Fórmula: `taxa_mut = exp(-ρ × afinidade_normalizada)`
  - `ρ`: Taxa de decaimento (ex: 2.0)
  - Soluções boas: pouca mutação (exploração local)
  - Soluções ruins: muita mutação (exploração ampla)

#### **3. Seleção Clonal**
- Avalia clones mutados
- Para cada anticorpo original, mantém o melhor clone
- Substitui o original se o clone for melhor

#### **4. Substituição**
- Remove anticorpos de baixa afinidade
- Substitui por novos anticorpos aleatórios (diversidade)
- Mantém diversidade na população

#### **5. Memória**
- Mantém conjunto de melhores soluções encontradas
- Atualiza periodicamente
- Pode ser usado para reinicialização ou elitismo

---

## 3. Fluxo do Algoritmo CLONALG

```
1. INICIALIZAÇÃO
   ├─> Cria população inicial de anticorpos (soluções aleatórias)
   ├─> Avalia afinidade de cada anticorpo
   └─> Inicializa conjunto de memória (vazio ou com melhores)

2. LOOP (por N iterações):
   
   a) SELEÇÃO E CLONAGEM
      ├─> Seleciona N melhores anticorpos
      └─> Clona cada um proporcionalmente à afinidade
   
   b) HIPERMUTAÇÃO
      └─> Aplica mutação inversa em cada clone
          └─> Taxa de mutação: exp(-ρ × afinidade_normalizada)
   
   c) AVALIAÇÃO
      └─> Calcula afinidade de cada clone mutado
   
   d) SELEÇÃO CLONAL
      └─> Para cada anticorpo original:
          └─> Mantém melhor clone (se melhor que original)
   
   e) SUBSTITUIÇÃO
      ├─> Remove d% piores anticorpos
      └─> Substitui por novos aleatórios (diversidade)
   
   f) ATUALIZAÇÃO DE MEMÓRIA
      └─> Adiciona melhores soluções ao conjunto de memória

3. RETORNO
   └─> Melhor solução do conjunto de memória ou população
```

---

## 4. Adaptação do Problema de Montagem de Provas para CLONALG

### 4.1 Representação

**Anticorpo = Prova**
- Cada anticorpo é uma lista de 10 questões
- Representação idêntica ao Algoritmo Genético
- `Ab = [q1, q2, q3, ..., q10]`

**Afinidade = Fitness**
- Usa a mesma função `fitness()` do AG
- Quanto maior o fitness, maior a afinidade
- Fitness alto = boa solução = alta afinidade

### 4.2 Operadores Específicos

#### **1. Inicialização**
```python
def criar_anticorpo():
    """Cria um anticorpo aleatório (prova aleatória)."""
    return random.sample(questoes_candidatas, 10)
```

#### **2. Clonagem**
```python
def clonar(anticorpo, afinidade_normalizada, beta):
    """
    Clona um anticorpo proporcionalmente à sua afinidade.
    
    Args:
        anticorpo: Solução a ser clonada
        afinidade_normalizada: Afinidade normalizada [0, 1]
        beta: Fator de clonagem
    
    Returns:
        Lista de clones (cópias do anticorpo)
    """
    n_clones = round(beta * afinidade_normalizada)
    # Garante pelo menos 1 clone
    n_clones = max(1, n_clones)
    
    clones = []
    for _ in range(n_clones):
        clones.append(anticorpo.copy())  # Cópia profunda
    
    return clones
```

**Exemplo:**
- `beta = 10`
- Anticorpo com afinidade normalizada = 0.8
- `n_clones = round(10 × 0.8) = 8 clones`
- Anticorpo com afinidade normalizada = 0.3
- `n_clones = round(10 × 0.3) = 3 clones`

#### **3. Hipermutação Inversa**
```python
def hipermutacao_inversa(clone, afinidade_normalizada, rho):
    """
    Aplica mutação inversa: quanto melhor a afinidade, menos mutação.
    
    Args:
        clone: Clone a ser mutado
        afinidade_normalizada: Afinidade normalizada [0, 1]
        rho: Taxa de decaimento
    
    Returns:
        Clone mutado
    """
    # Taxa de mutação inversa
    taxa_mut = np.exp(-rho * afinidade_normalizada)
    
    # Número de mutações (trocar questões)
    n_mutacoes = max(1, int(taxa_mut * len(clone)))
    
    clone_mutado = clone.copy()
    
    for _ in range(n_mutacoes):
        # Escolhe posição aleatória
        idx = random.randint(0, len(clone_mutado) - 1)
        
        # Encontra questões válidas (não usadas)
        ids_usados = {q.id for q in clone_mutado}
        candidatas = [q for q in questoes_candidatas 
                     if q.id not in ids_usados]
        
        if candidatas:
            # Substitui por questão aleatória
            clone_mutado[idx] = random.choice(candidatas)
    
    return clone_mutado
```

**Exemplo:**
- `rho = 2.0`
- Afinidade normalizada = 0.9 (muito boa)
- `taxa_mut = exp(-2.0 × 0.9) = exp(-1.8) ≈ 0.17`
- `n_mutacoes = max(1, int(0.17 × 10)) = 2 mutações`
- Afinidade normalizada = 0.2 (ruim)
- `taxa_mut = exp(-2.0 × 0.2) = exp(-0.4) ≈ 0.67`
- `n_mutacoes = max(1, int(0.67 × 10)) = 7 mutações`

**Interpretação:**
- Soluções boas: poucas mutações (refinamento local)
- Soluções ruins: muitas mutações (exploração ampla)

#### **4. Seleção Clonal**
```python
def selecao_clonal(anticorpo_original, clones_mutados, fitness_fn):
    """
    Seleciona o melhor clone para substituir o original.
    
    Args:
        anticorpo_original: Anticorpo original
        clones_mutados: Lista de clones após mutação
        fitness_fn: Função de avaliação
    
    Returns:
        Melhor anticorpo (original ou melhor clone)
    """
    fitness_original = fitness_fn(anticorpo_original)
    
    melhor_clone = anticorpo_original
    melhor_fitness = fitness_original
    
    for clone in clones_mutados:
        fitness_clone = fitness_fn(clone)
        if fitness_clone > melhor_fitness:
            melhor_fitness = fitness_clone
            melhor_clone = clone
    
    return melhor_clone
```

#### **5. Substituição (Diversidade)**
```python
def substituir_piores(populacao, fitnesses, d=0.1):
    """
    Remove d% piores e substitui por novos aleatórios.
    
    Args:
        populacao: Lista de anticorpos
        fitnesses: Lista de fitnesses correspondentes
        d: Fração a substituir (ex: 0.1 = 10%)
    
    Returns:
        População atualizada
    """
    n_substituir = max(1, int(len(populacao) * d))
    
    # Encontra índices dos piores
    indices_ordenados = np.argsort(fitnesses)
    indices_piores = indices_ordenados[:n_substituir]
    
    # Substitui por novos aleatórios
    for idx in indices_piores:
        populacao[idx] = criar_anticorpo()
    
    return populacao
```

---

## 5. Detalhamento da Aplicação

### 5.1 Estrutura de Dados

**População:**
```python
populacao = [Ab1, Ab2, ..., AbN]  # N anticorpos (provas)
afinidades = [f1, f2, ..., fN]    # Fitness de cada anticorpo
```

**Memória:**
```python
memoria = [Ab_best1, Ab_best2, ..., Ab_bestM]  # M melhores soluções
```

### 5.2 Normalização de Afinidade

Para calcular número de clones e taxa de mutação, precisamos normalizar afinidades:

```python
def normalizar_afinidades(afinidades):
    """
    Normaliza afinidades para [0, 1].
    """
    min_af = min(afinidades)
    max_af = max(afinidades)
    range_af = max_af - min_af
    
    if range_af == 0:
        # Todas iguais
        return [1.0] * len(afinidades)
    
    return [(af - min_af) / range_af for af in afinidades]
```

### 5.3 Função de Fitness

Reutiliza a mesma função do AG:
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

## 6. Fluxo Completo do Algoritmo CLONALG

```
1. INICIALIZAÇÃO
   ├─> Cria população de N anticorpos aleatórios
   ├─> Avalia afinidade de cada um
   └─> Inicializa conjunto de memória

2. LOOP (por N iterações):
   
   a) NORMALIZAÇÃO
      └─> Normaliza afinidades para [0, 1]
   
   b) SELEÇÃO E CLONAGEM
      ├─> Seleciona N melhores anticorpos
      └─> Para cada um:
          └─> Clona proporcionalmente à afinidade normalizada
   
   c) HIPERMUTAÇÃO
      └─> Para cada clone:
          ├─> Calcula taxa de mutação: exp(-ρ × afinidade)
          └─> Aplica mutação (troca questões)
   
   d) AVALIAÇÃO
      └─> Calcula afinidade de cada clone mutado
   
   e) SELEÇÃO CLONAL
      └─> Para cada anticorpo original:
          └─> Substitui pelo melhor clone (se melhor)
   
   f) SUBSTITUIÇÃO
      ├─> Remove d% piores anticorpos
      └─> Substitui por novos aleatórios
   
   g) ATUALIZAÇÃO DE MEMÓRIA
      └─> Adiciona melhores soluções à memória
   
   h) LOGGING
      └─> Registra melhor solução da iteração

3. RETORNO
   └─> Melhor solução do conjunto de memória
```

---

## 7. Parâmetros do CLONALG

### 7.1 Parâmetros Principais

- **N (pop_size)**: Tamanho da população
  - Mais anticorpos: mais diversidade, mais lento
  - Típico: 20-100
  
- **β (beta)**: Fator de clonagem
  - Controla quantos clones são gerados
  - Alto (ex: 10): mais clones, mais exploração
  - Baixo (ex: 5): menos clones, mais rápido
  - Típico: 5-20
  
- **ρ (rho)**: Taxa de decaimento da mutação
  - Controla quão rápido a taxa de mutação decai com afinidade
  - Alto (ex: 3.0): mutação decai rápido (soluções boas quase não mutam)
  - Baixo (ex: 1.0): mutação decai devagar (mais mutação mesmo em boas soluções)
  - Típico: 1.0-3.0
  
- **d (diversity_rate)**: Taxa de substituição
  - Fração da população substituída por novos aleatórios
  - Alto (ex: 0.2): muita diversidade, menos convergência
  - Baixo (ex: 0.05): pouca diversidade, pode convergir prematuramente
  - Típico: 0.05-0.2
  
- **M (memory_size)**: Tamanho do conjunto de memória
  - Quantas melhores soluções manter
  - Típico: 5-20

### 7.2 Valores Sugeridos para o Problema

```python
pop_size = 50
beta = 10          # Fator de clonagem
rho = 2.0          # Taxa de decaimento
diversity_rate = 0.1  # 10% substituição
memory_size = 10   # Tamanho da memória
n_iterations = 50
```

---

## 8. Diferenças entre CLONALG, AG e ACO

| Aspecto | Algoritmo Genético | ACO | CLONALG |
|---------|-------------------|-----|---------|
| **Inspiração** | Evolução biológica | Comportamento de formigas | Sistema imunológico |
| **Representação** | População de soluções | Feromônio em grafo | População de anticorpos |
| **Seleção** | Torneio, roleta | Probabilística (feromônio+heurística) | Baseada em afinidade |
| **Operadores** | Crossover + Mutação | Construção guiada | Clonagem + Hipermutação |
| **Mutação** | Taxa fixa | Não aplica mutação direta | Taxa inversa (melhor = menos mutação) |
| **Memória** | Elitismo (1 melhor) | Feromônio (todas as arestas) | Conjunto de melhores |
| **Exploração** | Mutação aleatória | Evaporação + construção | Substituição de piores |
| **Adequado para** | Problemas gerais | Problemas de caminho/grafo | Problemas de otimização contínua/discreta |

**Vantagens do CLONALG para este problema:**
- Mutação adaptativa (refina boas soluções, explora ruins)
- Clonagem proporcional (foca em boas soluções)
- Memória mantém histórico de melhores
- Simples de implementar (similar ao AG)

**Desvantagens:**
- Não tem crossover (menos combinação de soluções)
- Pode convergir localmente se diversidade não for mantida
- Parâmetros precisam ser ajustados

---

## 9. Estrutura de Código Proposta

```
clonalg.py
├── class CLONALG
│   ├── __init__(pop_size, beta, rho, diversity_rate, memory_size, ...)
│   ├── inicializar_populacao()
│   ├── normalizar_afinidades()
│   ├── clonar(anticorpo, afinidade_norm) -> clones
│   ├── hipermutacao_inversa(clone, afinidade_norm) -> clone_mutado
│   ├── selecao_clonal(original, clones) -> melhor
│   ├── substituir_piores()
│   ├── atualizar_memoria()
│   └── run(n_iterations) -> melhor_solucao
│
└── class ExamProblemCLONALG
    ├── __init__(banco, materia, topico)
    ├── criar_anticorpo() -> prova
    ├── fitness(prova) -> float  # Reutiliza do AG
    ├── mutar(prova) -> prova_mutada
    └── validar_solucao(prova) -> bool
```

---

## 10. Considerações de Implementação

### 10.1 Clonagem Eficiente

```python
# Cópia profunda para evitar referências compartilhadas
import copy

clones = [copy.deepcopy(anticorpo) for _ in range(n_clones)]
```

### 10.2 Mutação Adaptativa

A mutação inversa é a característica distintiva do CLONALG:
- Soluções boas: poucas mutações (refinamento)
- Soluções ruins: muitas mutações (exploração)

Isso permite:
- **Exploração local** em torno de boas soluções
- **Exploração ampla** de soluções ruins
- **Balanceamento** automático entre exploração e exploração

### 10.3 Manutenção de Diversidade

A substituição de piores é crucial:
- Sem ela, população pode convergir prematuramente
- Com muita substituição, algoritmo vira busca aleatória
- Taxa de 10% é um bom equilíbrio

### 10.4 Conjunto de Memória

O conjunto de memória:
- Mantém histórico de melhores soluções
- Pode ser usado para reinicialização
- Pode ser retornado como resultado final
- Evita perder boas soluções encontradas

---

## 11. Resumo da Lógica de Aplicação

1. **Representação**: Anticorpo = Prova (lista de 10 questões)
   - Idêntica ao Algoritmo Genético
   - Cada anticorpo é uma solução completa

2. **Avaliação**: Afinidade = Fitness
   - Reutiliza função do AG
   - Quanto maior, melhor

3. **Clonagem**: Proporcional à afinidade
   - Melhores soluções geram mais clones
   - Foco em explorar áreas promissoras

4. **Hipermutação Inversa**: Taxa adaptativa
   - Boas soluções: pouca mutação (refinamento)
   - Ruins soluções: muita mutação (exploração)
   - Balanceamento automático

5. **Seleção Clonal**: Melhor clone substitui original
   - Garante que população sempre melhora
   - Similar ao elitismo, mas por anticorpo

6. **Diversidade**: Substituição de piores
   - Mantém população diversa
   - Previne convergência prematura

7. **Memória**: Histórico de melhores
   - Preserva soluções encontradas
   - Pode ser usado para resultado final

---

## 12. Comparação com Outros Algoritmos

### CLONALG vs Algoritmo Genético

**Semelhanças:**
- População de soluções
- Operadores de mutação
- Seleção baseada em fitness

**Diferenças:**
- CLONALG: Clonagem proporcional (AG: seleção uniforme)
- CLONALG: Mutação inversa (AG: mutação fixa)
- CLONALG: Sem crossover (AG: tem crossover)
- CLONALG: Memória explícita (AG: apenas elitismo)

### CLONALG vs ACO

**Semelhanças:**
- Ambos são meta-heurísticas
- Ambos mantêm informação sobre boas soluções

**Diferenças:**
- CLONALG: População de soluções completas (ACO: constrói passo a passo)
- CLONALG: Mutação adaptativa (ACO: construção probabilística)
- CLONALG: Clonagem (ACO: feromônio)

---

## 13. Vantagens do CLONALG para Este Problema

1. **Mutação Adaptativa**: Refina boas provas, explora ruins
2. **Foco em Boas Soluções**: Clonagem proporcional concentra esforço
3. **Simplicidade**: Mais simples que ACO, similar ao AG
4. **Memória**: Mantém histórico de melhores provas
5. **Diversidade Controlada**: Substituição mantém exploração

---

## 14. Desafios e Soluções

### Desafio 1: Taxa de Mutação Muito Baixa
**Problema**: Soluções muito boas podem não mutar o suficiente
**Solução**: Garantir mínimo de 1 mutação: `max(1, int(taxa_mut * n))`

### Desafio 2: Convergência Prematura
**Problema**: População pode convergir para solução subótima
**Solução**: Substituição de piores mantém diversidade

### Desafio 3: Clonagem Excessiva
**Problema**: Muitos clones podem tornar algoritmo lento
**Solução**: Limitar número máximo de clones por anticorpo

### Desafio 4: Normalização de Afinidades
**Problema**: Afinidades negativas ou muito diferentes
**Solução**: Normalizar para [0, 1] antes de usar em fórmulas

---

Esta é a lógica completa para aplicar CLONALG ao problema de montagem de provas. O algoritmo será implementado seguindo esta estrutura e raciocínio, com foco na mutação adaptativa e clonagem proporcional como características distintivas.

