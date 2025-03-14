rule load_data:
    input:
        validated = os.path.join(LOGS_DIR, "valid_datasets.txt")
    output:
        os.path.join(DATA_DIR, "{dataset}", "raw_data.csv")
    params:
        dataset = "{dataset}",
        extra_args = lambda wc: build_extra_args(wc.dataset, config)
    log:
        os.path.join(LOGS_DIR, "load_data", "{dataset}.log")
    conda:
        COMMON_CONDA_ENV
    #shell:
    #    f"python {os.path.join(SCRIPTS_DIR, 'load_data.py')} --dataset {{params.dataset}} {{params.extra_args}} > {{log}} 2>&1"
    shell:
        "python {script} --dataset {{params.dataset}} {{params.extra_args}} > {{log}} 2>&1".format(script=os.path.join(SCRIPTS_DIR, "load_data.py"))
