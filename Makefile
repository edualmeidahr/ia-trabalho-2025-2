.PHONY: setup part1 part2 part3 part4 clean

setup:
	python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt

part1:
	python src/part1_tree_manual/tree_manual.py

part2:
	python src/part2_ml/train_knn.py && \
	python src/part2_ml/train_svm.py && \
	python src/part2_ml/train_tree.py

part3:
	python src/part3_ga/run_ga.py --problem tsp --iters 2000

part4:
	python src/part4_swarm_immune/run_meta.py --algo pso --problem rastrigin

clean:
	rm -rf __pycache__ .pytest_cache data/processed/* reports/figs/*