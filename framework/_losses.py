import json
data = json.load(open('C:/Users/evija/dsbench/registry/final_rollup.json'))
losses = [r for r in data if not r.get('beats_dsbench')]
mod_losses = [r for r in losses if r.get('problem_type') != 'qa_excel']
ana_losses = [r for r in losses if r.get('problem_type') == 'qa_excel']
print(f'Total losses: {len(losses)}')
print(f'Modeling losses: {len(mod_losses)}')
print(f'Analysis losses: {len(ana_losses)}')
print()
print('=== modeling losses ===')
for r in sorted(mod_losses, key=lambda r: r['delta_vs_dsbench']):
    print(f'  {r["task"][:55]:55s} {r["problem_type"]:25s} test={r["test_score"]:.4f} dsb={r["dsbench_baseline"]:.4f} delta={r["delta_vs_dsbench"]:+.4f}')
print()
print('=== analysis losses (first 10) ===')
for r in sorted(ana_losses, key=lambda r: r['delta_vs_dsbench'])[:10]:
    print(f'  {r["task"][:55]:55s} test={r["test_score"]:.4f} dsb={r["dsbench_baseline"]:.4f} delta={r["delta_vs_dsbench"]:+.4f}')
# write loss list to disk for use by hill-climb-more
with open('C:/Users/evija/dsbench/registry/losses.json', 'w') as f:
    json.dump({'modeling': [r['task'] for r in mod_losses], 'analysis': [r['task'] for r in ana_losses]}, f, indent=2)
