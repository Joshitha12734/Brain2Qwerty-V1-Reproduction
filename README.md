# Brain2Qwerty V1 – Reproduction Study

A student research reproduction study for **Track B: EEG-to-Text Generation**. This repository records the setup, experiments, observations, and limitations encountered while attempting to reproduce the Brain2Qwerty V1 decoding workflow.

> **Current status:** The reproduction environment and raw ensemble stage were completed locally. The language-model decoding stage did not finish on the available laptop, so the final reproduction is still pending.

## Research background

Brain2Qwerty investigates decoding typed sentences from non-invasive brain recordings. The research paper describes a MEG-based Spanish typed-sentence task. This study examines the decoding pipeline and its reproducibility; it is **not** a Hindi imagined-speech experiment.

## Track B objective

1. Set up the reproduction environment.
2. Prepare the supplied prediction inputs.
3. Generate the raw ensemble predictions.
4. Run language-model decoding with KenLM.
5. Compare the reproduced metrics with the release's documented reference result.

## Local environment

- Windows Subsystem for Linux (Ubuntu)
- Python 3.12 in a dedicated virtual environment
- KenLM 0.3.0
- Intel Core i5-8265U laptop CPU
- Approximately 8 GB physical system RAM

## Progress

| Stage | Status |
|---|---|
| Ubuntu and Python setup | Completed |
| Reproduction virtual environment | Completed |
| KenLM installation | Completed |
| Raw ensemble generation | Completed |
| Language-model decoding | Pending |
| Final verified reproduction | Pending |

The local raw ensemble stage generated **521 rows across 19 subjects**. The subsequent language-model decoding run was interrupted after taking an extended time on the available CPU. Therefore, the reference CER/WER below must not be interpreted as results independently reproduced in this study.

## Reference metrics from the community release

The community bundle documents these held-out reference metrics:

- **CER_LM:** 0.29096357106460957
- **WER_LM:** 0.560563820633256

CER is character error rate, not accuracy; lower is better. These are reported reference values, not independently verified results from the local run.

## Sources and acknowledgements

- Research paper: *Noninvasive decoding of typed sentences from human brain activity*, Nature Neuroscience (2026). [DOI: 10.1038/s41593-026-02303-2](https://doi.org/10.1038/s41593-026-02303-2)
- Original research code: [facebookresearch/brain2qwerty](https://github.com/facebookresearch/brain2qwerty)
- Community reproduction bundle: [farmakohealth/brain2qwerty-v1-beta](https://huggingface.co/farmakohealth/brain2qwerty-v1-beta)

The community bundle identifies its release as **CC BY-NC 4.0** and describes modifications made by Farmako Health. Original authors, community contributors, and the SpanishBCBL dataset creators must receive appropriate attribution. Dataset and upstream-code terms also apply. This repository does not claim ownership of those materials or imply endorsement by Meta, BCBL, or Farmako Health.

## Repository scope

This repository is intended to document the student reproduction process. Large model weights, the 6+ GB language-model binary, raw recordings, credentials, private data, and third-party artifacts whose redistribution terms have not been checked are intentionally excluded.

See [docs/reproduction-status.md](docs/reproduction-status.md) for the detailed local run status and limitations.
