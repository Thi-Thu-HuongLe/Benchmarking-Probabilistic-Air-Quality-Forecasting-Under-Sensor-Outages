# Benchmarking Probabilistic Air-Quality Forecasting Under Sensor Outages

This repository contains the Houston--Harris County code, prepared public data, and
frozen protocol records for the accompanying single-network Houston benchmark. The study
evaluates ten learned implementations and two deterministic baselines under controlled
loss of recent measurements at air-quality monitoring stations.

## Scope

- U.S. EPA Air Quality System hourly data from seven Harris County stations.
- Five pollutants: PM$_{2.5}$, NO$_2$, O$_3$, CO, and SO$_2$.
- 2021--2023 model training; 2024 validation, selection, and calibration; a 2025 temporal
  holdout.
- A 168-hour input window, 48-hour forecasts, and reported leads 1, 6, 12, 24, and 48 h.
- Primary controlled outages remove the final 6 or 24 h of one target station's input
  history. Secondary analyses include random blocks, full station-history removal,
  connected three-station outages, and descriptive counts of core-reporting gaps.

The paper is a benchmark, not a proposal of a new winning model. The IGNNK-style
imputation--forecasting implementation is a reference selected using development data; it
is not an exact reproduction of IGNNK. The benchmark framing was amended after development
and before the Houston 2025 holdout was downloaded. It is not described as prospective
preregistration. See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for the chronology and limits.

## Included and excluded

The repository includes source code, Houston-specific protocol and hash records, prepared
2021--2024 development and 2025 holdout tensors, data-availability summaries, preprocessing
reports, and focused tests. EPA AQS measurements are public domain; see [DATA.md](DATA.md)
for source and reuse notes.

It excludes trained checkpoints, saved predictions, per-run metric outputs, publication
tables and figures, manuscript files, and scripts that generate those publication assets.
Fresh runs write their outputs under `experiment_protocol/`, which is ignored by Git.
The separate saved-result archive described in [REPRODUCIBILITY.md](REPRODUCIBILITY.md)
contains the immutable experiment artifacts and is publicly available on
[Zenodo](https://doi.org/10.5281/zenodo.23486862). The same record includes an archived
core-code snapshot. Download requires no login or access request.
No paper figures, result tables, or paper-illustration scripts are added to this folder.
Code is distributed under the repository's MIT license; EPA measurements remain public
domain data under the EPA reuse statement cited below.

Some source files retain historical names or compatibility branches because their bytes
are referenced by the Houston freeze/amendment chain. They are provenance dependencies,
not an active earlier-paper workflow; no Beijing, Dhaka, Salt Lake, or Las Vegas dataset is
included. `scripts/freeze_journal_candidate.py` contains only the generic run-integrity
helper imported by a Houston freeze generator. The freeze-generation scripts require
archived intermediate run artifacts that are intentionally not distributed. Later
technical amendments document the approved source-hash transitions; see
[REPRODUCIBILITY.md](REPRODUCIBILITY.md).

## Repository layout

```text
data_external/epa_aqs_houston/  Prepared Houston tensors, reports, and provenance
journal_protocol/               Houston benchmark and freeze records
scripts/                        Data preparation, training, evaluation, and analysis
src/aqriskformer/                Model, preprocessing, and evaluation implementation
tests/                           Focused implementation and protocol tests
reproducibility/                  Historical environment and companion-archive identity
```

## Installation

Python 3.10--3.12 is supported. A CUDA-enabled PyTorch installation is recommended for
the full multi-seed neural-model workflow. A CPU can run the plan command and focused tests.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

On Linux or macOS, activate the environment with `source .venv/bin/activate`.

## Verify and inspect

Verify prepared-data hashes against `DATA_SHA256SUMS`, then inspect the locked training
plan without starting a fit:

```powershell
python scripts\run_journal_development.py --stage plan `
  --protocol journal_protocol\third_comparison_protocol.json
python -m pytest -q
```

The plan command reads the development tensor only. The 2025 prepared tensor is already
included for transparency and reproducibility, but it must not be used for new model,
threshold, or calibration selection.

## Development workflow

The locked development specification and prepared development tensor are included. A fresh
multi-seed fit writes new checkpoints under the chosen output directory:

```powershell
python scripts\run_journal_development.py --stage run --device cuda:0 `
  --protocol journal_protocol\third_comparison_protocol.json `
  --output experiment_protocol\reproduction\base

python scripts\run_journal_development.py --stage run --device cuda:0 `
  --protocol journal_protocol\third_comparison_protocol.json `
  --learned-models adaptive_graph_mask_tcn fixed_graph_equal_training `
  --without-deterministic `
  --refinement-base-runs experiment_protocol\reproduction\base\runs `
  --output experiment_protocol\reproduction\refinement

python scripts\analyze_third_development.py `
  --protocol journal_protocol\third_comparison_protocol.json `
  --base-root experiment_protocol\reproduction\base `
  --refinement-root experiment_protocol\reproduction\refinement `
  --output experiment_protocol\reproduction\development_analysis
```

These commands perform new development fits; they do not reproduce the original saved
checkpoints bit-for-bit.

For a single-command development workflow, use the included PowerShell runner. It stops on
the first failed stage and refuses to overwrite an existing output directory:

```powershell
.\scripts\run_houston_development.ps1 -Device cuda:0
# Or select another available GPU, or use CPU:
.\scripts\run_houston_development.ps1 -Device cuda:2 -OutputRoot experiment_protocol\reproduction\gpu2
```

This workflow fits/analyzes development models only. It intentionally does not run the
2025 holdout; saved-result verification uses the separate archive described below.

## Holdout analysis and reproducibility limits

The 2025 holdout was evaluated once under the frozen experiment archive. The core code
folder intentionally omits checkpoints, calibration arrays, saved predictions and metrics.
A separate `houston_saved_results_20261020.zip` now packages these artifacts and their
historical provenance. Its identity and local verification report are recorded in
[`reproducibility/saved_results_bundle.json`](reproducibility/saved_results_bundle.json).
Download the ZIP and its checksums from the version-specific
[Zenodo record](https://doi.org/10.5281/zenodo.23486862). The saved-result ZIP is
544,987,907 bytes (544.99 MB); the archived core-code ZIP is 4,349,033 bytes (4.35 MB).
The published ZIPs preserve their original bytes. Any pre-deposition access-status text
inside them is historical; the DOI record and this README give the current access status.

Once the companion ZIP is available locally, verification requires only Python 3.10+
and its standard library, with no package installation or GPU:

```powershell
python scripts/verify_saved_archive.py PATH/TO/houston_saved_results_20261020.zip
```

This checks hashes and already stored metrics. It does not run inference, read
concentration arrays, fit calibration, or rerun statistical tests. The historical
holdout runner and analysis script are not part of this verification workflow.

The code and public data support inspection and fresh development experiments. A fresh
evaluation using the now-public 2025 period is a rerun of an observed holdout, not a new
independent confirmation. The study's result tables and figures are intentionally not
generated or distributed by this repository. The frozen natural audit has four 24-hour
core-reporting gaps, three at a station with only PM2.5 support; these are neither four
simultaneous three-pollutant outages nor verified hardware failures.

## Data source

Ambient air-quality measurements originate from the
[U.S. EPA Air Quality System API](https://aqs.epa.gov/aqsweb/documents/data_api.html).
The prepared data in the deposition do not require an EPA API key.

## Citation and licenses

For the deposited software, prepared inputs and saved-result artifacts, cite:

An importable BibTeX record is provided in [CITATION.bib](CITATION.bib).

Le, T.-T.-H., Cho, J., and Kim, H. (2026). *Reproducibility for Benchmarking Probabilistic
Air-Quality Forecasting Under Sensor Outages*. Zenodo.
[https://doi.org/10.5281/zenodo.23486862](https://doi.org/10.5281/zenodo.23486862).

This is the archive citation, not a claim that the accompanying manuscript has been
published. Code remains MIT-licensed; author-created results and documentation in the
archive use CC BY 4.0; EPA measurements retain their public-domain status. See the
deposition's `LICENSES.txt` for the scope of each license.

## EPA attribution

Ambient air-quality measurements originate from the U.S. EPA Air Quality System (AQS).
EPA states that AQS ambient monitoring data are public domain and may be reused without a
permission request. Cite the original AQS source and document any downstream filtering or
transformation. See [DATA.md](DATA.md) and the
[EPA AQS data page](https://www.epa.gov/outdoor-air-quality-data/do-i-need-request-permission-use-monitoring-data-and-graphics-airdata).
