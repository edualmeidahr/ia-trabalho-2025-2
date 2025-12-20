# Variáveis
PYTHON = python3
SRC_DIR = src

.PHONY: all install preprocess part1 part2 part3 part4 clean

all: part1 part2 part3 part4

# Instalação das dependências
install:
	pip install -r requirements.txt

# Pré-processamento dos dados (Necessário para a Parte 2)
preprocess:
	$(PYTHON) $(SRC_DIR)/part2_ml/preprocess.py

# --- Execução das Partes ---

# Parte 1: Árvore de Decisão Manual
part1:
	$(PYTHON) $(SRC_DIR)/part1_tree_manual/tree_manual.py

# Parte 2: Machine Learning (Preprocessamento -> KNN -> SVM -> SVM Otimizado -> Tree)
part2: preprocess
	$(PYTHON) $(SRC_DIR)/part2_ml/train_knn.py
	$(PYTHON) $(SRC_DIR)/part2_ml/train_svm.py
	$(PYTHON) $(SRC_DIR)/part2_ml/train_tree.py

# Parte 3: Algoritmos Genéticos
part3:
	$(PYTHON) $(SRC_DIR)/part3_ga/export_db.py
	$(PYTHON) $(SRC_DIR)/part3_ga/run_ga.py --materia Física --topico Cinemática --gens 100 --pop 100

# Parte 4: Inteligência de Enxame (ACO) e Imunológico (CLONALG)
part4:
	@echo "Executando Otimização por Colônia de Formigas (ACO)..."
	$(PYTHON) $(SRC_DIR)/part4_swarm_immune/run_aco.py --materia Física --topico Cinemática --iters 50 --ants 20
	@echo "Executando Algoritmo de Seleção Clonal (CLONALG)..."
	$(PYTHON) $(SRC_DIR)/part4_swarm_immune/run_clonalg.py --materia Física --topico Cinemática --iters 50 --pop 50

# Limpeza de arquivos temporários e processados
clean:
	rm -rf __pycache__ .venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -f data/processed/*.npy data/processed/*.csv
	rm -f reports/figs/*.png