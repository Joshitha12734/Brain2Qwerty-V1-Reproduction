# Brain2Qwerty V1 — S5 Reproduction Results

## Scope
Track B checkpoint-based reproduction using the provided frozen prediction checkpoints for **S5 only**. This is not full model training and does not represent all 19 subjects.

## Dataset and ensemble
- Subject: S5
- Prediction records: 57
- Checkpoints: 5
- Ensemble weights:
  - gate005: 0.675
  - late: 0.100
  - seed101: 0.100
  - seed202: 0.100
  - l2e6: 0.025

## Decoder configuration
- Language model: Spanish character-level 9-gram KenLM
- Beam size: 200
- Maximum labels: 10
- LM weight: 2.05
- Space bias: 0.0
- Repeat penalty: -0.05
- Acoustic weight: 1.0
- Logit temperature: 1.0

## Verified aggregate results

| Metric | Raw ensemble | After KenLM |
|---|---:|---:|
| CER | 42.0490% | 38.0195% |
| WER | 77.4123% | 69.2836% |

Absolute improvement:
- CER: 4.0295 percentage points
- WER: 8.1287 percentage points

Metrics were independently recomputed from the 57-row S5 prediction files and agree with the decoder summary.

## Files
- `raw_ensemble_summary.csv`: aggregate raw ensemble summary.
- `decode_grid_summary.csv`: aggregate language-model decoding summary.
- `raw_ensemble_predictions.csv`: per-record raw ensemble output (to be added).
- `final_lm_predictions.csv`: per-record LM-decoded output (to be added).

## Data-sharing note
The prediction CSVs include sentence-level participant data. Keep this repository private or share those files only if the study consent and ethics approval explicitly permit public release.
