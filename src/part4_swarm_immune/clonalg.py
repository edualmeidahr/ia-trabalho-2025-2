"""
Clonal Selection Algorithm (CLONALG)
Implementação genérica baseada no sistema imunológico adaptativo.
"""

import random
import numpy as np
import copy
from typing import List, Callable, Any, Dict


class CLONALG:
    """
    Classe genérica para Clonal Selection Algorithm (CLONALG).
    """
    
    def __init__(
        self,
        pop_size: int,
        fitness_fn: Callable[[List[Any]], float],
        create_antibody: Callable[[], Any],
        mutate_fn: Callable[[Any], Any],
        beta: float = 10.0,          # Fator de clonagem
        rho: float = 2.0,             # Taxa de decaimento da mutação
        diversity_rate: float = 0.1,   # Taxa de substituição (d%)
        memory_size: int = 10,        # Tamanho do conjunto de memória
        seed: int = 42
    ):
        """
        Args:
            pop_size: Tamanho da população de anticorpos
            fitness_fn: Função que avalia qualidade de uma solução
            create_antibody: Função que cria um anticorpo aleatório
            mutate_fn: Função que aplica mutação em um anticorpo
            beta: Fator de clonagem (quantos clones por anticorpo)
            rho: Taxa de decaimento da mutação (quanto maior, mais rápido decai)
            diversity_rate: Fração da população a substituir (0 < d < 1)
            memory_size: Tamanho do conjunto de memória
            seed: Semente para reprodutibilidade
        """
        random.seed(seed)
        np.random.seed(seed)
        
        self.pop_size = pop_size
        self.fitness_fn = fitness_fn
        self.create_antibody = create_antibody
        self.mutate_fn = mutate_fn
        
        self.beta = beta
        self.rho = rho
        self.diversity_rate = diversity_rate
        self.memory_size = memory_size
        
        # Inicializa população
        self.population = [self.create_antibody() for _ in range(pop_size)]
        
        # Conjunto de memória (melhores soluções encontradas)
        self.memory = []
        
        # Histórico para gráficos
        self.history = []
        self.best_solution = None
        self.best_fitness = float('-inf')
    
    def normalizar_afinidades(self, afinidades: List[float]) -> List[float]:
        """
        Normaliza afinidades para o intervalo [0, 1].
        
        Args:
            afinidades: Lista de valores de fitness
        
        Returns:
            Lista de afinidades normalizadas
        """
        if not afinidades:
            return []
        
        min_af = min(afinidades)
        max_af = max(afinidades)
        range_af = max_af - min_af
        
        if range_af == 0:
            # Todas iguais, retorna 1.0 para todas
            return [1.0] * len(afinidades)
        
        return [(af - min_af) / range_af for af in afinidades]
    
    def clonar(self, antibody: Any, afinidade_norm: float) -> List[Any]:
        """
        Clona um anticorpo proporcionalmente à sua afinidade normalizada.
        
        Args:
            antibody: Anticorpo a ser clonado
            afinidade_norm: Afinidade normalizada [0, 1]
        
        Returns:
            Lista de clones (cópias profundas)
        """
        n_clones = round(self.beta * afinidade_norm)
        # Garante pelo menos 1 clone
        n_clones = max(1, n_clones)
        
        clones = []
        for _ in range(n_clones):
            clones.append(copy.deepcopy(antibody))
        
        return clones
    
    def hipermutacao_inversa(self, clone: Any, afinidade_norm: float) -> Any:
        """
        Aplica hipermutação inversa: quanto melhor a afinidade, menos mutação.
        
        Args:
            clone: Clone a ser mutado
            afinidade_norm: Afinidade normalizada [0, 1]
        
        Returns:
            Clone mutado
        """
        # Taxa de mutação inversa: exp(-ρ × afinidade)
        taxa_mut = np.exp(-self.rho * afinidade_norm)
        
        # Aplica mutação usando função fornecida
        # A função mutate_fn deve aplicar mutação proporcional à taxa
        clone_mutado = self.mutate_fn(clone, taxa_mut)
        
        return clone_mutado
    
    def selecao_clonal(self, antibody_original: Any, clones_mutados: List[Any]) -> Any:
        """
        Seleciona o melhor clone para substituir o original.
        
        Args:
            antibody_original: Anticorpo original
            clones_mutados: Lista de clones após mutação
        
        Returns:
            Melhor anticorpo (original ou melhor clone)
        """
        fitness_original = self.fitness_fn(antibody_original)
        
        melhor_anticorpo = antibody_original
        melhor_fitness = fitness_original
        
        for clone in clones_mutados:
            fitness_clone = self.fitness_fn(clone)
            if fitness_clone > melhor_fitness:
                melhor_fitness = fitness_clone
                melhor_anticorpo = clone
        
        return melhor_anticorpo
    
    def substituir_piores(self, populacao: List[Any], fitnesses: List[float]):
        """
        Remove d% piores e substitui por novos aleatórios.
        
        Args:
            populacao: Lista de anticorpos
            fitnesses: Lista de fitnesses correspondentes
        
        Returns:
            População atualizada
        """
        n_substituir = max(1, int(len(populacao) * self.diversity_rate))
        
        # Encontra índices dos piores
        indices_ordenados = np.argsort(fitnesses)
        indices_piores = indices_ordenados[:n_substituir]
        
        # Substitui por novos aleatórios
        for idx in indices_piores:
            populacao[idx] = self.create_antibody()
        
        return populacao
    
    def atualizar_memoria(self, populacao: List[Any], fitnesses: List[float]):
        """
        Atualiza conjunto de memória com melhores soluções.
        
        Args:
            populacao: Lista de anticorpos
            fitnesses: Lista de fitnesses correspondentes
        """
        # Combina memória atual com população
        todas_solucoes = self.memory + populacao
        todas_fitnesses = [self.fitness_fn(sol) for sol in self.memory] + fitnesses
        
        # Ordena por fitness (decrescente)
        indices_ordenados = np.argsort(todas_fitnesses)[::-1]
        
        # Mantém apenas os melhores (sem duplicatas)
        nova_memoria = []
        solucoes_vistas = set()
        
        for idx in indices_ordenados:
            if len(nova_memoria) >= self.memory_size:
                break
            
            solucao = todas_solucoes[idx]
            # Cria identificador único baseado no conteúdo da solução
            # Assumindo que solução é uma lista com objetos que têm atributo 'id'
            if hasattr(solucao, '__iter__') and len(solucao) > 0:
                # Para listas de questões, usa tupla de IDs ordenados
                try:
                    ids = tuple(sorted([getattr(item, 'id', hash(item)) for item in solucao]))
                    if ids not in solucoes_vistas:
                        nova_memoria.append(copy.deepcopy(solucao))
                        solucoes_vistas.add(ids)
                except:
                    # Fallback: usa hash da solução
                    sol_hash = hash(str(solucao))
                    if sol_hash not in solucoes_vistas:
                        nova_memoria.append(copy.deepcopy(solucao))
                        solucoes_vistas.add(sol_hash)
            else:
                # Fallback para outros tipos
                sol_hash = hash(str(solucao))
                if sol_hash not in solucoes_vistas:
                    nova_memoria.append(copy.deepcopy(solucao))
                    solucoes_vistas.add(sol_hash)
        
        self.memory = nova_memoria
    
    def run(self, n_iterations: int, verbose: bool = True) -> Any:
        """
        Loop principal de execução do CLONALG.
        
        Args:
            n_iterations: Número de iterações
            verbose: Se True, imprime progresso
        
        Returns:
            Melhor solução encontrada
        """
        for iteration in range(n_iterations):
            # 1. Avaliação da população atual
            fitnesses = [self.fitness_fn(ab) for ab in self.population]
            
            # 2. Normalização de afinidades
            afinidades_norm = self.normalizar_afinidades(fitnesses)
            
            # 3. Seleção e Clonagem
            # Seleciona todos os anticorpos (ou pode selecionar apenas os melhores)
            novos_anticorpos = []
            
            for i, antibody in enumerate(self.population):
                afinidade_norm = afinidades_norm[i]
                
                # Clona proporcionalmente à afinidade
                clones = self.clonar(antibody, afinidade_norm)
                
                # 4. Hipermutação Inversa
                clones_mutados = []
                for clone in clones:
                    clone_mutado = self.hipermutacao_inversa(clone, afinidade_norm)
                    clones_mutados.append(clone_mutado)
                
                # 5. Seleção Clonal
                melhor_anticorpo = self.selecao_clonal(antibody, clones_mutados)
                novos_anticorpos.append(melhor_anticorpo)
            
            # 6. Substituição (diversidade)
            novos_fitnesses = [self.fitness_fn(ab) for ab in novos_anticorpos]
            self.population = self.substituir_piores(novos_anticorpos, novos_fitnesses)
            
            # 7. Atualização de Memória
            fitnesses_finais = [self.fitness_fn(ab) for ab in self.population]
            self.atualizar_memoria(self.population, fitnesses_finais)
            
            # 8. Atualiza melhor solução global
            melhor_idx = np.argmax(fitnesses_finais)
            melhor_fitness_iter = fitnesses_finais[melhor_idx]
            
            if melhor_fitness_iter > self.best_fitness:
                self.best_fitness = melhor_fitness_iter
                self.best_solution = copy.deepcopy(self.population[melhor_idx])
            
            # Também verifica memória
            if self.memory:
                memoria_fitnesses = [self.fitness_fn(sol) for sol in self.memory]
                melhor_memoria_idx = np.argmax(memoria_fitnesses)
                melhor_memoria_fitness = memoria_fitnesses[melhor_memoria_idx]
                
                if melhor_memoria_fitness > self.best_fitness:
                    self.best_fitness = melhor_memoria_fitness
                    self.best_solution = copy.deepcopy(self.memory[melhor_memoria_idx])
            
            self.history.append(self.best_fitness)
            
            # 9. Logging
            if verbose and iteration % 10 == 0:
                print(f"Iter {iteration}: Melhor Fitness = {self.best_fitness:.4f} "
                      f"(Iter atual: {melhor_fitness_iter:.4f}, Memória: {len(self.memory)})")
        
        # Retorna melhor da memória ou população
        if self.memory:
            memoria_fitnesses = [self.fitness_fn(sol) for sol in self.memory]
            melhor_memoria_idx = np.argmax(memoria_fitnesses)
            return self.memory[melhor_memoria_idx]
        
        return self.best_solution

