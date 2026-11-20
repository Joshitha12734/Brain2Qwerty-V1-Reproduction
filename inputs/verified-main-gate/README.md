# Verified Main-Gate Decoder Inputs

The community release describes these as the frozen held-out prediction inputs
used for its headline decoder result:

`CER_LM=0.29096357106460957`

The release says these files are derived from the public SpanishBCBL benchmark
pipeline and are included in its bundle to reproduce the reported decoder score.

Expected files referenced by the reproduction launcher:

- `gate005_full_test.csv`: full 521-row frozen gate input.
- `late_soup_test.csv`: late soup component predictions.
- `seed101_e10_test.csv`: readout-rank-8 seed 101 component predictions.
- `seed202_e26_test.csv`: readout-rank-8 seed 202 component predictions.
- `l2reg_seed404_e6_test.csv`: L2-regularized seed 404 component predictions.
- `selected_subject_adapters_only_test.csv`: 251-row adapter audit export.

**These CSV files are not included in this student repository.** Their
redistribution terms and provenance have not been independently cleared here.
Raw SpanishBCBL MEG recordings are also not included.
