import numpy as np
import os 
from sklearn.neighbors import KNeighborsClassifier
from utils_metrics import evaluate_model, load_data

#Caminhos 
PROCESSED_PATH = 'data/processed/'
REPORTS_PATH = 'reports'


def train_knn():
    X_train, X_test, y_train, y_test = load_data()
    
    # Configuração do KNN
    k = 15
    print(f"Treinando KNN com k={k}...")
    
    # n_jobs=-1 usa todos os núcleos disponíveis 
    model = KNeighborsClassifier(n_neighbors=k, metric='euclidean', n_jobs=-1)
    model.fit(X_train, y_train)
    
    # Predição
    print("Realizando as predições...")
    y_pred = model.predict(X_test)
    
    # Avaliação completa usando utils_metrics
    # Usando nome simples para manter compatibilidade com nomes de arquivo originais
    metrics = evaluate_model(
        y_test, 
        y_pred, 
        model_name="knn",
        save_dir=f'{REPORTS_PATH}/figs',
        cmap='Blues'
    )
    
    return model, metrics
    
if __name__ == "__main__":
    train_knn()