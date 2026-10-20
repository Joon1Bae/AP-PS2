# BUSFIN 8200 — Problem Set 2

Author: Joon1Bae

## Reproduce

```
uv sync                         # creates .venv with pinned dependencies (uv.lock)
uv run python src/<script>.py   # regenerates output/ from data/
cd tex && latexmk -pdf ps2_solution.tex
```

## Contents

| Path | What |
|---|---|
| `ps2.pdf` | Problem set statement |
| `data/` | Course-provided datasets (see `data/README.md`) |
| `spec/` | Student-written empirical specifications, one per data question |
| `src/` | Python scripts implementing the specifications |
| `output/` | Figures and tables used by the LaTeX solution |
| `tex/` | LaTeX source and compiled PDF of the solution |
| `AI_INTERACTIONS.md` | Append-only record of AI use (course AI policy) |
| `AI_USAGE.md` | Final AI usage summary (created after completion) |
