
# CREA — Air Quality & Energy (Advanced v3)
- Déweathering multi-stations (baseline linéaire rapide + code ML plus poussé prêt à l'emploi).
- Tracker CO₂ secteur électrique (émissions, intensité g/kWh, mix).
- Beaucoup de figures pré-générées (overview, par-ville, cycles, diagnostics, énergie).

## Exécution rapide (facultative)
```bash
pip install -e .
python -m crea_ds deweather   # génère data/processed + figures
python -m crea_ds energy      # figures énergie
```
