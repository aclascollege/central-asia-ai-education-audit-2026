# Contributing

Corrections and additions are welcome. This is a data repository — most
contributions are **data corrections**, not code.

## Data corrections

1. **Fork** this repository and create a branch.
2. Edit `central-asia-ai-policies-2026.csv` (it is the source of truth) (it is the source of truth).
3. In your pull request, include for every changed row:
   - the row `id`,
   - what changed and why,
   - a link to the **official source** (university domain page, official PDF)
     backing the correction. PRs without a verifiable source will not be merged.
4. If the repo has a `parse.py`, regenerate the JSON from the CSV and include it.

## What makes a good correction

- One issue per PR; keep diffs small and reviewable.
- `UNCLEAR` → `YES`/`NO` upgrades need a directly opened official page.
- Do not "fix" a row based on a third-party article or aggregator.

## Questions

Open an issue with the `question` template. For questions about the research
program itself, see [Study Intelligence](https://aclas.si).

## License

By contributing, you agree your contribution is released under this
repository's [CC-BY-4.0](LICENSE) license.
