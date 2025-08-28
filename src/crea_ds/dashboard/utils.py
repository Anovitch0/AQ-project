from __future__ import annotations
from pathlib import Path
from typing import List, Optional
from PIL import Image

def find_images_dir(start: Path | None = None) -> Optional[Path]:
    """
    Cherche 'images/' en partant d'abord du dossier courant (cwd),
    puis en remontant depuis 'start' (par défaut, le dossier du fichier appelant).
    """
    # 1) d'abord cwd (utile si tu lances streamlit depuis la racine du projet)
    cwd = Path.cwd()
    for p in [cwd, *cwd.parents]:
        cand = p / "images"
        if cand.exists():
            return cand

    # 2) fallback : les parents du fichier où se trouve le package
    if start is not None:
        for p in [start, *start.parents]:
            cand = p / "images"
            if cand.exists():
                return cand
    return None

def list_cities(img_dir: Path) -> List[str]:
    names = []
    for p in img_dir.glob("deweathered_*.png"):
        city = p.stem.replace("deweathered_", "")
        names.append(city)
    return sorted(set(names))

def safe_open_image(path: Path) -> Image.Image | None:
    try:
        return Image.open(path)
    except Exception:
        return None
