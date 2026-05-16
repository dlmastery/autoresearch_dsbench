# Inference for 2012-round-2-find-that-error

Run `python predict.py` to reproduce val-set predictions from the
champion config. Synthetic data is regenerated deterministically;
replace `framework/runner.py:load_or_make_data` with a real-data
adapter for live deployment.
