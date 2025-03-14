import os
import sys
import yaml
import pandas as pd
from SurvSet.data import SurvLoader

def validate_columns(df, ds_name):
    """
    Validate that the dataframe `df` has:
      - Required columns: 'pid', 'event', 'time'
      - All other columns start with either 'fac_' or 'num_'
    """
    required = {'pid', 'event', 'time'}
    df_columns = set(df.columns)
    
    # Check that all required columns are present.
    missing = required - df_columns
    if missing:
        print(f"Warning: Dataset '{ds_name}' is missing required columns: {missing}", file=sys.stderr)
        return False
    
    # Check that every column besides the required ones starts with 'fac_' or 'num_'
    for col in df.columns:
        if col in required:
            continue
        if not (col.startswith("fac_") or col.startswith("num_")):
            print(f"Warning: Dataset '{ds_name}' column '{col}' does not start with 'fac_' or 'num_'", file=sys.stderr)
            return False
    return True



def get_valid_datasets(config_path=None):
    """
    Validate and merge SurvSet and external datasets.
    
    - SurvSet datasets are read from the datasets_list_path (specified in the config) and validated using SurvLoader.
    - External datasets are read from the config file (under 'datasets') and validated by checking that their file paths exist.
    
    Additionally, each dataset is loaded to check that it contains the required columns and that all other columns start
    with 'fac_' or 'num_'.
    """
    
    # Load configuration.
    if config_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, "..", "config", "config.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # Get the SurvSet datasets list file path from the config.
    list_path = config.get("datasets_list_path", "datasets_list.txt")
    try:
        with open(list_path, "r") as f:
            survset_names = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Warning: {list_path} not found. No SurvSet datasets will be processed.", file=sys.stderr)
        survset_names = []

    valid_survset_datasets = []
    loader = SurvLoader()
    for ds in survset_names:
        if ds in loader.df_ds['ds'].values and ds not in loader.df_ds['ds'][loader.df_ds.is_td].values:
            try:
                df = loader.load_dataset(ds)['df']
                if validate_columns(df, ds):
                    valid_survset_datasets.append(ds)
            except Exception as e:
                print(f"Warning: Could not load dataset '{ds}' for column validation: {e}", file=sys.stderr)
        else:
            print(f"Warning: Dataset '{ds}' not available or is time-dependent in SurvSet.", file=sys.stderr)
    
    valid_external_datasets = []
    for ds_name, ds_info in config.get("datasets", {}).items():
        if ds_info.get("source", "").lower() == "external":
            file_path = ds_info.get("file_path", "")
            if file_path and os.path.exists(file_path):
                try:
                    df = pd.read_csv(file_path)
                    if validate_columns(df, ds_name):
                        valid_external_datasets.append(ds_name)
                except Exception as e:
                    print(f"Warning: Could not load external dataset '{ds_name}' from file '{file_path}': {e}", file=sys.stderr)
            else:
                print(f"Warning: External dataset '{ds_name}' with file_path '{file_path}' not found. Skipping.", file=sys.stderr)
    
    # Merge both lists.
    return valid_survset_datasets + valid_external_datasets

if __name__ == "__main__":
    datasets = get_valid_datasets()
    print("\n".join(datasets))
