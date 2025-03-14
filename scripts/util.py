def read_valid_datasets(file_path):
    """Read valid dataset names from the provided file path."""
    with open(file_path, "r") as f:
        datasets = [line.strip() for line in f if line.strip()]
    return datasets

def build_extra_args(dataset, config):
    ds_conf = config.get("datasets", {}).get(dataset, {})
    if ds_conf.get("source", "survset") == "external":
        file_path = ds_conf.get("file_path", "")
        # Use an f-string to build the argument without using '+'
        return f"--external {'--file_path ' + file_path if file_path else ''}".strip()
    return ""
