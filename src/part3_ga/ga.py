import random
from typing import List, Callable, Any, Tuple

class GA:
    """
    Classe genérica para Algoritmo Genético.
    """
    def __init__(
        self,
        pop_size: int,
        fitness_fn: Callable[[Any], float],  # Função que dá nota ao indivíduo
        create_ind: Callable[[], Any],       # Função que cria um indivíduo aleatório
        mutate_fn: Callable[[Any], Any],     # Função que altera um indivíduo
        crossover_fn: Callable[[Any, Any], Tuple[Any, Any]], # Função que cruza dois pais
        cx_rate: float = 0.7,    # Chance de Cruzamento
        mut_rate: float = 0.01,   # Chance de Mutação
        elitism: bool = True,    # Se mantém o melhor de todos sempre
        seed: int = 42
    ):
        random.seed(seed)
        self.pop_size = pop_size
        self.fitness_fn = fitness_fn
        self.create_ind = create_ind
        self.mutate_fn = mutate_fn
        self.crossover_fn = crossover_fn
        self.cx_rate = cx_rate
        self.mut_rate = mut_rate
        self.elitism = elitism
        
        # Inicializa a população
        self.population = [self.create_ind() for _ in range(pop_size)]
        
        # Histórico para gráficos
        self.history = []

    def select_tournament(self, k: int = 3) -> Any:
        """
        Seleção por Torneio: Pega K indivíduos aleatórios e retorna o melhor.
        """
        competitors = random.sample(self.population, k)
        # Retorna o que tiver maior fitness
        return max(competitors, key=self.fitness_fn)

    def step(self):
        """
        Executa UMA geração (evolução).
        """
        new_pop = []
        
        # 1. Elitismo: Mantém o melhor da geração anterior intacto?
        if self.elitism:
            best_ind = max(self.population, key=self.fitness_fn)
            new_pop.append(best_ind)
            
        # 2. Gera novos indivíduos até encher a população
        while len(new_pop) < self.pop_size:
            # Seleção dos Pais
            p1 = self.select_tournament()
            p2 = self.select_tournament()
            
            # Cruzamento (Crossover)
            offspring1, offspring2 = p1, p2 # Padrão: cópia
            if random.random() < self.cx_rate:
                # Se não for uma lista (ex: objeto customizado), o crossover deve lidar com a cópia
                offspring1, offspring2 = self.crossover_fn(p1, p2)
            
            # Mutação
            if random.random() < self.mut_rate:
                offspring1 = self.mutate_fn(offspring1)
            if random.random() < self.mut_rate:
                offspring2 = self.mutate_fn(offspring2)
                
            # Adiciona na nova população
            new_pop.append(offspring1)
            if len(new_pop) < self.pop_size:
                new_pop.append(offspring2)
        
        self.population = new_pop

    def run(self, n_generations: int, verbose: bool = True) -> Any:
        """
        Loop principal de execução.
        """
        for gen in range(n_generations):
            self.step()
            
            # Coleta estatísticas
            best_ind = max(self.population, key=self.fitness_fn)
            best_score = self.fitness_fn(best_ind)
            self.history.append(best_score)
            
            if verbose and gen % 10 == 0:
                print(f"Gen {gen}: Melho Fitness = {best_score:.4f}")
                
        return max(self.population, key=self.fitness_fn)