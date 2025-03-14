import os
import argparse
import pickle
import pandas as pd
import numpy as np
import logging
from survhive.metrics import concordance_index_antolini_scorer

# Configure logging to include timestamps and log levels.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

def load_pickle(file_path):
    """Load a pickle file."""
    try:
        with open(file_path, "rb") as f:
            data = pickle.load(f)
        logger.info("Loaded pickle file from %s", file_path)
        return data
    except Exception as e:
        logger.error("Failed to load pickle file %s: %s", file_path, e)
        raise

def evaluate_model(model, X_test, y_test):
    """Evaluate model on test set and compute performance metrics."""
    try:
        return concordance_index_antolini_scorer(model, X_test, y_test)
    except Exception as e:
        logger.error("Error evaluating model: %s", e)
        return np.nan  # Assign NaN if there's an error

def save_results(file_path, results):
    """Save evaluation results to a CSV file."""
    try:
        df = pd.DataFrame(results)
        df.to_csv(file_path, index=False)
        logger.info("Results saved to %s", file_path)
    except Exception as e:
        logger.error("Error saving results to %s: %s", file_path, e)
        raise

def main():
    parser = argparse.ArgumentParser(description="Evaluate survival models on test data.")
    parser.add_argument("--input_dir", required=True, help="Path to cross-validation results.")
    parser.add_argument("--data_dir", required=True, help="Path to preprocessed data.")
    parser.add_argument("--output", required=True, help="Path to save evaluation results.")
    args = parser.parse_args()
    
    overall_results = []
    
    for dataset in os.listdir(args.data_dir):
        data_path = os.path.join(args.data_dir, dataset, "preprocessed_data.pkl")
        if not os.path.exists(data_path):
            logger.warning("Preprocessed data not found for dataset: %s", dataset)
            continue
        
        data = load_pickle(data_path)
        X_test, y_test = data["X_test"], data["y_test"]
        model_dir = os.path.join(args.input_dir, dataset)
        if not os.path.exists(model_dir):
            logger.warning("Model directory not found for dataset: %s", dataset)
            continue
        
        dataset_results = []
        dataset_output_path = os.path.join(args.output, dataset, "evaluation.csv")
        os.makedirs(os.path.dirname(dataset_output_path), exist_ok=True)
        
        for model_name in os.listdir(model_dir):
            model_path = os.path.join(model_dir, model_name, "cv_results.pkl")
            if not os.path.exists(model_path):
                logger.warning("cv_results.pkl not found for model: %s in dataset: %s", model_name, dataset)
                continue
            
            model_data = load_pickle(model_path)
            model = model_data["opt_model"]
            c_index = evaluate_model(model, X_test, y_test)
            
            result_entry = {"Model": model_name, "C-Index": c_index}
            dataset_results.append(result_entry)
            overall_results.append({"Dataset": dataset, **result_entry})
            logger.info("Evaluated model %s for dataset %s: C-Index = %s", model_name, dataset, c_index)
        
        save_results(dataset_output_path, dataset_results)
        logger.info("Saved evaluation for dataset %s", dataset)
    
    final_output = os.path.join(args.output, "evaluation.csv")
    save_results(final_output, overall_results)
    logger.info("Overall evaluation completed. Results saved to %s", final_output)

if __name__ == "__main__":
    main()
