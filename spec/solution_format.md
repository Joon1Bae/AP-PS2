# Formatting guide for the Problem Set 2 solution (.tex)

## Rule 0: formatting only
- Change only the layout and presentation. Do not add, remove, rewrite, or reorder any
  mathematical step, economic argument, interpretation, or number.
- Keep every placeholder written by me (e.g., "[to be computed by the student]",
  "[Definition ... will be here]", "[?]") exactly as it is, and make it visible
  (e.g., \textcolor{red}{...}) so I can find and fill it.
- If something looks wrong, leave it unchanged and list it in a comment for me to check.

## Document structure
- Title block: course, problem set number, name, date.
- One \section per Question and one \subsection per item (1a, 1b, ...).
- Start each Question on a new page.
- Inside each item, use the same order of short paragraphs (omit any that do not apply):
  0. Task: an excerpt of the problem statement (see "Problem statement excerpts" below).
  1. Setup: the object being computed and the data used.
  2. Method: the estimator or derivation steps.
  3. Result: the number, table, or figure.
  4. Interpretation: my discussion (text written by me only).

## Problem statement excerpts (as in ps1_solution.pdf)
- Start each item with a "Task." paragraph that quotes the problem statement verbatim
  from Problem Set 2.pdf. Do not paraphrase or reword it.
- Omit sentences that are not instructions (e.g., data descriptions, motivation) and mark
  each omission with [...].
- If an item contains several instructions, split them into numbered tasks (1), (2), ...,
  and refer to the same numbers in the answer (e.g., "(2) Table 7 reports ...").
- Typeset the Task paragraph so that it is visually distinct from the answer
  (e.g., indented with a smaller font, or a quote environment).
- Keep footnotes of the problem statement out of the excerpt unless they contain an instruction.

## Math
- Use display environments (align or equation) for multi-step derivations, one step per line,
  aligned at the relation sign (=, ⇔, ⇒).
- Number only equations that are referred to later.
- Notation: bold for vectors and matrices (\mathbf{X}), prime for transpose (X'),
  hats for estimates (\hat{\gamma}), \mathbb{E}[\cdot] for expectations, \mathbb{E}_t[\cdot]
  for conditional expectations, \widehat{\mathbb{E}}[\cdot] for sample means.
- Write matrices with bmatrix and label rows and columns in the text right after.

## Tables
- Use booktabs (\toprule, \midrule, \bottomrule); no vertical lines.
- Same number of decimals within a column (estimates and standard errors: 3 or 4 decimals;
  p-values: 3 decimals).
- Standard errors or t-stats in parentheses under or next to the estimate, as stated in the note.
- Every table note states: the sample period, the data frequency and return horizon,
  the units, the standard-error method (e.g., Newey-West (1987, 1994) with the selected lag),
  and any symbol used in the table (e.g., "–").

## Long tables (21 assets: Q3(e), Q4(b)-(e))
- Put the book-to-market and momentum deciles side by side: rows = deciles 1-10,
  column groups = "Book-to-market" and "Momentum" (each with Ê[ε_j] and t-stat, or α̂_j and
  t-stat), headed with \cmidrule(lr). Put the market (xR_w,t) in a separate row below.
- Split each table into panels: A (parameter estimate and s.e.), B (pricing errors),
  C (joint test, Newey-West lag, sample), separated by \midrule or \addlinespace.
- Align numbers at the decimal point with siunitx S columns.
- Do not change any number; only the layout changes.

## Figures
- Axis labels with units -- a legend only when there is more than one series.
- Every caption should include the sample period, the data, and the units.

## Cross-references and consistency
- Refer to earlier items with \ref (e.g., "as in Question 3(c)"), not by page.
- Use the same name for the same object across all questions (e.g., always xR_{w,t} for the market excess return).
