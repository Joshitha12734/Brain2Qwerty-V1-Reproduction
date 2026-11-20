# Local reproduction status

## Environment setup

The reproduction environment was created under WSL Ubuntu using Python 3.12. The community bundle's installation script built and installed KenLM 0.3.0 with the required maximum order.

## Completed stage: raw ensemble

The official reproduction workflow produced a raw ensemble CSV with:

- 521 data rows
- 19 subjects
- Recipe: `gate005_late_s101_s202_l2e6_675_10_10_10_025`
- Raw CER: approximately 0.3433873
- Raw WER: approximately 0.7322031

These are raw ensemble metrics before language-model decoding.

## Pending stage: language-model decoding

The full decoding process was started with the release's configured parameters, including beam size 200 and maximum labels 10. It remained CPU-active for an extended period but did not complete in a reasonable time on the available laptop. The process was interrupted.

A small diagnostic benchmark was also attempted but did not complete promptly. No decoded output or final decoder summary was produced by the local run.

## Interpretation

The community release's documented held-out values (CER_LM 0.29096357106460957 and WER_LM 0.560563820633256) are reference metrics only. They must not be reported as locally reproduced results.

The work completed so far verifies environment installation and raw ensemble generation, but **does not verify the final language-model decoding result or fresh neural-network inference**.

## Hardware limitation

The local machine has an Intel Core i5-8265U CPU and approximately 8 GB physical RAM. The decoding configuration is computationally demanding on this hardware. No claim is made that CPU or memory was the sole cause of the long runtime.

## Reproduction provenance

The workflow and reference metrics were obtained from the community bundle:

https://huggingface.co/farmakohealth/brain2qwerty-v1-beta

The bundle identifies its license as CC BY-NC 4.0. Its scripts, inputs, model artifacts, and dataset are third-party materials and are not reproduced in this repository unless their redistribution terms have been checked.
