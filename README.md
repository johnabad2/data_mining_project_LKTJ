# Hydrogen-Bond Acceptors and Acute Toxicity

**Research question:** Is an increased number of hydrogen-bond acceptors associated with greater acute toxicity in organic compounds?

**H0:** No association. **H1:** Increasing acceptor count is associated with greater acute toxicity.
`LD50` is already **−log10(LD50 in mol/kg)** for acute oral toxicity in rats: higher means more toxic. Do not log-transform it again.

## Findings

- **Statistics:** A weak positive association (Spearman ρ = 0.252, two-sided p = 1.45 × 10⁻¹⁰⁷; n = 7,388). The HBA coefficient remains positive after adjustment for molecular weight and LogP: 0.083, 95% CI 0.065–0.102. Duplicate-record and influence sensitivities retain the positive direction.
- **Prediction:** Linear Regression, Random Forest and Gradient Boosting were compared. **Random Forest** performed best in five-fold CV (RMSE 0.641 ± 0.015 fold SD) and on the test set: **R² = 0.561, RMSE = 0.627, MAE = 0.456**.
- **HBA contribution:** For Random Forest, test R² is 0.064 using HBA alone and 0.559 without HBA. HBA ranks **21/25** by held-out permutation importance. Removing it changes RMSE by +0.0007 (paired 95% interval -0.0036 to +0.0047). The interval includes zero, so this holdout does not establish a clear incremental benefit.

**Conclusion:** More acceptors are associated with greater toxicity on average, but acceptor count alone is a weak predictor. Other molecular properties and overlapping descriptor information matter. Statistical significance, prediction and feature importance do not establish causation.

## Data and method

Recorded provenance: ChemIDplus → EPA TEST → `data/raw/ld50-smiles-descriptors-dataset.csv`.
Cleaning removed one missing target and eight exact duplicates: **7,397 → 7,388 records**.
The original adjusted regressions use 7,378 complete cases; ML retains all 7,388 records through training-only imputation.

Seed 42 gives **5,909 training / 1,479 test records**. Repeated SMILES stay together in the split and CV. Grouping uses identical recorded SMILES; alternative SMILES and related scaffolds are not resolved. This is internal validation. Both dataset hashes remain unchanged.

## Reproduce and inspect

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src/machine_learning.py --all
```

Create `.venv` with `python -m venv .venv` first if needed. In VS Code, select this environment for both notebooks.

- [Exploration notebook](notebooks/01_data_exploration.ipynb): cleaning, dataset audit and Spearman test, with code, outputs and method notes.
- [ML notebook](notebooks/02_machine_learning.ipynb): regression diagnostics, model comparisons and feature importance, with code, outputs and method notes.
- [results/](results/): numerical outputs, predictions, splits and version/hash manifest.
- [figures/](figures/): five new `ml_*.png` figures; original graphs preserved.

Omit `--all` to run only ML. Regenerate original plots with `python src/data_visualisation.py --no-show`; additional scripts remain in `src/exploratory/`.

Cleaning and statistical analysis are implemented in the notebooks. Both notebooks are technical records; findings are summarised above.

## Current progress

- [x] Define the question, audit and clean the dataset.
- [x] Complete descriptive plots and statistical association analysis.
- [x] Complete regression diagnostics and sensitivity checks.
- [x] Compare three regression models with training-only tuning and held-out evaluation.
- [x] Complete permutation importance and the three HBA descriptor comparisons.
- [x] Interpret the results and write the final conclusion.
- [x] Execute both notebooks and verify saved outputs and unchanged data.

The requested repository analysis is complete. External/scaffold validation and mechanistic experiments remain possible follow-up research.
