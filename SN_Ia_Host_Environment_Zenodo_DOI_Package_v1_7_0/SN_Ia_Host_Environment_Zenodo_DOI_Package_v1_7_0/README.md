# ZTF DR2 SN Ia host-environment correction-validity release v1.7.0

This archive is the clean reproducibility and audit package for the analysis
**Testing the Correction Validity and Environmental Dependence of the ZTF DR2
Type Ia Supernova Host-Mass Residual**.

## Scientific scope

The release contains the canonical 2642-object ZTF residual layer, the
3483-object raw-to-final selection-training layer (2670 selected), processed
Pantheon+ and DES-SN5YR comparison products, machine-readable results,
statistical audit code, and final vector figures in PDF format.

The evidence is deliberately hierarchical:

- the global ZTF host-mass residual is securely detected;
- the five-bin sequence challenges an unqualified redshift-invariant scalar,
  but its formal strength depends on estimator and variance calibration;
- projected host offset supplies the clearest additional structure through a
  strong mass-offset interaction;
- Pantheon+ and DES-SN5YR provide product-level context rather than direct
  replications of the complete ZTF protocol.

Exact headline values and their claim boundaries are consolidated in
`metadata/key_results.csv`. The complete audit-to-code-to-output mapping is in
`metadata/audit_inventory.csv`.

## Validated forward-selection rerun

Version 1.7.0 consolidates the published v1.5.0 release with the validated-layer v1.6.0 rerun and replaces the legacy harmonized selection-forward tomography
reference with a fully aligned rerun. The current audit uses the validated
2642-object residual layer to define the fixed five-bin edges, observed bin
steps, response model, standardized residual pools, and observed slope/Q. The
broader raw-to-final layer supplies the empirical selection surface. Residual
uncertainties are recomputed with the frozen 250 km s^-1 peculiar-velocity
convention, and every simulated fit uses the same residual-scale WLS covariance
as the primary analysis.

The empirical selection odds are preserved. A single intercept-only
recalibration over regression-eligible parent rows makes the expected selected
denominator equal to 2642; this conditioning step is recorded in
`results/tables/validated_forward_selection_probability_audit.csv`.

## Data-source separation

- `data/processed/` - canonical analysis-ready tables.
- `data/diagnostic_layers/` - non-duplicated response and identifier audit layers.
- `data/external_products/source/` - external source products required by the
  reduced product audit.
- `metadata/workflow_source_mapping.csv` - explicit mapping of each input layer
  to its permitted analysis branches.

The primary residual layer feeds global, redshift-stability, observation-level
influence, environmental, and validated response-generation components. The
broader ZTF layer supplies the empirical selection surface and parent
covariates. External products feed the reduced external-product audit.

## Package layout

- `code/` - audit and figure-generation code, including the complete validated
  forward-selection rerun and Python/MATLAB sources for Figure 1.
- `results/tables/` - machine-readable results and stochastic draws.
- `figures/` - final figures, PDF only.
- `docs/` - scope, statistical notes, audit reports, accessibility text, and
  deposition checklist.
- `metadata/` - Zenodo metadata, key-result registry, audit inventory, data
  dictionary, indices, provenance, and SHA-256 manifest.
- `checks/` - release verification, manifest rebuild, and DOI insertion tools.
- `archive/` - clearly segregated v1.5.0 selection-forward artefacts retained only for provenance.

## Start here

```bash
python checks/verify_release.py
```

Rerun commands are given in `RUNBOOK.md`.

## Zenodo identifiers

- Reserved exact-version DOI for this consolidated release: `10.5281/zenodo.TBD`
- Concept DOI for all versions: `10.5281/zenodo.21495899`
- Previous exact release DOI (v1.5.0): `10.5281/zenodo.21495900`

The published v1.5.0 exact DOI remains historical. After creating a new Zenodo version and reserving its DOI, run
`checks/set_reserved_doi.py` before upload. The manuscript must cite the new
exact-version DOI after this rerun, not the superseded v1.5.0 DOI.

## Deliberate exclusions

The manuscript PDF, LaTeX source, bibliography, referee correspondence, and
journal build products are not included. No PNG or EPS figure duplicates are
stored in the deposition archive. Upstream cadence, targeting, classification,
host-association, and collaboration-level bias-correction pipelines remain
outside this derived-analysis release.

## Licensing

- Code: MIT.
- Authors' derived tables, figures, metadata, and documentation: CC BY 4.0,
  subject to the terms of the underlying survey products.

See `docs/THIRD_PARTY_DATA_NOTICE.md` and the licence files in `licenses/`.

## Consolidation note

See `docs/VERSION_LINEAGE_AND_CONSOLIDATION.md` for the merge policy, version lineage, and the strict separation between canonical and archived superseded files.
