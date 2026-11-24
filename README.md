# 🧠 Brain2Qwerty V1 — Checkpoint-Based Reproduction

<p align="center">
  <strong>Decoding typed sentences from non-invasive brain activity</strong><br/>
  A focused reproduction of the released Brain2Qwerty V1 prediction-and-decoding pipeline.
</p>

<p align="center">
  <img alt="Track B" src="https://img.shields.io/badge/Track-B%20%7C%20Checkpoint%20Reproduction-2563eb?style=for-the-badge"/>
  <img alt="Subject" src="https://img.shields.io/badge/Subject-S5-7c3aed?style=for-the-badge"/>
  <img alt="Records" src="https://img.shields.io/badge/Records-57-0891b2?style=for-the-badge"/>
  <img alt="Status" src="https://img.shields.io/badge/Decoding-Completed-16a34a?style=for-the-badge"/>
</p>

> **Scope:** Track B uses supplied frozen checkpoint predictions, a weighted ensemble, and KenLM decoding. It does **not** retrain Brain2Qwerty or run fresh neural-network inference from raw brain recordings.

---

## ✨ Results at a glance

Our S5-only run evaluated **57 records**. KenLM decoding reduced both character and word error rates.

| Metric | Raw ensemble | After KenLM | Absolute improvement |
|:--|--:|--:|--:|
| **Character Error Rate (CER)** ↓ | 42.0490% | **38.0195%** | **4.0295 pp** |
| **Word Error Rate (WER)** ↓ | 77.4123% | **69.2836%** | **8.1287 pp** |

**Relative error reduction:** 9.59% CER · 10.50% WER

Lower error rates are better. Values were independently recomputed from the 57-row output and agree with the decoder summary.

### 📊 S5: before vs. after language-model decoding

| Metric | Raw ensemble | After KenLM |
|:--|:--|:--|
| CER | 42.05% | **38.02%** |
| WER | 77.41% | **69.28%** |

---

## 🔬 Comparison with published and released references

These comparisons provide context, but they are **not identical evaluation settings**.

| Reference | Evaluation scope | CER | WER |
|:--|:--|--:|--:|
| **Original paper — MEG** | Cohort mean reported in the paper | **29.0%** | Not reported as a headline result |
| **Original paper — median MEG participant** | Median of 19 MEG participants (Fig. 3) | **38.0%** | Not reported |
| **V1 beta bundle reference** | 19-subject / 521-record held-out release summary | **29.0964%** | **56.0564%** |
| **This reproduction — S5** | One subject / 57 records, after KenLM | **38.0195%** | **69.2836%** |

### How to interpret this comparison

- The paper reports a **29% cohort-average MEG CER**. Its Figure 3 describes the median MEG participant at approximately **38% CER**.
- Our S5 CER of **38.0195%** is numerically close to that reported median participant value. This is a contextual comparison, **not proof of an exact subject-level match**.
- The V1 beta bundle's 19-subject reference is a broader aggregate than our S5-only evaluation. S5 has higher error rates than that aggregate.
- The paper's headline result is CER; a directly comparable headline WER is not provided here.
- Differences in cohort aggregation, split, prediction release, and evaluation scope mean these values should not be treated as a strict apples-to-apples benchmark.

**Takeaway:** The S5 run shows a measurable benefit from language-model decoding, while its single-subject performance remains distinct from the 19-subject aggregate.

---

## ⚙️ Reproduction configuration

**Ensemble recipe:** `gate005_late_s101_s202_l2e6_675_10_10_10_025`

| Checkpoint input | Weight |
|:--|--:|
| gate005 | 0.675 |
| late | 0.100 |
| seed101 | 0.100 |
| seed202 | 0.100 |
| l2e6 | 0.025 |

| Decoder parameter | Value |
|:--|--:|
| Language model | Spanish character-level 9-gram KenLM |
| Beam size | 200 |
| Maximum labels | 10 |
| LM weight | 2.05 |
| Space bias | 0.0 |
| Repeat penalty | −0.05 |
| Acoustic weight | 1.0 |
| Logit temperature | 1.0 |

## 📁 S5 result files

All generated S5 outputs are available in [`results/S5/`](results/S5/).

| File | Description |
|:--|:--|
| [Final LM predictions](results/S5/final_lm_predictions.csv) | 57 sentence-level records after KenLM decoding |
| [Raw ensemble predictions](results/S5/raw_ensemble_predictions.csv) | 57 sentence-level records before KenLM |
| [Decoding summary](results/S5/decode_grid_summary.csv) | Decoder configuration and aggregate metrics |
| [Raw ensemble summary](results/S5/raw_ensemble_summary.csv) | Raw ensemble aggregate metrics |
| [S5 README](results/S5/README.md) | Detailed experiment settings and results |

## 🧭 Workflow

1. Selected the five supplied frozen prediction files for **S5 only**.
2. Checked that the five inputs aligned on the 57 S5 sentence records.
3. Combined checkpoint predictions using the fixed weighted recipe.
4. Built KenLM with support for the supplied 9-gram model.
5. Ran a one-record pilot before the complete S5 decoding.
6. Decoded all 57 S5 records with the specified configuration.
7. Independently recomputed aggregate CER and WER and saved the outputs.

## 📌 What this reproduction does — and does not — claim

**Completed**
- Checkpoint-based weighted ensemble for S5.
- KenLM 9-gram decoding for all 57 S5 records.
- Raw-versus-decoded evaluation.
- Saved prediction files and aggregate summaries.

**Outside this Track B run**
- Training the Brain2Qwerty neural network from scratch.
- Fresh inference from raw EEG/MEG recordings.
- Reproducing all 19 participants or the complete paper benchmark.
- Claiming an exact reproduction of the paper's cohort-level 29% CER.

## 📚 References and attribution

1. Lévy, J., Zhang, M., Pinet, S. et al. **Noninvasive decoding of typed sentences from human brain activity.** *Nature Neuroscience* 29, 2438–2444 (2026). [https://doi.org/10.1038/s41593-026-02303-2](https://doi.org/10.1038/s41593-026-02303-2)
2. Original research implementation: [facebookresearch/brain2qwerty](https://github.com/facebookresearch/brain2qwerty)
3. Checkpoint and decoding bundle used in this Track B workflow: [farmakohealth/brain2qwerty-v1-beta](https://huggingface.co/farmakohealth/brain2qwerty-v1-beta)

The community bundle identifies its release as **CC BY-NC 4.0**. Please review the upstream code, dataset, and model-artifact terms before redistribution. This repository does not claim ownership of third-party materials or endorsement by the paper authors, Meta, BCBL, or Farmako Health.

## 🔐 Data-sharing note

The S5 prediction CSVs contain sentence-level participant data. Their public availability should be consistent with the study's participant consent, ethics approval, and applicable data-sharing conditions. If public sharing is not authorized, make this repository private or remove the sentence-level CSVs.

---

<p align="center">
  <strong>Track B · S5 · 57 records · Weighted ensemble + KenLM</strong><br/>
  <sub>Reproduction results, configuration, and limitations documented for transparency.</sub>
</p>
