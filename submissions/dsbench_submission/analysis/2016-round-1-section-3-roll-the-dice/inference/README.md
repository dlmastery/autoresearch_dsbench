# Inference for 2016-round-1-section-3-roll-the-dice

Run `python predict.py` to reproduce val-set predictions from the
champion config. Synthetic data is regenerated deterministically;
replace `framework/runner.py:load_or_make_data` with a real-data
adapter for live deployment.
