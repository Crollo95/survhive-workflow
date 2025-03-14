rule preprocess_and_split:
    input:
        os.path.join(DATA_DIR, "{dataset}", "raw_data.csv")
    output:
        os.path.join(DATA_DIR, "{dataset}", "preprocessed_data.pkl")
    params:
        dataset = "{dataset}"
    log:
        os.path.join(LOGS_DIR, "preprocess_and_split", "{dataset}.log")
    conda:
        COMMON_CONDA_ENV
    #shell:
    #    f"python {os.path.join(SCRIPTS_DIR, 'preprocess_and_split.py')} --dataset {{params.dataset}} > {{log}} 2>&1"
    shell:
        "python {script} --dataset {{params.dataset}} > {{log}} 2>&1".format(script=os.path.join(SCRIPTS_DIR, "preprocess_and_split.py"))