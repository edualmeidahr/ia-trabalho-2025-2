"""
Script principal para executar CLONALG no problema de montagem de provas.
"""

import argparse
import random
import sys
import os
import numpy as np
import copy

# Adiciona o diretório raiz ao path para importar os módulos do projeto
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from src.part4_swarm_immune.clonalg import CLONALG
from src.part3_ga.problems.exam import BancoDeQuestoes, Questao


TAMANHO_PROVA = 10
ALVO_TEMPO_MIN = 50   # Mínimo de minutos
ALVO_TEMPO_MAX = 60   # Máximo de minutos
ALVO_DIFICULDADE = 4.0


class ExamProblemCLONALG:
    """
    Classe que adapta o problema de montagem de provas para o CLONALG.
    Define criação de anticorpos, mutação e avaliação.
    """
    
    def __init__(self, materia_filtro: str, topico_filtro: str, banco: BancoDeQuestoes):
        # Filtra questões disponíveis
        self.questoes_candidatas = banco.filtrar(materia=materia_filtro, subtopico=topico_filtro)
        
        # Validação
        if len(self.questoes_candidatas) < TAMANHO_PROVA:
            raise ValueError(f"Erro: Questões insuficientes para o filtro '{materia_filtro}'/'{topico_filtro}'. "
                           f"Encontradas: {len(self.questoes_candidatas)} (Mínimo: {TAMANHO_PROVA})")
        
        print(f"\n--- Configuração do Problema (CLONALG) ---")
        print(f"Filtro: {materia_filtro} " + (f"({topico_filtro})" if topico_filtro else "(Todos os tópicos)"))
        print(f"Espaço de busca: {len(self.questoes_candidatas)} questões candidatas.")
        print(f"Meta: {TAMANHO_PROVA} questões | Tempo {ALVO_TEMPO_MIN}-{ALVO_TEMPO_MAX}min | Dif média {ALVO_DIFICULDADE}")
    
    def criar_anticorpo(self) -> list[Questao]:
        """
        Cria um anticorpo aleatório (prova aleatória).
        """
        return random.sample(self.questoes_candidatas, TAMANHO_PROVA)
    
    def fitness(self, prova: list[Questao]) -> float:
        """
        Calcula a aptidão (nota) da prova.
        Reutiliza a mesma função do AG.
        """
        # 1. Hard Constraint: Questões duplicadas
        ids = [q.id for q in prova]
        if len(set(ids)) < len(ids):
            return -1000.0  # Solução inválida
        
        # 2. Cálculo das métricas da prova
        tempo_total = sum(q.tempo for q in prova)
        dificuldade_media = np.mean([q.dificuldade for q in prova])
        
        score = 1000.0  # Pontuação base
        
        # 3. Penalidade de Tempo (Soft Constraint)
        if not (ALVO_TEMPO_MIN <= tempo_total <= ALVO_TEMPO_MAX):
            erro_min = abs(tempo_total - ALVO_TEMPO_MIN)
            erro_max = abs(tempo_total - ALVO_TEMPO_MAX)
            distancia = min(erro_min, erro_max)
            score -= distancia * 10  # -10 pts por minuto errado
        
        # 4. Penalidade de Dificuldade (Soft Constraint)
        erro_dif = abs(dificuldade_media - ALVO_DIFICULDADE)
        score -= erro_dif * 200  # -200 pts por 1.0 de desvio na dificuldade
        
        return score
    
    def mutar(self, prova: list[Questao], taxa_mut: float) -> list[Questao]:
        """
        Aplica mutação na prova com taxa especificada.
        A taxa é usada para determinar quantas questões trocar.
        
        Args:
            prova: Prova a ser mutada
            taxa_mut: Taxa de mutação [0, 1] (da hipermutação inversa)
        
        Returns:
            Prova mutada
        """
        prova_mutada = copy.deepcopy(prova)
        
        # Número de mutações baseado na taxa
        # taxa_mut já vem da hipermutação inversa (exp(-ρ × afinidade))
        n_mutacoes = max(1, int(taxa_mut * len(prova_mutada)))
        
        # Encontra questões já usadas
        ids_usados = {q.id for q in prova_mutada}
        
        for _ in range(n_mutacoes):
            # Escolhe posição aleatória para trocar
            idx = random.randint(0, len(prova_mutada) - 1)
            
            # Encontra candidatas válidas (não usadas)
            candidatas_validas = [q for q in self.questoes_candidatas 
                                 if q.id not in ids_usados]
            
            if candidatas_validas:
                # Substitui questão
                questao_antiga = prova_mutada[idx]
                ids_usados.remove(questao_antiga.id)
                
                questao_nova = random.choice(candidatas_validas)
                prova_mutada[idx] = questao_nova
                ids_usados.add(questao_nova.id)
        
        return prova_mutada


def main():
    # Configuração via terminal
    parser = argparse.ArgumentParser(description='CLONALG para Montagem de Prova')
    
    # Filtros de Dados
    parser.add_argument('--materia', type=str, default='Física', help='Matéria principal')
    parser.add_argument('--topico', type=str, default=None, help='Subtópico específico (opcional)')
    
    # Parâmetros do CLONALG
    parser.add_argument('--iters', type=int, default=50, help='Número de iterações')
    parser.add_argument('--pop', type=int, default=50, help='Tamanho da população')
    parser.add_argument('--beta', type=float, default=10.0, help='Fator de clonagem')
    parser.add_argument('--rho', type=float, default=2.0, help='Taxa de decaimento da mutação')
    parser.add_argument('--diversity', type=float, default=0.1, help='Taxa de substituição (diversidade)')
    parser.add_argument('--memory', type=int, default=10, help='Tamanho do conjunto de memória')
    
    args = parser.parse_args()
    
    # 1. Carrega Dados e Configura o Problema
    try:
        banco = BancoDeQuestoes()
        problem = ExamProblemCLONALG(args.materia, args.topico, banco)
    except ValueError as e:
        print(e)
        return
    
    # 2. Inicializa o CLONALG
    clonalg = CLONALG(
        pop_size=args.pop,
        fitness_fn=problem.fitness,
        create_antibody=problem.criar_anticorpo,
        mutate_fn=problem.mutar,
        beta=args.beta,
        rho=args.rho,
        diversity_rate=args.diversity,
        memory_size=args.memory
    )
    
    # 3. Execução
    print(f"\nIniciando CLONALG: Pop={args.pop}, Iters={args.iters}, "
          f"β={args.beta}, ρ={args.rho}, Diversity={args.diversity}")
    best_solution = clonalg.run(n_iterations=args.iters)
    
    # 4. Relatório Final da Melhor Solução
    score = problem.fitness(best_solution)
    tempo_total = sum(q.tempo for q in best_solution)
    dif_media = np.mean([q.dificuldade for q in best_solution])
    
    print("\n" + "="*40)
    print(" MELHOR PROVA ENCONTRADA (CLONALG)")
    print("="*40)
    print(f"Fitness Final: {score:.2f}")
    print(f"Tempo Total..: {tempo_total} min  \t[Meta: {ALVO_TEMPO_MIN}-{ALVO_TEMPO_MAX}]")
    print(f"Dif. Média...: {dif_media:.2f}     \t[Meta: {ALVO_DIFICULDADE}]")
    print("-" * 40)
    
    # Exibe as questões formatadas
    for i, q in enumerate(best_solution):
        print(f"{i+1:02d}. {q}")
    print("="*40)
    
    # Estatísticas adicionais
    print(f"\nEstatísticas:")
    print(f"  Melhor fitness histórico: {clonalg.best_fitness:.2f}")
    print(f"  Número de iterações: {args.iters}")
    print(f"  Tamanho da população: {args.pop}")
    print(f"  Tamanho da memória: {len(clonalg.memory)}")


if __name__ == "__main__":
    main()

