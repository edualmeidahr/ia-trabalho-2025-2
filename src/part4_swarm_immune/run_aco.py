"""
Script principal para executar ACO no problema de montagem de provas.
"""

import argparse
import random
import sys
import os
import numpy as np

# Adiciona o diretório raiz ao path para importar os módulos do projeto
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from src.part4_swarm_immune.aco import ACO
from src.part3_ga.problems.exam import BancoDeQuestoes, Questao


TAMANHO_PROVA = 10
ALVO_TEMPO_MIN = 50   # Mínimo de minutos
ALVO_TEMPO_MAX = 60   # Máximo de minutos
ALVO_DIFICULDADE = 4.0


class ExamProblemACO:
    """
    Classe que adapta o problema de montagem de provas para o ACO.
    Define heurística, validação e funções auxiliares.
    """
    
    def __init__(self, materia_filtro: str, topico_filtro: str, banco: BancoDeQuestoes):
        # Filtra questões disponíveis
        self.questoes_candidatas = banco.filtrar(materia=materia_filtro, subtopico=topico_filtro)
        
        # Validação
        if len(self.questoes_candidatas) < TAMANHO_PROVA:
            raise ValueError(f"Erro: Questões insuficientes para o filtro '{materia_filtro}'/'{topico_filtro}'. "
                           f"Encontradas: {len(self.questoes_candidatas)} (Mínimo: {TAMANHO_PROVA})")
        
        # Mapeia IDs das questões para índices na lista de candidatas (0 a N-1)
        # Isso é necessário porque o ACO usa índices de 0 a n_options-1
        self.questao_to_idx = {q.id: idx for idx, q in enumerate(self.questoes_candidatas)}
        
        print(f"\n--- Configuração do Problema (ACO) ---")
        print(f"Filtro: {materia_filtro} " + (f"({topico_filtro})" if topico_filtro else "(Todos os tópicos)"))
        print(f"Espaço de busca: {len(self.questoes_candidatas)} questões candidatas.")
        print(f"Meta: {TAMANHO_PROVA} questões | Tempo {ALVO_TEMPO_MIN}-{ALVO_TEMPO_MAX}min | Dif média {ALVO_DIFICULDADE}")
    
    def get_questao_idx(self, questao: Questao) -> int:
        """Retorna o índice da questão na lista de candidatas."""
        return self.questao_to_idx[questao.id]
    
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
    
    def heuristica(self, posicao: int, questao: Questao, estado: dict) -> float:
        """
        Calcula atratividade de escolher 'questao' na 'posicao' atual.
        Retorna valor maior para escolhas mais promissoras.
        """
        # 1. Hard Constraint: Duplicatas
        if 'prova' in estado:
            ids_na_prova = {q.id for q in estado['prova']}
            if questao.id in ids_na_prova:
                return 0.0  # Não pode escolher
        
        # 2. Cálculo de métricas projetadas
        tempo_atual = estado.get('tempo_total', 0)
        dificuldades_atual = estado.get('dificuldades', [])
        
        tempo_projetado = tempo_atual + questao.tempo
        dificuldades_projetadas = dificuldades_atual + [questao.dificuldade]
        dificuldade_media_projetada = np.mean(dificuldades_projetadas)
        
        # 3. Questões restantes
        questoes_restantes = TAMANHO_PROVA - (posicao + 1)
        
        # 4. Heurística baseada em quão próximo está das metas
        score = 1.0  # Base
        
        # 4a. Tempo: penaliza se já passou do limite ou está muito abaixo
        if tempo_projetado > ALVO_TEMPO_MAX:
            # Já passou do máximo, muito ruim
            score *= 0.1
        elif tempo_projetado < ALVO_TEMPO_MIN:
            # Ainda abaixo, mas precisa considerar questões restantes
            tempo_medio_necessario = (ALVO_TEMPO_MIN - tempo_projetado) / max(questoes_restantes, 1)
            if questao.tempo < tempo_medio_necessario * 0.5:
                # Questão muito rápida, pode não conseguir atingir meta
                score *= 0.5
            elif questao.tempo > tempo_medio_necessario * 1.5:
                # Questão muito lenta, pode passar do limite
                score *= 0.7
            else:
                # Questão adequada para atingir meta
                score *= 1.2
        else:
            # Dentro do intervalo, bom!
            # Mas precisa evitar passar do máximo com questões restantes
            tempo_disponivel = ALVO_TEMPO_MAX - tempo_projetado
            tempo_medio_restante = tempo_disponivel / max(questoes_restantes, 1)
            if questao.tempo > tempo_medio_restante * 1.5:
                # Questão muito lenta, pode passar do limite
                score *= 0.8
            else:
                score *= 1.5
        
        # 4b. Dificuldade: penaliza desvios da meta
        erro_dificuldade = abs(dificuldade_media_projetada - ALVO_DIFICULDADE)
        if erro_dificuldade < 0.3:
            score *= 1.3  # Muito próximo da meta
        elif erro_dificuldade < 0.5:
            score *= 1.1  # Próximo da meta
        elif erro_dificuldade > 1.0:
            score *= 0.6  # Muito longe da meta
        elif erro_dificuldade > 0.7:
            score *= 0.8  # Longe da meta
        
        # 4c. Balanceamento: questões muito extremas são menos desejáveis
        if questao.dificuldade < 2.0 or questao.dificuldade > 4.5:
            score *= 0.8
        
        # 4d. Considera questões restantes para ajustar dificuldade
        if questoes_restantes > 0:
            # Se está abaixo da meta, precisa de questões mais difíceis
            if dificuldade_media_projetada < ALVO_DIFICULDADE - 0.3:
                if questao.dificuldade > ALVO_DIFICULDADE:
                    score *= 1.1  # Ajuda a subir a média
            # Se está acima da meta, precisa de questões mais fáceis
            elif dificuldade_media_projetada > ALVO_DIFICULDADE + 0.3:
                if questao.dificuldade < ALVO_DIFICULDADE:
                    score *= 1.1  # Ajuda a baixar a média
        
        return max(0.0, score)  # Garante não negativo
    
    def get_valid_options(self, posicao: int, estado: dict) -> list[Questao]:
        """
        Retorna questões válidas para escolher na posição atual.
        Remove questões já usadas na prova.
        """
        if 'prova' not in estado:
            # Primeira questão: todas são válidas
            return self.questoes_candidatas.copy()
        
        # Remove questões já usadas
        ids_usados = {q.id for q in estado['prova']}
        validas = [q for q in self.questoes_candidatas if q.id not in ids_usados]
        
        return validas
    
    def update_state(self, estado: dict, questao: Questao) -> dict:
        """
        Atualiza estado parcial ao adicionar uma questão.
        """
        if 'prova' not in estado:
            estado = {
                'prova': [],
                'tempo_total': 0,
                'dificuldades': []
            }
        
        estado['prova'].append(questao)
        estado['tempo_total'] += questao.tempo
        estado['dificuldades'].append(questao.dificuldade)
        
        return estado


def main():
    # Configuração via terminal
    parser = argparse.ArgumentParser(description='ACO para Montagem de Prova')
    
    # Filtros de Dados
    parser.add_argument('--materia', type=str, default='Física', help='Matéria principal')
    parser.add_argument('--topico', type=str, default=None, help='Subtópico específico (opcional)')
    
    # Parâmetros do ACO
    parser.add_argument('--iters', type=int, default=50, help='Número de iterações')
    parser.add_argument('--ants', type=int, default=20, help='Número de formigas')
    parser.add_argument('--alpha', type=float, default=1.0, help='Peso do feromônio')
    parser.add_argument('--beta', type=float, default=2.0, help='Peso da heurística')
    parser.add_argument('--rho', type=float, default=0.1, help='Taxa de evaporação')
    parser.add_argument('--Q', type=float, default=10.0, help='Constante de deposição')
    parser.add_argument('--tau0', type=float, default=1.0, help='Feromônio inicial')
    parser.add_argument('--elite', type=float, default=5.0, help='Peso da elite')
    
    args = parser.parse_args()
    
    # 1. Carrega Dados e Configura o Problema
    try:
        banco = BancoDeQuestoes()
        problem = ExamProblemACO(args.materia, args.topico, banco)
    except ValueError as e:
        print(e)
        return
    
    # 2. Inicializa o ACO
    # n_options precisa ser >= max_id das questões
    # Mas vamos usar o tamanho da lista de candidatas como limite
    # e mapear IDs para índices
    n_options = len(problem.questoes_candidatas)
    
    aco = ACO(
        n_ants=args.ants,
        n_positions=TAMANHO_PROVA,
        n_options=n_options,
        fitness_fn=problem.fitness,
        heuristica_fn=problem.heuristica,
        get_valid_options=problem.get_valid_options,
        update_state=problem.update_state,
        get_option_id=problem.get_questao_idx,  # Função para mapear questão -> índice
        alpha=args.alpha,
        beta=args.beta,
        rho=args.rho,
        Q=args.Q,
        tau_zero=args.tau0,
        e=args.elite
    )
    
    # 3. Execução
    print(f"\nIniciando ACO: Ants={args.ants}, Iters={args.iters}, "
          f"α={args.alpha}, β={args.beta}, ρ={args.rho}")
    best_solution = aco.run(n_iterations=args.iters)
    
    # 4. Relatório Final da Melhor Solução
    score = problem.fitness(best_solution)
    tempo_total = sum(q.tempo for q in best_solution)
    dif_media = np.mean([q.dificuldade for q in best_solution])
    
    print("\n" + "="*40)
    print(" MELHOR PROVA ENCONTRADA (ACO)")
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
    print(f"  Melhor fitness histórico: {aco.best_fitness:.2f}")
    print(f"  Número de iterações: {args.iters}")
    print(f"  Número de formigas: {args.ants}")


if __name__ == "__main__":
    main()

