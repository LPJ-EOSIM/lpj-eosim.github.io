"""Pack NMIP3 SH1 climatologies + NMIP factorial stock series into docs/index.html, the site's landing page.

Inputs:
  data/<var>.npz   2015-2024 climatologies at 1 deg, made on Hellgate by globe_page_extract.py
                   (copy of NMIP/code/globe_page_extract.py; output in NMIP/globe_page/). Not in git.
  ~/nmip/LPJ_EOSIM/SH*/LPJ_EOSIM_zonalSH*_<stock>.csv   NMIP3 global stock series, PgC

Edit template.html, then: python tools/welcome/build_story.py
"""
import base64
import gzip
import json
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=RuntimeWarning)  # all-NaN ocean blocks

if __name__ == "__main__":
    # --- edit me ---
    here = Path(__file__).parent
    data_dir = here / "data"  # <var>.npz from Hellgate: NMIP/code/globe_page_extract.py, 1 deg, north first
    zonal_dir = Path.home() / "nmip/LPJ_EOSIM"  # SH*/LPJ_EOSIM_zonalSH*_<stock>.csv, PgC
    template = here / "template.html"
    outf = here.parents[1] / "docs/index.html"  # landing page; its footer links to the docs home (home.md)
    experiments = ["SH1", "SH7", "SH6", "SH0"]
    # ---------------

    def load(v):
        return np.load(data_dir / f"{v}.npz")["data"].astype("f8")

    lat = np.arange(89.5, -90, -1.0)
    cell05_ha = (6371.0 * np.deg2rad(0.5)) ** 2 * np.cos(np.deg2rad(lat)) * 100  # 0.5 deg cell, km2 -> ha

    fields = {
        "tair": load("mtair"),
        "ppt": load("mppt"),
        "swdown": load("mswdown"),
        "totc": load("vegc") + load("litc") + load("soilc"),
        "gpp": load("mgpp") * 1000,
        "npp": np.clip(load("mnpp") * 1000, 0, None),
        "rh": load("mrh") * 1000,
        "firec": load("mfirec"),
        "lai": load("mlai"),
        "vegc": load("vegc"),
        "litc": load("litc"),
        "soilc": load("soilc"),
        "et": load("mevapotrans"),
        "swc": load("mswc1"),
        "runoff": load("mrunoff"),
        "snow": load("msnowpack"),
        "burnt": load("mburntarea") / cell05_ha[None, :, None] * 100,  # % of the cell per month
        "isopr": load("misopr") * 1e6,
        "n2o": load("mn2o_soil") * 1000,
        "bnf": load("mbnf") * 1000,
    }

    # key: (res deg, lo, hi or None -> percentile, pct, gamma, blank-below threshold)
    specs = {
        "tair":   (1, -30, 32, None, 1.0, 0.0),
        "ppt":    (1, 0, None, 99.0, 0.6, 0.08),
        "swdown": (1, 0, None, 99.5, 1.0, 0.06),
        "totc":   (1, 0, None, 99.0, 0.7, 0.05),
        "gpp":    (2, 0, None, 99.0, 0.7, 0.08),
        "npp":    (2, 0, None, 99.0, 0.7, 0.08),
        "rh":     (2, 0, None, 99.0, 0.7, 0.08),
        "firec":  (2, 0, None, 99.0, 0.4, 0.12),
        "lai":    (2, 0, None, 99.0, 0.8, 0.06),
        "vegc":   (2, 0, None, 99.0, 0.8, 0.05),
        "litc":   (2, 0, None, 99.0, 0.7, 0.05),
        "soilc":  (2, 0, None, 99.0, 0.7, 0.05),
        "et":     (2, 0, None, 99.0, 0.7, 0.08),
        "swc":    (2, 0, 1, None, 1.0, 0.05),
        "runoff": (2, 0, None, 99.0, 0.5, 0.10),
        "snow":   (2, 0, 400, None, 0.5, 0.06),
        "burnt":  (2, 0, None, 99.0, 0.4, 0.12),
        "isopr":  (2, 0, None, 99.0, 0.6, 0.08),
        "n2o":    (2, 0, None, 99.0, 0.5, 0.10),
        "bnf":    (2, 0, None, 99.0, 0.6, 0.08),
    }

    blobs, meta, offset = [], {}, 0
    for key, (res, lo, hi, pct, gamma, thr) in specs.items():
        a = fields[key]
        if res == 2:
            a = np.nanmean(a.reshape(a.shape[0], 90, 2, 180, 2), axis=(2, 4))
        if hi is None:
            vals = a[np.isfinite(a) & (a > lo)]
            hi = float(np.percentile(vals, pct))
        norm = (np.clip(a, lo, hi) - lo) / (hi - lo)
        norm = norm ** gamma
        q = np.where(np.isfinite(norm), np.round(norm * 254), 255).astype(np.uint8)
        blobs.append(q.tobytes())
        meta[key] = {"offset": offset, "nt": a.shape[0], "res": res, "lo": lo, "hi": hi, "gamma": gamma, "thr": thr}
        offset += q.size
        print(f"{key:7s} res={res} nt={a.shape[0]:2d} lo={lo} hi={hi:.4g}")

    raw = b"".join(blobs)
    packed = base64.b64encode(gzip.compress(raw, compresslevel=9)).decode()
    print(f"fields: raw {len(raw)/1e6:.2f} MB -> gzip+b64 {len(packed)/1e6:.2f} MB")

    stocks = {"years": None}
    for exp in experiments:
        cols = {}
        for name, stock in (("veg", "cveg"), ("soil", "csoil"), ("litter", "clitter"), ("product", "cproduct")):
            df = pd.read_csv(zonal_dir / exp / f"LPJ_EOSIM_zonal{exp}_{stock}.csv")
            cols[name] = df["Global"].to_numpy()
            stocks["years"] = df["Year"].astype(int).tolist()
        cols["total"] = cols["veg"] + cols["soil"] + cols["litter"] + cols["product"]
        stocks[exp] = {k: [round(float(x), 1) for x in cols[k]] for k in ("veg", "soil", "litter", "total")}
        print(exp, {k: (stocks[exp][k][0], stocks[exp][k][-1]) for k in ("veg", "soil", "litter", "total")})

    html = template.read_text()
    html = html.replace("/*META*/null", json.dumps(meta)).replace("/*B64*/", packed)
    html = html.replace("/*STOCKS*/null", json.dumps(stocks, separators=(",", ":")))
    outf.write_text(html)
    print(f"wrote {outf} ({outf.stat().st_size/1e6:.2f} MB)")
