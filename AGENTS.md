# AGENTS.md — Image Gallery Agent (router)

This is a thin router. It points to the artifacts that govern work here; it does not
restate them.

## Source of truth
- **[`SPEC.md`](SPEC.md)** — the contract the implementation obeys. GitHub Issues are
  *intake*; `SPEC.md` decides. (Absent until `/specify` scaffolds it from the first story.)

## Conventions (always on)
- **[`.agents/conventions/code-layout.md`](.agents/conventions/code-layout.md)** — the code
  layout: `src/gallery/` package, `core/` vs `agent/` seam, one-rule-per-file, test
  placement. Read before creating any file. Its machine twin
  [`code-layout.env`](.agents/conventions/code-layout.env) feeds the hooks.

## Reference (not the contract)
- **[`docs/PRD.md`](docs/PRD.md)** — Product Owner artifact. Background/intent only; the
  developer works from the GitHub Issue + `SPEC.md`, not from the PRD.

The canonical `SPEC.md` *shape* lives in the plugin's `SPEC.template.md` (and is enforced
at commit); `/specify` derives the content from the Issue — there is no example to copy.

## Workflow (skills)
- `/specify #<n>` — Issue → proposed `SPEC.md` + tests, **STOP for approval**, then commit on `issue/<n>-<title>`.
- `/implement R<n>` — one rule, TDD → green, **STOP for approval**. Never commits, never auto-advances.
- `/commit` — separate, user-initiated, after approval. Conventional message `type(scope): summary [Rn] (#n)`.

**One user story = one session.** No commit without explicit approval; no auto-advance to the next story.

> [!IMPORTANT]
> **Core/Shell Partitioning Rule:**
> Given any user story that involves both logical decision-making (e.g., calculations, thresholds, state validations) and visual layouts (HTML, CSS, JS), the agent MUST split the story during `/specify` into two distinct GitHub issues:
>
> 1. **`[Core] <Title> Logic`** — To be implemented as pure Python rules with 100% test coverage.
> 2. **`[UI] <Title> Visual Shell`** — To be implemented as the presentation interface.