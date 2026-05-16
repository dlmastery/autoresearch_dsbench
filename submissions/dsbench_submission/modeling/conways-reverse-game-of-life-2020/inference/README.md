# Inference for conways-reverse-game-of-life-2020

Run `python predict.py` to reproduce val-set predictions from the
champion config. Synthetic data is regenerated deterministically;
replace `framework/runner.py:load_or_make_data` with a real-data
adapter for live deployment.
