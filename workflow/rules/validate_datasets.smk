checkpoint validate_datasets:
    output:
        os.path.join(LOGS_DIR, "valid_datasets.txt")
    log:
        os.path.join(LOGS_DIR, "validate_datasets.log")
    conda:
        COMMON_CONDA_ENV
    #shell:
    #    f"python {os.path.join(SCRIPTS_DIR, 'validate_datasets.py')} > {{output}} 2> {{log}}"
    shell:
        "python {script} > {{output}} 2> {{log}}".format(script=os.path.join(SCRIPTS_DIR, "validate_datasets.py"))
