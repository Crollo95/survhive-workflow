import os
import argparse
import pickle
import json
import numpy as np
import logging
import survhive

# Configure logging to output timestamps and log levels.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

def load_preprocessed_data(dataset):
    """Load the preprocessed data from the pickle file."""
    data_path = os.path.join("data", dataset, "preprocessed_data.pkl")
    logger.info("Loading preprocessed data from %s", data_path)
    with open(data_path, "rb") as f:
        data = pickle.load(f)
    logger.info("Preprocessed data loaded successfully")
    return data

def main():
    parser = argparse.ArgumentParser(
        description="Cross-validate and optimize a survival model."
    )
    parser.add_argument("--dataset", required=True, help="Name of the dataset")
    parser.add_argument("--model", required=True, help="Survival model")
    parser.add_argument("--n_trials", type=int, default=10, help="Number of trials (default: 10)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--output_dir", required=True, help="Path to the output pickle file")
    args = parser.parse_args()

    # Load preprocessed training data.
    data = load_preprocessed_data(args.dataset)
    
    # Extract training features and labels.
    X_train = data["X_train"]
    y_train = data["y_train"]
    # Ensure X_train is a numpy array.
    if not isinstance(X_train, np.ndarray):
        X_train = np.array(X_train)
        logger.info("Converted X_train to numpy array")
    
    logger.info("X_train shape: %s, y_train shape: %s", X_train.shape, y_train.shape)
    
    model_name = args.model
    model_cls = getattr(survhive, model_name, None)
    if model_cls is None:
        logger.error("Model '%s' not found in survhive.", model_name)
        exit(1)
    
    model = model_cls(rng_seed=args.seed)
    
    logger.info("Starting optimization for model '%s' with n_trials=%d and seed=%d", model_name, args.n_trials, args.seed)
    # Perform optimization using random search on the default grid.
    try:
        _opt_model, _opt_model_params, _opt_model_search = survhive.optimize(
            model, X_train, y_train, 
            mode='sklearn-random',
            tries=args.n_trials, 
            n_jobs=2
        )
    except Exception as e:
        logger.exception("Error during optimization: %s", e)
        exit(1)
    
    logger.info("Optimization completed. Processing search results...")
    df_search_results = survhive.get_model_scores_df(_opt_model_search)
    logger.info("Obtained search results dataframe with shape: %s", df_search_results.shape)


   ### SAVE 
   # Create output directory if not exists
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Save best hyperparameters as JSON
    opt_params_path = os.path.join(args.output_dir, "opt_params.json")
    with open(opt_params_path, "w") as f:
        json.dump(_opt_model_params, f, indent=4)
    logger.info("Best hyperparameters saved to %s", opt_params_path)
    
    # Save cross-validation results as CSV
    search_results_path = os.path.join(args.output_dir, "df_search_results.csv")
    df_search_results.to_csv(search_results_path, index=False)
    logger.info("Search results saved to %s", search_results_path)
    
    # Save everything in cv_results.pkl
    cv_results_path = os.path.join(args.output_dir, "cv_results.pkl")
    output_dict = {
        "opt_model": _opt_model,
        "opt_params": _opt_model_params,
        "df_search_results": df_search_results,
    }
    with open(cv_results_path, "wb") as f:
        pickle.dump(output_dict, f)
    logger.info("Complete cross-validation results saved to %s", cv_results_path)
    
    logger.info("Optimization for model '%s' on dataset '%s' completed.", args.model, args.dataset)
    logger.info("Best hyperparameters: %s", _opt_model_params)

if __name__ == "__main__":
    main()
