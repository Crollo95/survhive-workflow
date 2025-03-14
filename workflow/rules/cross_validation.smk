rule cross_validation:
    input:
        os.path.join(DATA_DIR, "{dataset}", "preprocessed_data.pkl")
    output:
        os.path.join(RESULTS_DIR, "{dataset}", "{model}", "cv_results.pkl"),
        os.path.join(RESULTS_DIR, "{dataset}", "{model}", "opt_params.json"),
        os.path.join(RESULTS_DIR, "{dataset}", "{model}", "df_search_results.csv")
    params:
        dataset = "{dataset}",
        model = "{model}",
        output_dir = lambda wildcards, output: os.path.dirname(output[0]) 
    log:
        os.path.join(LOGS_DIR, "cross_validation", "{dataset}_{model}.log")
    conda:
        COMMON_CONDA_ENV
    shell:
        (
            f"python {os.path.join(SCRIPTS_DIR, 'cross_validation.py')} "
            f"--dataset {{params.dataset}} --model {{params.model}} --seed 42 "
            f"--output_dir {{params.output_dir}} "
            f"--n_trials {config.get('n_trials', 10)} > {{log}} 2>&1"
        )