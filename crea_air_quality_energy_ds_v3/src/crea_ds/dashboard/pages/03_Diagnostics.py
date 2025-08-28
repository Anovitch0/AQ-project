# src/crea_ds/dashboard/pages/03_Diagnostics.py
from __future__ import annotations
import streamlit as st
from pathlib import Path
from crea_ds.dashboard.utils import find_images_dir, safe_open_image
st.set_page_config(page_title="Diagnostics", layout="wide")
pkg_root = Path(__file__).resolve().parents[3]
img_dir = find_images_dir(pkg_root) or (pkg_root / "images")

st.title("Diagnostics — Résidu vs Météo")

names = [
    "residual_vs_temperature_C.png",
    "residual_vs_wind_speed_ms.png",
    "residual_vs_humidity_pct.png",
    "residual_vs_rain_mm.png",
]
rows = [st.columns(2), st.columns(2)]
for i, name in enumerate(names):
    p = img_dir / name
    if p.exists():
        col = rows[i//2][i%2]
        col.subheader(name.replace("_"," ").replace(".png","").title())
        col.image(safe_open_image(p), use_container_width=True)
