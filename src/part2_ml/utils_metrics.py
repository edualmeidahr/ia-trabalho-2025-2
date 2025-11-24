"""
Módulo de utilitários para cálculo e visualização de métricas de classificação
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score,
    classification_report,
    confusion_matrix
)

#Caminhos 
PROCESSED_PATH = 'data/processed/'
REPORTS_PATH = 'reports'


def load_data():
    """
    Carrega os dados processados do diretório data/processed/
    
    Returns:
        X_train: Array de features de treino
        X_test: Array de features de teste
        y_train: Array de target de treino
        y_test: Array de target de teste
    """
    
    print("Carregando dados processados...")
    X_train = np.load(os.path.join(PROCESSED_PATH, 'X_train.npy')) # features de treino
    X_test = np.load(os.path.join(PROCESSED_PATH, 'X_test.npy')) # features de teste
    y_train = np.load(os.path.join(PROCESSED_PATH, 'y_train.npy')) # target de treino
    y_test = np.load(os.path.join(PROCESSED_PATH, 'y_test.npy')) # target de teste
    
    return X_train, X_test, y_train, y_test
def calculate_all_metrics(y_true, y_pred):
    """
    Calcula todas as métricas principais de classificação
    
    Args:
        y_true: Valores reais (ground truth)
        y_pred: Valores previstos pelo modelo
        
    Returns:
        dict: Dicionário com todas as métricas calculadas
    """
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, average='weighted'),
        'recall': recall_score(y_true, y_pred, average='weighted'),
        'f1_score': f1_score(y_true, y_pred, average='weighted')
    }
    
    # Métricas por classe (para problemas binários)
    if len(np.unique(y_true)) == 2:
        metrics['precision_class_0'] = precision_score(y_true, y_pred, pos_label=0, zero_division=0)
        metrics['recall_class_0'] = recall_score(y_true, y_pred, pos_label=0, zero_division=0)
        metrics['f1_class_0'] = f1_score(y_true, y_pred, pos_label=0, zero_division=0)
        metrics['precision_class_1'] = precision_score(y_true, y_pred, pos_label=1, zero_division=0)
        metrics['recall_class_1'] = recall_score(y_true, y_pred, pos_label=1, zero_division=0)
        metrics['f1_class_1'] = f1_score(y_true, y_pred, pos_label=1, zero_division=0)
    
    return metrics


def print_metrics_summary(y_true, y_pred, model_name, labels=[0, 1], target_names=['<=50k', '>50k']):
    """
    Imprime um resumo formatado das métricas de classificação
    
    Args:
        y_true: Valores reais
        y_pred: Valores previstos
        model_name: Nome do modelo para exibição
        labels: Lista de labels das classes
        target_names: Nomes amigáveis das classes
    """
    # Mapear nomes simples para nomes amigáveis
    name_mapping = {
        'knn': 'KNN',
        'svm': 'SVM',
        'tree': 'ÁRVORE DE DECISÃO'
    }
    display_name = name_mapping.get(model_name.lower(), model_name.upper())
    
    print("\n" + "="*50)
    print(f"RESULTADOS {display_name}")
    print("="*50)
    
    # Acurácia
    acc = accuracy_score(y_true, y_pred)
    print(f"Acurácia: {acc:.4f}\n")
    
    # Classification Report
    print("Classification Report:")
    print(classification_report(y_true, y_pred, labels=labels, target_names=target_names))
    
    # Métricas adicionais
    metrics = calculate_all_metrics(y_true, y_pred)
    print(f"Precisão (weighted): {metrics['precision']:.4f}")
    print(f"Recall (weighted): {metrics['recall']:.4f}")
    print(f"F1-Score (weighted): {metrics['f1_score']:.4f}")


def plot_confusion_matrix(y_true, y_pred, model_name, save_path, 
                          labels=[0, 1], target_names=['<=50k', '>50k'], 
                          cmap='Blues'):
    """
    Cria e salva uma visualização da matriz de confusão
    
    Args:
        y_true: Valores reais
        y_pred: Valores previstos
        model_name: Nome do modelo para o título
        save_path: Caminho completo para salvar a figura
        labels: Lista de labels das classes
        target_names: Nomes amigáveis das classes
        cmap: Mapa de cores para o heatmap
    """
    # Mapear nomes simples para nomes amigáveis
    name_mapping = {
        'knn': 'KNN',
        'svm': 'SVM',
        'tree': 'Árvore de Decisão'
    }
    display_name = name_mapping.get(model_name.lower(), model_name)
    
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap=cmap,
                xticklabels=target_names, 
                yticklabels=target_names,
                cbar_kws={'label': 'Quantidade'})
    plt.title(f'Matriz de Confusão - {display_name}', fontsize=14, fontweight='bold')
    plt.ylabel('Valor Real', fontsize=12)
    plt.xlabel('Valor Previsto', fontsize=12)
    plt.tight_layout()
    
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f'Matriz de confusão salva em: {save_path}')
    plt.close()


def evaluate_model(y_true, y_pred, model_name, save_dir='reports/figs',
                   labels=[0, 1], target_names=['<=50k', '>50k'],
                   cmap='Blues'):
    """
    Função completa para avaliar um modelo: calcula métricas, imprime resumo
    e salva matriz de confusão
    
    Args:
        y_true: Valores reais
        y_pred: Valores previstos
        model_name: Nome do modelo
        save_dir: Diretório para salvar a matriz de confusão
        labels: Lista de labels das classes
        target_names: Nomes amigáveis das classes
        cmap: Mapa de cores para o heatmap
        
    Returns:
        dict: Dicionário com todas as métricas calculadas
    """
    import os
    
    # Garantir que o diretório existe
    os.makedirs(save_dir, exist_ok=True)
    
    # Imprimir resumo das métricas
    print_metrics_summary(y_true, y_pred, model_name, labels, target_names)
    
    # Criar e salvar matriz de confusão
    save_path = os.path.join(save_dir, f'confusion_matrix_{model_name.lower().replace(" ", "_")}.png')
    plot_confusion_matrix(y_true, y_pred, model_name, save_path, labels, target_names, cmap)
    
    # Retornar métricas calculadas
    return calculate_all_metrics(y_true, y_pred)


def compare_models_metrics(models_results):
    """
    Compara métricas de múltiplos modelos e retorna um resumo
    
    Args:
        models_results: Dicionário no formato {model_name: {'y_true': ..., 'y_pred': ...}}
        
    Returns:
        pandas.DataFrame: DataFrame com métricas comparativas
    """
    import pandas as pd
    
    comparison = []
    
    for model_name, results in models_results.items():
        metrics = calculate_all_metrics(results['y_true'], results['y_pred'])
        metrics['model'] = model_name
        comparison.append(metrics)
    
    df = pd.DataFrame(comparison)
    df = df.set_index('model')
    
    return df

