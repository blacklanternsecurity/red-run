# red-run — Session Log

## 2026-02-21 — Bootstrap

### Done
- Initialized repo at `~/claude/red-run`
- Surveyed all three reference repos:
  - `~/docs/InternalAllTheThings` — internal/AD-focused, 9 top-level categories
  - `~/docs/PayloadsAllTheThings` — web-focused, 40+ injection/vuln directories
  - `~/docs/hacktricks` — broadest scope, 700+ files across 20 categories
- Built unified topic taxonomy (see `findings.md`)
- Categorized all topics into 8 skill groups
- Created phased task plan (`task_plan.md`)
- Designed skill directory layout and file format
- Created template skill at `skills/_template/skill.md`

### Observations
- AD coverage in InternalAllTheThings is exceptional — 15 individual ADCS ESC files, full Kerberos delegation chain, modern tooling (Certipy, NetExec, bloodyAD)
- Web coverage in PayloadsAllTheThings is the deepest — SQL injection alone has 10 files across 8 DB engines
- HackTricks has the broadest scope (binary exploitation, macOS, mobile, AI security, forensics) but some sections are thin
- Cloud content is split: InternalAllTheThings has Azure (144K) and AWS (80K); HackTricks main repo has none (lives in HackTricks Cloud, separate repo)
- Notable gaps across all repos: GCP, wireless, physical security

---

## 2026-02-21 — Web Skills Session 1

### Done
- Authored 4 v1 reference skills (static `skill.md` format):
  - `web-vuln-discovery` — content discovery, parameter fuzzing, decision tree
  - `sql-injection-union` — UNION-based extraction, 5 DB engines
  - `sql-injection-error` — error-based extraction, 4 DB engines
  - `sql-injection-blind` — boolean, time-based, OOB blind extraction

### Decisions
- Skills split by **technique**, not by DB engine or technology
- DB/engine variants go as subsections within each technique skill
- Discovery/triage skills as entry points with decision trees routing to technique skills

---

## 2026-02-22 — Web Skills Session 2 + Architecture Redesign

### Done
- Authored `sql-injection-stacked` on `skills/web-sqli` branch (stacked queries + second-order injection)
- SQLi v1 skill set complete (4 techniques: union, error, blind, stacked)

### Architecture Redesign (v1 → v2)

Decided to restructure from static reference docs to Claude Code native skills:

**Problem with v1:** Static `skill.md` reference docs required manual invocation (`Read ~/claude/red-run/skills/...`). No auto-triggering, no guided/autonomous modes, no orchestration. A separate reference layer duplicated content from `~/docs/` and would go stale.

**v2 architecture:**
- **SKILL.md** is the only artifact per technique (Claude Code native format)
- Skills **auto-trigger** via pushy `description` field — no slash commands needed
- Two **modes**: guided (interactive, default) and autonomous (end-to-end)
- **Orchestrator** skill: takes a target → recon → route to discovery → route to techniques → report
- **Discovery** skills: identify vulnerabilities, route to technique skills via decision tree
- **Technique** skills: exploit specific vuln classes with embedded critical payloads
- `~/docs/` is a **dependency** (not copied) for deep reference content
- Skills install **globally** to `~/.claude/skills/red-run-*/` via `install.sh` (symlinks)

### Created
- `skills/_template/SKILL.md` — new canonical template with mode handling, routing, deep reference sections
- `install.sh` — symlink-based installer with `red-run-` prefix and `~/docs` dependency check
- `uninstall.sh` — cleanup script
- Updated `CLAUDE.md` with new architecture, format, install workflow
- Updated `task_plan.md` — v2 architecture tasks, conversion checklist

### Status
- Infrastructure ready (template, install scripts)
- 5 existing v1 skills need conversion to SKILL.md format
- All remaining web skills (XSS, SSTI, SSRF, etc.) to be authored in SKILL.md format from scratch
- Orchestrator skill still needs to be written

### Engagement Logging (planned)

Skills need to track what happens during an engagement. Rough design:

- **Engagement directory**: Created by orchestrator (or user) at engagement start. Probably `./engagement/` or user-specified path. Contains:
  - `activity.md` — chronological log of all actions taken (recon scans, injection tests, exploitation attempts). Each entry timestamped. Append-only.
  - `findings.md` — confirmed vulnerabilities. Each finding gets: title, severity, affected host/endpoint, description, reproduction steps, evidence (terminal output, screenshots), impact.
  - `evidence/` — directory for screenshots, saved responses, captured credentials, etc.
  - `scope.md` — target scope, credentials, constraints (written at engagement start)
- **Every skill** logs to activity.md when it runs (what was tried, what worked, what didn't)
- **Successful exploits** get a full finding entry with reproduction steps and evidence
- **Orchestrator** initializes the engagement dir, maintains the activity log, and produces a summary at the end
- This integrates with the existing `pentest-findings` skill for formal finding writeups

### Next Steps
1. Convert 5 existing skills: web-vuln-discovery, sql-injection-{union,error,blind,stacked}
2. Write orchestrator skill (including engagement dir initialization)
3. Design engagement logging conventions and bake into template
4. Continue Phase 3 web skills in SKILL.md format (XSS next)
5. Note: `sql-injection-stacked` is on `skills/web-sqli` branch — merge to main or cherry-pick before converting
