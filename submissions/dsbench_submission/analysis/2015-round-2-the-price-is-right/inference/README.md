# Inference for 2015-round-2-the-price-is-right

Run `python predict.py` to reproduce val-set predictions from the
champion config. Synthetic data is regenerated deterministically;
replace `framework/runner.py:load_or_make_data` with a real-data
adapter for live deployment.
