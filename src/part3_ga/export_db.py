import sys
import os
import pandas as pd


sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from src.part3_ga.problems.exam import BancoDeQuestoes

def main():
    print("Gerando banco de questões sintético...")
    
    banco = BancoDeQuestoes(tamanho=5000)
    
    print(f"Banco gerado com {len(banco.questoes)} questões.")
    
    # Converte a lista de objetos Questao para uma lista de dicionários
    data = []
    for q in banco.questoes:
        data.append({
            'ID': q.id,
            'Materia': q.materia,
            'Subtopico': q.subtopico,
            'Dificuldade': q.dificuldade,
            'Tempo_Min': q.tempo
        })
    
    # Cria um DataFrame pandas para facilitar a visualização e exportação
    df = pd.DataFrame(data)
    
    # Define o caminho de saída
    output_path = 'data/processed/banco_questoes.csv'
    
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Salva em CSV
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"Arquivo salvo com sucesso em: {output_path}")
    
    # Mostra uma amostra (head) no terminal para conferência rápida
    print("\n--- Amostra das primeiras 10 questões ---")
    print(df.head(10))
    
    
    print("\n--- Estatísticas por Matéria ---")
    print(df['Materia'].value_counts())
    
    print("\n--- Resumo Numérico (Dificuldade e Tempo) ---")
    print(df[['Dificuldade', 'Tempo_Min']].describe())

if __name__ == "__main__":
    main()