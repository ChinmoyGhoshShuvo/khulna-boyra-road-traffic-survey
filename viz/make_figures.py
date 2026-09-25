"""
Charts rebuilt from the report's tables (data/*.csv). Nothing is estimated.
Run:  python make_figures.py   -> PNGs in ../images/
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).parent
DATA, OUT = HERE / "data", HERE.parent / "images"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.titlesize": 10, "axes.titleweight": "bold",
    "axes.spines.top": False, "axes.spines.right": False, "savefig.dpi": 200,
    "savefig.bbox": "tight", "figure.facecolor": "white",
})
SITE_COL = {"Baikali": "#0072B2", "Boyra College Mor": "#E69F00", "Navy Colony": "#009E73"}
PERIODS = ["Off-peak", "Morning peak", "Evening peak"]


def intensity():
    d = pd.read_csv(DATA / "pcu_intensity.csv", comment="#")
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.2), sharey=True, gridspec_kw={"wspace": 0.08})
    x = np.arange(len(PERIODS))
    w = 0.26
    for ax, day, letter in zip(axes, ["Weekday", "Weekend"], "ab"):
        sub = d[d.day == day].set_index("period").loc[PERIODS]
        for i, (site, col) in enumerate(SITE_COL.items()):
            bars = ax.bar(x + (i - 1) * w, sub[site], width=w, color=col, label=site)
            for b in bars:
                ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 50, f"{b.get_height():,.0f}",
                        ha="center", va="bottom", fontsize=6.5, rotation=90)
        ax.set_xticks(x)
        ax.set_xticklabels(PERIODS)
        ax.set_title(day, loc="left")
        ax.text(-0.08, 1.06, letter, transform=ax.transAxes, fontweight="bold", fontsize=11)
    axes[0].set_ylabel("Traffic volume (PCU per hour)")
    axes[0].set_ylim(0, 4900)
    axes[1].spines["left"].set_visible(False)
    axes[1].tick_params(left=False)
    axes[0].legend(frameon=False, fontsize=7.5, loc="upper left")
    fig.text(0, -0.06, "Rebuilt from report Table 5 (manual 15-min counts x 4, converted to PCU).",
             fontsize=7, color="#555")
    fig.savefig(OUT / "traffic-intensity-pcu-by-intersection.png")
    plt.close(fig)


def split():
    d = pd.read_csv(DATA / "baikali_motorized_split.csv", comment="#").set_index("period").loc[PERIODS]
    fig, ax = plt.subplots(figsize=(5.2, 2.2))
    ax.barh(d.index, d.Motorized, color="#0072B2", height=0.55, label="Motorized")
    ax.barh(d.index, d["Non-motorized"], left=d.Motorized, color="#E69F00", height=0.55, label="Non-motorized")
    for y, (m, n) in enumerate(zip(d.Motorized, d["Non-motorized"])):
        ax.text(m + n + 40, y, f"{n / (m + n) * 100:.1f}% non-motorized", va="center", fontsize=7.5)
    ax.invert_yaxis()
    ax.set_xlim(0, 5000)
    ax.set_xlabel("PCU per hour (weekday, Baikali)")
    ax.legend(frameon=False, fontsize=7.5, loc="upper center", bbox_to_anchor=(0.5, -0.32), ncol=2)
    fig.text(0, -0.28, "Rebuilt from report Table 6.", fontsize=7, color="#555")
    fig.savefig(OUT / "baikali-motorized-vs-nonmotorized.png")
    plt.close(fig)


if __name__ == "__main__":
    intensity()
    split()
    print("written to", OUT.resolve())
