# Pull Request Template

> Copy this template into a new PR description. Replace the sections.

```markdown
## Summary

<One-paragraph "what + why". Imperative voice. Cite the issue / postmortem / ADR that motivated this PR.>

## Type of change

- [ ] Bug fix
- [ ] New feature / capability
- [ ] Protocol change (touches `framework/CLAUDE_template.md` or `SECTION_MAPPING.md`)
- [ ] New ADR
- [ ] New postmortem
- [ ] Documentation only
- [ ] Refactor (no behaviour change)

## Detailed changes

<Bullet list. One bullet per substantive change.>

- `framework/runner.py:_excel_agent` — added new `prior_ensemble` backend per Wolpert 1992 'Stacked Generalization' Neural Networks 5(2).
- `framework/hill_climb.py:_excel_agent_proposals` — added 3 new iters citing the ensemble.
- `framework/CLAUDE_template.md` — Lesson 27 added.

## Audit gate

- [ ] Layer 1 — `framework/validator.py` — 112/112 ok
- [ ] Layer 2 — `framework/forensic_audit.py` — 112/112 PASS
- [ ] Layer 3 — `framework/build_submission.py` — refreshed
- [ ] Layer 4 — `skills/autoresearch-pack/audit/audit_pack.py` — 100%
- [ ] Aggregator — `framework/_final_audit.py` — green

## Test plan

- [ ] Unit tests: `python -m pytest framework/_test_*.py`
- [ ] One-task hill climb on `<slug>` shows expected behaviour
- [ ] Spot-check forensic narrative on `<slug>`
- [ ] Dashboard renders correctly

## Status snapshot

```
BEAT-DSBENCH:   modeling=X/74  analysis=Y/38  total=Z/112
FORENSIC PASS:  modeling=A/74  analysis=B/38  total=C/112
```

## Linked items

- ADR(s): #
- Postmortem(s): #
- Issue(s): #
- Skill(s) added or extended: `skill-name-here`

## Backward compatibility

- [ ] No breaking changes
- [ ] Breaking changes documented below

## Co-Authored-By

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Tips

- Keep the PR scoped — one logical change.
- Run `framework/_final_audit.py` BEFORE opening the PR.
- If you touched the master `CLAUDE.md` template, re-run `framework/_regenerate_claude_only.py`.
- For protocol changes, link the new ADR explicitly.

## Related

- [`CONTRIBUTING.md`](CONTRIBUTING.md)
- [`../part_4_tools/23_continuous_integration.md`](../part_4_tools/23_continuous_integration.md)
- [`issue_template.md`](issue_template.md)
