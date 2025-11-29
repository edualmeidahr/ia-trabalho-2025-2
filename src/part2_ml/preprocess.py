import pandas as pd 
import numpy as np
import os 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

RAW_PATH = 'data/raw/adult.data'
PROCESSED_PATH = 'data/processed/'

COLUMNS = [
    'age', 'workclass', 'fnlwgt', 'education', 'education-num', 
    'marital-status', 'occupation', 'relationship', 'race', 'sex', 
    'capital-gain', 'capital-loss', 'hours-per-week', 'native-country', 'income'
] 


def load_and_clean_data():
    print("Loading data...")
    
    df = pd.read_csv(RAW_PATH, names=COLUMNS,sep=',\s' ,na_values='?', engine='python')
    
    print("Initial data shape:", df.shape)
    
    # Tratamento de Nulos
    missing_before = df.isnull().sum().sum()
    df.dropna(inplace=True)
    print(f"Linhas com nulos removidas: {missing_before} dados faltantes tratados.")
    print("Data shape after dropping NAs:", df.shape)
    
    # Codificação da Variável Alvo (Target)
    # Normaliza espaços e case para garantir que capture todas as variações
    df['income'] = df['income'].str.strip().str.lower()
    df['income'] = df['income'].apply(lambda x: 1 if '>50k' in x or '>50' in x else 0)
    
    # Verificar distribuição das classes
    print(f"\nDistribuição da variável alvo:")
    print(df['income'].value_counts())
    print(f"Proporção: {df['income'].mean():.4f} para classe 1 (>50k)")
    
    return df


def preprocess_data():
    if not os.path.exists(PROCESSED_PATH):
        os.makedirs(PROCESSED_PATH)
        
    df = load_and_clean_data()
    
    # Separação entre featues (X) e target (Y)
    X = df.drop('income', axis=1)
    y = df['income']
    
    
    #One-hot encoding para variáveis categóricas
    #Seleciona colunas que são texto 
    categorical_cols = X.select_dtypes(include=['object']).columns
    
    # get_dummies tranforma texto em números binários (0 e 1)
    X = pd.get_dummies(X, columns=categorical_cols, drop_first=True)
    
    #Divisão entre treino e teste 
    #O stratify garante que a proporção das classes na variável alvo seja mantida em ambos os conjuntos
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, stratify=y, random_state=42
    )
    
    # Escalonamento dos dados 
    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    # Usa transform() no teste para manter consistência com o scaler treinado
    X_test_scaled = scaler.transform(X_test)
    
    # Converter y para numpy array
    y_train = y_train.values
    y_test = y_test.values
    
    # Salvando os dados processados
    np.save(os.path.join(PROCESSED_PATH, 'X_train.npy'), X_train_scaled)
    np.save(os.path.join(PROCESSED_PATH, 'X_test.npy'), X_test_scaled)
    np.save(os.path.join(PROCESSED_PATH, 'y_train.npy'), y_train)
    np.save(os.path.join(PROCESSED_PATH, 'y_test.npy'), y_test)
    
    # Salvando nome das colunas 
    np.save(os.path.join(PROCESSED_PATH, 'feature,names.npy'), X.columns.values)

    print("Pré-processamento conluído")
    
    
if __name__ == "__main__":
    preprocess_data()    
    