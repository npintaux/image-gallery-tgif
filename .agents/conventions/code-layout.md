# Code layout convention — Smart Photo Gallery

> **Why this file exists.** `/implement` carries the *method* (TDD, OO, docstrings).
> This file carries the *layout* — where code goes — so the structure is
> **deterministic** rather than improvised on each run. `/implement` MUST read this
> before creating files. Its machine-readable twin, `code-layout.env` (same directory),
> declares the same paths/patterns as key=value so the hooks can enforce them. Keep
> the two in sync: this file is for the agent, `code-layout.env` is for the hooks.

## Repository layout

```
image-gallery-tgif/
├── SPEC.md                  # the contract /implement obeys — ROOT, load-bearing
├── pyproject.toml           # package metadata + semantic version
├── AGENTS.md                # thin router → SPEC.md, this convention, the skills
├── .agents/conventions/
│  ├── code-layout.md             # this file (prose, for the agent)
│  └── code-layout.env            # the same invariants as key=value (for the hooks)
├── docs/                    # reference material (e.g. the PRD)
└── src/                     # source root
   └── gallery/              # the importable package
      ├── core/              # pure decision core — deterministic, NO I/O
      │  ├── __init__.py
      │  ├── engine.py       # the execution engine
      │  └── rules/          # one rule per file, named r<n>_<slug>.py
      │     ├── __init__.py
      │     ├── base.py      # abstract base class for Rule
      │     └── r1_responsive_grid.py
      └── shell/             # optional: the I/O shell / frontend / assets around the core
   tests/                    # mirrors the rules; test_r<n>_<slug>.py
```

## The pure-core / shell seam

Split the package in two so the deterministic logic stays portable and testable:

- **pure core** (`src/gallery/core/`) — no I/O, no network, no model calls; same input →
  same output. This is what `/implement` builds and tests in TDD.
- **shell** (`src/gallery/shell/` or top-level UI files) — the I/O around the core (HTML, CSS, frontend client scripts, and side effects).

**The dependency points one way: shell → core.** The core must never import the shell.

## Rules — the unit of the engine

A *rule* is one declarative decision unit with a **stable ID** (`R1`, `R2`, …; never reused or renumbered).

- **One rule class per file**, named `r<n>_<slug>.py` (e.g. `r1_responsive_grid.py`), under `src/gallery/core/rules/`.
- Each rule **subclasses the `Rule` ABC** (`abc.ABC` + `@abstractmethod` `evaluate(...) -> Decision | None`).
- The **engine** (`src/gallery/core/engine.py`) holds the rule instances in an **ordered list at the SPEC's precedence**, exposes the `evaluate(...)` entry point, and returns the first non-`None` decision.

## Tests

- Live in `tests/`, mirroring the rule files: `test_r<n>_<slug>.py`.
- Plus an **engine-level test** (`tests/test_engine.py`) that drives rules through the engine's entry point.
