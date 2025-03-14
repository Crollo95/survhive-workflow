rule evaluate_model:
    input:
        results = lambda wc: expand(
            os.path.join(RESULTS_DIR, "{dataset}", "{model}", "cv_results.pkl"),
            dataset=[wc.dataset], model=config.get("models", ["CoxPH"])
        ),
        data = os.path.join(DATA_DIR, "{dataset}", "preprocessed_data.pkl")
    output:
        os.path.join(RESULTS_DIR, "{dataset}", "evaluation.csv")
    params:
        dataset = "{dataset}"
    log:
        os.path.join(LOGS_DIR, "evaluate_model", "{dataset}.log")
    conda:
        COMMON_CONDA_ENV
    shell:
        f"python {os.path.join(SCRIPTS_DIR, 'evaluate_model.py')} --input_dir {RESULTS_DIR} --data_dir {DATA_DIR} --output {RESULTS_DIR} > {{log}} 2>&1"
