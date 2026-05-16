import json
data = json.load(open('C:/Users/evija/dsbench/registry/final_rollup.json'))
modeling = [r for r in data if r.get('problem_type') != 'qa_excel']
analysis = [r for r in data if r.get('problem_type') == 'qa_excel']
n_mod_beat = sum(1 for r in modeling if r.get('beats_dsbench'))
n_ana_beat = sum(1 for r in analysis if r.get('beats_dsbench'))
print(f'modeling: {n_mod_beat}/{len(modeling)} beat DSBench ({100*n_mod_beat/len(modeling):.1f}%)')
print(f'analysis: {n_ana_beat}/{len(analysis)} beat DSBench ({100*n_ana_beat/len(analysis):.1f}%)')
print()
print('=== TOP 10 BEATS (modeling) ===')
for r in sorted([r for r in modeling if r.get('beats_dsbench')], key=lambda r: -r['delta_vs_dsbench'])[:10]:
    print(f'  {r["task"][:55]:55s} {r["problem_type"]:25s} test={r["test_score"]:.4f} delta=+{r["delta_vs_dsbench"]:.4f}')
print()
print('=== TOP 5 BEATS (analysis) ===')
for r in sorted([r for r in analysis if r.get('beats_dsbench')], key=lambda r: -r['delta_vs_dsbench'])[:5]:
    print(f'  {r["task"][:55]:55s} test={r["test_score"]:.4f} delta=+{r["delta_vs_dsbench"]:.4f}')
print()
print('=== BACKBONE WINS ===')
from collections import Counter
champ_bb = Counter(r.get('champion_backbone', '?') for r in data if r.get('beats_dsbench'))
for bb, n in champ_bb.most_common():
    print(f'  {bb:20s} {n} winning champions')
