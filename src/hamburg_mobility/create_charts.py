
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# Project paths
PROJECT_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_DIR / "data" / "exports" / "road_network_by_class.csv"
OUTPUT_DIR = PROJECT_DIR / "reports" / "charts"

# Shared design for all charts
BG = "#08090B"
GOLD = "#B08D3C"
DARK_GOLD = "#8B702B"
GOLD_LIGHT = "#E3C56E"
TEXT = "#E7E1D2"
MUTED = "#AAA28F"
GRID = "#292824"


def apply_dark_gold_style(fig, ax, title, subtitle):
    """Apply the shared dark and gold style to every chart."""

    fig.patch.set_facecolor(BG)
    fig.patch.set_edgecolor(DARK_GOLD)
    fig.patch.set_linewidth(0.8)

    ax.set_facecolor(BG)

    # Centered, bright-gold title
    ax.set_title(
        title,
        color=GOLD_LIGHT,
        loc="center",
        fontsize=14,
        fontweight="bold",
        pad=28
    )

    # Subtitle
    ax.text(
        0.5,
        1.035,
        subtitle,
        transform=ax.transAxes,
        color=MUTED,
        fontsize=8.5,
        ha="center",
        va="bottom"
    )

    # Axis tick labels
    ax.tick_params(
        axis="both",
        colors=TEXT,
        labelsize=8.5,
        length=0,
        pad=7
    )

    # Axis titles
    ax.xaxis.label.set_color(GOLD_LIGHT)
    ax.yaxis.label.set_color(GOLD_LIGHT)
    ax.xaxis.label.set_size(9)
    ax.yaxis.label.set_size(9)
    ax.xaxis.label.set_weight("medium")
    ax.yaxis.label.set_weight("medium")

    ax.xaxis.labelpad = 10
    ax.yaxis.labelpad = 12

    # Clean chart with subtle grid
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.grid(
        axis="x",
        color=GRID,
        linewidth=0.5,
        alpha=0.8
    )

    ax.set_axisbelow(True)


def chart_road_length_by_class():
    """Chart 1: Total road length by road class."""

    df = pd.read_csv(DATA_FILE)
    df = df.sort_values("total_length_km", ascending=True)

    fig, ax = plt.subplots(figsize=(9, 4.8))

    apply_dark_gold_style(
        fig,
        ax,
        "Hamburger Straßennetz nach Straßenklasse",
        "Gesamtlänge innerhalb Hamburgs · km"
    )

    bars = ax.barh(
        df["klasse"],
        df["total_length_km"],
        color=GOLD,
        height=0.48,
        edgecolor="none"
    )

    max_value = df["total_length_km"].max()
    ax.set_xlim(0, max_value * 1.18)

    ax.set_xlabel("Länge (km)")
    ax.set_ylabel("Straßenklasse")
    ax.grid(axis="y", visible=False)

    for bar, value in zip(bars, df["total_length_km"]):
        ax.text(
            value + max_value * 0.015,
            bar.get_y() + bar.get_height() / 2,
            f"{value:,.2f} km",
            va="center",
            color=TEXT,
            fontsize=9
        )

    fig.tight_layout(rect=[0.04, 0.04, 0.98, 0.88])

    output_file = OUTPUT_DIR / "road_network_by_class.png"

    fig.savefig(
        output_file,
        dpi=180,
        facecolor=BG,
        edgecolor=DARK_GOLD,
        bbox_inches="tight"
    )

    print("Created:", output_file)

    return fig


def chart_segment_count_by_class():
    """Chart 2: Number of road segments by road class."""

    df = pd.read_csv(DATA_FILE)
    df = df.sort_values("segment_count", ascending=True)

    fig, ax = plt.subplots(figsize=(8, 4.5))

    apply_dark_gold_style(
        fig,
        ax,
        "Anzahl der Straßenabschnitte nach Klasse",
        "Anzahl der Segmente innerhalb Hamburgs"
    )

    bars = ax.barh(
        df["klasse"],
        df["segment_count"],
        color=GOLD,
        height=0.48,
        edgecolor="none"
    )

    max_value = df["segment_count"].max()
    ax.set_xlim(0, max_value * 1.18)

    ax.set_xlabel("Anzahl der Segmente")
    ax.set_ylabel("Straßenklasse")
    ax.grid(axis="y", visible=False)

    for bar, value in zip(bars, df["segment_count"]):
        ax.text(
            value + max_value * 0.015,
            bar.get_y() + bar.get_height() / 2,
            f"{value:,.0f}",
            va="center",
            color=TEXT,
            fontsize=9
        )

    fig.tight_layout(rect=[0.04, 0.04, 0.98, 0.88])

    output_file = OUTPUT_DIR / "road_segments_by_class.png"

    fig.savefig(
        output_file,
        dpi=180,
        facecolor=BG,
        edgecolor=DARK_GOLD,
        bbox_inches="tight"
    )

    print("Created:", output_file)

    return fig



def chart_road_length_share():
    """Chart 3: Percentage share of total road length by class."""

    df = pd.read_csv(DATA_FILE)
    df = df.sort_values("total_length_km", ascending=True)

    total_length = df["total_length_km"].sum()
    df["length_share_pct"] = (
        df["total_length_km"] / total_length * 100
    )

    fig, ax = plt.subplots(figsize=(8, 4.5))

    apply_dark_gold_style(
        fig,
        ax,
        "Anteil der Straßenlänge nach Klasse",
        "Anteil an der gesamten Straßenlänge innerhalb Hamburgs · %"
    )

    bars = ax.barh(
        df["klasse"],
        df["length_share_pct"],
        color=GOLD,
        height=0.48,
        edgecolor="none"
    )

    max_value = df["length_share_pct"].max()
    ax.set_xlim(0, max_value * 1.18)

    ax.set_xlabel("Anteil an der Gesamtlänge (%)")
    ax.set_ylabel("Straßenklasse")
    ax.grid(axis="y", visible=False)

    for bar, value in zip(bars, df["length_share_pct"]):
        ax.text(
            value + max_value * 0.015,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.2f} %",
            va="center",
            color=TEXT,
            fontsize=9
        )

    fig.tight_layout(rect=[0.04, 0.04, 0.98, 0.88])

    output_file = OUTPUT_DIR / "road_length_share_by_class.png"

    fig.savefig(
        output_file,
        dpi=180,
        facecolor=BG,
        edgecolor=DARK_GOLD,
        bbox_inches="tight"
    )

    print("Created:", output_file)

    return fig



def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Generate all charts
    figures = [
        chart_road_length_by_class(),
        chart_segment_count_by_class(),
        chart_road_length_share()
    ]

    print(f"\nCharts created: {len(figures)}")
    print("Chart images saved in:", OUTPUT_DIR)
    print("Close the chart windows to finish.")

    plt.show()


if __name__ == "__main__":
    main()
