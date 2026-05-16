import json
data = json.load(open('C:/Users/evija/dsbench/registry/forensic_summary.json'))
final = json.load(open('C:/Users/evija/dsbench/registry/final_rollup.json'))
final_map = {r['task']: r for r in final}
passes = [r for r in data if r['verdict'] == 'PASS']
fails = [r for r in data if r['verdict'] == 'FAIL']
print(f'PASS: {len(passes)} FAIL: {len(fails)}')
print()
print('=== FORENSIC FAILS (sample) ===')
for r in fails[:20]:
    delta = final_map.get(r['task'], {}).get('delta_vs_dsbench', 0)
    print(f'  {r["task"][:50]:50s} {r["kind"]:10s} dsb_delta={delta:+.4f} warnings={len(r["warnings"])}')
print()
print('=== STILL-LOSING TASKS ===')
still_losing = [r for r in final if not r.get('beats_dsbench')]
print(f'Total: {len(still_losing)}')
mod_losing = [r for r in still_losing if r.get('problem_type') != 'qa_excel']
ana_losing = [r for r in still_losing if r.get('problem_type') == 'qa_excel']
print(f'Modeling losses: {len(mod_losing)}  Analysis losses: {len(ana_losing)}')
for r in mod_losing[:15]:
    print(f'  MOD: {r["task"][:55]:55s} {r["problem_type"]:25s} test={r["test_score"]:.4f} delta={r["delta_vs_dsbench"]:+.4f}')
