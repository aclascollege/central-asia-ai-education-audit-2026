# Online Degree Tuition 2026

An open dataset of **740 online degree programs at 537 U.S. institutions**,
with tuition verified against each university's official website. Built for the
cheapest-online-degrees tool (aclas.edu.gr) and released here as open data.

## Coverage

| Level | Programs |
|---|---|
| Online MBA | 228 |
| Online DBA | 38 |
| Business bachelor's | 299 |
| Online BSCS | 67 |
| Online MCS | 108 |
| **Total** | **740** |

## Columns

`school`, `program`, `level` (mba/dba/bachelor/bscs/mcs), `tuition_usd`
(total program tuition in USD), `tuition_note`, `estimate` (true = figure is an
informed estimate, e.g. per-credit × required credits — see note below),
`accreditation`, `format`, `source_url` (the official page the figure was taken
from), `verified` (date last checked, 2026-10-15).

## Honest notes

- `estimate: true` (439 rows) means the total is computed, not quoted — e.g.
  per-credit-hour price × program credits. The `tuition_note` explains the basis.
  Treat these as comparisons, not quotes.
- Tuition changes; `verified` tells you how fresh each row is. Verify before
  citing a single figure for a current claim.
- USD conversions use the rate at time of verification.

## License

[CC-BY-4.0](LICENSE) — cite "Study Intelligence (aclas.si)".

```bibtex
@dataset{studyintelligence2026tuition,
  author = {{Study Intelligence}},
  title = {Online Degree Tuition 2026},
  year = {2026},
  publisher = {Study Intelligence (aclas.si)},
  url = {https://aclas.si/data/online-degree-tuition-2026}
}
```
