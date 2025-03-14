import os
import argparse
import pickle
import pandas as pd
import numpy as np
import logging
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler

# Configure logging for the script.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def impute_data(X_train, X_test):
    """
    Impute missing values in both train and test datasets.
    """
    X_train = X_train.copy()
    X_test = X_test.copy()
    
    num_columns = [col for col in X_train.columns if col.startswith('num_')]
    for column in num_columns:
        fill_value = X_train[column].median() if abs(X_train[column].skew()) > 1 else X_train[column].mean()
        X_train[column] = X_train[column].fillna(fill_value)
        X_test[column] = X_test[column].fillna(fill_value)
    
    fac_columns = [col for col in X_train.columns if col.startswith('fac_')]
    logger.info("Categorical columns found: %s", fac_columns)
    if not fac_columns:
        logger.warning("No categorical columns detected in X_train!")
    for column in fac_columns:
        mode_value = X_train[column].mode()[0]
        X_train[column] = X_train[column].fillna(mode_value)
        X_test[column] = X_test[column].fillna(mode_value)
    
    return X_train, X_test


def main():
    parser = argparse.ArgumentParser(
        description="Preprocess and split raw data for a given dataset."
    )
    parser.add_argument("--dataset", required=True, help="Name of the dataset to process")
    args = parser.parse_args()
    
    raw_data_path = os.path.join("data", args.dataset, "raw_data.csv")
    out_dir = os.path.join("data", args.dataset)
    out_path = os.path.join(out_dir, "preprocessed_data.pkl")
    
    df = pd.read_csv(raw_data_path)
    df = df[~((df['event'] == 0) & (df['time'] == 0))]
    
    event = df['event'].astype(bool)
    time = df['time']
    
    X = pd.get_dummies(df.drop(['pid', 'time', 'event'], axis=1))
    y = np.array(list(zip(event, time)), dtype=np.dtype([("event", "?"), ("time", "<f8")]))
    col_names = list(X.columns)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X.astype(float), y, stratify=y["event"], random_state=0
    )
    
    time_train = y_train["time"]
    time_test = y_test["time"]
    event_train = y_train["event"]
    event_test = y_test["event"]
    
    X_train, X_test = impute_data(X_train, X_test)
    
    scaler = RobustScaler()
    X_train_norm = scaler.fit_transform(X_train)
    X_test_norm = scaler.transform(X_test)
    
    output_dict = dict(
        col_names=col_names,
        X_train=X_train_norm,
        X_test=X_test_norm,
        y_train=y_train,
        y_test=y_test,
        time_train=time_train,
        time_test=time_test,
        event_train=event_train,
        event_test=event_test,
    )
    
    with open(out_path, "wb") as f:
        pickle.dump(output_dict, f)
    
    logger.info("Preprocessing and splitting completed for dataset '%s'.", args.dataset)
    logger.info("Output saved to %s", out_path)

if __name__ == "__main__":
    main()
