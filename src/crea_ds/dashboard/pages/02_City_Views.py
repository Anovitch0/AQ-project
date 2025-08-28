# src/crea_ds/dashboard/pages/02_City_Views.py
from __future__ import annotations
import streamlit as st
from pathlib import Path
from crea_ds.dashboard.utils import find_images_dir, list_cities, safe_open_image
st.set_page_config(page_title="Air Quality — Par ville", layout="wide")
pkg_root = Path(__file__).resolve().parents[3]
img_dir = find_images_dir(pkg_root) or (pkg_root / "images")

st.title("Air Quality — Par ville")

cities = list_cities(img_dir)
if not cities:
    st.info("Aucune ville détectée. Lance `crea-ds deweather` d’abord.")
else:
    city = st.sidebar.selectbox("Ville", cities)
    cols = st.columns(3)
    for name, col in [
        (f"deweathered_{city}.png", cols[0]),
        (f"diurnal_{city}.png", cols[1]),
        (f"weekly_{city}.png", cols[2]),
    ]:
        p = img_dir / name
        if p.exists():
            col.subheader(name.replace(".png","").replace("_"," ").title())
            col.image(safe_open_image(p), use_container_width=True)
