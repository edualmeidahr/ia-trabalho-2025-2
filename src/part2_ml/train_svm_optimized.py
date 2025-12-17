"""
Script para treinar SVM com otimização de hiperparâmetros via Grid Search.
Compara SVM otimizado com SVM padrão e Árvore de Decisão.
"""

import numpy as np
import os
import time
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from utils_metrics import evaluate_model, load_data

# Caminhos
PROCESSED_PATH = 'data/processed/'
REPORTS_PATH = 'reports'


def train_svm_optimized():
    """
    Treina SVM com Grid Search para otimizar hiperparâmetros.
    """
    X_train, X_test, y_train, y_test = load_data()
    
    print("="*60)
    print("OTIMIZAÇÃO DE HIPERPARÂMETROS - SVM")
    print("="*60)
    
    # 1. Treina SVM padrão (para comparação)
    print("\n1. Treinando SVM com parâmetros padrão...")
    start_time = time.time()
    
    svm_padrao = SVC(kernel='rbf', C=1, gamma='scale', random_state=42)
    svm_padrao.fit(X_train, y_train)
    y_pred_padrao = svm_padrao.predict(X_test)
    
    tempo_padrao = time.time() - start_time
    
    print(f"   Tempo de treinamento: {tempo_padrao:.2f} segundos")
    
    # 2. Grid Search para otimização
    print("\n2. Executando Grid Search (isso pode demorar alguns minutos)...")
    print("   Testando combinações de C, gamma e class_weight...")
    
    start_time = time.time()
    
    # Define espaço de busca de hiperparâmetros
    param_grid = {
        'C': [0.1, 1, 10, 100],
        'gamma': ['scale', 'auto', 0.001, 0.01, 0.1],
        'class_weight': [None, 'balanced']
    }
    
    # Grid Search com validação cruzada (5 folds)
    svm_base = SVC(kernel='rbf', random_state=42)
    grid_search = GridSearchCV(
        svm_base,
        param_grid,
        cv=5,                    # 5-fold cross-validation
        scoring='accuracy',       # Métrica de avaliação
        n_jobs=-1,               # Usa todos os núcleos
        verbose=1                # Mostra progresso
    )
    
    # Executa Grid Search
    grid_search.fit(X_train, y_train)
    
    tempo_grid = time.time() - start_time
    
    print(f"\n   Tempo de Grid Search: {tempo_grid:.2f} segundos")
    print(f"   Melhores parâmetros encontrados:")
    print(f"     C: {grid_search.best_params_['C']}")
    print(f"     gamma: {grid_search.best_params_['gamma']}")
    print(f"     class_weight: {grid_search.best_params_['class_weight']}")
    print(f"   Melhor score (CV): {grid_search.best_score_:.4f}")
    
    # 3. Treina modelo otimizado
    print("\n3. Treinando SVM com parâmetros otimizados...")
    svm_otimizado = grid_search.best_estimator_
    y_pred_otimizado = svm_otimizado.predict(X_test)
    
    # 4. Avaliação comparativa
    print("\n" + "="*60)
    print("COMPARAÇÃO DE RESULTADOS")
    print("="*60)
    
    # SVM Padrão
    print("\n--- SVM Padrão (C=1, gamma='scale', class_weight=None) ---")
    metrics_padrao = evaluate_model(
        y_test,
        y_pred_padrao,
        model_name="SVM Padrão",
        save_dir=f'{REPORTS_PATH}/figs',
        cmap='Greens'
    )
    
    # SVM Otimizado
    print("\n--- SVM Otimizado (Grid Search) ---")
    metrics_otimizado = evaluate_model(
        y_test,
        y_pred_otimizado,
        model_name="SVM Otimizado",
        save_dir=f'{REPORTS_PATH}/figs',
        cmap='Blues'
    )
    
    # 5. Resumo Comparativo
    print("\n" + "="*60)
    print("RESUMO COMPARATIVO")
    print("="*60)
    print(f"{'Métrica':<25} {'SVM Padrão':<15} {'SVM Otimizado':<15} {'Melhoria':<15}")
    print("-" * 60)
    
    melhorias = {}
    for metrica in ['accuracy', 'precision', 'recall', 'f1_score']:
        valor_padrao = metrics_padrao[metrica]
        valor_otimizado = metrics_otimizado[metrica]
        melhoria = valor_otimizado - valor_padrao
        melhorias[metrica] = melhoria
        
        sinal = "+" if melhoria >= 0 else ""
        print(f"{metrica.capitalize():<25} {valor_padrao:<15.4f} {valor_otimizado:<15.4f} {sinal}{melhoria:<14.4f}")
    
    print("="*60)
    
    # 6. Análise de Melhoria
    melhoria_acc = melhorias['accuracy']
    if melhoria_acc > 0:
        print(f"\n✅ SVM Otimizado melhorou a acurácia em {melhoria_acc*100:.2f} pontos percentuais")
        print(f"   Melhorias em outras métricas:")
        for metrica, valor in melhorias.items():
            if metrica != 'accuracy' and valor > 0:
                print(f"     - {metrica}: +{valor:.4f}")
    else:
        print(f"\n⚠️  SVM Otimizado não melhorou significativamente")
        print(f"   Diferença de acurácia: {melhoria_acc*100:.2f} pontos percentuais")
    
    # 7. Informações sobre Grid Search
    print(f"\n--- Informações do Grid Search ---")
    print(f"Total de combinações testadas: {len(grid_search.cv_results_['params'])}")
    print(f"Tempo total: {tempo_grid:.2f} segundos")
    print(f"Tempo médio por combinação: {tempo_grid/len(grid_search.cv_results_['params']):.2f} segundos")
    
    # Top 5 melhores combinações
    print(f"\nTop 5 melhores combinações de hiperparâmetros:")
    resultados = list(zip(
        grid_search.cv_results_['params'],
        grid_search.cv_results_['mean_test_score']
    ))
    resultados.sort(key=lambda x: x[1], reverse=True)
    
    for i, (params, score) in enumerate(resultados[:5], 1):
        print(f"  {i}. Score: {score:.4f} | C={params['C']}, gamma={params['gamma']}, "
              f"class_weight={params['class_weight']}")
    
    return svm_otimizado, metrics_otimizado, grid_search


if __name__ == "__main__":
    train_svm_optimized()

