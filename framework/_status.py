import json
data = json.load(open('C:/Users/evija/dsbench/registry/final_rollup.json'))
forensic = json.load(open('C:/Users/evija/dsbench/registry/forensic_summary.json'))

def is_mod(r):
    return r.get('problem_type') != 'qa_excel'

mod_beat = sum(1 for r in data if is_mod(r) and r.get('beats_dsbench'))
ana_beat = sum(1 for r in data if not is_mod(r) and r.get('beats_dsbench'))
mod_pass = sum(1 for f in forensic if f.get('kind') == 'modeling' and f.get('verdict') == 'PASS')
ana_pass = sum(1 for f in forensic if f.get('kind') == 'analysis' and f.get('verdict') == 'PASS')
mod_fail = sum(1 for f in forensic if f.get('kind') == 'modeling' and f.get('verdict') == 'FAIL')
print(f'BEAT-DSBENCH:   modeling={mod_beat}/74  analysis={ana_beat}/38  total={mod_beat+ana_beat}/112')
print(f'FORENSIC PASS:  modeling={mod_pass}/74  analysis={ana_pass}/38  total={mod_pass+ana_pass}/112')
print(f'FORENSIC FAIL:  modeling={mod_fail}/74')
print()
print('=== modeling FORENSIC FAILS ===')
for f in forensic:
    if f.get('kind') == 'modeling' and f.get('verdict') == 'FAIL':
        warns = f.get('warnings', [])
        print(f'  {f["task"][:55]:55s} {warns}')
