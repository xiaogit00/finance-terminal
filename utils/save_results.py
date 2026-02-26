import os
from datetime import datetime

def save_results(ticker, start, end, hyper_param_str, results_csv):
    """
    Saves the results of the backtest as CSV so that it can be used again.

    :param ticker: ticker of the data
    :param start: start date, must be in format "2015-01-01"
    :param end: end date, must be in format "2015-01-01"
    :param hyper_param_str: a string that encapsulates the hyperparams used for this run e.g. '3d'
    :param results_csv: Pandas dataframe; within my context, the values stored in backtest_object.results
    """
    results_dir = "backtest_df"

    os.makedirs(results_dir, exist_ok=True)
    run_id = datetime.now().strftime("%d%b%y").upper()
    result_path = os.path.join(results_dir, f"{start}_to_{end}_{ticker}_{hyper_param_str}_{run_id}.csv")
    results_csv.to_csv(result_path)
    
    print(f"Results saved to {result_path}")