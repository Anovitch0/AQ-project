from __future__ import annotations
from pathlib import Path
import subprocess, sys

def main():
    home = Path(__file__).with_name("dashboard") / "Home.py"
    print(f"[crea-ds-dashboard] launching: {home}")
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(home)], check=False)
