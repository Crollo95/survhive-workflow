# Configuration Guide for SurvHive Workflow

This document explains how to set up and configure the `config.yaml` file for the SurvHive Snakemake workflow.

## 1️⃣ Creating a Configuration File
Before running the workflow, copy the example configuration file and modify it as needed:
```bash
cp config/config.yaml.example config/config.yaml
```

## 2️⃣ Dataset Configuration
The `datasets` section defines datasets that will be processed. Each dataset requires a **source** and, if necessary, a file path.

### Dataset Entry Format
```yaml
datasets:
  dataset_name:
    source: survset  # Must be either 'survset' or 'external'
    file_path: "path/to/dataset.csv"  # Only required for 'external' datasets
```

- **`source` must be `survset` or `external`** (case-insensitive):
  - `survset`: The dataset is from the **SurvSet** repository.
  - `external`: The dataset is a CSV file (requires `file_path`).
- **For `external` datasets, `file_path` must be specified.**
- **For `survset` datasets, `file_path` must NOT be provided.**
- Any other value for `source` will trigger an error.

### Example Configuration
```yaml
datasets:
  lung_cancer:
    source: survset
  clinical_study:
    source: external
    file_path: "data/clinical_study.csv"
```

## 3️⃣ Model Selection
Define which survival models should be used for training and evaluation.

```yaml
models:
  - CoxPH
  - RSF
  - DeepHitSingle
```

You can comment out models you do not want to use.

## 4️⃣ Feature Naming Conventions
To ensure consistency, datasets should follow these column conventions:
- **Mandatory Columns:**
  - `pid`: Unique identifier for patients or samples
  - `event`: Binary event indicator (1 = event occurred, 0 = censored)
  - `time`: Time-to-event or censoring
- **Feature Columns:**
  - `num_`: Prefix for numerical features
  - `fac_`: Prefix for categorical features

## 5️⃣ Running the Workflow
Once `config.yaml` is set up, execute Snakemake:
```bash
snakemake --use-conda --cores <n>
```
Where `<n>` is the number of CPU cores to allocate.

## 6️⃣ Troubleshooting
- Ensure `source` is correctly set (`survset` or `external`).
- If using `external`, verify that `file_path` is correct.
- Use `snakemake --use-conda --dry-run` to test the configuration before execution.

For further details, refer to the main `README.md`. 🚀

