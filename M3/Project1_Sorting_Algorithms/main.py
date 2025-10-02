"""
Main module for Sorting Algorithm Comparator
-------------------------------------------
Provides functions to:
- Generate random data CSVs for various sizes
- Run sorting benchmarks (single-run or averaged) with status callbacks
- Export timing results to CSV
- Plot timing results with theoretical baselines
- Launch the Tkinter GUI for interactive use

Data flow:
1. `gen_data` uses `data/rand_data.py` to generate CSVs.
2. `run` calls `sorting_algorithms/run_all.py` to execute benchmarks in parallel.
3. Results are padded and exported via pandas DataFrame.
4. `gen_graph` reads a CSV and plots empirical curves with O(n²) and O(n log n) baselines.
5. `start` sets up sys.path and launches `GUI/gui.py`.

All long-running operations accept an optional `status_callback(msg)` to report progress.
"""

import os
import sys
import multiprocessing

# Deep imports deferred to within functions for better startup performance

data_sizes = (1000, 10000, 100000, 1000000, 10000000)


def _concat_status(msg, sort_name=None, size=None, elapsed=None):
    """
    Helper to format a status message with optional context:
    - msg: primary message text
    - sort_name: name of the algorithm (optional)
    - size: data size (optional)
    - elapsed: elapsed time in seconds (optional)
    """
    msg_str = str(msg)
    parts = [msg_str]
    # Only append size if not already present
    if size and not (msg_str.startswith(str(size)) or f"{size}:" in msg_str):
        parts.append(f"Size: {size}")
    if sort_name:
        parts.append(f"Sort: {sort_name}")
    if elapsed is not None:
        # Display elapsed as seconds with two decimals
        if isinstance(elapsed, (int, float)):
            parts.append(f"Elapsed: {elapsed:.2f}s")
        else:
            parts.append(f"Elapsed: {elapsed}")
    # Join parts with separator for readability
    return ' | '.join(parts)


def gen_data(status_callback=None):
    """
    Generate random data CSV files for each size in `data_sizes`.
    Calls into `data/rand_data.py`.
    Reports progress via status_callback.
    """
    from data import rand_data as rand  # local import

    def status_cb(msg, *args, **kwargs):
        # Wrap to enforce a single-argument callback
        if status_callback:
            status_callback(_concat_status(msg, *args, **kwargs))

    # Delegate to rand_data module
    rand.gen_data(data_sizes, status_callback=status_cb)


def run(file_path=None, status_callback=None):
    """
    Run a single series of sorting benchmarks over all data_sizes.
    Exports the results to CSV at `file_path` (defaults to timing_results.csv).
    Reports status updates via status_callback.

    Returns None. Results are written to disk.
    """
    from sorting_algorithms import run_all as tests
    import pandas as pd

    # Wrap callback to include context formatting
    def status_cb(msg, sort_name=None, size=None, elapsed=None, *_, **__):
        if status_callback:
            status_callback(_concat_status(msg, sort_name, size, elapsed))

    # Notify start
    status_cb("run() called")
    # Execute benchmarks in parallel
    status_cb("Starting benchmarks...")
    # Collect only the first two return values (ignoring any extras)
    run_ret = tests.run(
        data_sizes,
        status_callback=status_cb
    )
    sort_names = run_ret[0]
    results = run_ret[1]
    status_cb("Benchmark execution completed")

    # Ensure result structure is rectangular: pad or truncate to len(data_sizes)
    num_cols = len(data_sizes)
    for row in results:
        # Pad with None if missing
        while len(row) < num_cols:
            row.append(None)
        # Truncate if too long
        if len(row) > num_cols:
            del row[num_cols:]

    # Save to CSV via pandas DataFrame
    df = pd.DataFrame(results, index=sort_names, columns=data_sizes).T
    if not file_path:
        file_path = "timing_results.csv"
    df.to_csv(file_path, index=True, header=True, index_label="Data Size")
    status_cb(f"Timing results exported to {file_path}")


def run_average(file_path=None, runs=5, status_callback=None):
    """
    Run all sorting benchmarks multiple times (default 5),
    save both raw and averaged results to CSV files.
    file_path: where to save averaged results (raw results get _raw.csv)
    status_callback: function to receive status messages (optional)
    """
    from sorting_algorithms import run_all as tests
    import numpy as np
    import pandas as pd
    # Wrap callback
    def status_cb(msg, sort_name=None, size=None, elapsed=None, *_, **__):
        if status_callback:
            status_callback(_concat_status(msg, sort_name, size, elapsed))
    all_results = []
    # Perform multiple runs using the same run() semantics
    for i in range(runs):
        def run_status(msg, sort_name=None, size=None, elapsed=None, run_num=i+1, *_, **__):
            prefix = f"[Run {run_num}/{runs}] "
            status_cb(prefix + str(msg), sort_name, size, elapsed)
        status_cb(f"Starting run {i+1} of {runs}...")
        # Call run() without external timing cache
        sort_names, results = tests.run(
            data_sizes,
            status_callback=run_status
        )
        all_results.append(results)
    # Convert to numpy array: shape (runs, algorithms, sizes)
    all_np = np.array(all_results)
    # Save raw results
    raw_path = file_path.replace('.csv', '_raw.csv') if file_path else 'timing_results_average_raw.csv'
    idx = [f"{sort_names[j]}_run{i+1}" for i in range(runs) for j in range(len(sort_names))]
    raw_data = all_np.reshape(runs * len(sort_names), len(data_sizes))
    df_raw = pd.DataFrame(raw_data, index=idx, columns=data_sizes)
    df_raw.to_csv(raw_path, index=True, header=True, index_label='Sort_Run')
    status_cb(f"Raw timing results exported to {raw_path}")
    # Save averaged results
    avg = np.mean(all_np, axis=0)
    df_avg = pd.DataFrame(avg, index=sort_names, columns=data_sizes).T
    avg_path = file_path if file_path else 'timing_results_average.csv'
    df_avg.to_csv(avg_path, index=True, header=True, index_label='Data Size')
    status_cb(f"Averaged timing results exported to {avg_path}")


def gen_graph(file_path, save_png=True, status_callback=None):
    """
    Read a timing-results CSV and plot the benchmarks.
    Overlays empirical curves (extrapolated via log-log fit) and
    theoretical O(n²) and O(n log n) baselines for comparison.
    Saves a PNG and opens it with the default system viewer.
    """
    # Report load start
    if status_callback:
        status_callback(f"Loading graph from {file_path}")

    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import os

    # Load timing data
    df = pd.read_csv(file_path, index_col=0)

    # Use a clean grid style
    plt.style.use('ggplot')
    
    # Prepare figure
    fig, ax = plt.subplots(figsize=(10, 6))
    x = df.index.values
    # Colors keyed by algorithm name
    colors = {'Bubble': 'red', 'Insertion': 'green', 'Merge': 'blue',
              'Quick': 'purple', 'Radix': 'orange'}

    # Create log-log interpolation grid
    x_logs = np.log10(x)
    x_smooth_logs = np.linspace(x_logs.min(), x_logs.max(), 300)
    x_smooth = 10 ** x_smooth_logs

    # Plot empirical trends for each algorithm
    for col in df.columns:
        y = df[col].values
        ax.scatter(x, y, facecolors=colors.get(col),
                   edgecolors='black', s=40)
        # Fit a straight line in log-log space (power-law model)
        mask = (y > 0)
        if mask.sum() >= 2:
            m, b = np.polyfit(x_logs[mask], np.log10(y[mask]), 1)
            y_smooth = (10 ** b) * (x_smooth ** m)
            ax.plot(x_smooth, y_smooth, '-',
                    color=colors.get(col), linewidth=2,
                    label=col)

    # Add theoretical baselines for context
    # Scale constants so baselines pass through first data point
    if 'Bubble' in df.columns and df['Bubble'].iloc[0] > 0:
        c2 = df['Bubble'].iloc[0] / (x[0] ** 2)
        ax.plot(x_smooth, c2 * x_smooth ** 2, '--', color='black',
                linewidth=1.5, label='O(n²)')
    if 'Merge' in df.columns and df['Merge'].iloc[0] > 0:
        cnl = df['Merge'].iloc[0] / (x[0] * np.log2(x[0]))
        ax.plot(x_smooth,
                cnl * x_smooth * np.log2(x_smooth), '--',
                color='gray', linewidth=1.5, label='O(n log n)')

    # Log-log axes so power laws become straight lines
    ax.set_xscale('log')
    ax.set_yscale('log')

    # Labels, title, and legend
    ax.set_title('Sorting Algorithm Performance')
    ax.set_xlabel('Data Size')
    ax.set_ylabel('Time (seconds, log scale)')
    ax.legend(title='Algorithm', loc='upper left')
    plt.tight_layout()

    # Save to PNG then open externally
    png_path = os.path.splitext(file_path)[0] + '_graph.png'
    fig.savefig(png_path)
    if status_callback:
        status_callback(f"Graph saved to {png_path}")
    # On Windows, attempt to open automatically
    try:
        os.startfile(png_path)
    except Exception:
        pass


def start():
    """
    Configure sys.path for submodules and launch the Tkinter GUI.
    """
    gui_folder = os.path.join(os.getcwd(), 'GUI')
    sys.path.append(gui_folder)
    alg_folder = os.path.join(os.getcwd(), 'sorting_algorithms')
    sys.path.append(alg_folder)
    data_folder = os.path.join(os.getcwd(), 'data')
    sys.path.append(data_folder)
    from GUI import gui  # launches mainloop


if __name__ == '__main__':
    start()