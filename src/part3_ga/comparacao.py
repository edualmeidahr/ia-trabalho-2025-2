import matplotlib.pyplot as plt
import sys
import os


sys.path.append(os.path.dirname(__file__))

from ga import GA
from problems.exam import BancoDeQuestoes

from run_ga import ExamProblem 

def run_experiment(pop_size, generations, problem, label, color):
    print(f"--- Rodando: {label} (Pop={pop_size}, Gens={generations}) ---")
    
    # Instancia o SEU AG com as funções do problema
    ga = GA(
        pop_size=pop_size,
        fitness_fn=problem.fitness,
        create_ind=problem.create_ind,
        mutate_fn=problem.mutate,
        crossover_fn=problem.crossover,
        cx_rate=0.7,    # Fixo conforme metodologia
        mut_rate=0.01,  # Fixo conforme metodologia
        elitism=True,
        seed=42         # Seed fixa para reprodutibilidade
    )
    
    
    ga.run(n_generations=generations, verbose=False)
    
   
    return ga.history, color

def main():
    # 1. Configura o Problema (Física - Cinemática)
    print("Inicializando Banco de Questões e Definindo Problema...")
    try:
        banco = BancoDeQuestoes()
        problem = ExamProblem(materia_filtro="Física", topico_filtro="Cinemática", banco=banco)
    except ValueError as e:
        print(e)
        return

    # 2. Define os 3 Cenários para o Relatório
    scenarios = [
        
        {"pop": 50,  "gens": 50, "label": "Baixa Diversidade (Pop=50)", "color": "red"},
        
        
        {"pop": 50, "gens": 100, "label": "Baseline (Pop=50)",         "color": "blue"},
        
        
        {"pop": 50, "gens": 500,  "label": "Alta Diversidade (Pop=50)", "color": "green"}
    ]

    # 3. Executa e Plota
    plt.figure(figsize=(10, 6))

    for s in scenarios:
        hist, col = run_experiment(s["pop"], s["gens"], problem, s["label"], s["color"])
        plt.plot(hist, label=s["label"], color=col, linewidth=2)

    # 4. Estética do Gráfico (Padrão Acadêmico IEEE)
    plt.title("Análise de Convergência: Impacto do Tamanho da População", fontsize=14)
    plt.xlabel("Gerações", fontsize=12)
    plt.ylabel("Melhor Fitness (Aptidão)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=11)
    
    # Ajuste para garantir que mostre até a geração 100 no eixo X
    plt.xlim(0, 100)
    
    plt.tight_layout()

    # Salva na pasta correta (ajuste o caminho se necessário)
    output_path = "../../reports/figs/ga_comparison_pop.png"
    
    # Cria a pasta se não existir
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.savefig(output_path, dpi=300)
    print(f"\nGráfico salvo com sucesso em: {output_path}")
    

if __name__ == "__main__":
    main()