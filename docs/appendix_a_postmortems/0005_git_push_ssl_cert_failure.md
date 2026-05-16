# Postmortem 0005 — `git push` blocked by SSL certificate error on Windows

**Severity:** Low
**Date:** 2026-05-15
**Owner:** framework author

## TL;DR

`git push origin main` on the reference Windows 11 machine failed with `unable to access ... SSL certificate problem: unable to get local issuer certificate`. The default git TLS backend (OpenSSL) couldn't validate GitHub's certificate chain via the Windows certificate store. Fix: switch git's TLS backend to **schannel** (Windows native TLS), which uses the OS certificate store directly.

## Timeline

| Time | Event |
|---|---|
| Day 0 | First push attempt to `dlmastery/autoresearch_dsbench` after `gh repo create`. Fails with the SSL certificate error. |
| Day 0 + 5m | Author tries to disable SSL verification (`git config --global http.sslVerify false`). Push succeeds — but disabling verification is a security regression. |
| Day 0 + 10m | Author reverts the disable, instead switches the TLS backend: `git config --global http.sslBackend schannel`. Push succeeds with full SSL verification using the Windows certificate store. |
| Day 0 + 12m | Author documents the workaround in `framework/CLAUDE_template.md` Lesson 24 and the autoresearch-pack `mlops-documentation` skill. |

## Root cause

**Technical:** Git for Windows ships two TLS backends: OpenSSL (default) and schannel (Windows native). OpenSSL reads its own CA bundle, which on this machine was either out-of-date or didn't include the issuer for `github.com`'s certificate (corporate proxy / OpenVPN intermediate cert can also be the cause). schannel reads the Windows certificate store, which is kept up to date by Windows Update.

**Systemic:** Windows-specific git gotchas aren't in the autoresearch protocol's "setup" section. The original FX project ran on a Unix-style workstation; the DSBench port to Windows surfaced this for the first time. Without documentation, a new contributor cloning the repo on a fresh Windows machine would hit the same wall.

## Impact

- ~10 minutes of debug time on the initial push.
- No code or data affected.
- The fix is per-user, not per-repo — once set on a machine, it persists across all git operations.

## What went well

- The error message named the exact subsystem (SSL cert validation). A quick search yielded the schannel workaround within minutes.
- The fix has zero downside: schannel is a fully-supported git TLS backend, not a workaround.
- Documentation lives in two places (Lesson 24 + `mlops-documentation` skill), so any future Windows contributor finds it.

## What went badly

- The workaround disables-then-re-enables flow temporarily ran with `sslVerify=false`. This was a security regression for the ~5-minute window. In a CI environment this would be unacceptable.
- The autoresearch-pack `mlops-documentation` skill didn't have a "Windows setup" section before; it now does.

## Action items

| AI | Owner | Status | Tracking |
|---|---|---|---|
| Document the schannel workaround in `framework/CLAUDE_template.md` | author | Done | Lesson 24 |
| Add a "Windows setup" subsection to the `mlops-documentation` skill | author | Done | `skills/autoresearch-pack/skills/mlops-documentation/SKILL.md` |
| Add a one-line check to `framework/_status.py` that warns if `git config --get http.sslBackend` returns anything other than `schannel` on Windows | author | Open | TODO |

## Related

- [`../appendix_b_adrs/0014_github_checkpoint_protocol.md`](../appendix_b_adrs/0014_github_checkpoint_protocol.md)
- Skill `mlops-documentation`.
- Git docs: <https://git-scm.com/docs/git-config#Documentation/git-config.txt-httpsslBackend>.
