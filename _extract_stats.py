"""Extract precise stats from the dsbench registries for the paper."""
import json, collections

ROLLUP = r"C:/Users/evija/dsbench/registry/final_rollup.json"
FORENSIC = r"C:/Users/evija/dsbench/registry/forensic_summary.json"
ANAL_TASKS = r"C:/Users/evija/dsbench/registry/analysis_tasks.json"
MOD_TASKS = r"C:/Users/evija/dsbench/registry/modeling_tasks.json"

with open(ROLLUP, "r", encoding="utf-8") as f: roll = json.load(f)
with open(FORENSIC, "r", encoding="utf-8") as f: forensic = json.load(f)
with open(ANAL_TASKS, "r", encoding="utf-8") as f: anal_tasks = json.load(f)
with open(MOD_TASKS, "r", encoding="utf-8") as f: mod_tasks = json.load(f)

# Identify which tasks are modeling vs analysis from forensic kind
kinds = {e["task"]: e["kind"] for e in forensic}
print("total tasks (roll):", len(roll))
print("total tasks (forensic):", len(forensic))
print("kinds histogram:", collections.Counter(kinds.values()))

# Beat rate by kind
beat_count = {"modeling": 0, "analysis": 0}
total_count = {"modeling": 0, "analysis": 0}
beat_by_problem = collections.defaultdict(lambda: [0, 0])  # [beat, total]
champ_backbone_modeling = collections.Counter()
champ_backbone_analysis = collections.Counter()
top_deltas = []
all_deltas = []
for e in roll:
    k = kinds.get(e["task"], "?")
    total_count[k] = total_count.get(k, 0) + 1
    pt = e.get("problem_type", "?")
    beat_by_problem[(k, pt)][1] += 1
    if e["beats_dsbench"]:
        beat_count[k] += 1
        beat_by_problem[(k, pt)][0] += 1
    if k == "modeling":
        champ_backbone_modeling[e["champion_backbone"]] += 1
    elif k == "analysis":
        champ_backbone_analysis[e["champion_backbone"]] += 1
    top_deltas.append((e["task"], k, e["problem_type"], e.get("champion_backbone"),
                       e["test_score"], e["dsbench_baseline"], e["delta_vs_dsbench"],
                       e["beats_dsbench"]))
    all_deltas.append(e["delta_vs_dsbench"])

print("\n=== Beat-rate by kind ===")
for k in ["modeling", "analysis"]:
    print(f"  {k}: {beat_count[k]}/{total_count[k]}")

print("\n=== Beat-rate by (kind, problem_type) ===")
for (k, pt), (b, t) in sorted(beat_by_problem.items()):
    print(f"  {k:>10s} / {pt:>20s} : {b}/{t}")

print("\n=== Champion backbones — MODELING (74) ===")
for bb, c in champ_backbone_modeling.most_common():
    print(f"  {bb}: {c}")

print("\n=== Champion backbones — ANALYSIS (38) ===")
for bb, c in champ_backbone_analysis.most_common():
    print(f"  {bb}: {c}")

print("\n=== Forensic verdict histogram ===")
verdict_hist = collections.Counter(e["verdict"] for e in forensic)
print(verdict_hist)

# top 10 by delta among wins
top_deltas.sort(key=lambda x: x[6], reverse=True)
print("\n=== Top 10 wins by delta ===")
for row in top_deltas[:10]:
    print(f"  {row[0]:<48s} | kind={row[1]:<8s} | pt={row[2]:<22s} | bb={row[3]:<14s} | test={row[4]:+.4f} | base={row[5]:+.4f} | delta={row[6]:+.4f}")

# Modeling-only beat-rate
mod_only = [e for e in roll if kinds[e["task"]] == "modeling"]
mod_only_problem = collections.Counter(e["problem_type"] for e in mod_only)
print("\n=== Modeling problem_type distribution ===", dict(mod_only_problem))

# Analysis-only
anal_only = [e for e in roll if kinds[e["task"]] == "analysis"]
print("=== Analysis problem_type distribution ===", collections.Counter(e["problem_type"] for e in anal_only))

# Champion-of-champions in modeling
print("\n=== Top 5 modeling test_score (raw) ===")
m_sorted = sorted(mod_only, key=lambda x: x["delta_vs_dsbench"], reverse=True)
for e in m_sorted[:5]:
    print(f"  {e['task']:<48s} bb={e['champion_backbone']:<14s} test={e['test_score']:+.4f} base={e['dsbench_baseline']:+.4f} delta={e['delta_vs_dsbench']:+.4f}")

# Output the full appendix list as JSON for reuse
appendix = []
forensic_by_task = {e["task"]: e for e in forensic}
for e in roll:
    fe = forensic_by_task.get(e["task"], {})
    appendix.append({
        "task": e["task"],
        "kind": kinds.get(e["task"], "?"),
        "problem_type": e["problem_type"],
        "metric": e["metric"],
        "backbone": e["champion_backbone"],
        "composite": e["champion_composite"],
        "test_score": e["test_score"],
        "dsbench_baseline": e["dsbench_baseline"],
        "delta": e["delta_vs_dsbench"],
        "beats": e["beats_dsbench"],
        "verdict": fe.get("verdict", "?"),
    })
with open(r"C:/Users/evija/dsbench/_appendix_rows.json", "w", encoding="utf-8") as f:
    json.dump(appendix, f, indent=2)
print(f"\nWrote {len(appendix)} appendix rows.")

# How many tasks "obviously" beat by category for the headline
print("\n=== Final tally ===")
print(f"Total: 112 | Beat: {sum(beat_count.values())} | Modeling beat: {beat_count['modeling']} | Analysis beat: {beat_count['analysis']}")
print(f"Forensic PASS: {verdict_hist['PASS']} / 112")
