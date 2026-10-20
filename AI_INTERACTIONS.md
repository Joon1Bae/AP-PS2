# AI_INTERACTIONS.md — BUSFIN 8200 Problem Set 2

Contemporaneous record of every substantive AI interaction on this problem set, created by the
`/TP` skill (see `.claude/skills/TP/SKILL.md`). Entries are **append-only**: nothing below is ever
edited, deleted, or merged. Corrections are made by adding a new entry.

Environment: VS Code + Claude Code (Anthropic), workspace = this repository.

## Interaction 1 — Q2(a) — 2026-10-20 19:38

- **Problem set item:** Q2(a)
- **Substantive prompt (verbatim):** "Could you read the q2a instruction and write a codes for it? Please let me know if you need further information or decisions to make." (The student did not prefix the request with `/TP`; the AI reminded the student and ran the `/TP` procedure.)
- **Purpose:** Implement the student's Q2(a) specification (`spec/q2a.md`): the SDF M* = a - b'xR that prices the 10 BE/ME decile excess returns with E[M*] = 1, plus a scatterplot of b by decile.
- **Git commit before:** 4e4be92440ba1e6fad4f42ad27185f703891b92b
- **Assistance provided:** Read `spec/q2a.md` and the Q2(a) statement in `Problem Set 2.pdf`. Inspected the structure of the two data files (block layout, units, date ranges, missing-value codes). Found two substantive choices the spec leaves open and one deliverable question, and asked the student to decide (answers below). **No code was written in this interaction.** Per `CLAUDE.md` ("the student updates the spec before AI implements it"), implementation is deferred to a new `/TP` cycle after the student adds these decisions to `spec/q2a.md`. Student decisions (selected options, verbatim):
  1. Q: "Which returns should define the BM Dataset?" → **"Monthly value-weighted"**
  2. Q: "What units should xR have when computing E[xR] and E[xR xR']?" → **"Decimal (divide by 100)"**
  3. Q: "Should I also create the LaTeX solution file?" → **"Also create tex skeleton"**
- **Files inspected:** `spec/q2a.md`, `Problem Set 2.pdf`, `data/Portfolios_Formed_on_BE-ME.csv`, `data/F-F_Research_Data_Factors.csv`, `data/README.md`, `AI_INTERACTIONS.md`, `pyproject.toml`, `.gitignore`
- **Files directly modified by AI:** `AI_INTERACTIONS.md` (this entry only)
- **Errors, omissions, or ambiguities identified:**
  1. The spec does not say which block of `Portfolios_Formed_on_BE-ME.csv` to use. The file has value-weighted and equal-weighted blocks, at both monthly and annual frequency, all with the same "Lo 10" ... "Hi 10" columns.
  2. The spec does not specify units. The files report returns and RF in percent, and the choice rescales b by a factor of 100.
  3. Minor, not substantive: the spec refers to "Portfolios_Formed_on_BE.csv" and "F_Research_Data_Factors.csv". The actual files are `data/Portfolios_Formed_on_BE-ME.csv` and `data/F-F_Research_Data_Factors.csv`, and the column header is "RF" (not "Rf").
  4. Data facts (no decision needed): both monthly series end in 2026-08, so the full sample is 1927-07 to 2026-08. No missing-value codes (-99.99 or -999) appear in the Lo 10 ... Hi 10 columns of either monthly block.
- **Substantive mathematical / economic / empirical suggestions made:** When presenting the weighting options, the AI described the monthly value-weighted block as "the Ken French default and the usual choice in the literature". It made no recommendation on units or on the LaTeX question.
- **Type of assistance:** other (specify): identifying ambiguities in the student's empirical specification before implementation
- **Grouped follow-up requests:** none
- **Git commit after:** f7e7d183269023dd54243c48aba64000e22c6c19
