.PHONY: setup part1 part2 part3 part4 clean

setup:
	python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt

part1:
	python3 src/part1_tree_manual/tree_manual.py

part2:
	python3 src/part2_ml/train_knn.py && \
	python3 src/part2_ml/train_svm.py && \
	python3 src/part2_ml/train_tree.py

part3:
	python3 src/part3_ga/export_db.py
	python3 src/part3_ga/run_ga.py --materia Física --topico Cinemática --gens 50 --pop 100

part4:
	python3 src/part4_swarm_immune/run_meta.py --algo pso --problem rastrigin

clean:
	rm -rf __pycache__ .pytest_cache data/processed/* reports/figs/*