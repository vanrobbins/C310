"""
Random Data Generation for Sorting Benchmarks
--------------------------------------------
Generates random integer data and saves as CSV files for each specified data size.
Intended for use by the Sorting Algorithm Comparator project.
"""

import random
import pandas as pd
import os

def gen_data(data_size, status_callback=None):
    """
    Generate random integer data for each size in data_size.
    Saves each as output_<size>.csv in the data/ directory.
    status_callback: function to receive status messages (optional)
    """
    curr_dir = os.getcwd()
    os.chdir(os.path.join(curr_dir, "data"))  # Use os.path.join for portability
    for size in data_size:
        if status_callback:
            status_callback(f"Generating data for size {size}...")
        output = []
        for i in range(size):
            add_int = random.randint(0, 2147483647)
            output.append(add_int)
        series = pd.Series(output)
        df = pd.DataFrame(series)
        cus_head = ["data_value"]
        df.to_csv('output_' + str(size) + '.csv', index=True, header=cus_head)
    os.chdir(curr_dir)  # Return to original directory
# gen_data will only run if called explicitly, not on import
