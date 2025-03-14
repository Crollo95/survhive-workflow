# Standardized Snakemake Workflow for Survival Analysis

This repository provides a **Snakemake-based workflow** for survival analysis using datasets from **SurvSet** and external CSV files. The workflow automates data preprocessing, model training, cross-validation, and evaluation using survival models from **SurvHive**.

## 🚀 Overview
This workflow follows Snakemake best practices and ensures reproducibility across different computational environments. It allows users to:
- Load survival datasets (SurvSet or external sources)
- Preprocess and split the data
- Perform cross-validation with multiple survival models
- Evaluate model performance using the Concordance Index
- Generate a final report summarizing results

## 🛠️ Installation & Dependencies
To run this workflow, you need:
- **Snakemake** (v7.0+)
- **Conda** (to manage dependencies)

### Install Snakemake & Conda
If not installed, set up **Miniconda** and Snakemake:
```bash
conda install -c conda-forge mamba  # Faster Conda environment management
mamba create -n snakemake_env -c conda-forge snakemake
conda activate snakemake_env
```

### ⚠️ First-Time Setup Warning
During the **first run**, Snakemake will create Conda environments for different survival models, which may take some time due to the number of required dependencies. Once built, subsequent runs will be much faster.

## 📂 Repository Structure
```
├── config/                 # Configuration files
│   ├── config.yaml.example # Example configuration file
│   ├── README.md           # Configuration guide
├── data/                   # Input datasets (ignored in Git)
├── logs/                   # Log files (ignored in Git)
├── results/                # Processed outputs
├── scripts/                # Python scripts for preprocessing & training
├── workflow/               # Snakemake rules and pipeline logic
│   ├── Snakefile           # Main Snakemake workflow
│   ├── rules/              # Individual Snakemake rule definitions
│   ├── envs/               # Conda environments (optional)
├── .snakemake/             # Snakemake cache (ignored in Git)
├── .snakemake-workflow-catalog.yml  # Snakemake catalog metadata
├── .gitignore              # Ignore unnecessary files
└── README.md               # This document
```

## ⚙️ Configuring the Workflow
Before running, create a **custom configuration file**:
```bash
cp config/config.yaml.example config/config.yaml
```
Edit `config/config.yaml` to specify:
- **Datasets** (SurvSet or external CSVs)
- **Models** to use for training
- **Dataset structure** (Required columns: `pid`, `event`, `time`)

## ▶️ Running the Workflow
Once configured, execute Snakemake:
```bash
snakemake --use-conda --cores <n>
```
- `<n>`: Number of CPU cores (e.g., `--cores 4`)
- Use `--configfile config/config.yaml` to specify a custom config file

### Running a Specific Rule
```bash
snakemake --use-conda preprocess_and_split
```

## 📖 References & Citations
This workflow is built upon the following frameworks and datasets:

- **SurvHive**: A package for survival model optimization and evaluation.  
  **Citation:** Birolo, Giovanni, et al. "SurvHive: a package to consistently access multiple survival-analysis packages." arXiv preprint arXiv:2502.02223 (2025).  
  **GitHub:** [SurvHive Repository](https://github.com/compbiomed-unito/survhive)

- **SurvSet**: An open-source time-to-event dataset repository.  
  **Citation:** Drysdale, Erik. "SurvSet: An open-source time-to-event dataset repository." arXiv preprint arXiv:2203.03094 (2022).  
  **GitHub:** [SurvSet Repository](https://github.com/ErikinBC/SurvSet)

---
For additional support, refer to the **config README** (`config/README.md`) or contact the workflow maintainer. 🚀

