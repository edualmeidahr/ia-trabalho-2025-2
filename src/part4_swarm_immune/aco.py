"""
Algoritmo de Otimização Baseado em Colônia de Formigas (ACO)
Implementação genérica que pode ser aplicada a diferentes problemas.
"""

import random
import numpy as np
from typing import List, Callable, Any, Dict, Tuple


class ACO:
    """
    Classe genérica para Algoritmo de Colônia de Formigas (ACO).
    """
    
    def __init__(
        self,
        n_ants: int,
        n_positions: int,
        n_options: int,
        fitness_fn: Callable[[List[Any]], float],
        heuristica_fn: Callable[[int, Any, Dict], float],
        get_valid_options: Callable[[int, Dict], List[Any]],
        update_state: Callable[[Dict, Any], Dict],
        get_option_id: Callable[[Any], int] = None,  # Função para obter ID da opção
        alpha: float = 1.0,      # Peso do feromônio
        beta: float = 2.0,       # Peso da heurística
        rho: float = 0.1,        # Taxa de evaporação
        Q: float = 10.0,         # Constante de deposição
        tau_zero: float = 1.0,   # Feromônio inicial
        e: float = 5.0,          # Peso da elite
        seed: int = 42
    ):
        """
        Args:
            n_ants: Número de formigas
            n_positions: Número de posições na solução (ex: 10 questões)
            n_options: Número de opções disponíveis (ex: N questões no banco)
            fitness_fn: Função que avalia uma solução completa
            heuristica_fn: Função que calcula heurística para escolha (pos, opção, estado)
            get_valid_options: Função que retorna opções válidas para uma posição
            update_state: Função que atualiza estado parcial ao adicionar opção
            alpha: Peso do feromônio na probabilidade
            beta: Peso da heurística na probabilidade
            rho: Taxa de evaporação (0 < rho < 1)
            Q: Constante de deposição de feromônio
            tau_zero: Valor inicial do feromônio
            e: Peso da formiga elite
            seed: Semente para reprodutibilidade
        """
        random.seed(seed)
        np.random.seed(seed)
        
        self.n_ants = n_ants
        self.n_positions = n_positions
        self.n_options = n_options
        self.fitness_fn = fitness_fn
        self.heuristica_fn = heuristica_fn
        self.get_valid_options = get_valid_options
        self.update_state = update_state
        self.get_option_id = get_option_id or (lambda op: getattr(op, 'id', hash(op) % n_options))
        
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.Q = Q
        self.tau_zero = tau_zero
        self.e = e
        
        # Inicializa matriz de feromônio: pheromone[posição][opção_id]
        # Para cada posição, temos feromônio para cada opção possível
        self.pheromone = [[tau_zero] * n_options for _ in range(n_positions)]
        
        # Histórico para gráficos
        self.history = []
        self.best_solution = None
        self.best_fitness = float('-inf')
    
    def construir_solucao(self, ant_id: int) -> Tuple[List[Any], Dict]:
        """
        Uma formiga constrói uma solução completa passo a passo.
        
        Returns:
            (solucao, estado_final): Solução construída e estado final
        """
        solucao = []
        estado = {}  # Estado parcial (pode conter tempo_total, dificuldades, etc.)
        
        # Para cada posição na solução
        for posicao in range(self.n_positions):
            # 1. Obtém opções válidas para esta posição
            opcoes_validas = self.get_valid_options(posicao, estado)
            
            if not opcoes_validas:
                # Não há mais opções válidas (não deveria acontecer)
                break
            
            # 2. Calcula probabilidades para cada opção válida
            probabilidades = []
            denominador = 0.0
            
            for opcao in opcoes_validas:
                # Calcula heurística
                eta = self.heuristica_fn(posicao, opcao, estado)
                
                if eta <= 0.0:  # Opção inválida (heurística zero ou negativa)
                    continue
                
                # Obtém ID da opção usando função fornecida ou padrão
                opcao_id = self.get_option_id(opcao) % self.n_options
                
                # Obtém feromônio
                tau = self.pheromone[posicao][opcao_id]
                
                # Calcula numerador: τ^α × η^β
                numerador = (tau ** self.alpha) * (eta ** self.beta)
                probabilidades.append((opcao, numerador))
                denominador += numerador
            
            # 3. Escolhe opção probabilísticamente
            if not probabilidades:
                # Nenhuma opção válida, escolhe aleatoriamente
                opcao_escolhida = random.choice(opcoes_validas)
            elif denominador == 0:
                # Todas as probabilidades são zero, escolhe aleatoriamente
                opcao_escolhida = random.choice([p[0] for p in probabilidades])
            else:
                # Normaliza e escolhe por roleta
                probabilidades = [(op, prob/denominador) for op, prob in probabilidades]
                opcao_escolhida = self._escolher_roleta(probabilidades)
            
            # 4. Adiciona à solução e atualiza estado
            solucao.append(opcao_escolhida)
            estado = self.update_state(estado, opcao_escolhida)
        
        return solucao, estado
    
    def _escolher_roleta(self, probabilidades: List[Tuple[Any, float]]) -> Any:
        """
        Escolhe uma opção usando roleta probabilística.
        
        Args:
            probabilidades: Lista de (opcao, probabilidade)
        
        Returns:
            Opção escolhida
        """
        r = random.random()
        acumulado = 0.0
        
        for opcao, prob in probabilidades:
            acumulado += prob
            if r <= acumulado:
                return opcao
        
        # Fallback: retorna última opção
        return probabilidades[-1][0]
    
    def atualizar_feromonio(self, solucoes: List[List[Any]], fitnesses: List[float]):
        """
        Atualiza feromônio: evaporação + deposição.
        
        Args:
            solucoes: Lista de soluções construídas pelas formigas
            fitnesses: Lista de fitness de cada solução
        """
        # 1. Evaporação global
        for posicao in range(self.n_positions):
            for opcao_id in range(self.n_options):
                self.pheromone[posicao][opcao_id] *= (1 - self.rho)
        
        # 2. Deposição de todas as formigas
        # Normaliza fitnesses para garantir valores positivos para deposição
        if fitnesses:
            min_fitness = min(fitnesses)
            max_fitness = max(fitnesses)
            range_fitness = max_fitness - min_fitness
            
            for solucao, fitness in zip(solucoes, fitnesses):
                if range_fitness > 0:
                    # Normaliza fitness para [0, 1] e depois escala
                    fitness_normalizado = (fitness - min_fitness) / range_fitness
                    delta_tau = self.Q * fitness_normalizado
                else:
                    # Todas as soluções têm mesmo fitness
                    delta_tau = self.Q * 0.5
                
                # Deposita em todas as posições usadas
                for posicao, opcao in enumerate(solucao):
                    opcao_id = self.get_option_id(opcao) % self.n_options
                    self.pheromone[posicao][opcao_id] += delta_tau
        
        # 3. Deposição extra da melhor formiga (elite)
        if fitnesses:
            melhor_idx = np.argmax(fitnesses)
            melhor_solucao = solucoes[melhor_idx]
            melhor_fitness = fitnesses[melhor_idx]
            
            if len(fitnesses) > 1:
                min_fitness = min(fitnesses)
                max_fitness = max(fitnesses)
                range_fitness = max_fitness - min_fitness
                
                if range_fitness > 0:
                    fitness_normalizado = (melhor_fitness - min_fitness) / range_fitness
                    delta_tau_elite = self.e * self.Q * fitness_normalizado
                else:
                    delta_tau_elite = self.e * self.Q * 0.5
            else:
                delta_tau_elite = self.e * self.Q
            
            for posicao, opcao in enumerate(melhor_solucao):
                opcao_id = self.get_option_id(opcao) % self.n_options
                self.pheromone[posicao][opcao_id] += delta_tau_elite
    
    def run(self, n_iterations: int, verbose: bool = True) -> List[Any]:
        """
        Loop principal de execução do ACO.
        
        Args:
            n_iterations: Número de iterações
            verbose: Se True, imprime progresso
        
        Returns:
            Melhor solução encontrada
        """
        for iteration in range(n_iterations):
            # 1. Construção de soluções
            solucoes = []
            estados = []
            
            for ant_id in range(self.n_ants):
                solucao, estado = self.construir_solucao(ant_id)
                solucoes.append(solucao)
                estados.append(estado)
            
            # 2. Avaliação
            fitnesses = [self.fitness_fn(sol) for sol in solucoes]
            
            # 3. Atualização de feromônio
            self.atualizar_feromonio(solucoes, fitnesses)
            
            # 4. Atualiza melhor solução global
            melhor_idx = np.argmax(fitnesses)
            melhor_fitness_iter = fitnesses[melhor_idx]
            
            if melhor_fitness_iter > self.best_fitness:
                self.best_fitness = melhor_fitness_iter
                self.best_solution = solucoes[melhor_idx].copy()
            
            self.history.append(self.best_fitness)
            
            # 5. Logging
            if verbose and iteration % 10 == 0:
                print(f"Iter {iteration}: Melhor Fitness = {self.best_fitness:.4f} "
                      f"(Iter atual: {melhor_fitness_iter:.4f})")
        
        return self.best_solution
