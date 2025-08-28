# src/crea_ds/dashboard/pages/01_Air_Quality_Overview.py
from __future__ import annotations
import streamlit as st
from pathlib import Path
from crea_ds.dashboard.utils import find_images_dir, safe_open_image
st.set_page_config(page_title="Air Quality — Overview", layout="wide")
pkg_root = Path(__file__).resolve().parents[3]
img_dir = find_images_dir(pkg_root) or (pkg_root / "images")

st.title("Air Quality — Overview")

names = ["deweathered_overview.png", "cycle_hour.png", "cycle_dow.png"]
cols = st.columns(3)
for name, col in zip(names, cols):
    p = img_dir / name
    if p.exists():
        col.subheader(name.replace("_", " ").replace(".png", "").title())
        col.image(safe_open_image(p), use_container_width=True)
