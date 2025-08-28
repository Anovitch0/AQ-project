
from __future__ import annotations
import pandas as pd
def add_time_features(df: pd.DataFrame, ts: str="datetime")->pd.DataFrame:
    d=df.copy(); t=pd.to_datetime(d[ts])
    d["hour"]=t.dt.hour; d["dow"]=t.dt.dayofweek; d["month"]=t.dt.month
    d["dayofyear"]=t.dt.dayofyear; d["is_weekend"]=d["dow"].isin([5,6]).astype(int)
    return d
