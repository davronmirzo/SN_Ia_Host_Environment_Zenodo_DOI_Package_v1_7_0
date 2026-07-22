# Release notes - v1.7.0

Release date: 2026-07-22

## Consolidated release

- Consolidated all non-duplicated content from the published v1.5.0 package and
  the validated-layer v1.6.0 forward-selection rerun into one clean release.
- Retained v1.6.0 files as canonical whenever a relative path changed.
- Preserved the five files unique to v1.5.0 under a clearly labelled archive
  directory together with the v1.5.0 citation and release metadata.
- Added a machine-readable legacy index and an explicit version-lineage report.

## Canonical selection-forward analysis

- The current analysis remains the validated 2642-object rerun with the current
  fixed five-bin edges, residual-scale WLS covariance, and 250 km s^-1
  peculiar-velocity convention.
- Canonical numerical results are unchanged from the corrected v1.6.0 build.
- Superseded harmonized artefacts do not appear in canonical `results/` or
  `figures/` directories.

## Figure 4 accessibility update

- Enlarged and bolded all axis titles, tick labels, and category labels.
- Added a fast Python figure-only regeneration script.
- Patched the complete rerun script so a full rerun reproduces the final figure
  typography.
- No numerical values or statistical conclusions changed.

## Identifier status

- Previous published exact DOI: `10.5281/zenodo.21495900` (v1.5.0).
- Concept DOI: `10.5281/zenodo.21495899`.
- New consolidated exact-version DOI: `10.5281/zenodo.TBD` until reserved.
