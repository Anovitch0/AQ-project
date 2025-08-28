
from __future__ import annotations
import pandas as pd, matplotlib.pyplot as plt

def ts(df, col, title, path):
    fig,ax=plt.subplots(figsize=(10,4))
    ax.plot(df["datetime"], df[col], label=col)
    ax.set_title(title); ax.set_xlabel("Date"); ax.set_ylabel(col); ax.legend()
    fig.tight_layout(); fig.savefig(path, dpi=150, bbox_inches="tight"); plt.close(fig)

def stack_daily(mix_daily, path):
    cols=[c for c in mix_daily.columns if c.endswith("_MW")]
    if not cols: return
    fig,ax=plt.subplots(figsize=(10,4))
    ax.stackplot(mix_daily["datetime"], *[mix_daily[c] for c in cols], labels=cols)
    ax.set_title("Generation by fuel (daily sum)"); ax.set_xlabel("Date"); ax.set_ylabel("MWh")
    ax.legend(loc="upper left", ncols=4, fontsize=7)
    fig.tight_layout(); fig.savefig(path, dpi=150, bbox_inches="tight"); plt.close(fig)
