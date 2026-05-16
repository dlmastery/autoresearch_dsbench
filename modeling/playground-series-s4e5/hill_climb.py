import sys
from pathlib import Path
ROOT = Path(__file__).resolve()
sys.path.insert(0, str(ROOT.parents[2]))
from framework.hill_climb import main

if __name__ == '__main__':
    if '--repo' not in sys.argv:
        sys.argv += ['--repo', str(Path(__file__).resolve().parent)]
    main()
