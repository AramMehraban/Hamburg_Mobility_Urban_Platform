
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# ==================================================
# 1. Project configuration
# ==================================================
PROJECT_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_DIR / "data" / "exports" / "road_network_by_class.csv"

PROJECT_NAME = "Hamburg Mobility & Urban Data Platform"
AUTHOR = "Aram Mehraban | Portfolio Projekt" 
PROJECT_GOAL = (
    "Analyse der Straßenstruktur Hamburgs mit Geodaten, "
    "SQL, Python und Business Intelligence."
)

BG = "#08090B"
PANEL = "#121316"
GOLD = "#B08D3C"
GOLD_LIGHT = "#E3C56E"
DARK_GOLD = "#8B702B"
TEXT = "#E7E1D2"
MUTED = "#AAA28F"
GRID = "#292824"

st.set_page_config(
    page_title="Hamburg Mobility | Analytics",
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# 2. Global design
# ==================================================
st.markdown(
    f"""
    <style>
    .stApp {{
        background: {BG};
        color: {TEXT};
    }}

    .block-container {{
        width: 100%;
        max-width: 1450px;
        padding: 1.5rem clamp(1rem, 2vw, 2rem);
        margin-left: auto;
        margin-right: auto;
        box-sizing: border-box;
    }}

    h1, h2, h3 {{
        color: {GOLD_LIGHT} !important;
    }}

    p, li, label {{
        color: {TEXT};
    }}

    [data-testid="stSidebar"] {{
        background: #101114;
        border-right: 1px solid {DARK_GOLD};
    }}

    [data-testid="stMetric"] {{
        background: linear-gradient(145deg, #17181B, #101114);
        border: 1px solid {DARK_GOLD};
        box-shadow: 0 4px 14px rgba(176, 141, 60, 0.12);
        padding: 17px;
        border-radius: 12px;
        min-height: 112px;
    }}

    [data-testid="stMetricLabel"] {{
        color: {MUTED};
    }}

    [data-testid="stMetricValue"] {{
        color: {GOLD_LIGHT};
    }}

    .gold-card {{
        background: linear-gradient(145deg, #17181B, #101114);
        border: 1px solid {DARK_GOLD};
        border-radius: 12px;
        padding: 20px 22px;
        margin: 8px 0 18px 0;
        box-shadow: 0 5px 18px rgba(176, 141, 60, 0.12);
    }}

    .gold-card h3 {{
        color: {GOLD_LIGHT};
        margin-top: 0;
        margin-bottom: 12px;
    }}

    .gold-card p, .gold-card li {{
        color: {TEXT};
        line-height: 1.65;
    }}

    .project-subtitle {{
        color: {MUTED};
        font-size: 0.95rem;
        margin-top: -4px;
        margin-bottom: 18px;
    }}

    .sidebar-heading {{
        color: {GOLD_LIGHT};
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 5px;
    }}

    .sidebar-small {{
        color: {MUTED};
        font-size: 0.83rem;
        line-height: 1.55;
    }}

    div[data-testid="stVerticalBlockBorderWrapper"] {{
        border-color: {DARK_GOLD} !important;
        box-shadow: 0 5px 18px rgba(176, 141, 60, 0.10);
        border-radius: 12px;
    }}

    div[data-testid="stDataFrame"] {{
        border: 1px solid {DARK_GOLD};
        border-radius: 10px;
        overflow: hidden;
    }}

    div.stButton > button {{
        border: 1px solid {DARK_GOLD};
        border-radius: 8px;
    }}

    div.stButton > button:hover {{
        border-color: {GOLD_LIGHT};
        color: {GOLD_LIGHT};
    }}

    hr {{
        border-color: {DARK_GOLD};
        opacity: 0.5;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ==================================================
# 3. Load and validate data
# ==================================================
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)

    required = {
        "klasse",
        "segment_count",
        "total_length_km"
    }

    missing = required - set(df.columns)

    if missing:
        raise ValueError(f"Fehlende Spalten: {sorted(missing)}")

    if df.empty:
        raise ValueError("Die CSV-Datei enthält keine Daten.")

    df["klasse"] = df["klasse"].astype(str)
    df["segment_count"] = pd.to_numeric(
        df["segment_count"], errors="raise"
    )
    df["total_length_km"] = pd.to_numeric(
        df["total_length_km"], errors="raise"
    )

    if df[list(required)].isna().any().any():
        raise ValueError("Die CSV-Datei enthält fehlende Werte.")

    return df


if not DATA_FILE.exists():
    st.error(f"Datendatei nicht gefunden: {DATA_FILE}")
    st.stop()

try:
    df = load_data()
except Exception as error:
    st.error(f"Fehler beim Laden der Daten: {error}")
    st.stop()

all_classes = sorted(df["klasse"].unique().tolist())

# ==================================================
# 4. Sidebar: project information and filters
# ==================================================
def reset_all_filters():
    st.session_state["selected_classes"] = all_classes


def clear_all_filters():
    st.session_state["selected_classes"] = []


with st.sidebar:
    st.markdown(
        f'<div class="sidebar-heading">{PROJECT_NAME}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sidebar-small">
        Geodatenanalyse · Python · SQL/PostGIS ·
        Streamlit · Power BI
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("**Projektziel**")
    st.caption(PROJECT_GOAL)

    st.markdown("**Autor**")
    st.write(AUTHOR)

    st.divider()

    st.markdown("### Analysefilter")

    if "selected_classes" not in st.session_state:
        st.session_state["selected_classes"] = all_classes.copy()

    st.multiselect(
        "Straßenklasse auswählen",
        options=all_classes,
        key="selected_classes",
        help="Eine oder mehrere Klassen auswählen."
    )

    button_col1, button_col2 = st.columns(2)

    with button_col1:
        st.button(
            "Zurücksetzen",
            on_click=reset_all_filters,
            use_container_width=True
        )

    with button_col2:
        st.button(
            "Alle abwählen",
            on_click=clear_all_filters,
            use_container_width=True
        )

    st.divider()

    st.markdown("### Datenquellen")

    st.markdown(
        """
        <div class="sidebar-small">
        <b>Aktive Quelle</b><br>
        data/exports/road_network_by_class.csv
        <br><br>
        <b>Datengrundlage</b><br>
        Aggregierte Ergebnisse der räumlichen
        SQL/PostGIS-Analyse.
        <br><br>
        <b>Originaldaten</b><br>
        public.road_network
        <br><br>
        <b>Hinweis</b><br>
        Das Dashboard liest die CSV-Datei.
        Es besteht hier keine direkte Datenbankverbindung.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption("Lokale Projektversion · Datenstand gemäß CSV-Export")

selected_classes = st.session_state["selected_classes"]
filtered_df = df[df["klasse"].isin(selected_classes)].copy()

# ==================================================
# 5. Main header
# ==================================================
st.title(PROJECT_NAME)

st.markdown(
    """
    <div class="project-subtitle">
    Analyse des Hamburger Straßennetzes
    &nbsp;|&nbsp; SQL · Python · Geodaten · Business Intelligence
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="gold-card">
        <h3>Projektüberblick</h3>
        <p>
        Dieses Projekt untersucht die Struktur des Hamburger
        Straßennetzes anhand räumlicher Daten. Die Analyse verbindet
        SQL/PostGIS für räumliche Abfragen, Python für Datenprüfung
        und Visualisierung sowie Streamlit und Power BI für die
        verständliche Darstellung von Kennzahlen.
        </p>
        <p>
        <b>Aktueller Schwerpunkt:</b>
        Anzahl und Gesamtlänge der Straßenabschnitte nach Klasse.
        Weitere Verkehrsanalysen benötigen zusätzliche geeignete Daten.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ==================================================
# 5a. Die wichtigsten Kennzahlen (gesamter Datenbestand)
# ==================================================
# Diese Kennzahlen beziehen sich immer auf den vollständigen CSV-Datenbestand,
# unabhängig davon, welche Straßenklassen links im Filter ausgewählt sind.
overall_segments = int(df["segment_count"].sum())
overall_length = float(df["total_length_km"].sum())

class_g_length = float(
    df.loc[df["klasse"] == "G", "total_length_km"].sum()
)
class_g_share = (
    class_g_length / overall_length * 100
    if overall_length > 0
    else 0
)

# Deutsche Zahlenformatierung: 40.642 | 5.156,25 | 93,60
overall_segments_de = f"{overall_segments:,}".replace(",", ".")
overall_length_de = (
    f"{overall_length:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
)
class_g_share_de = f"{class_g_share:.2f}".replace(".", ",")

st.markdown(
    """
    <h2 style="
        color: #E3C56E;
        text-align: center;
        margin-top: 1.5rem;
        margin-bottom: 1.2rem;
    ">
        Die wichtigsten Kennzahlen
    </h2>
    """,
    unsafe_allow_html=True
)

key_col1, key_col2, key_col3 = st.columns(3, gap="large")

with key_col1:
    st.markdown(
        f"""
        <div class="gold-card" style="text-align:center; min-height:150px;">
            <div style="color:#E3C56E; font-size:15px;">
                Straßensegmente
            </div>
            <div style="color:#FFFFFF; font-size:32px;
                        font-weight:700; margin:12px 0;">
                {overall_segments_de}
            </div>
            <div style="color:#AAA28F; font-size:12px;">
                innerhalb des Analysegebiets
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with key_col2:
    st.markdown(
        f"""
        <div class="gold-card" style="text-align:center; min-height:150px;">
            <div style="color:#E3C56E; font-size:15px;">
                Gesamte Netzlänge
            </div>
            <div style="color:#FFFFFF; font-size:32px;
                        font-weight:700; margin:12px 0;">
                {overall_length_de} km
            </div>
            <div style="color:#AAA28F; font-size:12px;">
                geometrische Länge innerhalb Hamburgs
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with key_col3:
    st.markdown(
        f"""
        <div class="gold-card" style="text-align:center; min-height:150px;">
            <div style="color:#E3C56E; font-size:15px;">
                Anteil der Klasse G
            </div>
            <div style="color:#FFFFFF; font-size:32px;
                        font-weight:700; margin:12px 0;">
                {class_g_share_de} %
            </div>
            <div style="color:#AAA28F; font-size:12px;">
                Anteil an der gesamten Netzlänge
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==================================================
# 6. Filter state and KPI calculations
# ==================================================
if filtered_df.empty:
    st.warning(
        "Keine Straßenklasse ausgewählt. "
        "Bitte wähle eine Klasse aus oder klicke auf „Zurücksetzen“."
    )
    st.stop()

total_segments = int(filtered_df["segment_count"].sum())
total_length = float(filtered_df["total_length_km"].sum())
class_count = len(filtered_df)

full_segments = int(df["segment_count"].sum())
full_length = float(df["total_length_km"].sum())

st.markdown("### Kennzahlen im aktuellen Filter")

k1, k2, k3, k4 = st.columns(4)

k1.metric("Straßenabschnitte", f"{total_segments:,}")
k2.metric("Gesamtlänge", f"{total_length:,.2f} km")
k3.metric("Straßenklassen", str(class_count))
k4.metric(
    "Anteil an der Gesamtlänge",
    f"{total_length / full_length * 100:.2f}%"
)

st.caption(
    f"Gesamter CSV-Datenbestand: {full_segments:,} Abschnitte · "
    f"{full_length:,.2f} km"
)

st.divider()

# ==================================================
# 7. Common chart styling
# ==================================================
def style_chart(fig, x_title, y_title):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=PANEL,
        plot_bgcolor=PANEL,
        font=dict(
            family="Arial",
            color=TEXT,
            size=12
        ),
        title=None,
        showlegend=False,
        margin=dict(l=75, r=105, t=30, b=75),
        xaxis=dict(
            title=dict(
                text=x_title,
                font=dict(color=GOLD_LIGHT, size=11),
                standoff=28
            ),
            tickfont=dict(color=TEXT, size=10),
            gridcolor=GRID,
            zeroline=False,
            automargin=True
        ),
        yaxis=dict(
            title=dict(
                text=y_title,
                font=dict(color=GOLD_LIGHT, size=11),
                standoff=24
            ),
            tickfont=dict(color=TEXT, size=11),
            showgrid=False,
            automargin=True
        ),
        uniformtext_minsize=9,
        uniformtext_mode="hide"
    )

    fig.update_traces(
        marker=dict(
            color=GOLD,
            line=dict(color=DARK_GOLD, width=1)
        ),
        textfont=dict(color=GOLD_LIGHT, size=11),
        cliponaxis=False
    )

    return fig


# ==================================================
# 8. Chart 1: road length by class
# ==================================================
st.markdown("### 1. Straßenlänge nach Straßenklasse")

with st.container(border=True):
    length_df = filtered_df.sort_values(
        "total_length_km", ascending=True
    )

    fig_length = px.bar(
        length_df,
        x="total_length_km",
        y="klasse",
        orientation="h",
        text="total_length_km"
    )

    fig_length.update_traces(
        texttemplate="%{text:,.2f} km",
        textposition="outside"
    )

    style_chart(
        fig_length,
        "Gesamtlänge (km)",
        "Straßenklasse"
    )

    st.plotly_chart(
        fig_length,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# ==================================================
# 9. Chart 2: number of segments
# ==================================================
st.markdown("### 2. Anzahl der Straßenabschnitte")

with st.container(border=True):
    count_df = filtered_df.sort_values(
        "segment_count", ascending=True
    )

    fig_count = px.bar(
        count_df,
        x="segment_count",
        y="klasse",
        orientation="h",
        text="segment_count"
    )

    fig_count.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside"
    )

    style_chart(
        fig_count,
        "Anzahl der Abschnitte",
        "Straßenklasse"
    )

    st.plotly_chart(
        fig_count,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# ==================================================
# 10. Chart 3: percentage share of road length
# ==================================================
st.markdown("### 3. Anteil an der gesamten Straßenlänge")

with st.container(border=True):
    share_df = filtered_df.copy()

    selected_total = share_df["total_length_km"].sum()

    share_df["length_share_pct"] = (
        share_df["total_length_km"] / selected_total * 100
    )

    share_df = share_df.sort_values(
        "length_share_pct", ascending=True
    )

    fig_share = px.bar(
        share_df,
        x="length_share_pct",
        y="klasse",
        orientation="h",
        text="length_share_pct"
    )

    fig_share.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    style_chart(
        fig_share,
        "Anteil an der ausgewählten Gesamtlänge (%)",
        "Straßenklasse"
    )

    st.plotly_chart(
        fig_share,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# ==================================================
# 11. Data table: centered and compact
# ==================================================
st.divider()
st.markdown("### Datentabelle")

st.caption(
    "Aggregierte Werte für die aktuell ausgewählten Straßenklassen."
)

table_df = filtered_df[
    ["klasse", "segment_count", "total_length_km"]
].copy()

table_df = table_df.rename(
    columns={
        "klasse": "Straßenklasse",
        "segment_count": "Anzahl der Segmente",
        "total_length_km": "Gesamtlänge (km)"
    }
)

table_df["Gesamtlänge (km)"] = table_df[
    "Gesamtlänge (km)"
].round(2)

left_space, table_col, right_space = st.columns([1, 3, 1])

with table_col:
    with st.container(border=True):
        centered_table_df = (
            table_df.style
            .set_properties(**{"text-align": "center"})
            .set_table_styles([
                {
                    "selector": "th",
                    "props": [("text-align", "center")]
                },
                {
                    "selector": "td",
                    "props": [("text-align", "center")]
                },
            ])
        )

        st.dataframe(
            centered_table_df,
            use_container_width=True,
            hide_index=True,
            height=170,
            column_config={
                "Straßenklasse": st.column_config.TextColumn(
                    "Straßenklasse",
                    width="small"
                ),
                "Anzahl der Segmente": st.column_config.NumberColumn(
                    "Anzahl der Segmente",
                    format="%d",
                    width="medium"
                ),
                "Gesamtlänge (km)": st.column_config.NumberColumn(
                    "Gesamtlänge (km)",
                    format="%.2f",
                    width="medium"
                )
            }
        )

st.caption(
    f"Angezeigte Klassen: {class_count} von {len(all_classes)}"
)


# ==================================================
# 12. First insights and statistics
# ==================================================
st.divider()
st.markdown("### Erste fachliche Erkenntnisse")

insight_total_length = filtered_df["total_length_km"].sum()

insights = filtered_df.copy()
insights["length_share_pct"] = (
    insights["total_length_km"] / insight_total_length * 100
)

dominant = insights.loc[
    insights["total_length_km"].idxmax()
]

dominant_class = dominant["klasse"]
dominant_length = dominant["total_length_km"]
dominant_share = dominant["length_share_pct"]

with st.container(border=True):
    st.markdown(
        f"""
        <div class="gold-card">
            <h3>Struktur und Umfang</h3>
            <ul>
                <li>
                Der aktuelle Filter umfasst
                <b>{total_segments:,} Straßenabschnitte</b>
                mit einer berechneten Gesamtlänge von
                <b>{total_length:,.2f} km</b>.
                </li>
                <li>
                Die Auswertung unterscheidet
                <b>{class_count} Straßenklassen</b>.
                Anzahl und Gesamtlänge werden getrennt betrachtet,
                da sie unterschiedliche Eigenschaften des Netzes zeigen.
                </li>
                <li>
                Die Klasse <b>{dominant_class}</b> hat im aktuellen Filter
                mit <b>{dominant_length:,.2f} km</b> den größten Anteil
                an der Straßenlänge
                (<b>{dominant_share:.2f}%</b>).
                </li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

with st.container(border=True):
    st.markdown(
        """
        <div class="gold-card">
            <h3>Datenqualität und Interpretation</h3>
            <ul>
                <li>
                Die CSV-Zusammenfassung enthält drei Klassen und
                keine fehlenden Werte in den geprüften Spalten.
                </li>
                <li>
                Diese Prüfung bestätigt die Vollständigkeit der
                Zusammenfassung, aber nicht automatisch die Qualität
                jeder einzelnen Geometrie.
                </li>
                <li>
                Aussagen zu Stau, Verkehrsaufkommen, Erreichbarkeit
                oder Verkehrssicherheit sind aus diesen aggregierten
                Kennzahlen allein nicht ableitbar.
                Dafür sind zusätzliche geeignete Verkehrs- und
                Geodaten erforderlich.
                </li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==================================================
# 13. Project status and source
# ==================================================
st.divider()
st.markdown("### Projektstatus und Datenbasis")

with st.container(border=True):
    st.markdown(
        """
        <div class="gold-card">
            <h3>Projektstatus: Lokales Analyse-Dashboard</h3>
            <p>
            <b>Datenbasis:</b> aggregierte CSV-Auswertung
            aus der räumlichen SQL/PostGIS-Analyse.
            </p>
            <p>
            <b>Umgesetzt:</b> drei interaktive Diagramme,
            Klassenfilter, KPI-Karten, Datentabelle und erste Insights.
            </p>
            <p>
            <b>Nächste Schritte:</b> weitere Datenqualitätsprüfungen,
            Power-BI-Datenmodell, DAX-Kennzahlen und gegebenenfalls
            die Integration detaillierter Verkehrsdaten.
            </p>
            <p>
            <b>Technologien:</b> PostgreSQL/PostGIS, Python,
            Pandas, Plotly und Streamlit.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.caption(
    "Hamburg Mobility & Urban Data Platform · "
    f"Autor: {AUTHOR} · "
    "Datenquelle: data/exports/road_network_by_class.csv"
)





# ============================================================
# DATA QUALITY - Hamburg road network
# ============================================================

st.divider()
st.header("Datenqualität des Hamburger Straßennetzes")

st.markdown(
    """
    Untersuchung der Vollständigkeit wichtiger Straßenattribute
    innerhalb der Hamburger Stadtgrenze. Fehlende Angaben werden
    transparent dokumentiert und nicht automatisch ergänzt.
    """
)

# Validierte Kennzahlen aus PostgreSQL/PostGIS
total_segments = 40642
missing_speed = 8697
missing_road_type = 21

missing_speed_pct = missing_speed / total_segments * 100
missing_road_type_pct = missing_road_type / total_segments * 100

# 1. Drei gleich breite und gleich hohe KPI-Boxen
q1, q2, q3 = st.columns(3, gap="medium")

with q1:
    st.markdown(
        f"""
        <div class="gold-card" style="text-align:center; height:145px; box-sizing:border-box; display:flex; flex-direction:column; justify-content:center; align-items:center; margin:0;">
            <div style="color:{GOLD_LIGHT}; font-size:15px; font-weight:600;">Straßensegmente</div>
            <div style="color:#FFFFFF; font-size:32px; font-weight:700; margin:12px 0 8px 0;">{total_segments:,}</div>
            <div style="color:{MUTED}; font-size:12px;">innerhalb Hamburgs</div>
        </div>
        """.replace(",", "."),
        unsafe_allow_html=True,
    )

with q2:
    st.markdown(
        f"""
        <div class="gold-card" style="text-align:center; height:145px; box-sizing:border-box; display:flex; flex-direction:column; justify-content:center; align-items:center; margin:0;">
            <div style="color:{GOLD_LIGHT}; font-size:15px; font-weight:600;">Geschwindigkeit fehlt</div>
            <div style="color:#FFFFFF; font-size:32px; font-weight:700; margin:12px 0 8px 0;">{missing_speed:,}</div>
            <div style="color:{MUTED}; font-size:12px;">{missing_speed_pct:.2f}% des Netzes</div>
        </div>
        """.replace(",", "."),
        unsafe_allow_html=True,
    )

with q3:
    st.markdown(
        f"""
        <div class="gold-card" style="text-align:center; height:145px; box-sizing:border-box; display:flex; flex-direction:column; justify-content:center; align-items:center; margin:0;">
            <div style="color:{GOLD_LIGHT}; font-size:15px; font-weight:600;">Straßenart fehlt</div>
            <div style="color:#FFFFFF; font-size:32px; font-weight:700; margin:12px 0 8px 0;">{missing_road_type}</div>
            <div style="color:{MUTED}; font-size:12px;">{missing_road_type_pct:.2f}% des Netzes</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# 2. Diagramm in einer goldenen Box
st.markdown("### Fehlende Geschwindigkeitsangaben nach Straßenklasse")

quality_df = pd.DataFrame({
    "Straßenklasse": ["A", "B", "G"],
    "Segmente gesamt": [618, 785, 39239],
    "Geschwindigkeit fehlt": [105, 17, 8575],
    "Fehlende Werte (%)": [16.99, 2.17, 21.85],
})

with st.container(border=True):
    fig_quality = px.bar(
        quality_df,
        x="Straßenklasse",
        y="Fehlende Werte (%)",
        text="Fehlende Werte (%)",
        color="Straßenklasse",
        color_discrete_map={
            "A": GOLD_LIGHT,
            "B": GOLD,
            "G": DARK_GOLD,
        },
    )

    fig_quality.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
        cliponaxis=False,
    )

    fig_quality.update_layout(
        template="plotly_dark",
        paper_bgcolor=PANEL,
        plot_bgcolor=PANEL,
        font=dict(color=TEXT),
        showlegend=False,
        height=350,
        margin=dict(l=35, r=35, t=25, b=45),
        xaxis=dict(
            title=None,
            tickfont=dict(color=GOLD_LIGHT),
            gridcolor=GRID,
        ),
        yaxis=dict(
            title="Fehlende Angaben (%)",
            range=[0, 25],
            ticksuffix="%",
            title_font=dict(color=GOLD_LIGHT),
            tickfont=dict(color=TEXT),
            gridcolor=GRID,
        ),
    )

    st.plotly_chart(
        fig_quality,
        use_container_width=True,
        config={"displayModeBar": False},
    )

# 3. Tabelle: kompakt und zentriert wie Datentabelle
st.markdown("### Detailübersicht")

display_quality_df = quality_df.rename(
    columns={
        "Straßenklasse": "Straßenklasse",
        "Segmente gesamt": "Segmente gesamt",
        "Geschwindigkeit fehlt": "Geschwindigkeit fehlt",
        "Fehlende Werte (%)": "Fehlende Werte (%)",
    }
).copy()

display_quality_df["Fehlende Werte (%)"] = (
    display_quality_df["Fehlende Werte (%)"].map(
        lambda value: f"{value:.2f}%"
    )
)

left_space, table_col, right_space = st.columns([1, 3, 1])

with table_col:
    with st.container(border=True):
        st.dataframe(
            display_quality_df,
            use_container_width=True,
            hide_index=True,
            height=170,
        )

# 4. Interpretation im vorhandenen Gold-Card-Stil
st.markdown("### Interpretation")

with st.container(border=True):
    st.markdown(
        """
        <div class="gold-card">
            <h3>Einordnung der Datenqualität</h3>
            <p>
                <b>Klasse G:</b> 21,85 % der Segmente haben
                keine Geschwindigkeitsangabe.
            </p>
            <p>
                <b>Klasse A:</b> Bei 16,99 % der Segmente fehlt
                die Geschwindigkeitsangabe.
            </p>
            <p>
                <b>Klasse B:</b> Mit 2,17 % ist der Anteil
                fehlender Geschwindigkeitsangaben am niedrigsten.
            </p>
            <p>
                Fehlende Attribute bedeuten nicht automatisch,
                dass ein Datensatz fehlerhaft ist. Deshalb werden
                Werte nicht ungeprüft ergänzt oder gelöscht.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# 5. Datenquelle in einer klaren, goldenen Box
st.markdown("### Datenbasis und Methodik")

with st.container(border=True):
    st.markdown(
        """
        <div class="gold-card">
            <h3>Quelle und Aktualisierung</h3>
            <p>
                <b>Räumliche Datengrundlage</b><br>
                <code>analytics.v_road_network_hamburg</code>
            </p>
            <p>
                <b>Datenqualitätsprüfung</b><br>
                <code>analytics.v_road_network_data_quality</code>
            </p>
            <p>
                <b>Umfang:</b> 40.642 Straßensegmente innerhalb
                der ausgewerteten Hamburger Stadtgrenze.
            </p>
            <p>
                <b>Aktualisierung:</b> Die angezeigten Kennzahlen
                stammen aus zuvor ausgeführten SQL-Abfragen.
                Sie werden nicht live aus PostgreSQL aktualisiert.
            </p>
            <p>
                <b>Methodischer Hinweis:</b> Die fehlenden Werte
                werden gezählt und nach Straßenklasse verglichen.
                Es erfolgt keine automatische Datenkorrektur.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.caption(
    "Hamburg Mobility & Urban Data Platform · "
    f"Autor: {AUTHOR} · "
    "Dashboard-Daten: data/exports/road_network_by_class.csv"
)
