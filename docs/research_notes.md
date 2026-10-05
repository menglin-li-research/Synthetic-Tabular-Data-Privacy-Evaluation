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

## Experiment checklist

- [x] Repository created
- [x] README and reproducible structure
- [x] Exact source-data provenance recorded
- [x] Automated data-download scripts
- [x] Gaussian multivariate generator
- [x] Pima Indians Diabetes baseline
- [x] Contraceptive Method Choice baseline
- [x] Binary and multiclass utility evaluation
- [x] Resemblance metrics
- [x] Nearest-neighbour privacy screening
- [x] Exact-match screening
- [x] Upstream-style membership-inference simulation
- [x] Execute in a clean GitHub Actions environment
- [x] Audit and document first-stage results
- [ ] Add second generator
- [ ] Add upstream similarity evaluation
- [ ] Add attribute inference
- [ ] Add explicit differential privacy
- [ ] Add fairness/subgroup analysis
- [ ] Add presentation-ready figures
- [ ] Prepare final presentation

## Current interpretation

Both datasets retain roughly 96% of the TRTR ROC-AUC under the current TSTR evaluation.

Pima shows no exact synthetic duplicate under the current screening. The Contraceptive dataset shows a 2.55% exact-match rate; because its variables are highly discrete, this requires careful interpretation rather than an automatic disclosure claim.

The adapted membership-inference simulation produces near-chance mean accuracy for Pima and somewhat stronger separation for the Contraceptive dataset at the strictest threshold. This reinforces the point that privacy evidence is attack- and data-dependent.

## Interpretation discipline

Do not use "privacy-preserving" as a blanket claim merely because data are synthetic.

Synthetic data can still reproduce rare or identifying patterns. Privacy evidence should be linked to an explicit threat model and to specific empirical or formal privacy tests.
