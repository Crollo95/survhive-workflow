def read_valid_datasets(file_path):
    """Read valid dataset names from the provided file path."""
    with open(file_path, "r") as f:
        datasets = [line.strip() for line in f if line.strip()]
    return datasets

def build_extra_args(dataset, config):
    ds_conf = config.get("datasets", {}).get(dataset, {})
    source = ds_conf.get("source", "survset").lower()  # Convert to lowercase
    
    if source not in ["survset", "external"]:
        raise ValueError(f"Invalid source '{source}' for dataset {dataset}. Must be 'survset' or 'external'.")
    
    if source == "external":
        file_path = ds_conf.get("file_path", "")
        return f"--external --file_path {file_path}" if file_path else "--external"
    
    return ""  # Default is SurvSet