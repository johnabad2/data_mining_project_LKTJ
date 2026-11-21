"""Execute the visible machine-learning notebook using this Python environment.

Run: python src/machine_learning.py
Use --all to execute the original exploration notebook first as well.
The analysis itself remains visible in notebooks/02_machine_learning.ipynb.
"""

import argparse
import hashlib
from pathlib import Path
import sys

import nbformat
from jupyter_client import KernelManager
from nbclient import NotebookClient


def execute_notebook(path):
    notebook = nbformat.read(path, as_version=4)
    manager = KernelManager(kernel_name="python3")
    # Use the invoking environment, even if a global Jupyter kernel exists.
    manager.kernel_spec.argv = [
        sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}",
    ]
    client = NotebookClient(
        notebook, km=manager, timeout=1800,
        resources={"metadata": {"path": str(path.parent)}},
    )
    print(f"Executing {path.name} ...", flush=True)
    # A supplied kernel manager is not owned by nbclient; request cleanup explicitly.
    client.execute(cleanup_kc=True)
    nbformat.write(notebook, path)
    print(f"Saved executed {path.name}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="Run both notebooks.")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    data_paths = sorted((root / "data").rglob("*.csv"))
    before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in data_paths}
    paths = [root / "notebooks" / "02_machine_learning.ipynb"]
    if args.all:
        paths.insert(0, root / "notebooks" / "01_data_exploration.ipynb")
    try:
        for path in paths:
            execute_notebook(path)
    finally:
        for path, digest in before.items():
            if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                raise RuntimeError(f"Dataset bytes changed during execution: {path}")
    print("Both dataset SHA-256 checks passed.", flush=True)


if __name__ == "__main__":
    main()
