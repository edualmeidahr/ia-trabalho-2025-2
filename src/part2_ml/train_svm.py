import numpy as np 
import os 
from sklearn.svm import SVC
from utils_metrics import evaluate_model, load_data

#Caminhos 
PROCESSED_PATH = 'data/processed/'
REPORTS_PATH = 'reports'


def train_svm():
    X_train, X_test, y_train, y_test = load_data()
    
    # Configuração do SVM
    print("Treinando SVM...")
    
    # SVM com kernel RBF (Radial Basis Function) - é bom para dados não lineares
    # C=1 é o parâmetro de regularização padrão
    # gamma='scale' ajusta automaticamente o parâmetro gamma
    model = SVC(kernel='rbf', C=1, gamma='scale', random_state=42)
    model.fit(X_train, y_train)
    
    # Predição
    print("Realizando as predições...")
    y_pred = model.predict(X_test)
    
    # Avaliação completa usando utils_metrics
    metrics = evaluate_model(
        y_test, 
        y_pred, 
        model_name="svm",
        save_dir=f'{REPORTS_PATH}/figs',
        cmap='Greens'
    )
    
    return model, metrics
    
if __name__ == "__main__":
    train_svm()
