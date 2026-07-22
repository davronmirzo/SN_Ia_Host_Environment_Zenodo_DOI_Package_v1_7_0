# Reproduction runbook

## Environment

```bash
conda env create -f environment.yml
conda activate snia-host-environment
```

## Verify the extracted archive

```bash
python checks/verify_release.py
```

## Rerun the validated forward-selection analysis

```bash
python code/77_validated_forward_selection_rerun.py --root .
```

This command reproduces the 3000-draw global null, the three 300-draw
fixed-edge tomography scenarios, the 150-draw offset positive control, Figure 4,
Appendix Figure B1, Table 6, and all associated machine-readable tables.

## Regenerate Figure 4 from the frozen canonical draws

```bash
python code/make_fig04_selection_forward_validation.py
```

This fast path changes no simulations or tables. It reproduces the final vector PDF with enlarged bold axis typography.

## Recompute the Q summary from the regenerated bin-level table

```bash
python code/71_selection_stress_heterogeneity_Q.py --root . --outdir rerun_phase2_summary
```

## Recompute the five-bin variance calibration

```bash
python code/76_statistical_calibration_audit.py
```

## Rerun object-level influence

```bash
python code/73_object_level_jackknife_influence.py   --input data/processed/ZTF_DR2_validated_residual_layer.csv   --outdir rerun_phase3
```

## Rerun the environmental audit

```bash
python code/74_environment_stratification_interaction.py   --input data/processed/ZTF_DR2_validated_residual_layer.csv   --outdir rerun_phase4   --n-bootstrap 2000   --n-permutation 5000   --seed 20260716
```

## Rerun the external-product audit

```bash
python code/75_external_product_common_support_influence.py   --root .   --outdir rerun_phase5   --n-bootstrap 2000   --seed 20260721
```

## Regenerate Figure 1

Python:

```bash
python code/make_fig01_correction_validity_workflow.py
```

MATLAB, from the package root:

```matlab
run('code/make_fig01_correction_validity_workflow.m')
```

Only vector PDF figures belong in the deposition archive.

## Insert a reserved Zenodo DOI

```bash
python checks/set_reserved_doi.py 10.5281/zenodo.XXXXXXX
```

The release includes frozen stochastic draws and summaries. Exact draw-level
reproduction requires the listed seeds, package versions, and input tables.
Small floating-point differences can occur across BLAS implementations.

## Historical v1.5.0 artefacts

Files under `archive/v1_5_0_superseded_selection_forward/` are provenance-only and are never inputs to current rerun commands.
