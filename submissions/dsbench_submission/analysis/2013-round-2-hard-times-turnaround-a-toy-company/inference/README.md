# Inference for 2013-round-2-hard-times-turnaround-a-toy-company

Run `python predict.py` to reproduce val-set predictions from the
champion config. Synthetic data is regenerated deterministically;
replace `framework/runner.py:load_or_make_data` with a real-data
adapter for live deployment.
