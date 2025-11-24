import numpy as np
import os 
from sklearn.tree import DecisionTreeClassifier
from utils_metrics import evaluate_model, load_data

#Caminhos 
PROCESSED_PATH = 'data/processed/'
REPORTS_PATH = 'reports'


def train_tree():
    X_train, X_test, y_train, y_test = load_data()
    
    # Configuração da Árvore de Decisão
    print("Treinando Árvore de Decisão...")
    
    # max_depth controla a profundidade máxima da árvore (evita overfitting)
    # min_samples_split: número mínimo de amostras necessárias para dividir um nó
    # random_state para reprodutibilidade
    model = DecisionTreeClassifier(
        max_depth=10, 
        min_samples_split=20, 
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # Predição
    print("Realizando as predições...")
    y_pred = model.predict(X_test)
    
    # Avaliação completa usando utils_metrics
    metrics = evaluate_model(
        y_test, 
        y_pred, 
        model_name="tree",
        save_dir=f'{REPORTS_PATH}/figs',
        cmap='Oranges'
    )
    
    return model, metrics
    
if __name__ == "__main__":
    train_tree()

