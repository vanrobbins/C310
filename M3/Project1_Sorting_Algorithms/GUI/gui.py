"""
GUI module for Sorting Algorithm Comparator
-------------------------------------------
Defines a Tkinter-based interface to:
  - Generate random data for benchmarks
  - Run benchmarks (single or averaged) and export CSVs
  - Display timing results graphically

Long-running operations are executed in background threads,
with status_text updated via callbacks to keep the UI responsive.
"""

import tkinter as tk
from tkinter import filedialog
from main import gen_data, run, run_average, gen_graph
import style
import threading
import subprocess
import sys
import os

# Initialize main Tkinter window
root = tk.Tk()
root.title("Comparing Sorting Algorithms")
root.geometry(style.WINDOW_SIZE)
root.configure(bg=style.BG_COLOR)

# Title label setup
title_label = tk.Label(
    root,
    text="Sorting Algorithm Comparator",
    font=style.TITLE_FONT,
    bg=style.BG_COLOR,
    fg=style.LABEL_COLOR
)
title_label.pack(pady=(10, 10))

# Multi-line Text widget for displaying status messages
status_text = tk.Text(
    root,
    height=3,
    wrap='word',
    bg=style.BG_COLOR,
    fg=style.LABEL_COLOR,
    font=style.LABEL_FONT,
    bd=0,
    relief='flat'
)
status_text.tag_configure('center', justify='center')
status_text.configure(state='disabled')
status_text.bind(
    "<MouseWheel>",
    lambda e: status_text.yview_scroll(int(-1*(e.delta/120)), "units")
)
status_text.pack(pady=(5,5), fill='x', padx=10)

# Frame to hold control buttons
button_frame = tk.Frame(root, bg=style.BG_COLOR)
button_frame.pack(expand=True)


def set_status(msg):
    """
    Update the status_text widget and print to console.
    Clears existing text and inserts new center-justified message.
    """
    print(f"[GUI STATUS] {msg}")
    status_text.configure(state='normal')
    status_text.delete('1.0', 'end')
    status_text.insert('end', msg, 'center')
    status_text.configure(state='disabled')
    status_text.yview('end')
    root.update_idletasks()


def run_with_dialog():
    """
    Open file-save dialog, then run single benchmark series.
    """
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        title="Save timing results as..."
    )
    if file_path:
        threaded_action(run, "Run Tests", file_path)


def gen_data_threaded():
    """
    Run data generation in a background thread.
    Calls gen_data and updates status.
    """
    def task():
        set_status("Running Generate Data")
        try:
            gen_data(status_callback=set_status)
            set_status("Generate Data complete!")
        except Exception as e:
            set_status(f"Error during Generate Data: {e}")
    t = threading.Thread(target=task, daemon=True)
    t.start()


def run_average_with_dialog():
    """
    Open save dialog and run 5x averaged benchmark.
    """
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        title="Save averaged timing results as..."
    )
    if file_path:
        threaded_action(run_average, "Run Average (5x)", file_path)


def gen_graph_with_dialog():
    """
    Open file-open dialog and display timing graph.
    """
    file_path = filedialog.askopenfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        title="Select timing results CSV"
    )
    if file_path:
        threaded_action(gen_graph, "Show Graph", file_path)


def threaded_action(action, task_name, *args):
    """
    Helper to run a long action in a background thread.
    - action: function to call (e.g., run, gen_graph)
    - task_name: label shown in status
    - args: positional args for action

    Wraps action in try/except and provides a per-line callback.
    """
    def task():
        set_status(f"Running {task_name}")
        try:
            # Create a callback to update GUI status
            def status_cb(msg, *_, **__):
                set_status(msg)
            action(*args, status_callback=status_cb)
            set_status(f"{task_name} complete!")
        except Exception as e:
            set_status(f"Error during {task_name}: {e}")
    t = threading.Thread(target=task, daemon=True)
    t.start()

# Create and style control buttons
gen_data_btn = tk.Button(button_frame, text="Generate Data", command=gen_data_threaded)
run_test_btn = tk.Button(button_frame, text="Run Tests", command=run_with_dialog)
run_avg_btn = tk.Button(button_frame, text="Run(5x) + Average", command=run_average_with_dialog)
graph_btn = tk.Button(button_frame, text="Show Graph", command=gen_graph_with_dialog)

style.style_button(gen_data_btn)
style.style_button(run_test_btn)
style.style_button(run_avg_btn)
style.style_button(graph_btn)

gen_data_btn.pack(pady=5)
run_test_btn.pack(pady=5)
run_avg_btn.pack(pady=5)
graph_btn.pack(pady=5)

# Start the Tkinter event loop
root.mainloop()
