# CLAUDE.md — BUSFIN 8200 Problem Set 2 (submission repository)

This folder is a **standalone Git repository** submitted for grading. It is nested inside the
`AP/` study repo only for convenience; the parent repo ignores this folder entirely.
Any `CLAUDE.md` found in parent directories is for the study project and does **not** apply here.
The rules in this file take precedence.

Files committed to this repo (code, comments, `AI_INTERACTIONS.md`, `AI_USAGE.md`, LaTeX)
should be in **English** so the instructor can audit them.

## Course AI policy — MANDATORY
Full text: `../../Problem Sets AI Policy.pdf` (in the parent study repo, not part of this submission).
Compliance directly affects the grade. The principle: **the student designs and derives; AI checks,
critiques, and implements.**

### Per question type
- **Mathematical derivations.** The student derives first (by hand or in `.tex`). AI may only
  *check* a completed derivation or *diagnose a specific step* of a partial one. AI may explain
  *why* a step is wrong but must **not** rewrite, complete, continue, or replace the derivation.
  When diagnosing an error, state why the step is wrong and leave the corrected expression to
  the student.
  Allowed: transcribing a photo of handwritten work into LaTeX; improving exposition, grammar,
  or LaTeX formatting after the substantive derivation exists (record as formatting/translation).
- **Economic reasoning.** The student writes the full answer in `.tex` first. AI may only
  *critique* it (errors, omissions, inconsistencies) and explain the critique. AI must **not**
  generate, rewrite, or directly edit the reasoning. Formatting/grammar help allowed afterward.
- **Data analysis.** AI may implement, optimize, integrate, and debug code extensively, but the
  **empirical design must come from the student**. Before AI writes code, a **student-authored**
  specification file must already exist in `spec/` (plain-English `.md` or initial code by the
  student) and be present in the "TP before" snapshot, covering, where relevant:
  data sources, sample restrictions, variable definitions, timing conventions, transformations,
  econometric specifications, standard-error procedures, desired outputs.
  AI may make pure programming choices (data structures, packages, vectorization, code layout).
  AI must **not** silently make substantive choices absent from the spec (sample restriction,
  timing, missing-data treatment, variable definition, winsorization, regression specification,
  SE choice, ...). When such a decision is needed: **stop, identify the ambiguity, and ask the
  student to decide**; the student updates the spec before AI implements it. Decisions are
  recorded by quoting the student verbatim.
  Debugging: purely computational bugs may be fixed directly; if a fix requires a design
  decision, ask first.
- AI-written descriptive sentences in the `.tex` (e.g., a restatement of the estimated equation
  or a caption drafted from the spec) are labeled as such in the `AI_INTERACTIONS.md` entry.

### Documentation of AI use
- All AI use for this problem set happens **inside this workspace only** (open this folder as
  its own VS Code window). No separate chats or other AI apps.
- Before any **substantive** request (check, critique, generate, revise, explain, debug, format,
  translate, summarize anything related to an answer, derivation, design, code, interpretation,
  or submission), the student invokes the **`/TP`** skill (`.claude/skills/TP/SKILL.md`).
  If the student makes a substantive request without `/TP`, **remind them and run the `/TP`
  procedure anyway** before doing the work. Never bypass it for substantive work.
- Administrative requests (navigating files, explaining a terminal command, environment setup
  that does not affect substance, clarifying something already said) do not need `/TP`.
- **One `/TP` cycle per substantive request.** Grouping is allowed only for minor debugging or
  formatting iterations on the same item in the same session that the student explicitly asks
  to group in their prompt (see the skill, Step 6).
- `AI_INTERACTIONS.md` is **append-only**: never delete, rewrite, combine, or omit entries, and
  never touch an entry once it has been committed. Correct mistakes with a new entry.
- After the problem set is finished, the student runs the `AI_USAGE.md` prompt from the policy
  (pp. 6–7). Both `AI_INTERACTIONS.md` and `AI_USAGE.md` are part of the submission.

## Deliverables
1. Problem set solution as a **PDF** (typeset, not handwritten), built from source in this repo.
2. This Git repository with everything needed to reproduce both the results and the PDF:
   `.tex` sources, all scripts, `pyproject.toml`/`uv.lock`.

## Layout
```
PS2/
├── ps2.pdf                 problem set statement
├── data/                   datasets provided by the course (see data/README.md)
├── spec/                   student-written empirical specifications (one per data question)
├── src/                    Python scripts implementing the specs
├── output/                 figures and tables produced by src/ (LaTeX includes these)
├── tex/                    LaTeX source of the solution → tex/ps2_solution.pdf
├── AI_INTERACTIONS.md      contemporaneous record of AI use (append-only)
├── AI_USAGE.md             final summary (created at the end)
└── pyproject.toml, uv.lock python environment (run with `uv run python src/...`)
```

## Technical notes
- Python via `uv` (this folder has its own project; do not use the parent repo's environment).
- Windows console is cp1252: never print non-ASCII to stdout; write results to UTF-8 files.
- PDF text extraction: `pypdf`; page rendering: `pymupdf`.
- Commit messages: plain English, no AI attribution trailers needed beyond what `/TP` records.
