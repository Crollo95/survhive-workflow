rule cross_validation:
    input:
        os.path.join(DATA_DIR, "{dataset}", "preprocessed_data.pkl")
    output:
        os.path.join(RESULTS_DIR, "{dataset}", "{model}", "cv_results.pkl")
    params:
        dataset = "{dataset}",
        model = "{model}"
    log:
        os.path.join(LOGS_DIR, "cross_validation", "{dataset}_{model}.log")
    conda:
        COMMON_CONDA_ENV
    shell:
        (
            f"python {os.path.join(SCRIPTS_DIR, 'cross_validation.py')} "
            f"--dataset {{params.dataset}} --model {{params.model}} --seed 42 --output {{output}} --n_trials {config.get('n_trials', 10)} > {{log}} 2>&1"
        )