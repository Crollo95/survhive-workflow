# Configuration Guide for the Snakemake Workflow of SurvHive

This document provides details on how to configure the workflow using `config/config.yaml`. The configuration file specifies dataset sources, preprocessing settings, and models to be used for survival analysis.

## Configuration File Location

The main configuration file is located at:
```
config/config.yaml
```

Before running the workflow, you must create a `config.yaml` file.  
Use the provided template and copy it:

```bash
cp config/config.yaml.example config/config.yaml
```

Users can specify a custom configuration file using:
```bash
snakemake --use-conda --cores <n> --configfile <path_to_config>
```

## Configuration Parameters

The `config.yaml` file is structured as follows:

### 1. Dataset List File
```yaml
datasets_list_path: "datasets_list.txt"
```
- This file lists the SurvSet datasets that will be processed.
- It should be placed in the root of the project.

### 2. Datasets Definition
```yaml
datasets:
  <dataset_name>:
    source: external  # Use 'survset' for SurvSet datasets
    file_path: "<path_to_your_dataset>.csv"  # Only required for external datasets
```
- **External datasets** should be provided with an explicit file path.
- **SurvSet datasets** do not need a file path; they will be automatically loaded.
- Ensure that dataset files follow the correct format:
  - **Required columns:** `pid`, `event`, `time`
  - **Feature columns:**
    - Categorical: prefixed with `fac_`
    - Numerical: prefixed with `num_`

### 3. Models Selection
```yaml
models: ["CoxNet", "CoxPH", "DeepSurvivalMachines", "RSF", "GrBoostSA", "SurvTraceSingle", "FastCPH", "DeepHitSingle"]
```
- Specifies the models to be used in survival analysis.
- Comment out models that should not be used.

## Editing and Customization

To modify configurations:
1. Edit `config/config.yaml` using any text editor.
2. Ensure correct indentation and syntax (YAML format sensitive to spacing).
3. Save changes and run Snakemake with:
   ```bash
   snakemake --use-conda --cores <n>
   ```

## Common Issues & Debugging

- **File Not Found Errors**: Ensure dataset paths in `config.yaml` exist and are correctly formatted.
- **YAML Formatting Issues**: Use a YAML validator to check for indentation errors.
- **Model Not Found**: Ensure the model name in `config.yaml` matches the available models in the workflow.

For additional support, refer to the repository documentation or contact the workflow maintainer.

