# Research Notes

## Conceptual frame

The project sits at the intersection of:

- privacy-enhancing technologies;
- synthetic data;
- generative AI;
- machine-learning evaluation;
- fairness;
- reproducibility.

The central question is not whether synthetic data is simply "private" or "useful", but how **privacy, utility, resemblance, and fairness trade off** under different generation and evaluation choices.

## Reading synthesis questions

For each paper or survey, record:

1. What has been covered?
2. What are the main technologies/methods?
3. What gaps remain?
4. What potential solutions are proposed?
5. How does the paper connect to privacy–utility–fairness trade-offs?

## Stage 1 experiment checklist

- [x] Repository created
- [x] README and reproducible structure
- [x] Exact source-data provenance recorded
- [x] Data-download script
- [x] Gaussian multivariate baseline
- [x] Resemblance metrics
- [x] TRTR/TSTR utility evaluation
- [x] Privacy-screening metrics
- [ ] Execute baseline in a clean environment
- [ ] Audit outputs for plausibility
- [ ] Add result tables/figures
- [ ] Add second generator or second dataset
- [ ] Add stronger privacy attacks
- [ ] Add fairness analysis
- [ ] Prepare presentation-ready summary

## Interpretation discipline

Do not use "privacy-preserving" as a blanket claim merely because data are synthetic.

Synthetic data can still reproduce rare or identifying patterns. Privacy evidence should be linked to an explicit threat model and to specific empirical or formal privacy tests.
