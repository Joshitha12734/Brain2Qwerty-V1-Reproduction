# 🧠 Brain2Qwerty V1 — S5 Experiment Details

<p align="center">
  <img alt="Subject S5" src="https://img.shields.io/badge/Subject-S5-7c3aed?style=for-the-badge"/>
  <img alt="Records" src="https://img.shields.io/badge/Test%20records-57-0891b2?style=for-the-badge"/>
  <img alt="Decoder" src="https://img.shields.io/badge/Decoder-KenLM%209--gram-16a34a?style=for-the-badge"/>
</p>

This page documents the single-subject S5 Track B run in more detail. For the complete project background, dataset description, workflow, code excerpts, comparison with the paper, and limitations, see the [main repository README](../../README.md).

## 1. Dataset and inputs

Brain2Qwerty V1 uses the SpanishBCBL dataset collected by the Basque Center on Cognition, Brain and Language (BCBL). The full dataset includes MEG/EEG recordings and behavioural information. **This S5 Track B run did not process the raw recordings.** It used supplied, frozen, sentence-level prediction CSVs for S5.

The five input files were:

- gate005_full_test.csv
- late_soup_test.csv
- seed101_e10_test.csv
- seed202_e26_test.csv
- l2reg_seed404_e6_test.csv

Each file contained 57 S5 records. Sentence UIDs were checked for alignment before the ensemble was formed.

## 2. Ensemble and decoding

Ensemble recipe: **gate005_late_s101_s202_l2e6_675_10_10_10_025**

~~~python
weights = {
    "gate005": 0.675,
    "late": 0.100,
    "seed101": 0.100,
    "seed202": 0.100,
    "l2e6": 0.025,
}
~~~

The weighted prediction outputs were then decoded using a Spanish character-level 9-gram KenLM model.

| Decoder parameter | Value |
|:--|--:|
| Beam size | 200 |
| Maximum labels | 10 |
| LM weight | 2.05 |
| Space bias | 0.0 |
| Repeat penalty | -0.05 |
| Acoustic weight | 1.0 |
| Logit temperature | 1.0 |
| Workers | 4 for full run |

## 3. Verified S5 results

| Metric | Raw ensemble | After KenLM | Absolute improvement |
|:--|--:|--:|--:|
| **CER** | 42.0490% | **38.0195%** | **4.0295 percentage points** |
| **WER** | 77.4123% | **69.2836%** | **8.1287 percentage points** |

Relative error reduction: **9.59% CER** and **10.50% WER**.

The metrics were independently recomputed from the 57-row output and agree with the decoder summary.

## 4. Comparison context

| Reference | Scope | CER | WER |
|:--|:--|--:|--:|
| Original paper — MEG mean | 19-participant cohort mean | ~29.0% | Not a headline value |
| Original paper — median MEG participant | Median participant | ~38.0% | Not reported |
| V1 beta release reference | 19 subjects / 521 records | 29.0964% | 56.0564% |
| **Our S5 result** | **1 subject / 57 records** | **38.0195%** | **69.2836%** |

Our CER is close numerically to the paper's approximate median participant CER, but it is not an exact participant-level match. The paper's mean and the 19-subject beta reference are broader aggregates, so this comparison is contextual rather than strictly apples-to-apples.

## 5. Output files

- **final_lm_predictions.csv:** final LM-decoded predictions for 57 S5 records.
- **raw_ensemble_predictions.csv:** raw ensemble predictions before KenLM.
- **decode_grid_summary.csv:** decoder settings and aggregate decoded metrics.
- **raw_ensemble_summary.csv:** aggregate raw ensemble metrics.

## 6. Scope and limitations

- This is S5 only; no all-subject run was performed.
- The workflow uses supplied frozen prediction CSVs.
- The neural network was not retrained, and no fresh inference was run on raw brain recordings.
- The full 19-subject paper benchmark was not reproduced.

## References

- Lévy, J., Zhang, M., Pinet, S. et al. (2026). *Noninvasive decoding of typed sentences from human brain activity.* Nature Neuroscience 29, 2438–2444. [DOI](https://doi.org/10.1038/s41593-026-02303-2)
- [Official Brain2Qwerty implementation](https://github.com/facebookresearch/brain2qwerty)
- [SpanishBCBL dataset](https://huggingface.co/datasets/bcbl190626/SpanishBCBL)
- [V1 beta prediction bundle](https://huggingface.co/farmakohealth/brain2qwerty-v1-beta)

**Data-sharing note:** these CSVs contain sentence-level participant data. Public sharing must be consistent with participant consent, ethics approval, and dataset terms.
