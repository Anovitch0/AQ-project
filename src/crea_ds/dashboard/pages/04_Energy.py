# src/crea_ds/dashboard/pages/04_Energy.py
from __future__ import annotations
import streamlit as st, pandas as pd
from pathlib import Path
from crea_ds.dashboard.utils import find_images_dir, safe_open_image
st.set_page_config(page_title="Énergie", layout="wide")
pkg_root = Path(__file__).resolve().parents[3]
img_dir = find_images_dir(pkg_root) or (pkg_root / "images")
data_dir = Path.cwd() / "data" / "processed"
if not data_dir.exists():
    data_dir = pkg_root / "data" / "processed"

st.title("Secteur électrique — CO₂ & mix")

top = st.columns(3)
for name, col in [
    ("eu_co2_daily.png", top[0]),
    ("eu_co2_daily_rolling.png", top[1]),
    ("eu_intensity_daily.png", top[2]),
]:
    p = img_dir / name
    if p.exists():
        col.subheader(name.replace("_"," ").replace(".png","").title())
        col.image(safe_open_image(p), use_container_width=True)

p = img_dir / "eu_generation_stack.png"
if p.exists():
    st.subheader("Mix journalier (stack)")
    st.image(safe_open_image(p), use_container_width=True)

csv_path = data_dir / "eu_emissions_daily.csv"
if csv_path.exists():
    st.subheader("Données (eu_emissions_daily.csv)")
    d = pd.read_csv(csv_path, parse_dates=["datetime"]).sort_values("datetime")
    st.dataframe(d.tail(60), use_container_width=True)
