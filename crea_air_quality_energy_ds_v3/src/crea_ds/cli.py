# src/crea_ds/cli.py
from __future__ import annotations
from pathlib import Path
import typer, pandas as pd, numpy as np

from .data.processing import load_air_quality, preprocess
from .modeling.deweather import fit_fast, apply as apply_model
from .modeling import report_tools as rpt
from .energy.emissions import hourly_emissions, daily_agg
from .viz.energy_plots import ts, stack_daily

app = typer.Typer(add_completion=False)

IMAGES_DIR = Path("images")
PROCESSED_DIR = Path("data/processed")

def _ensure_dirs():
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

@app.command()
def deweather(
    input_path: str = "data/raw/air_quality_long.csv",
    pollutant: str = "NO2_ugm3",
):
    """
    Déweathering multi-stations + figures (overview, par ville, cycles, diagnostics)
    """
    _ensure_dirs()
    df = load_air_quality(input_path)
    df = preprocess(df, pollutant)

    model, feat = fit_fast(df, pollutant)
    out = apply_model(df, model, pollutant=pollutant)
    out["residual"] = out[pollutant] - out["deweathered"]

    # Sauvegarde data
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out.to_csv(PROCESSED_DIR / "air_quality_deweathered.csv", index=False)

    # Overview (moyenne toutes stations)
    ov = (
        out.groupby("datetime", as_index=False)[[pollutant, "deweathered"]]
        .mean()
    )
    rpt.plot_deweathered(ov, pollutant, IMAGES_DIR / "deweathered_overview.png")
    rpt.plot_cycle(out, "hour", pollutant, IMAGES_DIR / "cycle_hour.png")
    rpt.plot_cycle(out, "dow", pollutant, IMAGES_DIR / "cycle_dow.png")

    # Diagnostics : résidu vs météo (si colonnes présentes)
    diag_cols = [
        ("temperature_C", "°C"),
        ("wind_speed_ms", "m/s"),
        ("humidity_pct", "%"),
        ("rain_mm", "mm"),
    ]
    for col, unit in diag_cols:
        if col in out.columns:
            rpt.scatter(
                out[col],
                out["residual"],
                f"{col} ({unit})",
                "Résidu (obs - deweathered)",
                f"Résidu vs {col}",
                IMAGES_DIR / f"residual_vs_{col}.png",
            )

    # Par station (supposées être des noms de villes)
    for city, sub in out.groupby("station_id"):
        safe = str(city).replace("/", "_")
        rpt.plot_deweathered(
            sub, pollutant, IMAGES_DIR / f"deweathered_{safe}.png"
        )
        rpt.plot_cycle(
            sub, "hour", pollutant, IMAGES_DIR / f"diurnal_{safe}.png"
        )
        rpt.plot_cycle(
            sub, "dow", pollutant, IMAGES_DIR / f"weekly_{safe}.png"
        )

    typer.echo("Deweathering done.")

@app.command()
def energy(input_path: str = "data/raw/eu_power_mix_long.csv"):
    """
    Figures énergie (CO2/jour, rolling 7j, intensité, stack mix journalier)
    """
    _ensure_dirs()
    mix = pd.read_csv(input_path, parse_dates=["datetime"])

    hour = hourly_emissions(mix)
    day = daily_agg(hour)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    day.to_csv(PROCESSED_DIR / "eu_emissions_daily.csv", index=False)

    # Stack des générations (agrégé en journalier)
    mix_d = (
        mix.set_index("datetime").resample("D").sum().reset_index()
    )
    stack_daily(mix_d, IMAGES_DIR / "eu_generation_stack.png")

    # Séries CO2 (brut + rolling 7j) + intensité
    ts(day, "CO2_kt", "EU Power CO₂ (kt/jour)", IMAGES_DIR / "eu_co2_daily.png")
    ts(
        day.assign(CO2_kt=day["CO2_kt"].rolling(7, min_periods=1).mean()),
        "CO2_kt",
        "EU Power CO₂ — moyenne mobile 7j",
        IMAGES_DIR / "eu_co2_daily_rolling.png",
    )
    ts(
        day,
        "intensity_g_per_kWh",
        "Intensité carbone (g/kWh)",
        IMAGES_DIR / "eu_intensity_daily.png",
    )
    typer.echo("Energy done.")

if __name__ == "__main__":
    app()
