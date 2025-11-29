# src/part3_ga/run_ga.py
import argparse
import random
import sys
import os
import numpy as np

# Adiciona o diretório raiz ao path para importar os módulos do projeto
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from src.part3_ga.ga import GA
from src.part3_ga.problems.exam import BancoDeQuestoes, Questao


TAMANHO_PROVA = 10
ALVO_TEMPO_MIN = 50   # Mínimo de minutos
ALVO_TEMPO_MAX = 60   # Máximo de minutos
ALVO_DIFICULDADE = 4.0

class ExamProblem:
    """
    Classe que conecta o domínio do problema (Prova) ao Algoritmo Genético.
    Define como criar, avaliar e modificar uma prova.
    """
    def __init__(self, materia_filtro: str, topico_filtro: str, banco: BancoDeQuestoes):
        # Filtra questões disponíveis baseadas na matéria e (opcionalmente) no tópico
        self.questoes_candidatas = banco.filtrar(materia=materia_filtro, subtopico=topico_filtro)
        
        # Validação: precisamos de pelo menos 10 questões para montar uma prova
        if len(self.questoes_candidatas) < TAMANHO_PROVA:
             raise ValueError(f"Erro: Questões insuficientes para o filtro '{materia_filtro}'/'{topico_filtro}'. "
                              f"Encontradas: {len(self.questoes_candidatas)} (Mínimo: {TAMANHO_PROVA})")
        
        print(f"\n--- Configuração do Problema ---")
        print(f"Filtro: {materia_filtro} " + (f"({topico_filtro})" if topico_filtro else "(Todos os tópicos)"))
        print(f"Espaço de busca: {len(self.questoes_candidatas)} questões candidatas.")
        print(f"Meta: {TAMANHO_PROVA} questões | Tempo {ALVO_TEMPO_MIN}-{ALVO_TEMPO_MAX}min | Dif média {ALVO_DIFICULDADE}")

    def create_ind(self):
        """Cria um indivíduo aleatório (lista de 10 questões únicas)."""
        return random.sample(self.questoes_candidatas, TAMANHO_PROVA)

    def fitness(self, prova: list[Questao]) -> float:
        """
        Calcula a aptidão (nota) da prova.
        Retorna um valor alto para soluções boas e baixo para ruins.
        """
        # 1. Penalidade Máxima (Hard Constraint): Questões duplicadas
        ids = [q.id for q in prova]
        if len(set(ids)) < len(ids):
            return -1000.0  # Solução inválida

        # 2. Cálculo das métricas da prova
        tempo_total = sum(q.tempo for q in prova)
        dificuldade_media = np.mean([q.dificuldade for q in prova])

        score = 1000.0  # Pontuação base

        # 3. Penalidade de Tempo (Soft Constraint)
        # Se estiver fora do intervalo 50-60min, desconta pontos pela distância
        if not (ALVO_TEMPO_MIN <= tempo_total <= ALVO_TEMPO_MAX):
            erro_min = abs(tempo_total - ALVO_TEMPO_MIN)
            erro_max = abs(tempo_total - ALVO_TEMPO_MAX)
            distancia = min(erro_min, erro_max)
            score -= distancia * 10  # -10 pts por minuto errado

        # 4. Penalidade de Dificuldade (Soft Constraint)
        # média 4.0. Desconta pontos proporcionalmente ao erro.
        erro_dif = abs(dificuldade_media - ALVO_DIFICULDADE)
        score -= erro_dif * 200  # -200 pts por 1.0 de desvio na dificuldade

        return score

    def mutate(self, prova: list[Questao]) -> list[Questao]:
        """
        Mutação: Troca uma questão da prova por outra do banco que não esteja na prova.
        """
        nova_prova = prova.copy()
        
        # Escolhe uma posição aleatória para trocar
        idx_to_remove = random.randint(0, TAMANHO_PROVA - 1)
        
        # Encontra candidatos válidos (questões do banco que não estão nesta prova)
        ids_na_prova = {q.id for q in nova_prova}
        candidatas_validas = [q for q in self.questoes_candidatas if q.id not in ids_na_prova]
        
        # Se houver substitutos, realiza a troca
        if candidatas_validas:
            nova_prova[idx_to_remove] = random.choice(candidatas_validas)
            
        return nova_prova

    def crossover(self, p1: list[Questao], p2: list[Questao]):
        """
        Cruzamento de Ponto Único (Single Point) com função de Reparo para evitar duplicatas.
        """
        # Escolhe ponto de corte
        point = random.randint(1, TAMANHO_PROVA - 1)
        
        # Gera filhos combinando partes dos pais
        f1 = p1[:point] + p2[point:]
        f2 = p2[:point] + p1[point:]
        
        # Função auxiliar para remover duplicatas geradas pelo corte
        def reparar(filho):
            ids_existentes = set()
            indices_duplicados = []
            
            # Mapeia onde estão as duplicatas
            for i, q in enumerate(filho):
                if q.id in ids_existentes:
                    indices_duplicados.append(i)
                else:
                    ids_existentes.add(q.id)
            
            # Substitui as duplicatas por questões novas
            if indices_duplicados:
                disponiveis = [q for q in self.questoes_candidatas if q.id not in ids_existentes]
                random.shuffle(disponiveis)
                
                for idx in indices_duplicados:
                    if disponiveis:
                        filho[idx] = disponiveis.pop()
            return filho

        return reparar(f1), reparar(f2)

def main():
    # Configuração via terminal para facilitar testes no relatório
    parser = argparse.ArgumentParser(description='AG para Montagem de Prova')
    
    # Filtros de Dados
    parser.add_argument('--materia', type=str, default='Física', help='Matéria principal')
    parser.add_argument('--topico', type=str, default=None, help='Subtópico específico (opcional)')
    
    
    parser.add_argument('--gens', type=int, default=50, help='Número de gerações')
    parser.add_argument('--pop', type=int, default=100, help='Tamanho da população')
    parser.add_argument('--cx', type=float, default=0.7, help='Probabilidade de Crossover')
    parser.add_argument('--mut', type=float, default=0.01, help='Probabilidade de Mutação')
    
    args = parser.parse_args()

    # 1. Carrega Dados e Configura o Problema
    try:
        banco = BancoDeQuestoes() # Gera/Carrega as 5000 questões
        problem = ExamProblem(args.materia, args.topico, banco)
    except ValueError as e:
        print(e)
        return

    # 2. Inicializa o AG
    ga = GA(
        pop_size=args.pop,
        fitness_fn=problem.fitness,
        create_ind=problem.create_ind,
        mutate_fn=problem.mutate,
        crossover_fn=problem.crossover,
        cx_rate=args.cx,   # Usa o valor 0.7 (padrão) ou o passado no terminal
        mut_rate=args.mut, # Usa o valor 0.01 (padrão) ou o passado no terminal
        elitism=True
    )

    # 3. Execução
    print(f"Iniciando AG: Pop={args.pop}, Gens={args.gens}, CX={args.cx}, MUT={args.mut}")
    best_ind = ga.run(n_generations=args.gens)

    # 4. Relatório Final da Melhor Solução
    score = problem.fitness(best_ind)
    tempo_total = sum(q.tempo for q in best_ind)
    dif_media = np.mean([q.dificuldade for q in best_ind])
    
    print("\n" + "="*40)
    print(" MELHOR PROVA ENCONTRADA")
    print("="*40)
    print(f"Fitness Final: {score:.2f}")
    print(f"Tempo Total..: {tempo_total} min  \t[Meta: {ALVO_TEMPO_MIN}-{ALVO_TEMPO_MAX}]")
    print(f"Dif. Média...: {dif_media:.2f}     \t[Meta: {ALVO_DIFICULDADE}]")
    print("-" * 40)
    
    # Exibe as questões formatadas
    for i, q in enumerate(best_ind):
        print(f"{i+1:02d}. {q}")
    print("="*40)

if __name__ == "__main__":
    main()