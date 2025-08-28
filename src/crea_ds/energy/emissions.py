
from __future__ import annotations
import pandas as pd
EF={"coal_MW":0.9,"gas_MW":0.4,"oil_MW":0.8,"nuclear_MW":0.0,"wind_MW":0.0,"solar_MW":0.0,"hydro_MW":0.0}
def hourly_emissions(mix: pd.DataFrame)->pd.DataFrame:
    d=mix.copy()
    for col,ef in EF.items():
        if col in d.columns: d[f"{col}_tCO2"]= d[col]*ef/1000.0
    co2=[c for c in d.columns if c.endswith("_tCO2")]
    d["CO2_tonnes"]= d[co2].sum(axis=1)
    d["generation_MWh"]= d[[c for c in d.columns if c.endswith("_MW")]].sum(axis=1)
    return d
def daily_agg(d: pd.DataFrame)->pd.DataFrame:
    g=d.set_index("datetime").resample("D").agg({"CO2_tonnes":"sum","generation_MWh":"sum"}).reset_index()
    g["CO2_kt"]= g["CO2_tonnes"]/1000.0
    g["intensity_g_per_kWh"]= (g["CO2_tonnes"]*1e6)/(g["generation_MWh"]*1000)
    return g
