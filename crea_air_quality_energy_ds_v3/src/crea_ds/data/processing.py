
from __future__ import annotations
import pandas as pd, numpy as np
from .utils import add_time_features

def load_air_quality(path: str)->pd.DataFrame:
    df=pd.read_csv(path, parse_dates=["datetime"])
    need=["NO2_ugm3","PM25_ugm3","temperature_C","wind_speed_ms","humidity_pct","rain_mm"]
    for c in need:
        if c not in df.columns: raise ValueError(f"Missing column: {c}")
    return df

def preprocess(df: pd.DataFrame, pollutant="NO2_ugm3")->pd.DataFrame:
    d=add_time_features(df)
    # robust clip
    q1,q99=d[pollutant].quantile([0.01,0.99]).tolist()
    d[pollutant]=d[pollutant].clip(q1,q99)
    # impute per station/hour median then ffill/bfill
    d=d.sort_values(["station_id","datetime"])
    med=d.groupby(["station_id","hour"])[pollutant].transform("median")
    d[pollutant]=d[pollutant].fillna(med).groupby(d["station_id"]).ffill().bfill()
    return d

def build_matrix(d: pd.DataFrame, pollutant: str):
    feats=["temperature_C","wind_speed_ms","humidity_pct","rain_mm","hour","dow","month","dayofyear","is_weekend"]
    X= pd.concat([d[feats].reset_index(drop=True),
                  pd.get_dummies(d["station_id"], prefix="st", drop_first=True).reset_index(drop=True)], axis=1).fillna(0)
    y=d[pollutant].reset_index(drop=True)
    return X,y
