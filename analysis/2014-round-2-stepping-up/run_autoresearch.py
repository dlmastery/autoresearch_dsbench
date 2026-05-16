import os, sys, json
from pathlib import Path
ROOT = Path(__file__).resolve()
sys.path.insert(0, str(ROOT.parents[2]))
from framework.runner import main

if __name__ == '__main__':
    # Inject --repo if not provided so user can call: run_autoresearch.py --backbone xgboost --description ...
    if '--repo' not in sys.argv:
        sys.argv += ['--repo', str(Path(__file__).resolve().parent)]
    main()
