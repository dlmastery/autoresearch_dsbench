"""End-to-end cross-check audit after all 4 work streams landed."""
import json
import subprocess
from pathlib import Path

ROOT = Path('C:/Users/evija/dsbench')
report = {'checks': []}

# 1. beat-dsbench scoreboard
data = json.load(open(ROOT / 'registry' / 'final_rollup.json'))
def is_mod(r): return r.get('problem_type') != 'qa_excel'
mod_beat = sum(1 for r in data if is_mod(r) and r.get('beats_dsbench'))
ana_beat = sum(1 for r in data if not is_mod(r) and r.get('beats_dsbench'))
report['checks'].append({'check': 'beat_dsbench',
                          'modeling': f'{mod_beat}/74',
                          'analysis': f'{ana_beat}/38',
                          'total': f'{mod_beat + ana_beat}/112'})

# 2. forensic 112/112 PASS
forensic = json.load(open(ROOT / 'registry' / 'forensic_summary.json'))
n_pass = sum(1 for f in forensic if f.get('verdict') == 'PASS')
n_fail = sum(1 for f in forensic if f.get('verdict') == 'FAIL')
report['checks'].append({'check': 'forensic',
                          'pass': f'{n_pass}/112',
                          'fail': f'{n_fail}/112'})

# 3. skill-pack coverage
sp_audit = ROOT / 'skills' / 'autoresearch-pack' / 'audit' / 'coverage_report.md'
sp_pass = 'PASS' in sp_audit.read_text(encoding='utf-8')[:600] if sp_audit.exists() else False
sp_head = sp_audit.read_text(encoding='utf-8').splitlines()[:3] if sp_audit.exists() else []
report['checks'].append({'check': 'skill_pack_coverage',
                          'pass': sp_pass,
                          'head': sp_head})

# 4. number of SKILL.md files
n_skills = sum(1 for _ in (ROOT / 'skills' / 'autoresearch-pack' / 'skills').iterdir()
                if (_ / 'SKILL.md').exists())
report['checks'].append({'check': 'n_skills', 'count': n_skills})

# 5. validator
val_path = ROOT / 'registry' / 'audit_report.json'
try:
    out = subprocess.run(['C:/Users/evija/anaconda3/python.exe', 'C:/Users/evija/dsbench/framework/validator.py'],
                         capture_output=True, text=True, timeout=120)
    n_ok = out.stdout.count('ok')  # naive
    report['checks'].append({'check': 'validator',
                              'stdout_last': out.stdout.splitlines()[-1] if out.stdout else 'empty'})
except Exception as e:
    report['checks'].append({'check': 'validator', 'error': str(e)})

# 6. Lessons Learned present in every task CLAUDE.md
n_with_lessons = 0
n_total = 0
for root in (ROOT / 'modeling', ROOT / 'analysis'):
    for child in sorted(root.iterdir()):
        cm = child / 'CLAUDE.md'
        if not cm.exists():
            continue
        n_total += 1
        if 'Lessons Learned' in cm.read_text(encoding='utf-8', errors='replace')[:50000]:
            n_with_lessons += 1
report['checks'].append({'check': 'lessons_learned_in_claude',
                          'count': f'{n_with_lessons}/{n_total}'})

# 7. About-dropdown present in every per-task dashboard
n_with_dropdown = 0
n_dash_total = 0
for root in (ROOT / 'modeling', ROOT / 'analysis'):
    for child in sorted(root.iterdir()):
        dh = child / 'autoresearch_results' / 'dashboard.html'
        if not dh.exists():
            continue
        n_dash_total += 1
        body = dh.read_text(encoding='utf-8', errors='replace')
        if 'About this task' in body:
            n_with_dropdown += 1
report['checks'].append({'check': 'about_dropdown_in_dashboard',
                          'count': f'{n_with_dropdown}/{n_dash_total}'})

# 8. md_viewer.html exists in both dashboard/ and submissions/
mv1 = (ROOT / 'dashboard' / 'md_viewer.html').exists()
mv2 = (ROOT / 'submissions' / 'md_viewer.html').exists()
report['checks'].append({'check': 'md_viewer',
                          'dashboard': mv1, 'submissions': mv2})

# 9. md_viewer routes in task_detail.html
td_body = (ROOT / 'dashboard' / 'task_detail.html').read_text(encoding='utf-8', errors='replace')
n_routes_td = td_body.count('md_viewer.html')
report['checks'].append({'check': 'task_detail_md_viewer_routes', 'count': n_routes_td})

# 10. md_viewer routes in dashboard template
tpl_body = (ROOT / 'framework' / 'dashboard_template.html').read_text(encoding='utf-8', errors='replace')
n_routes_tpl = tpl_body.count('md_viewer.html')
report['checks'].append({'check': 'dashboard_template_md_viewer_routes', 'count': n_routes_tpl})

# 11. New forensic agents I + J in submission archives
n_with_ij = 0
n_arch = 0
sub_root = ROOT / 'submissions' / 'dsbench_submission'
if sub_root.exists():
    for root in (sub_root / 'modeling', sub_root / 'analysis'):
        if not root.exists():
            continue
        for child in sorted(root.iterdir()):
            fa = child / 'forensic_audit.md'
            if not fa.exists():
                continue
            n_arch += 1
            body = fa.read_text(encoding='utf-8', errors='replace')
            if 'I_refit_consistency' in body and 'J_backbone_diversity' in body:
                n_with_ij += 1
report['checks'].append({'check': 'submission_forensic_has_I_J',
                          'count': f'{n_with_ij}/{n_arch}'})

print(json.dumps(report, indent=2))
