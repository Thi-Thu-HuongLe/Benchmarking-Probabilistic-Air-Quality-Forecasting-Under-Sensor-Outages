# Reproducibility record

Companion to **Benchmarking Probabilistic Air-Quality Forecasting Under Sensor Outages**.
This document separates core code, the saved-result archive, and fresh experiments.
The immutable deposition is available at
[doi:10.5281/zenodo.23486862](https://doi.org/10.5281/zenodo.23486862).
Local documentation edits do not automatically update the remote GitHub repository.

For an importable archive citation, use [CITATION.bib](CITATION.bib). This DOI
identifies the archived code/data/results deposit, not a published journal article.

## Scientific scope and chronology

The benchmark uses seven Houston--Harris County U.S. EPA AQS stations and five pollutants.
Training uses 2021--2023; validation, selection and calibration use 2024; the same-network
temporal holdout uses 2025, with a 168-hour embargo. Ten learned implementations use five
seeds each; two deterministic baselines use one run each (52 evaluations total).

The development-selected IGNNK-style + TCN is a statistical reference, not a proposed
winning model or an exact reproduction of IGNNK. The benchmark framing was amended after
development and before the 2025 download, not prospectively preregistered. Technical
amendments document loader repairs before inference and an analysis-path repair after
all 52 evaluations, before inspection of saved metric/prediction contents. No checkpoint,
calibration factor, primary endpoint, reference, or test family is changed in this release.

The natural audit retains the historical field name `core_comissingness`. Its rule
detects absence of any recorded core reading under the frozen eligibility conditions;
it does not require all three core channels to be monitored at a station. There are
eight 6-hour and four 24-hour core-reporting station-origin cases. Six and three,
respectively, occur at station 48-201-0058 with PM2.5-only support. These counts do not
identify simultaneous three-channel failures or verified hardware/communications faults.

## Two complementary distributions

| Distribution | Contents | What it supports |
| --- | --- | --- |
| Core code folder | Houston code, prepared data, protocols, tests, historical environment inventory, archive verifier | Code inspection, integrity checks, fresh development runs |
| Companion saved-result ZIP | Original source/provenance dependencies, prepared data, checkpoints, calibration, predictions, per-run/summary metrics and development histories | Read-only verification and inspection of the actual reported artifacts |

The core folder excludes paper figures/tables, manuscripts, saved run results and
paper-asset generation scripts. Those run results belong to the separate archive.
The archive also excludes publication figures/tables and paper-asset generation code.
Its machine-readable metric CSVs are original experiment outputs, not formatted paper tables.

Archive name: `houston_saved_results_20261020.zip`.
The checksum, byte size and successful local audit are recorded in
[`reproducibility/saved_results_bundle.json`](reproducibility/saved_results_bundle.json).
**Public archive:** [Zenodo, doi:10.5281/zenodo.23486862](https://doi.org/10.5281/zenodo.23486862).
Published 20 October 2026; both ZIPs and six supporting files are downloadable without
authentication or an access request. The result ZIP is 544,987,907 bytes (544.99 MB);
the archived core-code ZIP is 4,349,033 bytes (4.35 MB), including prepared inputs.
The record has no separately assigned version string or Git release tag; use this
record-specific DOI and the file checksums to identify the release.

On 20 October 2026, all eight files were downloaded without authentication and
matched the Zenodo MD5 checksums. Both ZIPs also matched the pre-deposition SHA-256
identities. The read-only check is recorded in
[zenodo_public_download_verification.json](reproducibility/zenodo_public_download_verification.json).
Creator metadata in that dated snapshot may precede later author-name corrections.

The ZIPs are byte-preserved pre-deposition snapshots. Some enclosed documents state
that deposition was pending when they were packaged; the published DOI and current
documentation supersede that access-status statement. Subsequent documentation edits
do not change the historical source/protocol/prediction bytes. Do not replace the
published ZIPs merely to insert their own DOI or add the large ZIP to the code tree.

## Saved-result verification: no training or holdout execution

Python 3.10+ and its standard library are sufficient. No PyTorch installation is needed.

```powershell
python scripts/verify_saved_archive.py PATH/TO/houston_saved_results_20261020.zip
```

Alternatively, extract into a new empty directory and run:

```powershell
python verify_saved_archive.py .
```

Do not extract over an existing experiment directory. The verifier also accepts an
extracted directory path from the core repository. Check the ZIP against its accompanying
`SHA256SUMS` before extraction; `BUNDLE_MANIFEST.json` checks the internal payload.

The verifier checks:

- Every archived payload file against its manifest SHA-256.
- The latest applicable source-hash mapping, with documented freeze/amendment transitions.
- Historical input hashes and all six final analysis-output hashes.
- All 52 holdout completion records and 50 learned development histories.
- Byte identity of all 52 holdout calibration arrays with their development originals.
- All 192 stored summary rows against the per-run seed means (96 calibration pairs).
- Unchanged point-error/scored-target counts between calibration states and the presence
  of the same 44 saved primary contrasts.

It never imports experiment modules, deserializes checkpoints, reads concentration arrays,
executes inference, fits calibration, rescores labels or reruns bootstrap/DM/Holm tests.
PASS establishes artifact integrity and stored-value consistency, not independent
scientific replication or a new validation of the scoring implementation.

## How saved results map to the manuscript

Files below are under `Code/experiment_protocol/results_third/holdout_2025/analysis/`
inside the archive:

| Saved artifact | Interpretation and reporting use |
| --- | --- |
| `primary_reference_tests.csv` | 44 origin-first paired contrasts, stored effect intervals and DM/Holm values; primary comparisons and Table S1 |
| `test_metrics_per_run.csv` | Stored outcomes by model, seed, condition and calibration state; seed dispersion |
| `test_metrics_summary.csv` | Station-condition descriptive averages; all controlled conditions and 96 before/after calibration pairs |
| `natural_case_counts.csv` | Frozen gap counts; join with `prepared_holdout/availability.csv` for channel support, not inferred hardware failure causes |
| `benchmark_summary.json` | Original benchmark-level audit counts and interpretation rule |
| `analysis_manifest.json` | Input and six final output identities |

Development `history.json` and `complete.json` support selected epochs, parameter counts
and optimization trajectories. Saved prediction archives are included for inspection
but were not rescored during packaging. Origin-first primary means and station-condition
descriptive means are different estimands; do not substitute one for the other.
Counts may include repeated targets across interventions, not independent observations.

The separate manuscript-source package contains its reporting-only script and input
manifest. To regenerate that reporting revision, keep those sources intact and point
`reporting/revise_saved_results.py --project-root` at the extracted archive containing
`Code/`. That optional formatting script is not in this core folder. Its pollutant-
coverage plot uses the previously rounded pollutant table; it is not a new full-precision
pollutant rescoring pipeline.

## Historical environment versus installation requirements

[`reproducibility/historical_holdout_environment.json`](reproducibility/historical_holdout_environment.json)
is a byte-preserved copy of the holdout execution inventory, not a new `pip freeze`:
Python 3.12.14; PyTorch 2.11.0+cu130; CUDA 13.0; Windows 11; RTX 3090, 24 GiB.
The JSON contains all recorded package versions. It documents the holdout run, not proof
of the exact environment of every development run or a validated dependency lock.
Do not infer a CPU model name from its processor-family identifier.

Current installation supports Python 3.10--3.12:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
python -m pytest -q
```

The broad dependency ranges in `pyproject.toml` do not guarantee historical numerical
identity. The saved-result verifier does not depend on these packages.

## Fresh development, separate from the archived evidence

```powershell
python scripts/run_journal_development.py --stage plan --protocol journal_protocol/third_comparison_protocol.json
.\scripts\run_houston_development.ps1 -Device cuda:0 -OutputRoot experiment_protocol\reproduction
```

The plan reads development data only; the runner refuses to overwrite an existing output
directory. CPU or another GPU index can be selected. Fresh optimization is not expected
to reproduce checkpoint bytes or scores exactly. Freeze-generation scripts are historical
provenance tools, not instructions to relabel fresh results as archived ones.

The core folder uses Git text-line-ending rules, whereas historical freezes refer to
original bytes. Verify historical source identity inside the ZIP's `Code/` snapshot,
not against a line-ending-normalized checkout. Superseded source hashes remain in
historical records; the applicable technical amendments explain their transitions.

Houston 2025 has already been evaluated and its labels are public. Do not tune models,
thresholds, reference selection or calibration against it. A fresh rerun on that period
is not new independent confirmation. No holdout execution is part of this release process.

## Attribution

The measurements originate from U.S. EPA AQS; see [DATA.md](DATA.md) for the source,
filtering and public-data reuse information. The software uses [LICENSE](LICENSE).
Author-created results and documentation in the deposition are licensed CC BY 4.0;
the EPA measurements retain their public-domain status. The deposition's `LICENSES.txt`
defines these scopes. Cite the archive as Le, T.-T.-H., Cho, J., and Kim, H. (2026),
*Reproducibility for Benchmarking Probabilistic Air-Quality Forecasting Under Sensor
Outages*, Zenodo, https://doi.org/10.5281/zenodo.23486862.
The paper's scoped conclusions concern a single network and temporal period, not
validated geographic transfer or observed hardware reliability.
