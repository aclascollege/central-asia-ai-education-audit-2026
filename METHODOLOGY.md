# Methodology — Central Asia AI Education Audit 2026

Audit date: **2026-10-17**. Snapshot.

## Sample

31 leading universities across Kazakhstan, Kyrgyzstan, Uzbekistan, Tajikistan and
Turkmenistan — national flagships and highest-ranked institutions (Webometrics /
regional standing), i.e. the institutions a policy survey must not miss.

## What was counted

Two questions per university:

(a) **AI policy**: does it publish a public, university-level AI usage policy for
students/teaching staff (academic integrity or teaching guidance mentioning
generative AI) on its official domain? `YES` requires the document to exist and
be retrievable. `UNVERIFIABLE` = not found / not retrievable — not proven absent.

(b) **AI programs**: AI-named degree programs or AI course portfolios verifiable
on the official domain.

Searches ran in English + Russian + national languages. All source access dates
recorded per claim in the audit notes.

## Caveats

- The UNVERIFIABLE rate (81%) is the highest measured in any region — partly a
  transparency/discoverability finding, not pure non-adoption. Turkmenistan's
  institutional web is largely closed.
- Policies are being published monthly; verify before citing a single row.

## Reproducibility

`parse.py` generated the CSV/JSON from the raw audit tables. Raw report:
`~/workspace/aclas-kg-seo/research/central-asia-ai-education-audit-2026.md`.
