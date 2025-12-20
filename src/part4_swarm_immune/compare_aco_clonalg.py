"""
Script para comparar ACO e CLONALG no problema de montagem de provas.
Gera gráficos comparativos de convergência e métricas finais.
"""

import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import time

# Adiciona o diretório raiz ao path para importar os módulos do projeto
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from src.part4_swarm_immune.aco import ACO
from src.part4_swarm_immune.clonalg import CLONALG
from src.part4_swarm_immune.run_aco import ExamProblemACO
from src.part4_swarm_immune.run_clonalg import ExamProblemCLONALG
from src.part3_ga.problems.exam import BancoDeQuestoes

# Configuração de estilo
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10

# Caminhos
BASE_DIR = os.path.join(os.path.dirname(__file__), '../..')
REPORTS_PATH = os.path.join(BASE_DIR, 'reports/figs')

# Parâmetros do problema (mesmos para ambos)
TAMANHO_PROVA = 10
ALVO_TEMPO_MIN = 50
ALVO_TEMPO_MAX = 60
ALVO_DIFICULDADE = 4.0

# Parâmetros dos algoritmos (padrões da metodologia)
ACO_PARAMS = {
    'ants': 20,
    'alpha': 1.0,
    'beta': 2.0,
    'rho': 0.1,
    'Q': 10.0,
    'tau0': 1.0,
    'elite': 5.0
}

CLONALG_PARAMS = {
    'pop': 50,
    'beta': 10.0,
    'rho': 2.0,
    'diversity': 0.1,
    'memory': 10
}

N_ITERATIONS = 50


def run_aco(materia='Física', topico=None, n_iterations=50):
    """
    Executa ACO e retorna resultados.
    """
    print("\n" + "="*60)
    print("EXECUTANDO ACO")
    print("="*60)
    
    # Carrega dados
    banco = BancoDeQuestoes()
    problem = ExamProblemACO(materia, topico, banco)
    
    # Inicializa ACO
    n_options = len(problem.questoes_candidatas)
    aco = ACO(
        n_ants=ACO_PARAMS['ants'],
        n_positions=TAMANHO_PROVA,
        n_options=n_options,
        fitness_fn=problem.fitness,
        heuristica_fn=problem.heuristica,
        get_valid_options=problem.get_valid_options,
        update_state=problem.update_state,
        get_option_id=problem.get_questao_idx,
        alpha=ACO_PARAMS['alpha'],
        beta=ACO_PARAMS['beta'],
        rho=ACO_PARAMS['rho'],
        Q=ACO_PARAMS['Q'],
        tau_zero=ACO_PARAMS['tau0'],
        e=ACO_PARAMS['elite']
    )
    
    # Executa
    start_time = time.time()
    best_solution = aco.run(n_iterations=n_iterations, verbose=False)
    execution_time = time.time() - start_time
    
    # Calcula métricas finais
    score = problem.fitness(best_solution)
    tempo_total = sum(q.tempo for q in best_solution)
    dif_media = np.mean([q.dificuldade for q in best_solution])
    
    print(f"Fitness Final: {score:.2f}")
    print(f"Tempo Total: {tempo_total} min (Meta: {ALVO_TEMPO_MIN}-{ALVO_TEMPO_MAX})")
    print(f"Dificuldade Média: {dif_media:.2f} (Meta: {ALVO_DIFICULDADE})")
    print(f"Tempo de Execução: {execution_time:.2f}s")
    
    return {
        'algorithm': 'ACO',
        'best_solution': best_solution,
        'best_fitness': aco.best_fitness,
        'history': aco.history,
        'score': score,
        'tempo_total': tempo_total,
        'dificuldade_media': dif_media,
        'execution_time': execution_time,
        'n_iterations': n_iterations
    }


def run_clonalg(materia='Física', topico=None, n_iterations=50):
    """
    Executa CLONALG e retorna resultados.
    """
    print("\n" + "="*60)
    print("EXECUTANDO CLONALG")
    print("="*60)
    
    # Carrega dados
    banco = BancoDeQuestoes()
    problem = ExamProblemCLONALG(materia, topico, banco)
    
    # Inicializa CLONALG
    clonalg = CLONALG(
        pop_size=CLONALG_PARAMS['pop'],
        fitness_fn=problem.fitness,
        create_antibody=problem.criar_anticorpo,
        mutate_fn=problem.mutar,
        beta=CLONALG_PARAMS['beta'],
        rho=CLONALG_PARAMS['rho'],
        diversity_rate=CLONALG_PARAMS['diversity'],
        memory_size=CLONALG_PARAMS['memory']
    )
    
    # Executa
    start_time = time.time()
    best_solution = clonalg.run(n_iterations=n_iterations, verbose=False)
    execution_time = time.time() - start_time
    
    # Calcula métricas finais
    score = problem.fitness(best_solution)
    tempo_total = sum(q.tempo for q in best_solution)
    dif_media = np.mean([q.dificuldade for q in best_solution])
    
    print(f"Fitness Final: {score:.2f}")
    print(f"Tempo Total: {tempo_total} min (Meta: {ALVO_TEMPO_MIN}-{ALVO_TEMPO_MAX})")
    print(f"Dificuldade Média: {dif_media:.2f} (Meta: {ALVO_DIFICULDADE})")
    print(f"Tempo de Execução: {execution_time:.2f}s")
    
    return {
        'algorithm': 'CLONALG',
        'best_solution': best_solution,
        'best_fitness': clonalg.best_fitness,
        'history': clonalg.history,
        'score': score,
        'tempo_total': tempo_total,
        'dificuldade_media': dif_media,
        'execution_time': execution_time,
        'n_iterations': n_iterations
    }


def plot_comparison(aco_results, clonalg_results):
    """
    Gera gráficos comparativos entre ACO e CLONALG.
    """
    print("\n" + "="*60)
    print("GERANDO GRÁFICOS COMPARATIVOS")
    print("="*60)
    
    # Criar figura com subplots
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
    
    # 1. Gráfico de Convergência (subplot grande)
    ax1 = fig.add_subplot(gs[0, :])
    
    iterations_aco = range(len(aco_results['history']))
    iterations_clonalg = range(len(clonalg_results['history']))
    
    ax1.plot(iterations_aco, aco_results['history'], 
             label='ACO', linewidth=2, color='#3498db', alpha=0.8)
    ax1.plot(iterations_clonalg, clonalg_results['history'], 
             label='CLONALG', linewidth=2, color='#e67e22', alpha=0.8)
    
    ax1.set_xlabel('Iteração', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Melhor Fitness', fontsize=12, fontweight='bold')
    ax1.set_title('Convergência: Evolução do Melhor Fitness ao Longo das Iterações', 
                  fontsize=14, fontweight='bold', pad=15)
    ax1.legend(loc='best', fontsize=11, framealpha=0.9)
    ax1.grid(True, linestyle='--', alpha=0.3)
    ax1.set_xlim([0, max(len(aco_results['history']), len(clonalg_results['history'])) - 1])
    
    # Adicionar valores finais
    ax1.axhline(y=aco_results['best_fitness'], color='#3498db', 
               linestyle='--', alpha=0.5, linewidth=1)
    ax1.axhline(y=clonalg_results['best_fitness'], color='#e67e22', 
               linestyle='--', alpha=0.5, linewidth=1)
    
    # 2. Comparação de Fitness Final
    ax2 = fig.add_subplot(gs[1, 0])
    algorithms = ['ACO', 'CLONALG']
    fitness_values = [aco_results['best_fitness'], clonalg_results['best_fitness']]
    colors = ['#3498db', '#e67e22']
    
    bars = ax2.bar(algorithms, fitness_values, color=colors, alpha=0.8, 
                   edgecolor='black', linewidth=1.5)
    
    for bar, val in zip(bars, fitness_values):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 5,
                f'{val:.2f}', ha='center', va='bottom', 
                fontsize=11, fontweight='bold')
    
    ax2.set_ylabel('Fitness Final', fontsize=11, fontweight='bold')
    ax2.set_title('Fitness Final', fontsize=12, fontweight='bold')
    ax2.grid(axis='y', linestyle='--', alpha=0.3)
    ax2.set_ylim([min(fitness_values) * 0.95, max(fitness_values) * 1.05])
    
    # 3. Comparação de Tempo de Execução
    ax3 = fig.add_subplot(gs[1, 1])
    time_values = [aco_results['execution_time'], clonalg_results['execution_time']]
    
    bars = ax3.bar(algorithms, time_values, color=colors, alpha=0.8, 
                   edgecolor='black', linewidth=1.5)
    
    for bar, val in zip(bars, time_values):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + max(time_values) * 0.02,
                f'{val:.2f}s', ha='center', va='bottom', 
                fontsize=11, fontweight='bold')
    
    ax3.set_ylabel('Tempo (segundos)', fontsize=11, fontweight='bold')
    ax3.set_title('Tempo de Execução', fontsize=12, fontweight='bold')
    ax3.grid(axis='y', linestyle='--', alpha=0.3)
    ax3.set_ylim([0, max(time_values) * 1.15])
    
    # 4. Comparação de Desvio das Metas
    ax4 = fig.add_subplot(gs[1, 2])
    
    # Desvio de tempo
    tempo_aco = aco_results['tempo_total']
    tempo_clonalg = clonalg_results['tempo_total']
    tempo_medio = (ALVO_TEMPO_MIN + ALVO_TEMPO_MAX) / 2
    desvio_tempo_aco = abs(tempo_aco - tempo_medio)
    desvio_tempo_clonalg = abs(tempo_clonalg - tempo_medio)
    
    # Desvio de dificuldade
    desvio_dif_aco = abs(aco_results['dificuldade_media'] - ALVO_DIFICULDADE)
    desvio_dif_clonalg = abs(clonalg_results['dificuldade_media'] - ALVO_DIFICULDADE)
    
    x = np.arange(2)
    width = 0.35
    
    bars1 = ax4.bar(x - width/2, [desvio_tempo_aco, desvio_tempo_clonalg], 
                    width, label='Desvio Tempo (min)', color='#3498db', alpha=0.8)
    bars2 = ax4.bar(x + width/2, [desvio_dif_aco, desvio_dif_clonalg], 
                    width, label='Desvio Dificuldade', color='#e67e22', alpha=0.8)
    
    ax4.set_ylabel('Desvio', fontsize=11, fontweight='bold')
    ax4.set_title('Desvio das Metas', fontsize=12, fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(algorithms)
    ax4.legend(fontsize=9)
    ax4.grid(axis='y', linestyle='--', alpha=0.3)
    
    # Adicionar valores nas barras
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + max(desvio_tempo_aco, desvio_tempo_clonalg, 
                     desvio_dif_aco, desvio_dif_clonalg) * 0.02,
                    f'{height:.2f}', ha='center', va='bottom', 
                    fontsize=9, fontweight='bold')
    
    # Título geral
    fig.suptitle('Comparação: ACO vs CLONALG - Problema de Montagem de Provas', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    # Salvar figura
    os.makedirs(REPORTS_PATH, exist_ok=True)
    output_path = os.path.join(REPORTS_PATH, 'aco_clonalg_comparison.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✅ Gráfico salvo em: {os.path.abspath(output_path)}")
    plt.close()
    
    # Imprimir resumo
    print("\n" + "="*60)
    print("RESUMO COMPARATIVO")
    print("="*60)
    print(f"{'Métrica':<25} {'ACO':<15} {'CLONALG':<15}")
    print("-" * 60)
    print(f"{'Fitness Final':<25} {aco_results['best_fitness']:<15.2f} {clonalg_results['best_fitness']:<15.2f}")
    print(f"{'Tempo Total (min)':<25} {aco_results['tempo_total']:<15.2f} {clonalg_results['tempo_total']:<15.2f}")
    print(f"{'Dificuldade Média':<25} {aco_results['dificuldade_media']:<15.2f} {clonalg_results['dificuldade_media']:<15.2f}")
    print(f"{'Tempo Execução (s)':<25} {aco_results['execution_time']:<15.2f} {clonalg_results['execution_time']:<15.2f}")
    
    # Desvios
    print(f"\n{'Desvio Tempo (min)':<25} {desvio_tempo_aco:<15.2f} {desvio_tempo_clonalg:<15.2f}")
    print(f"{'Desvio Dificuldade':<25} {desvio_dif_aco:<15.2f} {desvio_dif_clonalg:<15.2f}")
    print("="*60)
    
    # Análise
    melhor_fitness = 'ACO' if aco_results['best_fitness'] > clonalg_results['best_fitness'] else 'CLONALG'
    mais_rapido = 'ACO' if aco_results['execution_time'] < clonalg_results['execution_time'] else 'CLONALG'
    
    print(f"\n📊 Análise:")
    print(f"   • Melhor Fitness: {melhor_fitness} ({max(aco_results['best_fitness'], clonalg_results['best_fitness']):.2f})")
    print(f"   • Mais Rápido: {mais_rapido} ({min(aco_results['execution_time'], clonalg_results['execution_time']):.2f}s)")
    print("="*60)


def main():
    """
    Função principal: executa ambos os algoritmos e gera comparação.
    """
    # Parâmetros do problema específico
    materia = 'Física'
    topico = 'Cinemática'
    
    print("="*60)
    print("COMPARAÇÃO: ACO vs CLONALG")
    print("="*60)
    print(f"Parâmetros do Problema:")
    print(f"  • Matéria: {materia}")
    print(f"  • Tópico: {topico}")
    print(f"  • Tamanho da Prova: {TAMANHO_PROVA} questões")
    print(f"  • Tempo Alvo: {ALVO_TEMPO_MIN}-{ALVO_TEMPO_MAX} min")
    print(f"  • Dificuldade Alvo: {ALVO_DIFICULDADE}")
    print(f"  • Iterações: {N_ITERATIONS}")
    
    # Executa ACO
    aco_results = run_aco(materia=materia, topico=topico, n_iterations=N_ITERATIONS)
    
    # Executa CLONALG
    clonalg_results = run_clonalg(materia=materia, topico=topico, n_iterations=N_ITERATIONS)
    
    # Gera gráficos
    plot_comparison(aco_results, clonalg_results)
    
    print("\n✅ Processo concluído com sucesso!")


if __name__ == "__main__":
    main()

