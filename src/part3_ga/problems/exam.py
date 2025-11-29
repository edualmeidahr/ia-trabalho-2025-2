import random
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Questao:
    """
    Representa uma única questão no banco de dados.
    """
    id: int
    materia: str       
    subtopico: str     
    dificuldade: float 
    tempo: int        

    def __repr__(self):
        return f"Q{self.id:04d}[{self.materia[:3]}-{self.subtopico[:4]}|D:{self.dificuldade}|T:{self.tempo}m]"

class BancoDeQuestoes:
    def __init__(self, tamanho: int = 5000, seed: int = 42):
        self.tamanho = tamanho
        self.seed = seed
        self.questoes = self._gerar_banco_sintetico()

    def _gerar_banco_sintetico(self) -> List[Questao]:
        """
        Gera uma lista de 3000 questões fictícias com atributos complexos.
        """
        random.seed(self.seed)
        
        # Base de conhecimento expandida
        materias_topicos: Dict[str, List[str]] = {
            'Matemática': [
                'Álgebra', 'Geometria Plana', 'Geometria Espacial', 
                'Trigonometria', 'Cálculo', 'Estatística', 'Combinatória'
            ],
            'Física': [
                'Cinemática', 'Dinâmica', 'Termodinâmica', 
                'Óptica', 'Eletromagnetismo', 'Ondulatória', 'Moderna'
            ],
            'Química': [
                'Atomística', 'Físico-Química', 'Orgânica', 
                'Inorgânica', 'Estequiometria', 'Eletroquímica'
            ],
            'Biologia': [
                'Citologia', 'Genética', 'Ecologia', 
                'Fisiologia Humana', 'Botânica', 'Evolução'
            ],
            'História': [
                'Antiga', 'Medieval', 'Brasil Colônia', 
                'Brasil Império', 'Brasil República', 'Moderna', 'Contemporânea'
            ],
            'Geografia': [
                'Física', 'Humana', 'Geopolítica', 
                'Cartografia', 'Ambiental'
            ],
            'Português': [
                'Gramática', 'Literatura Brasileira', 'Interpretação de Texto', 
                'Semântica', 'Redação'
            ],
            'Inglês': [
                'Reading', 'Grammar', 'Vocabulary'
            ]
        }
        
        banco = []
        lista_materias = list(materias_topicos.keys())
        
        for i in range(self.tamanho):
            # 1. Escolha da Matéria e Tópico
            materia_escolhida = random.choice(lista_materias)
            subtopico_escolhido = random.choice(materias_topicos[materia_escolhida])
            
            # 2. Definição de Dificuldade (1.0 a 5.0)
            dificuldade = round(random.uniform(1.0, 5.0), 1)
            
            # 3. Definição de Tempo (com mais variância para dificultar o AG)
            # Regra base: Dificuldade * 3 + aleatoriedade
            tempo_base = int(dificuldade * 3)
            
            # Introduz "Outliers" (questões difíceis mas rápidas, ou fáceis mas longas)
            fator_caos = random.random()
            if fator_caos < 0.05: # 5% de chance de ser uma questão "pegadinha"
                if random.choice([True, False]):
                    tempo_final = tempo_base + random.randint(10, 20) # Muito longa
                else:
                    tempo_final = max(1, tempo_base - random.randint(2, 5)) # Muito rápida
            else:
                # Comportamento padrão
                tempo_final = max(2, tempo_base + random.randint(-2, 4))
            
            q = Questao(
                id=i,
                materia=materia_escolhida,
                subtopico=subtopico_escolhido,
                dificuldade=dificuldade,
                tempo=tempo_final
            )
            banco.append(q)
            
        return banco

    def filtrar(self, materia: str = None, subtopico: str = None) -> List[Questao]:
        """
        Filtra o banco.
        """
        resultado = self.questoes
        if materia:
            resultado = [q for q in resultado if q.materia.lower() == materia.lower()]
        if subtopico:
            resultado = [q for q in resultado if q.subtopico.lower() == subtopico.lower()]
        return resultado