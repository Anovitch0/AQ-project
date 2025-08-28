# src/crea_ds/dashboard/Home.py
from __future__ import annotations
import streamlit as st, pandas as pd
from pathlib import Path
from crea_ds.dashboard.utils import find_images_dir, safe_open_image
st.set_page_config(
    page_title="CREA — Air Quality & Energy",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -- Style léger pour un rendu clean
st.markdown("""
<style>
.block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
img { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

pkg_root = Path(__file__).resolve().parents[2]
img_dir = find_images_dir(pkg_root) or (pkg_root / "images")
data_dir = Path.cwd() / "data" / "processed"  # privilégie cwd si tu lances depuis la racine
if not data_dir.exists():
    data_dir = pkg_root / "data" / "processed"

st.title("Air Quality & Energy")
st.caption("Vue d’ensemble (déweathering + énergie). Utilise le menu de gauche pour naviguer.")

# KPIs énergie si dispo
col1, col2, col3 = st.columns(3)
csv_path = data_dir / "eu_emissions_daily.csv"
if csv_path.exists():
    d = pd.read_csv(csv_path, parse_dates=["datetime"]).sort_values("datetime")
    if len(d) > 7:
        last = d.iloc[-1]
        last7 = d.tail(7)["CO2_kt"].mean()
        prev7 = d.iloc[-14:-7]["CO2_kt"].mean() if len(d) >= 14 else None
        delta = (last7 - prev7) if prev7 is not None else 0.0
        col1.metric("CO₂ (kt/jour) — dernier point", f"{last['CO2_kt']:.0f}")
        col2.metric("CO₂ — moyenne 7j", f"{last7:.0f}", f"{delta:+.0f} vs 7j précédents")
        col3.metric("Intensité (g/kWh) — dernier point", f"{last['intensity_g_per_kWh']:.0f}")
    else:
        col1.info("CSV énergie trop court pour KPIs.")
else:
    col1.info("CSV énergie indisponible (lance `crea-ds energy`).")

st.divider()

# Grille des visuels clés
if img_dir.exists():
    c1, c2 = st.columns([1,1])
    for name, col in [
        ("deweathered_overview.png", c1),
        ("eu_co2_daily_rolling.png", c2),
    ]:
        path = img_dir / name
        if path.exists():
            col.subheader(name.replace("_", " ").replace(".png", "").title())
            col.image(safe_open_image(path), use_container_width=True)

    st.subheader("Cycles & mix")
    c3, c4, c5 = st.columns([1,1,1])
    for name, col in [
        ("cycle_hour.png", c3),
        ("cycle_dow.png", c4),
        ("eu_generation_stack.png", c5),
    ]:
        path = img_dir / name
        if path.exists():
            col.image(safe_open_image(path), use_container_width=True)
else:
    st.error("Dossier 'images/' introuvable. Lance d’abord `crea-ds deweather` et `crea-ds energy`.")
