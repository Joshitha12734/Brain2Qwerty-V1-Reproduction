# 🧠 Brain2Qwerty V1 — S5 Results

<p align="center">
  <img alt="Subject S5" src="https://img.shields.io/badge/Subject-S5-7c3aed?style=for-the-badge"/>
  <img alt="Records" src="https://img.shields.io/badge/Records-57-0891b2?style=for-the-badge"/>
  <img alt="KenLM" src="https://img.shields.io/badge/KenLM-9--gram-16a34a?style=for-the-badge"/>
</p>

## Verified results

| Metric | Raw ensemble | After KenLM | Absolute improvement |
|:--|--:|--:|--:|
| CER | 42.0490% | **38.0195%** | 4.0295 percentage points |
| WER | 77.4123% | **69.2836%** | 8.1287 percentage points |

Relative error reduction: **9.59% CER** and **10.50% WER**.

All 57 S5 records were evaluated. The aggregate values were independently recomputed from the output CSV and match the decoder summary.

## Experiment scope

This is a **Track B checkpoint-based reproduction for S5 only**. It uses supplied frozen predictions and does not train the neural network or perform fresh inference from raw brain recordings.

## Ensemble recipe

`gate005_late_s101_s202_l2e6_675_10_10_10_025`

| Checkpoint input | Weight |
|:--|--:|
| gate005 | 0.675 |
| late | 0.100 |
| seed101 | 0.100 |
| seed202 | 0.100 |
| l2e6 | 0.025 |

## Decoder configuration

| Parameter | Value |
|:--|:--|
| Language model | Spanish character-level 9-gram KenLM |
| Beam size | 200 |
| Maximum labels | 10 |
| LM weight | 2.05 |
| Space bias | 0.0 |
| Repeat penalty | −0.05 |
| Acoustic weight | 1.0 |
| Logit temperature | 1.0 |

## Comparison context

The original Brain2Qwerty paper reports a mean MEG CER of **29%** and a median MEG participant CER of approximately **38%** across 19 participants. The S5 result (38.0195%) is numerically close to the reported median, but this is a contextual comparison, not an exact subject-level replication.

The V1 beta bundle's held-out 19-subject reference reports CER **29.0964%** and WER **56.0564%**. It is an aggregate reference and is not directly comparable to a single-subject S5 result.

## Files in this folder

- `final_lm_predictions.csv`: 57 LM-decoded S5 predictions.
- `raw_ensemble_predictions.csv`: 57 raw ensemble S5 predictions.
- `decode_grid_summary.csv`: decoder settings and aggregate metrics.
- `raw_ensemble_summary.csv`: raw ensemble aggregate metrics.

## Data-sharing note

Prediction CSVs contain sentence-level participant data. Keep them public only if participant consent, ethics approval, and applicable data-sharing conditions explicitly permit public release.

## Reference

Lévy, J., Zhang, M., Pinet, S. et al. *Noninvasive decoding of typed sentences from human brain activity*. Nature Neuroscience 29, 2438–2444 (2026). [DOI: 10.1038/s41593-026-02303-2](https://doi.org/10.1038/s41593-026-02303-2).
