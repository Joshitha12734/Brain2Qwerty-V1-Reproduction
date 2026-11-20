# Reproduction commands and prerequisites

The commands below describe the workflow used by the community bundle. They
are documented for transparency; this student repository does not currently
contain all required inputs.

## 1. Prepare the environment

From the repository root on Ubuntu/WSL:

```bash
bash scripts/install_reproduce_env.sh
```

The script creates a local `.venv-reproduce` environment and builds KenLM
0.3.0 with `MAX_ORDER=10`.

## 2. Run the main-gate workflow

The community launcher is:

```bash
PYTHON=.venv-reproduce/bin/python bash scripts/reproduce_verified_main_gate.sh
```

**This command will not run successfully from this student repository alone.**
The launcher references the decoder implementation, five held-out prediction
CSV inputs, and a language-model binary that are not all included here. Obtain
those artifacts from their upstream source and confirm their current terms
before attempting a reproduction.

## Local status

Environment setup and raw ensemble generation were completed on the student's
WSL Ubuntu laptop. Language-model decoding did not finish locally. See
[reproduction status](reproduction-status.md) for the details.
