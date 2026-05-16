# Issue Template

> Copy this template into a new issue. Pick the section and delete the rest.

## Bug report

```markdown
### What happened
<One paragraph. Exact error messages in code fences.>

### What you expected
<Documented behaviour. Cite file/line if applicable.>

### How to reproduce
1. `cd C:/Users/evija/dsbench`
2. `& "C:/Users/evija/anaconda3/python.exe" framework/runner.py --repo ... --backbone ...`
3. <observed result>

### Environment
- Python: <`python --version`>
- OS: <Windows 11 / Linux / macOS>
- Git commit: <`git rev-parse HEAD`>

### Artefacts attached
- `experiment_log.jsonl` tail (last 5 lines):
```jsonl
<paste>
```
- `forensic_audit.md` excerpt if relevant.

### Hypothesised root cause
<If you have one. Otherwise "unknown".>

### Severity
- [ ] Critical (test-set leakage)
- [ ] High (numbers off by > 0.05)
- [ ] Medium (numbers off by 0.005-0.05, OR audit false-positive)
- [ ] Low (operational friction)
```

## Feature / capability request

```markdown
### Motivation
<Why this matters. Cite the postmortem / ADR / paper.>

### Proposed change
<One paragraph "what". Specific file + function + behaviour.>

### Alternatives considered
<At least one alternative. State why it's worse.>

### Acceptance criteria
- [ ] New capability covered by unit test
- [ ] ADR added (if protocol-changing)
- [ ] Skill added or extended
- [ ] 4-layer audit gate green
- [ ] Documentation updated

### Related
- ADR(s): #
- Postmortem(s): #
```

## Protocol question

```markdown
### Context
<What you're trying to do.>

### What the docs say
<Quote the relevant doc / CLAUDE.md / skill text.>

### What's unclear
<Specifically: which clause is ambiguous?>

### Suggested fix
<If you have one.>
```

## Documentation issue

```markdown
### Page
<URL or path: `docs/architecture/04_hill_climb.md` §5.>

### Issue
- [ ] Outdated information
- [ ] Broken link
- [ ] Missing diagram
- [ ] Typo / unclear sentence
- [ ] Wrong code example

### Proposed fix
<Or describe the gap.>
```

## Tips

- **Include reproducer commands.** Bug reports without reproducers take 10× longer.
- **One bug per issue.**
- **Link related issues** via `#NNN`.

## Related

- [`CONTRIBUTING.md`](CONTRIBUTING.md)
- [`pr_template.md`](pr_template.md)
- [`../appendix_a_postmortems/`](../appendix_a_postmortems/)
