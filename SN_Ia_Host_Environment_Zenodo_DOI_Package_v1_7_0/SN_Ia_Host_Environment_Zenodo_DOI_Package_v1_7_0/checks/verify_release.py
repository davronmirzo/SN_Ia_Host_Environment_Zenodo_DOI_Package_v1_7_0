#!/usr/bin/env python
from __future__ import annotations
from pathlib import Path
import hashlib, json, math, re
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def close(value: float, target: float, tolerance: float) -> None:
    if not math.isfinite(float(value)) or abs(float(value) - target) > tolerance:
        raise AssertionError(f'{value} differs from {target}')

required = [
    'README.md', 'RUNBOOK.md', 'RELEASE_NOTES.md', 'CITATION.cff',
    'codemeta.json', 'environment.yml', 'requirements.txt',
    'data/processed/ZTF_DR2_validated_residual_layer.csv',
    'data/processed/empirical_selection_training_sample.csv',
    'data/processed/PantheonPlus_analysis_sample.csv',
    'data/processed/DES_SN5YR_analysis_sample.csv',
    'code/77_validated_forward_selection_rerun.py',
    'code/make_fig04_selection_forward_validation.py',
    'figures/fig01_analysis_flow.pdf',
    'figures/fig04_selection_forward_validation.pdf',
    'figures/figB1_validated_selection_null_recovery.pdf',
    'results/tables/validated_forward_selection_probability_audit.csv',
    'results/tables/validated_forward_selection_global_null_summary.csv',
    'results/tables/validated_forward_selection_offset_positive_control_summary.csv',
    'results/tables/table06_selection_forward_summary.csv',
    'docs/FIGURE_4_CAPTION_AND_ALT_TEXT.md',
    'docs/VERSION_LINEAGE_AND_CONSOLIDATION.md',
    'metadata/version_lineage.json',
    'metadata/legacy_v1_5_0_index.csv',
    'metadata/key_results.csv', 'metadata/audit_inventory.csv',
    'metadata/workflow_source_mapping.csv',
    'metadata/table_index.csv', 'metadata/figure_index.csv',
    'metadata/file_manifest_sha256.csv',
    'archive/v1_5_0_superseded_selection_forward/README.md',
]
for rel in required:
    if not (ROOT / rel).exists():
        raise AssertionError(f'Missing required file: {rel}')

# Current metadata.
summary = json.loads((ROOT / 'metadata/release_summary.json').read_text(encoding='utf-8'))
if summary.get('version') != '1.7.0':
    raise AssertionError('Release version is not 1.7.0')
if summary.get('concept_doi') != '10.5281/zenodo.21495899':
    raise AssertionError('Concept DOI drift')
lineage = json.loads((ROOT / 'metadata/version_lineage.json').read_text(encoding='utf-8'))
if lineage['previous_published_version']['exact_doi'] != '10.5281/zenodo.21495900':
    raise AssertionError('Previous DOI drift')

# No manuscript/build products or non-PDF canonical figure duplicates.
for path in ROOT.rglob('*'):
    if not path.is_file():
        continue
    rel = path.relative_to(ROOT).as_posix()
    low = rel.lower()
    if path.suffix.lower() in {'.tex', '.bbl', '.aux', '.log', '.png', '.eps', '.pyc'}:
        raise AssertionError(f'Forbidden release format: {rel}')
    if '__pycache__' in path.parts:
        raise AssertionError(f'Python cache artefact present: {rel}')
    if 'manuscript' in low or low.startswith('sn_paper'):
        raise AssertionError(f'Manuscript artefact present: {rel}')
for path in (ROOT / 'figures').iterdir():
    if path.is_file() and path.suffix.lower() != '.pdf':
        raise AssertionError(f'Non-PDF canonical figure: {path.name}')

# Parseability.
for path in ROOT.rglob('*.csv'):
    pd.read_csv(path)
for path in ROOT.rglob('*.json'):
    json.loads(path.read_text(encoding='utf-8'))

# Frozen row counts.
if len(pd.read_csv(ROOT / 'data/processed/ZTF_DR2_validated_residual_layer.csv')) != 2642:
    raise AssertionError('ZTF row-count drift')
selection = pd.read_csv(ROOT / 'data/processed/empirical_selection_training_sample.csv')
if len(selection) != 3483 or int(selection['selected_final'].sum()) != 2670:
    raise AssertionError('Selection layer drift')
if len(pd.read_csv(ROOT / 'data/processed/PantheonPlus_analysis_sample.csv')) != 559:
    raise AssertionError('Pantheon row-count drift')
if len(pd.read_csv(ROOT / 'data/processed/DES_SN5YR_analysis_sample.csv')) != 1829:
    raise AssertionError('DES row-count drift')

# Frozen primary results.
binned = pd.read_csv(ROOT / 'results/tables/reconciliation60_best_binned_summary.csv').iloc[0]
close(binned.slope, 1.502655170668689, 1e-10)
close(binned.heterogeneity_Q, 10.613654195563075, 1e-10)
phase4 = pd.read_csv(ROOT / 'results/tables/phase4_global_interactions.csv')
row = phase4[(phase4.model == 'offset_interaction_simple') & (phase4.term == 'H_R')].iloc[0]
close(row.coefficient, 0.2341545357288053, 1e-10)

# Validated forward-selection outputs.
prob = pd.read_csv(ROOT / 'results/tables/validated_forward_selection_probability_audit.csv').iloc[0]
if int(prob.regression_eligible_parent_rows) != 3050:
    raise AssertionError('Eligible parent row-count drift')
close(prob.calibrated_expected_selected_n, 2642.0, 1e-8)
close(prob.vpec_km_s, 250.0, 1e-12)
observed = pd.read_csv(ROOT / 'results/tables/selection_stress_heterogeneity_Q_observed.csv').iloc[0]
close(observed.tomography_slope, 1.502655170668689, 1e-10)
close(observed.heterogeneity_Q, 10.613654195563075, 1e-10)
q = pd.read_csv(ROOT / 'results/tables/selection_stress_heterogeneity_Q_summary.csv').set_index('scenario')
expected_q = {
    'zero_mass_effect': (10, 0.03654485049833887),
    'constant_official_mass_step': (8, 0.02990033222591362),
    'observed_validated_tomographic_mass_step': (239, 0.7973421926910299),
}
for scenario, (count, p_value) in expected_q.items():
    if int(q.loc[scenario, 'n_Q_ge_observed']) != count:
        raise AssertionError(f'{scenario} Q-count drift')
    close(q.loc[scenario, 'empirical_p_leading_one'], p_value, 1e-12)
null = pd.read_csv(ROOT / 'results/tables/validated_forward_selection_global_null_summary.csv').iloc[0]
if int(null.n_sim_ok) != 3000 or int(null.n_mass_step_le_observed) != 0:
    raise AssertionError('Global selection-null drift')
close(null.empirical_p_leading_one, 1.0 / 3001.0, 1e-15)
offset = pd.read_csv(ROOT / 'results/tables/validated_forward_selection_offset_positive_control_summary.csv').iloc[0]
if int(offset.n_sim_ok) != 150:
    raise AssertionError('Offset positive-control draw-count drift')
close(offset.median_recovered_offset_interaction, 0.2326527194151899, 1e-12)

# Superseded artefacts must be absent from canonical directories but present in archive.
legacy_names = [
    'fig03_positive_control_injection.pdf',
    'fig_selection_stress_heterogeneity_Q.pdf',
    'fig_selection_null_recovery_harmonized.pdf',
    'selection_null_simulation_draws_harmonized.csv',
    'selection_null_simulation_harmonized.csv',
]
for name in legacy_names:
    if any((ROOT / d / name).exists() for d in ['figures', 'results/tables']):
        raise AssertionError(f'Superseded artefact remains canonical: {name}')
legacy_index = pd.read_csv(ROOT / 'metadata/legacy_v1_5_0_index.csv')
if len(legacy_index) < 9:
    raise AssertionError('Legacy index incomplete')
for rel in legacy_index.archived_path:
    if not (ROOT / rel).exists():
        raise AssertionError(f'Missing archived file: {rel}')

# Canonical indices cover canonical outputs exactly.
table_index = pd.read_csv(ROOT / 'metadata/table_index.csv')
indexed_tables = set(table_index.file)
actual_tables = {
    p.relative_to(ROOT).as_posix() for p in (ROOT / 'results/tables').iterdir()
    if p.is_file() and p.suffix.lower() in {'.csv', '.json'}
}
if indexed_tables != actual_tables:
    raise AssertionError(f'Table index mismatch: missing={sorted(actual_tables-indexed_tables)} extra={sorted(indexed_tables-actual_tables)}')
figure_index = pd.read_csv(ROOT / 'metadata/figure_index.csv')
indexed_figures = set(figure_index.file)
actual_figures = {p.relative_to(ROOT).as_posix() for p in (ROOT / 'figures').iterdir() if p.is_file()}
if indexed_figures != actual_figures:
    raise AssertionError(f'Figure index mismatch: missing={sorted(actual_figures-indexed_figures)} extra={sorted(indexed_figures-actual_figures)}')

# No private paths in current release text files.
for path in ROOT.rglob('*'):
    if not path.is_file() or path.suffix.lower() == '.pdf' or 'archive' in path.parts:
        continue
    rel = path.relative_to(ROOT).as_posix()
    if rel in {'metadata/file_manifest_sha256.csv', 'docs/verification_report.txt', 'checks/verify_release.py'}:
        continue
    text = path.read_text(encoding='utf-8', errors='ignore')
    if re.search(r'[A-Za-z]:\\(?:Users|ProgramData|Downloads|Desktop)\\', text):
        raise AssertionError(f'Private absolute path in {rel}')

# Manifest integrity.
manifest = pd.read_csv(ROOT / 'metadata/file_manifest_sha256.csv')
excluded = {'metadata/file_manifest_sha256.csv', 'docs/verification_report.txt'}
for row in manifest.itertuples(index=False):
    path = ROOT / row.relative_path
    if not path.exists():
        raise AssertionError(f'Manifest missing file: {row.relative_path}')
    if path.stat().st_size != int(row.size_bytes) or digest(path) != row.sha256:
        raise AssertionError(f'Manifest mismatch: {row.relative_path}')
current = {
    p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*')
    if p.is_file() and p.relative_to(ROOT).as_posix() not in excluded
}
listed = set(manifest.relative_path)
if current != listed:
    raise AssertionError(f'Manifest membership mismatch missing={sorted(current-listed)} extra={sorted(listed-current)}')

placeholder = []
for rel in ['README.md', 'RELEASE_NOTES.md', 'CITATION.cff', 'codemeta.json', 'metadata/zenodo_metadata.json', 'metadata/release_summary.json', 'metadata/version_lineage.json']:
    if '10.5281/zenodo.TBD' in (ROOT / rel).read_text(encoding='utf-8'):
        placeholder.append(rel)

print('PASS: v1.7.0 consolidated release verified.')
print(f'Root: {ROOT}')
print(f'Files verified: {len(manifest)}')
print(f'Canonical tables: {len(actual_tables)}')
print(f'Canonical figures: {len(actual_figures)}')
print(f'Archived historical files indexed: {len(legacy_index)}')
if placeholder:
    print('WARNING: reserved DOI placeholder remains in ' + ', '.join(placeholder))
