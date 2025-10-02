"""
Benchmark Runner for Sorting Algorithms (run_all.py)
-------------------------------------------------
Loads pre-generated CSV data, runs each sort in parallel processes,
collects timing results, estimates ETAs based on past runs,
and returns a rectangular matrix of results for all algorithms and sizes.
Accepts a status_callback to report progress to a GUI or CLI context.
"""

import os
import multiprocessing
import time as time_mod
import pandas as pd
from sort import bubble_sort, insertion_sort, merge_sort, quick_sort, radix_sort


def sort_proc(idx, func_name, data, result_queue):
    """
    Process target that runs a single sorting function on a copy of the data.
    - idx: index of the sort in the master list
    - func_name: name of the sort to invoke from sort module
    - data: NumPy array of values to sort
    - result_queue: multiprocessing.Queue to return (idx, elapsed, error)
    """
    start = time_mod.time()
    try:
        # Lookup and execute the sort implementation
        func = getattr(__import__('sort'), func_name)
        func(data.copy())
        elapsed = time_mod.time() - start
        # Return successful timing
        result_queue.put((idx, elapsed, None))
    except Exception as e:
        # On error, send exception string
        result_queue.put((idx, None, str(e)))


def run(data_sizes, status_callback=None, timeout_sec=1200, poll_interval=3):
    """
    Run benchmarks for all sort algorithms over the specified data sizes.
    Steps:
    1. For each size, load CSV into NumPy array.
    2. Pre-estimate and skip any sort whose ETA > 21 minutes.
    3. Launch each remaining sort in its own Process.
    4. Poll every poll_interval seconds, report live status and ETA.
    5. Collect results from the queue, updating previous_timings.
    6. Terminate any hung processes after timeout_sec.
    7. Pad the time_record list so every algorithm has an entry per size.

    Returns:
        sort_names: list of algorithm names
        time_record: list of lists [algorithm][size_index]
    """
    # Ensure a status_callback is always callable
    if status_callback is None:
        status_callback = print
    # Internal cache of previous timings for this run (only smaller sizes)
    previous_timings = {}
    # Helper to format ETA: seconds <60 as 'x.xs', >=60 as 'x.xm'
    def fmt_eta(seconds):
        try:
            sec = float(seconds)
        except Exception:
            return "N/A"
        # Format as minutes and seconds
        if sec >= 60:
            mins = int(sec // 60)
            rem = sec % 60
            return f"{mins}m {int(rem)}s"
        else:
            return f"{sec:.1f}s"
    # Inline ETA estimation using theoretical complexity and prior smaller-size timings
    import math
    complexity_map = {
        'Bubble': 'quadratic', 'Insertion': 'quadratic',
        'Merge': 'nlogn', 'Quick': 'nlogn', 'Radix': 'linear'
    }
    def estimate_eta(name, size, elapsed):
        # Exact previous timing
        prev = previous_timings.get((name, size))
        if prev is not None and prev > 0:
            return max(0.0, prev - elapsed)
        # Scale from smaller-size timings
        comp = complexity_map.get(name)
        best = None
        for (n, s), t in previous_timings.items():
            if n != name or t is None or t <= 0 or s >= size:
                continue
            # Determine scale factor
            if comp == 'quadratic':
                factor = (size / s) ** 2
            elif comp == 'nlogn':
                factor = (size * math.log2(size)) / (s * math.log2(s))
            else:
                factor = size / s
            total = t * factor
            eta_val = max(0.0, total - elapsed)
            if best is None or eta_val < best:
                best = eta_val
        return best

    # Determine absolute path to 'data' folder (sibling of this module)
    module_dir = os.path.dirname(__file__)
    data_dir = os.path.abspath(os.path.join(module_dir, '..', 'data'))

    # Define the algorithms and their function names
    sort_names = ['Bubble', 'Insertion', 'Merge', 'Quick', 'Radix']
    sort_funcs = ['bubble_sort', 'insertion_sort', 'merge_sort', 'quick_sort', 'radix_sort']

    # List to collect timing results per algorithm
    time_record = [[] for _ in sort_names]

    for size in data_sizes:
        # Load data CSV from absolute data_dir
        csv_path = os.path.join(data_dir, f'output_{size}.csv')
        # Fallback: perhaps data folder under CWD
        if not os.path.isfile(csv_path):
            alt_path = os.path.join(os.getcwd(), 'data', f'output_{size}.csv')
            if os.path.isfile(alt_path):
                csv_path = alt_path
            else:
                status_callback(f"Data file not found for size {size}: tried {csv_path} and {alt_path}")
                for rec in time_record:
                    rec.append(None)
                continue
        try:
            data = pd.read_csv(csv_path, usecols=['data_value'])['data_value'].to_numpy()
            status_callback(f"Loaded data size={size} from {csv_path}, N={len(data)}")
        except Exception as e:
            status_callback(f"Error loading data {size}: {e}")
            # Append None for all sorts and skip this size
            for rec in time_record:
                rec.append(None)
            continue

        # Initialize process trackers and result queue
        processes = [None] * len(sort_names)
        start_times = [None] * len(sort_names)
        skip_sort = [False] * len(sort_names)
        result_queue = multiprocessing.Queue()

        # Pre-check ETA to skip long sorts
        for idx, name in enumerate(sort_names):
            eta = estimate_eta(name, size, 0)
            if eta and eta > timeout_sec * 0.9:  # skip if likely to exceed timeout
                status_callback(f"Skipping {name}, ETA {fmt_eta(eta)} > {timeout_sec}s")
                skip_sort[idx] = True
                time_record[idx].append(None)

        # Start each non-skipped sort in its own process
        for idx, func_name in enumerate(sort_funcs):
            if skip_sort[idx]:
                continue
            status_callback(f"Starting {sort_names[idx]} sort for N={size}")
            p = multiprocessing.Process(target=sort_proc, args=(idx, func_name, data, result_queue))
            processes[idx] = p
            start_times[idx] = time_mod.time()
            p.start()

        # Polling loop: check running sorts and report ETA
        while True:
            alive = [i for i, p in enumerate(processes) if p and p.is_alive()]
            if not alive:
                break  # all done
            # Gather status (including skipped) for each sort
            status_parts = []
            for idx in range(len(sort_names)):
                if skip_sort[idx]:
                    status_parts.append(f"{sort_names[idx]}: skipped")
                elif idx in alive:
                    elapsed = time_mod.time() - start_times[idx]
                    eta = estimate_eta(sort_names[idx], size, elapsed)
                    eta_str = fmt_eta(eta)
                    # Format elapsed using fmt_eta for consistent Xm Ys or X.Ys
                    elapsed_str = fmt_eta(elapsed)
                    status_parts.append(f"{sort_names[idx]}: {elapsed_str} (ETA {eta_str})")
                # finished sorts are omitted in running status
            status_callback(f"N={size} running: {'; '.join(status_parts)}")
            time_mod.sleep(poll_interval)

        # Collect results from queue
        started = [i for i, p in enumerate(processes) if p]
        received = set()
        for _ in started:
            idx, elapsed, error = result_queue.get(timeout=5)
            if error:
                status_callback(f"Error in {sort_names[idx]}: {error}")
                time_record[idx].append(None)
            else:
                # Display completion elapsed time via fmt_eta
                elapsed_str = fmt_eta(elapsed)
                status_callback(f"{sort_names[idx]} done in {elapsed_str}")
                time_record[idx].append(elapsed)
                # update ETA history
                previous_timings[(sort_names[idx], size)] = elapsed

        # Ensure padding: if any algorithm didn't start, append None
        for idx in range(len(sort_names)):
            if len(time_record[idx]) < len(time_record[0]):
                time_record[idx].append(None)

    # No working-dir changes were made; no need to restore cwd

    # Final padding: guarantee shape [algorithms][data_sizes]
    for rec in time_record:
        while len(rec) < len(data_sizes):
            rec.append(None)

    return sort_names, time_record


# end of run_all.py
