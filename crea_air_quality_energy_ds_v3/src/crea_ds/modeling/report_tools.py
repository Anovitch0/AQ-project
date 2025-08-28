
from __future__ import annotations
import numpy as np, pandas as pd, matplotlib.pyplot as plt
def plot_deweathered(df, pol, path):
    fig,ax=plt.subplots(figsize=(10,4))
    ax.plot(df["datetime"], df[pol], label="Observed")
    ax.plot(df["datetime"], df["deweathered"], label="Deweathered", linestyle="--")
    ax.set_title(f"Observed vs Deweathered — {pol}"); ax.set_xlabel("Date"); ax.set_ylabel(pol); ax.legend()
    fig.tight_layout(); fig.savefig(path, dpi=150, bbox_inches="tight"); plt.close(fig)

def plot_cycle(df, key, pol, path):
    grp=df.groupby(key)[[pol,"deweathered"]].mean().reset_index()
    fig,ax=plt.subplots(figsize=(7,4))
    ax.plot(grp[key], grp[pol], marker="o", label="Observed")
    ax.plot(grp[key], grp["deweathered"], marker="o", linestyle="--", label="Deweathered")
    ax.set_title(f"{pol} — Mean by {key}"); ax.set_xlabel(key); ax.set_ylabel(pol); ax.legend()
    fig.tight_layout(); fig.savefig(path, dpi=150, bbox_inches="tight"); plt.close(fig)

def scatter(x, y, xlabel, ylabel, title, path):
    fig,ax=plt.subplots(figsize=(6,4)); ax.scatter(x, y, s=8, alpha=0.6)
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel); ax.set_title(title)
    fig.tight_layout(); fig.savefig(path, dpi=150, bbox_inches="tight"); plt.close(fig)
