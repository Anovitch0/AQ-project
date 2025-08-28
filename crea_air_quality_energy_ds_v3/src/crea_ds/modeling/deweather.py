
from __future__ import annotations
import numpy as np, pandas as pd
from sklearn.linear_model import LinearRegression
from . import report_tools
from ..data.processing import build_matrix

def fit_fast(df: pd.DataFrame, pollutant="NO2_ugm3"):
    X,y=build_matrix(df, pollutant)
    m=LinearRegression()
    m.fit(X,y)
    return m, X.columns.tolist()

def apply(df: pd.DataFrame, model, pollutant="NO2_ugm3"):
    X,_=build_matrix(df, pollutant)
    pred=model.predict(X)
    out=df.copy()
    out["pred_met_effect"]=pred
    out["deweathered"]= out[pollutant]-out["pred_met_effect"] + float(np.mean(pred))
    return out
