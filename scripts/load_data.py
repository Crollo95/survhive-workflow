import os
import argparse
import pandas as pd
from SurvSet.data import SurvLoader

def load_survset_dataset(data_name):
    loader = SurvLoader()
    if data_name not in loader.df_ds['ds'].values:
        raise ValueError(f"{data_name} dataset is not available in SurvSet")
    if data_name in loader.df_ds['ds'][loader.df_ds.is_td].values:
        raise ValueError("Supported only for time-independent datasets")
    return loader.load_dataset(data_name)['df']

def load_external_dataset(file_path):
    return pd.read_csv(file_path)

def main():
    parser = argparse.ArgumentParser(
        description="Load a dataset from SurvSet or an external source and save it as CSV."
    )
    parser.add_argument("--dataset", required=True, help="Name of the dataset")
    parser.add_argument("--external", action="store_true", help="Flag to indicate an external dataset")
    parser.add_argument("--file_path", help="Path to the external dataset CSV")
    args = parser.parse_args()

    if args.external:
        if not args.file_path:
            raise ValueError("For external datasets, --file_path must be provided")
        df = load_external_dataset(args.file_path)
    else:
        df = load_survset_dataset(args.dataset)

    out_dir = os.path.join("data", args.dataset)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "raw_data.csv")
    df.to_csv(out_path, index=False)
    print(f"Dataset '{args.dataset}' saved to {out_path}")

if __name__ == "__main__":
    main()
