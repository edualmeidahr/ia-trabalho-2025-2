"""
Script para gerar gráfico de comparação entre todos os modelos de ML.
Inclui KNN, SVM Padrão, SVM Otimizado e Árvore de Decisão.
"""

import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV

# Ajustar caminho para importar utils_metrics
sys.path.append(os.path.dirname(__file__))
from utils_metrics import load_data, calculate_all_metrics

# Configuração de estilo
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

# Caminhos (ajustar para caminho relativo ao diretório raiz do projeto)
BASE_DIR = os.path.join(os.path.dirname(__file__), '../..')
REPORTS_PATH = os.path.join(BASE_DIR, 'reports/figs')

def train_all_models():
    """
    Treina todos os modelos e retorna predições e métricas.
    """
    print("="*60)
    print("TREINANDO TODOS OS MODELOS PARA COMPARAÇÃO")
    print("="*60)
    
    # Mudar para diretório raiz do projeto para carregar dados
    original_dir = os.getcwd()
    os.chdir(BASE_DIR)
    
    try:
        X_train, X_test, y_train, y_test = load_data()
    finally:
        os.chdir(original_dir)
    
    results = {}
    
    # 1. KNN
    print("\n1. Treinando KNN (k=15)...")
    knn = KNeighborsClassifier(n_neighbors=15, metric='euclidean', n_jobs=-1)
    knn.fit(X_train, y_train)
    y_pred_knn = knn.predict(X_test)
    metrics_knn = calculate_all_metrics(y_test, y_pred_knn)
    results['KNN'] = {
        'y_pred': y_pred_knn,
        'metrics': metrics_knn
    }
    print(f"   Acurácia: {metrics_knn['accuracy']:.4f}")
    
    # 2. SVM Padrão
    print("\n2. Treinando SVM Padrão (C=1, gamma='scale')...")
    svm_padrao = SVC(kernel='rbf', C=1, gamma='scale', random_state=42)
    svm_padrao.fit(X_train, y_train)
    y_pred_svm_padrao = svm_padrao.predict(X_test)
    metrics_svm_padrao = calculate_all_metrics(y_test, y_pred_svm_padrao)
    results['SVM (Padrão)'] = {
        'y_pred': y_pred_svm_padrao,
        'metrics': metrics_svm_padrao
    }
    print(f"   Acurácia: {metrics_svm_padrao['accuracy']:.4f}")
    
    # 3. SVM Otimizado (usando os melhores parâmetros do Grid Search)
    print("\n3. Treinando SVM Otimizado (C=10, gamma=0.001)...")
    print("   (Usando melhores parâmetros encontrados no Grid Search)")
    svm_otimizado = SVC(kernel='rbf', C=10, gamma=0.001, random_state=42)
    svm_otimizado.fit(X_train, y_train)
    y_pred_svm_otimizado = svm_otimizado.predict(X_test)
    metrics_svm_otimizado = calculate_all_metrics(y_test, y_pred_svm_otimizado)
    results['SVM (Otimizado)'] = {
        'y_pred': y_pred_svm_otimizado,
        'metrics': metrics_svm_otimizado
    }
    print(f"   Acurácia: {metrics_svm_otimizado['accuracy']:.4f}")
    
    # 4. Árvore de Decisão
    print("\n4. Treinando Árvore de Decisão (max_depth=10, min_samples_split=20)...")
    tree = DecisionTreeClassifier(
        max_depth=10, 
        min_samples_split=20, 
        random_state=42
    )
    tree.fit(X_train, y_train)
    y_pred_tree = tree.predict(X_test)
    metrics_tree = calculate_all_metrics(y_test, y_pred_tree)
    results['Árvore de Decisão'] = {
        'y_pred': y_pred_tree,
        'metrics': metrics_tree
    }
    print(f"   Acurácia: {metrics_tree['accuracy']:.4f}")
    
    return results, y_test

def plot_comparison(results, y_test):
    """
    Gera gráfico de comparação entre os modelos.
    """
    print("\n" + "="*60)
    print("GERANDO GRÁFICO DE COMPARAÇÃO")
    print("="*60)
    
    # Preparar dados para o gráfico
    models = list(results.keys())
    metrics_to_plot = ['accuracy', 'precision', 'recall', 'f1_score']
    metric_labels = {
        'accuracy': 'Acurácia',
        'precision': 'Precisão',
        'recall': 'Revocação',
        'f1_score': 'F1-Score'
    }
    
    # Extrair valores
    values = {metric: [results[model]['metrics'][metric] for model in models] 
              for metric in metrics_to_plot}
    
    # Criar figura com subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Comparação de Desempenho: Modelos de Aprendizado de Máquina', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    # Cores para cada modelo
    colors = {
        'KNN': '#3498db',           # Azul
        'SVM (Padrão)': '#2ecc71',   # Verde
        'SVM (Otimizado)': '#9b59b6', # Roxo
        'Árvore de Decisão': '#e67e22' # Laranja
    }
    
    # Plotar cada métrica
    positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
    
    for idx, metric in enumerate(metrics_to_plot):
        row, col = positions[idx]
        ax = axes[row, col]
        
        # Criar gráfico de barras
        bars = ax.bar(models, values[metric], 
                      color=[colors.get(m, '#95a5a6') for m in models],
                      alpha=0.8, edgecolor='black', linewidth=1.2)
        
        # Adicionar valores nas barras
        for i, (bar, val) in enumerate(zip(bars, values[metric])):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.005,
                   f'{val:.4f}',
                   ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        # Configurações do gráfico
        ax.set_ylabel('Valor', fontsize=11, fontweight='bold')
        ax.set_title(metric_labels[metric], fontsize=12, fontweight='bold')
        ax.set_ylim([0.75, max(values[metric]) * 1.15])
        ax.grid(axis='y', linestyle='--', alpha=0.3)
        ax.set_xticks(range(len(models)))
        ax.set_xticklabels(models, rotation=15, ha='right', fontsize=9)
        
        # Adicionar linha de referência no máximo
        max_val = max(values[metric])
        ax.axhline(y=max_val, color='red', linestyle='--', linewidth=1.5, 
                  alpha=0.5, label=f'Melhor: {max_val:.4f}')
    
    plt.tight_layout()
    
    # Salvar figura
    os.makedirs(REPORTS_PATH, exist_ok=True)
    output_path = os.path.join(REPORTS_PATH, 'comparison_models.png')
    # Garantir que estamos no diretório correto
    original_dir = os.getcwd()
    os.chdir(BASE_DIR)
    try:
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\n✅ Gráfico salvo em: {os.path.abspath(output_path)}")
    finally:
        os.chdir(original_dir)
    
    plt.close()
    
    # Imprimir resumo
    print("\n" + "="*60)
    print("RESUMO COMPARATIVO")
    print("="*60)
    print(f"{'Modelo':<20} {'Acurácia':<12} {'Precisão':<12} {'Revocação':<12} {'F1-Score':<12}")
    print("-" * 60)
    for model in models:
        m = results[model]['metrics']
        print(f"{model:<20} {m['accuracy']:<12.4f} {m['precision']:<12.4f} "
              f"{m['recall']:<12.4f} {m['f1_score']:<12.4f}")
    print("="*60)

def main():
    """
    Função principal: treina todos os modelos e gera o gráfico de comparação.
    """
    # Treinar todos os modelos
    results, y_test = train_all_models()
    
    # Gerar gráfico
    plot_comparison(results, y_test)
    
    print("\n✅ Processo concluído com sucesso!")

if __name__ == "__main__":
    main()

