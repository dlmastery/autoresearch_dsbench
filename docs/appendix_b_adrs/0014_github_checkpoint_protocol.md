# ADR-0014: GitHub checkpoint cadence + Windows SSL workaround

## Status

Accepted (2026-05-15). Lessons 14, 15, 21, 24 in `framework/CLAUDE_template.md`.

## Context

The reference machine (Intel 14th-gen HX laptop) crashes intermittently due to E-core parity errors (see `framework/CLAUDE_template.md` § "Hardware Constraints"). Every minute of un-checkpointed work is lost work. A foreground Claude Code session ALSO needs a remote backup — local checkpoints survive process crashes, but not disk failures.

GitHub is the chosen remote backup. Three operational gotchas:

1. **Windows + corporate / OpenVPN environments** sometimes break `git push` with an `unable to access ... SSL certificate problem: unable to get local issuer certificate` error. The fix is to switch git's TLS backend to schannel (Windows native TLS) instead of OpenSSL.
2. **Initial push is large.** After excluding `.data_cache/`, `__pycache__/`, and stdout logs via `.gitignore`, the repo is ~156 MB across 24k files. Initial push takes 2-5 minutes; follow-up pushes are fast.
3. **The status-counting asymmetry** between `final_rollup.json` (no `kind` field — modeling-vs-analysis is `problem_type != "qa_excel"`) and `forensic_summary.json` (has `kind` field). Scripts that read both must account for the asymmetry; otherwise the BEAT-DSBENCH / FORENSIC-PASS counts silently miscount.

## Decision

**Five-part GitHub checkpoint protocol:**

1. **Repo identity.** `https://github.com/dlmastery/autoresearch_dsbench`. Created via `gh repo create dlmastery/autoresearch_dsbench --source . --public`. Branch: `main`. No long-running feature branches in the single-operator workflow.

2. **Windows SSL workaround.** Once per machine:

   ```powershell
   git config --global http.sslBackend schannel
   ```

3. **Commit cadence.** Every batch that changes experiment state (hill-climb run, audit refresh, dashboard regeneration) ends with:

   ```powershell
   git add -A
   git commit -F .commit_msg.txt   # heredocs are flaky in PowerShell — write to file
   git push origin main
   ```

   The commit message follows the autoresearch convention: subject ≤ 70 chars, bullet body, `Co-Authored-By: Claude` trailer.

4. **`.gitignore` discipline.** Exclude `.data_cache/` (regenerable npz), `__pycache__/`, `registry/run_all*_stdout.log`, `*.pkl` (over 100 MB cumulative), and `.commit_msg.txt`. Include `.npy`/`.npz` only when they are part of the audit (split_manifest hashes refer to them; the manifest stays in git).

5. **Canonical status snapshot.** `framework/_status.py` is the one-command "how do I see how things are going" tool. It reads `registry/final_rollup.json` + `registry/forensic_summary.json`, accounts for the `kind` vs `problem_type` asymmetry, prints BEAT-DSBENCH / FORENSIC-PASS / FORENSIC-FAIL by kind and total.

   ```python
   # Read with care: rollup rows don't carry `kind`; forensic rows do.
   def is_mod(r):  # rollup row
       return r.get('problem_type') != 'qa_excel'
   def is_mod_f(f):  # forensic row
       return f.get('kind') == 'modeling'
   ```

## Consequences

**Easier:**

- Every commit is a full project state snapshot; recovery from a laptop crash is `git clone`.
- The status-counting script is one command — no manual cross-referencing of two JSON files.
- New machines come online with `git config http.sslBackend schannel` + clone; no further setup.

**Harder:**

- The commit cadence is manual — there is no auto-commit hook. A long hill-climb run that crashes without a commit loses the in-flight experiments. Mitigated by the per-experiment local checkpoint in `memory/project_autoresearch_checkpoint.md`.
- The `kind` vs `problem_type` asymmetry must be remembered by every new script that touches both rollups. Mitigated by the canonical `_status.py` pattern.

**Riskier:**

- `gh` CLI auth can expire silently. The fix is `gh auth login` — but a forgotten auth means a session of work doesn't push. Run `gh auth status` at session start.

## Related

- Skills `crash-recovery-checkpoint`, `mlops-documentation`.
- `framework/CLAUDE_template.md` § "Crash-Recovery Checkpointing".
- `framework/_status.py` and `framework/_final_audit.py`.
- [`../part_4_tools/23_continuous_integration.md`](../part_4_tools/23_continuous_integration.md).
