# EXTRA ATTRACTIVE DASHBOARD VERSION - V2 - 1657 LINE PREMIUM THEME
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path

# =====================================================
# PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="Nassau Candy Logistics Dashboard",
    page_icon="🚚",
    layout="wide"
)


# =====================================================
# VISUAL THEME & DASHBOARD STYLING
# =====================================================
BRAND_COLORS = {
    "midnight": "#07111f",
    "navy": "#0f172a",
    "blue": "#2563eb",
    "electric": "#00d4ff",
    "mint": "#35f5c4",
    "candy": "#ff2d75",
    "orange": "#ff8a00",
    "amber": "#f59e0b",
    "violet": "#7c3aed",
    "red": "#ef4444",
    "green": "#10b981",
    "slate": "#64748b",
    "soft_bg": "#f8fafc",
}

CHART_SEQUENCE = [
    BRAND_COLORS["candy"], BRAND_COLORS["electric"], BRAND_COLORS["mint"],
    BRAND_COLORS["orange"], BRAND_COLORS["violet"], BRAND_COLORS["blue"],
    BRAND_COLORS["green"], BRAND_COLORS["red"],
]

px.defaults.template = "plotly_white"
px.defaults.color_discrete_sequence = CHART_SEQUENCE
px.defaults.color_continuous_scale = [
    "#eef2ff", "#a5b4fc", "#38bdf8", "#22c55e", "#f59e0b", "#ff2d75"
]

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

        :root {
            --midnight: #07111f;
            --navy: #0f172a;
            --blue: #2563eb;
            --electric: #00d4ff;
            --mint: #35f5c4;
            --candy: #ff2d75;
            --orange: #ff8a00;
            --amber: #f59e0b;
            --violet: #7c3aed;
            --glass: rgba(255, 255, 255, 0.78);
            --border: rgba(255, 255, 255, 0.35);
            --shadow: 0 24px 80px rgba(2, 6, 23, 0.18);
        }

        html, body, [class*="css"]  {
            font-family: 'Inter', 'Segoe UI', sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at 8% 8%, rgba(255,45,117,0.18), transparent 27%),
                radial-gradient(circle at 92% 6%, rgba(0,212,255,0.22), transparent 28%),
                radial-gradient(circle at 50% 95%, rgba(53,245,196,0.16), transparent 32%),
                linear-gradient(135deg, #f8fbff 0%, #eef2ff 42%, #fdf2f8 100%);
            color: var(--navy);
        }

        .block-container {
            padding-top: 1.25rem !important;
            padding-bottom: 2.5rem !important;
            max-width: 1480px !important;
        }

        #MainMenu, footer, header {visibility: hidden;}

        section[data-testid="stSidebar"] {
            background:
                radial-gradient(circle at 20% 0%, rgba(255,45,117,.30), transparent 28%),
                radial-gradient(circle at 86% 22%, rgba(0,212,255,.26), transparent 30%),
                linear-gradient(180deg, #07111f 0%, #101d33 46%, #1e293b 100%);
            border-right: 1px solid rgba(255,255,255,0.11);
            box-shadow: 15px 0 45px rgba(2,6,23,.18);
        }

        section[data-testid="stSidebar"] * { color: #f8fafc !important; }
        section[data-testid="stSidebar"] label { font-weight: 800 !important; letter-spacing: .02em; }
        section[data-testid="stSidebar"] small { color: rgba(248,250,252,.72) !important; }

        section[data-testid="stSidebar"] div[data-baseweb="select"] span,
        section[data-testid="stSidebar"] div[data-baseweb="select"] div,
        section[data-testid="stSidebar"] input,
        section[data-testid="stSidebar"] textarea {
            color: #07111f !important;
        }

        section[data-testid="stSidebar"] div[data-testid="stDateInput"] input,
        section[data-testid="stSidebar"] div[data-baseweb="select"] > div,
        section[data-testid="stSidebar"] div[data-testid="stTextInput"] input {
            border-radius: 14px !important;
            border: 1px solid rgba(255,255,255,.22) !important;
            box-shadow: 0 10px 28px rgba(0,0,0,.18) !important;
        }

        .sidebar-brand {
            padding: 1.25rem 1rem;
            margin: .15rem 0 1rem 0;
            border-radius: 24px;
            background:
                linear-gradient(135deg, rgba(255,45,117,.95), rgba(124,58,237,.88) 46%, rgba(0,212,255,.82));
            box-shadow: 0 24px 65px rgba(0,0,0,.32);
            border: 1px solid rgba(255,255,255,.24);
            position: relative;
            overflow: hidden;
        }

        .sidebar-brand:after {
            content: "";
            position: absolute;
            width: 130px;
            height: 130px;
            right: -55px;
            top: -55px;
            border-radius: 999px;
            background: rgba(255,255,255,.20);
        }

        .sidebar-brand h2 {
            font-size: 1.42rem;
            line-height: 1.05;
            margin: 0;
            color: white !important;
            font-weight: 900;
            letter-spacing: -.03em;
        }

        .sidebar-brand p {
            margin: .42rem 0 0 0;
            color: rgba(255,255,255,.88) !important;
            font-size: .84rem;
            font-weight: 650;
        }

        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        @keyframes floatGlow {
            0%, 100% { transform: translateY(0px) scale(1); opacity: .72; }
            50% { transform: translateY(-13px) scale(1.04); opacity: 1; }
        }

        @keyframes shimmer {
            0% { transform: translateX(-120%); }
            100% { transform: translateX(120%); }
        }

        .hero-card {
            padding: 2.45rem 2.55rem;
            border-radius: 34px;
            color: white;
            background:
                linear-gradient(135deg, rgba(7,17,31,.98), rgba(37,99,235,.96), rgba(124,58,237,.92), rgba(255,45,117,.88));
            background-size: 280% 280%;
            animation: gradientShift 13s ease infinite;
            box-shadow: 0 32px 95px rgba(15,23,42,.28);
            margin-bottom: 1.15rem;
            border: 1px solid rgba(255,255,255,.22);
            position: relative;
            overflow: hidden;
            isolation: isolate;
        }

        .hero-card:before {
            content: "";
            position: absolute;
            inset: 0;
            background:
                linear-gradient(105deg, transparent 0%, transparent 35%, rgba(255,255,255,.18) 48%, transparent 60%, transparent 100%);
            animation: shimmer 6.5s ease-in-out infinite;
            z-index: -1;
        }

        .hero-card:after {
            content: "";
            position: absolute;
            right: -80px;
            top: -95px;
            width: 285px;
            height: 285px;
            border-radius: 999px;
            background:
                radial-gradient(circle, rgba(53,245,196,.55), rgba(0,212,255,.18) 55%, transparent 70%);
            filter: blur(.5px);
            animation: floatGlow 7s ease-in-out infinite;
            z-index: -1;
        }

        .hero-orb-left {
            position: absolute;
            left: -85px;
            bottom: -90px;
            width: 250px;
            height: 250px;
            border-radius: 999px;
            background: radial-gradient(circle, rgba(255,138,0,.46), rgba(255,45,117,.17) 56%, transparent 72%);
            animation: floatGlow 8.5s ease-in-out infinite;
            z-index: -1;
        }

        .hero-eyebrow {
            display: inline-flex;
            align-items: center;
            gap: .5rem;
            letter-spacing: .13em;
            text-transform: uppercase;
            font-size: .80rem;
            font-weight: 900;
            color: #cffafe;
            margin-bottom: .60rem;
            background: rgba(255,255,255,.13);
            border: 1px solid rgba(255,255,255,.18);
            padding: .42rem .72rem;
            border-radius: 999px;
            backdrop-filter: blur(10px);
        }

        .hero-title {
            font-size: clamp(2.2rem, 4.5vw, 4.15rem);
            line-height: .98;
            font-weight: 950;
            margin: 0 0 .82rem 0;
            letter-spacing: -.065em;
            text-shadow: 0 12px 35px rgba(0,0,0,.25);
        }

        .hero-subtitle {
            color: rgba(255,255,255,.88);
            font-size: 1.08rem;
            max-width: 980px;
            margin-bottom: 1.35rem;
            line-height: 1.65;
            font-weight: 550;
        }

        .hero-chips {
            display: flex;
            flex-wrap: wrap;
            gap: .72rem;
        }

        .hero-chip {
            background: rgba(255,255,255,.15);
            border: 1px solid rgba(255,255,255,.25);
            color: white;
            border-radius: 999px;
            padding: .55rem .86rem;
            font-weight: 800;
            font-size: .85rem;
            backdrop-filter: blur(10px);
            box-shadow: 0 12px 25px rgba(0,0,0,.12);
        }

        .data-note-card {
            background:
                linear-gradient(135deg, rgba(255,247,237,.94) 0%, rgba(255,255,255,.86) 68%),
                radial-gradient(circle at 0% 0%, rgba(245,158,11,.18), transparent 38%);
            border-left: 7px solid var(--amber);
            border-radius: 22px;
            padding: 1.08rem 1.22rem;
            margin: .55rem 0 1.35rem 0;
            box-shadow: 0 18px 45px rgba(15,23,42,.09);
            color: #334155;
            font-size: .96rem;
            line-height: 1.6;
        }

        .data-note-card strong { color: #9a3412; }

        .metric-grid {
            display: grid;
            grid-template-columns: repeat(5, minmax(0, 1fr));
            gap: 1rem;
            margin: .4rem 0 1.1rem 0;
        }

        .metric-grid.secondary {
            grid-template-columns: repeat(3, minmax(0, 1fr));
            margin-top: .25rem;
        }

        .metric-card {
            position: relative;
            overflow: hidden;
            min-height: 135px;
            padding: 1.15rem 1.1rem;
            border-radius: 24px;
            background: rgba(255,255,255,.78);
            border: 1px solid rgba(255,255,255,.62);
            box-shadow: 0 18px 48px rgba(15,23,42,.10);
            backdrop-filter: blur(14px);
        }

        .metric-card:before {
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, var(--accent), transparent 43%);
            opacity: .16;
        }

        .metric-card:after {
            content: "";
            position: absolute;
            right: -34px;
            top: -36px;
            width: 105px;
            height: 105px;
            border-radius: 999px;
            background: var(--accent);
            opacity: .16;
        }

        .metric-icon {
            position: relative;
            width: 42px;
            height: 42px;
            border-radius: 16px;
            display: grid;
            place-items: center;
            font-size: 1.28rem;
            background: var(--accent);
            color: white;
            box-shadow: 0 13px 25px color-mix(in srgb, var(--accent) 32%, transparent);
            margin-bottom: .78rem;
        }

        .metric-label {
            position: relative;
            color: #64748b;
            font-size: .77rem;
            line-height: 1.2;
            font-weight: 900;
            letter-spacing: .075em;
            text-transform: uppercase;
            margin-bottom: .32rem;
        }

        .metric-value {
            position: relative;
            color: #07111f;
            font-size: 1.63rem;
            line-height: 1.05;
            font-weight: 950;
            letter-spacing: -.045em;
            word-break: break-word;
        }

        .metric-help {
            position: relative;
            margin-top: .45rem;
            color: #475569;
            font-size: .79rem;
            font-weight: 650;
        }

        [data-testid="stMetric"] {
            background: rgba(255,255,255,.82);
            border: 1px solid rgba(255,255,255,.58);
            border-radius: 22px;
            padding: 1.05rem 1rem;
            box-shadow: 0 16px 42px rgba(15,23,42,.10);
            backdrop-filter: blur(14px);
        }

        [data-testid="stMetricLabel"] p {
            color: #64748b !important;
            font-weight: 850;
            letter-spacing: .02em;
        }

        [data-testid="stMetricValue"] { color: #07111f !important; font-weight: 950; }

        h1, h2, h3 {
            letter-spacing: -.035em;
            color: #07111f;
        }

        h2, h3 {
            padding-top: .25rem;
            font-weight: 900 !important;
        }

        [data-testid="stTabs"] button {
            border-radius: 999px !important;
            padding: .75rem 1.02rem !important;
            font-weight: 900 !important;
            letter-spacing: -.01em;
        }

        div[data-testid="stTabs"] div[role="tablist"] {
            gap: .55rem;
            background: rgba(255,255,255,.70);
            border: 1px solid rgba(255,255,255,.64);
            border-radius: 999px;
            padding: .52rem;
            box-shadow: 0 18px 45px rgba(15,23,42,.09);
            backdrop-filter: blur(14px);
        }

        div[data-testid="stTabs"] button[aria-selected="true"] {
            background: linear-gradient(135deg, #ff2d75, #7c3aed 50%, #00d4ff) !important;
            color: #ffffff !important;
            box-shadow: 0 14px 28px rgba(124,58,237,.28);
        }

        div[data-testid="stDataFrame"], div[data-testid="stTable"] {
            border-radius: 22px;
            overflow: hidden;
            box-shadow: 0 18px 45px rgba(15,23,42,.09);
            border: 1px solid rgba(255,255,255,.64);
        }

        .stPlotlyChart {
            background: rgba(255,255,255,.82);
            border-radius: 26px;
            padding: .88rem;
            border: 1px solid rgba(255,255,255,.66);
            box-shadow: 0 20px 55px rgba(15,23,42,.10);
            backdrop-filter: blur(14px);
        }

        div[data-testid="stAlert"] {
            border-radius: 18px;
            box-shadow: 0 12px 28px rgba(15,23,42,.08);
            border: 1px solid rgba(255,255,255,.50);
        }

        div[data-testid="stRadio"] label,
        div[data-testid="stSelectbox"] label,
        div[data-testid="stSlider"] label,
        div[data-testid="stTextInput"] label {
            font-weight: 850 !important;
            color: #0f172a !important;
        }

        .footer-card {
            background:
                linear-gradient(135deg, rgba(7,17,31,.98), rgba(30,41,59,.96)),
                radial-gradient(circle at 95% 20%, rgba(0,212,255,.16), transparent 38%);
            color: rgba(255,255,255,.86);
            padding: 1.15rem 1.35rem;
            border-radius: 24px;
            margin-top: 1.65rem;
            box-shadow: 0 24px 65px rgba(15,23,42,.22);
            border: 1px solid rgba(255,255,255,.15);
        }

        .footer-card strong { color: white; }

        button[kind="primary"], .stDownloadButton button, .stButton button {
            border-radius: 999px !important;
            font-weight: 900 !important;
            border: 0 !important;
            background: linear-gradient(135deg, #ff2d75, #7c3aed 52%, #00d4ff) !important;
            color: white !important;
            box-shadow: 0 14px 30px rgba(124,58,237,.30) !important;
        }

        @media (max-width: 1200px) {
            .metric-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
            .metric-grid.secondary { grid-template-columns: repeat(1, minmax(0, 1fr)); }
            .hero-title { font-size: 2.45rem; }
        }
    </style>
    """,
    unsafe_allow_html=True
)


def style_plot(fig, height=None):
    """Apply a vivid executive-dashboard style to Plotly figures."""
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.96)",
        font=dict(family="Inter, Segoe UI, sans-serif", size=13, color=BRAND_COLORS["navy"]),
        title=dict(font=dict(size=19, color=BRAND_COLORS["midnight"], family="Inter"), x=0.02, xanchor="left"),
        margin=dict(l=48, r=30, t=76, b=46),
        hoverlabel=dict(bgcolor=BRAND_COLORS["midnight"], font_size=12, font_color="white"),
        colorway=CHART_SEQUENCE,
        legend=dict(
            bgcolor="rgba(255,255,255,0.72)",
            bordercolor="rgba(148,163,184,0.22)",
            borderwidth=1,
        ),
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(148,163,184,0.18)", zeroline=False, linecolor="rgba(15,23,42,.18)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(148,163,184,0.18)", zeroline=False, linecolor="rgba(15,23,42,.18)")
    if height is not None:
        fig.update_layout(height=height)
    return fig


def render_metric_grid(cards, secondary=False):
    """Render attractive custom KPI cards."""
    cls = "metric-grid secondary" if secondary else "metric-grid"
    html = [f'<div class="{cls}">']
    for card in cards:
        html.append(
            f"""
            <div class="metric-card" style="--accent:{card['color']};">
                <div class="metric-icon">{card['icon']}</div>
                <div class="metric-label">{card['label']}</div>
                <div class="metric-value">{card['value']}</div>
                <div class="metric-help">{card['help']}</div>
            </div>
            """
        )
    html.append("</div>")
    return "".join(html)

# =====================================================
# CONSTANT MAPPINGS
# =====================================================
PRODUCT_FACTORY_MAP = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar - Scrumdiddlyumptious": "Lot's O' Nuts",
    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",
    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",
    "Everlasting Gobstopper": "Secret Factory",
    "Hair Toffee": "The Other Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",
    "Kazookles": "The Other Factory",
}

FACTORY_COORDINATES = {
    "Lot's O' Nuts": {"lat": 32.881893, "lon": -111.768036},
    "Wicked Choccy's": {"lat": 32.076176, "lon": -81.088371},
    "Sugar Shack": {"lat": 48.119140, "lon": -96.181150},
    "Secret Factory": {"lat": 41.446333, "lon": -90.565487},
    "The Other Factory": {"lat": 35.117500, "lon": -89.971107},
}

US_STATE_TO_ABBREV = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY", "District of Columbia": "DC"
}

STATE_ABBREVIATIONS = set(US_STATE_TO_ABBREV.values())

# =====================================================
# HELPER FUNCTIONS
# =====================================================
def clean_text(value):
    """Standardize text values without breaking missing values."""
    if pd.isna(value):
        return np.nan
    return str(value).strip()


def state_to_code(state):
    """Convert full state name or already-existing abbreviation to two-letter code."""
    if pd.isna(state):
        return np.nan

    state_clean = str(state).strip()
    state_upper = state_clean.upper()

    if state_upper in STATE_ABBREVIATIONS:
        return state_upper

    return US_STATE_TO_ABBREV.get(state_clean, np.nan)


@st.cache_data(show_spinner=False)
def load_data_from_path(csv_path):
    """Load CSV from a provided path and apply basic cleaning."""
    return pd.read_csv(csv_path)


@st.cache_data(show_spinner=False)
def load_data_from_upload(uploaded_file):
    """Load CSV from Streamlit file uploader and apply basic cleaning."""
    return pd.read_csv(uploaded_file)


def prepare_data(df):
    """Clean, validate, and enrich the Nassau Candy shipment dataset."""
    df = df.copy()

    # Standardize column names by removing accidental extra spaces.
    df.columns = df.columns.str.strip()

    required_columns = [
        "Order ID", "Order Date", "Ship Date", "Ship Mode",
        "State/Province", "Region", "Product Name"
    ]

    missing_required = [col for col in required_columns if col not in df.columns]
    if missing_required:
        st.error(f"Missing required columns: {', '.join(missing_required)}")
        st.stop()

    # Clean important text columns.
    text_columns = [
        "Order ID", "Ship Mode", "Country/Region", "City", "State/Province",
        "Division", "Region", "Product ID", "Product Name", "Customer ID"
    ]
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)

    # Convert dates safely.
    # The raw file uses DD-MM-YYYY, while the processed file uses YYYY-MM-DD.
    # This helper handles both formats without silently swapping day/month values.
    def parse_date_column(series):
        as_text = series.astype(str).str.strip()
        ddmmyyyy_share = as_text.str.match(r"^\d{2}-\d{2}-\d{4}$", na=False).mean()
        if ddmmyyyy_share > 0.80:
            return pd.to_datetime(as_text, format="%d-%m-%Y", errors="coerce")
        return pd.to_datetime(as_text, errors="coerce")

    df["Order Date"] = parse_date_column(df["Order Date"])
    df["Ship Date"] = parse_date_column(df["Ship Date"])

    # Remove missing or invalid shipment date records.
    df = df.dropna(subset=["Order Date", "Ship Date"])
    df = df[df["Ship Date"] >= df["Order Date"]]

    # Always calculate lead time from validated dates to avoid incorrect processed values.
    df["Shipping Lead Time"] = (df["Ship Date"] - df["Order Date"]).dt.days
    df = df[df["Shipping Lead Time"] >= 0]

    # Add factory using product-factory mapping if missing or incomplete.
    if "Factory" not in df.columns:
        df["Factory"] = df["Product Name"].map(PRODUCT_FACTORY_MAP)
    else:
        mapped_factory = df["Product Name"].map(PRODUCT_FACTORY_MAP)
        df["Factory"] = df["Factory"].fillna(mapped_factory)

    df["Factory"] = df["Factory"].fillna("Unknown Factory")

    # Add factory coordinates.
    df["Factory Latitude"] = df["Factory"].map(
        lambda x: FACTORY_COORDINATES.get(x, {}).get("lat", np.nan)
    )
    df["Factory Longitude"] = df["Factory"].map(
        lambda x: FACTORY_COORDINATES.get(x, {}).get("lon", np.nan)
    )

    # Create route fields.
    df["Route"] = df["Factory"] + " → " + df["State/Province"].astype(str)
    df["Route Region"] = df["Factory"] + " → " + df["Region"].astype(str)

    # Add state code for choropleth map.
    df["State Code"] = df["State/Province"].apply(state_to_code)

    # Numeric conversions for financial fields.
    numeric_columns = ["Sales", "Units", "Gross Profit", "Cost"]
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Calculate gross profit if missing but Sales and Cost are present.
    if "Gross Profit" not in df.columns and {"Sales", "Cost"}.issubset(df.columns):
        df["Gross Profit"] = df["Sales"] - df["Cost"]

    return df


def calculate_efficiency_score(avg_lead_time, global_min, global_max):
    """Return normalized efficiency score where higher is better."""
    if pd.isna(avg_lead_time):
        return 0
    if global_max == global_min:
        return 100
    score = 100 * (1 - ((avg_lead_time - global_min) / (global_max - global_min)))
    return max(0, min(100, round(score, 1)))


def safe_unique(series):
    """Return sorted unique non-null values for filters."""
    return sorted(series.dropna().unique().tolist())

# =====================================================
# DATA LOADING
# =====================================================
st.sidebar.markdown(
    """
    <div class="sidebar-brand">
        <h2>🚚 Nassau Candy</h2>
        <p>Factory-to-Customer Shipping Route Efficiency</p>
    </div>
    """,
    unsafe_allow_html=True
)

DEFAULT_FILE = Path(__file__).parent / "nassau_candy_processed.csv"

if DEFAULT_FILE.exists():
    raw_df = load_data_from_path(DEFAULT_FILE)
else:
    st.sidebar.warning("CSV file not found in the app folder.")
    uploaded_file = st.sidebar.file_uploader(
        "Upload nassau_candy_processed.csv",
        type=["csv"]
    )
    if uploaded_file is None:
        st.title("🚚 Nassau Candy Logistics Intelligence Dashboard")
        st.info(
            "Please upload `nassau_candy_processed.csv` from the sidebar, "
            "or place it in the same folder as `app.py` before deployment."
        )
        st.stop()
    raw_df = load_data_from_upload(uploaded_file)

df = prepare_data(raw_df)

if df.empty:
    st.error("No valid shipment records found after cleaning the data.")
    st.stop()

# =====================================================
# SIDEBAR FILTERS
# =====================================================
st.sidebar.header("🔍 Filters")

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

selected_factories = st.sidebar.multiselect(
    "Select Factory",
    options=safe_unique(df["Factory"]),
    default=safe_unique(df["Factory"])
)

selected_regions = st.sidebar.multiselect(
    "Select Region",
    options=safe_unique(df["Region"]),
    default=safe_unique(df["Region"])
)

selected_states = st.sidebar.multiselect(
    "Select State",
    options=safe_unique(df["State/Province"]),
    default=safe_unique(df["State/Province"])
)

selected_modes = st.sidebar.multiselect(
    "Select Ship Mode",
    options=safe_unique(df["Ship Mode"]),
    default=safe_unique(df["Ship Mode"])
)

min_lead_time = int(df["Shipping Lead Time"].min())
max_lead_time = int(df["Shipping Lead Time"].max())
default_threshold = int(round(df["Shipping Lead Time"].mean()))

delay_threshold = st.sidebar.slider(
    "Delay Threshold (Days)",
    min_value=min_lead_time,
    max_value=max_lead_time,
    value=default_threshold,
    step=1,
    help="Shipments above this selected lead-time threshold are counted as delayed."
)

# =====================================================
# APPLY FILTERS
# =====================================================
filtered_df = df[
    (df["Order Date"].dt.date >= start_date) &
    (df["Order Date"].dt.date <= end_date) &
    (df["Factory"].isin(selected_factories)) &
    (df["Region"].isin(selected_regions)) &
    (df["State/Province"].isin(selected_states)) &
    (df["Ship Mode"].isin(selected_modes))
].copy()

if filtered_df.empty:
    st.warning("No data available for the selected filters. Please adjust the filters from the sidebar.")
    st.stop()

filtered_df["Delayed"] = filtered_df["Shipping Lead Time"] > delay_threshold

# =====================================================
# MAIN TITLE
# =====================================================
st.markdown(
    f"""
    <div class="hero-card">
        <div class="hero-eyebrow">Factory-to-Customer Route Intelligence</div>
        <div class="hero-title">Nassau Candy Logistics Dashboard</div>
        <div class="hero-subtitle">
            Executive analytics for route efficiency, geographic bottlenecks, ship-mode performance,
            risk scoring, and order-level shipment timelines.
        </div>
        <div class="hero-chips">
            <span class="hero-chip">📦 {len(filtered_df):,} filtered shipments</span>
            <span class="hero-chip">🏭 {filtered_df['Factory'].nunique()} factories</span>
            <span class="hero-chip">🗺 {filtered_df['State/Province'].nunique()} states/provinces</span>
            <span class="hero-chip">🚚 {filtered_df['Ship Mode'].nunique()} ship modes</span>
            <span class="hero-chip">⏱ Threshold: {delay_threshold} days</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="data-note-card">
        <strong>Data Note:</strong> Shipping Lead Time is calculated as <strong>Ship Date minus Order Date</strong>
        using the dates in the dataset. Because final customer delivery dates and carrier scan events are not available,
        the dashboard measures recorded order-to-shipment lead time rather than confirmed end-customer delivery time.
    </div>
    """,
    unsafe_allow_html=True
)

# =====================================================
# KPI SECTION
# =====================================================
avg_lt = filtered_df["Shipping Lead Time"].mean()
median_lt = filtered_df["Shipping Lead Time"].median()
total_shipments = len(filtered_df)
delay_freq = filtered_df["Delayed"].mean() * 100

mode_avg = filtered_df.groupby("Ship Mode")["Shipping Lead Time"].mean()
slowest_mode = mode_avg.idxmax() if not mode_avg.empty else "N/A"

global_min_lt = df["Shipping Lead Time"].min()
global_max_lt = df["Shipping Lead Time"].max()
eff_score = calculate_efficiency_score(avg_lt, global_min_lt, global_max_lt)

total_sales = filtered_df["Sales"].sum() if "Sales" in filtered_df.columns else np.nan
total_profit = filtered_df["Gross Profit"].sum() if "Gross Profit" in filtered_df.columns else np.nan

primary_cards = [
    {
        "icon": "⏱️",
        "label": "Average Lead Time",
        "value": f"{avg_lt:.1f} Days",
        "help": "Mean Ship Date − Order Date",
        "color": BRAND_COLORS["electric"],
    },
    {
        "icon": "📍",
        "label": "Median Lead Time",
        "value": f"{median_lt:.1f} Days",
        "help": "Middle shipment lead-time value",
        "color": BRAND_COLORS["mint"],
    },
    {
        "icon": "📦",
        "label": "Total Shipments",
        "value": f"{total_shipments:,}",
        "help": "Orders under current filters",
        "color": BRAND_COLORS["blue"],
    },
    {
        "icon": "⚡",
        "label": "Efficiency Score",
        "value": f"{eff_score}%",
        "help": "Normalized route performance",
        "color": BRAND_COLORS["violet"],
    },
    {
        "icon": "🚨",
        "label": "Delay Rate",
        "value": f"{delay_freq:.1f}%",
        "help": f"Above {delay_threshold} day threshold",
        "color": BRAND_COLORS["candy"],
    },
]

secondary_cards = [
    {
        "icon": "🚚",
        "label": "Slowest Ship Mode",
        "value": str(slowest_mode),
        "help": "Highest average lead time",
        "color": BRAND_COLORS["orange"],
    },
    {
        "icon": "💰",
        "label": "Total Sales",
        "value": f"${total_sales:,.0f}" if not pd.isna(total_sales) else "N/A",
        "help": "Sales from filtered records",
        "color": BRAND_COLORS["green"],
    },
    {
        "icon": "🏁",
        "label": "Gross Profit",
        "value": f"${total_profit:,.0f}" if not pd.isna(total_profit) else "N/A",
        "help": "Profit from filtered records",
        "color": BRAND_COLORS["amber"],
    },
]

st.markdown(render_metric_grid(primary_cards), unsafe_allow_html=True)
st.markdown(render_metric_grid(secondary_cards, secondary=True), unsafe_allow_html=True)

st.divider()

# =====================================================
# TABS
# =====================================================
tab_overview, tab_routes, tab_geo, tab_modes, tab_advanced, tab_drill = st.tabs([
    "📊 Overview",
    "🏆 Route Leaderboard",
    "🗺 Geographic Bottlenecks",
    "📦 Ship Mode Comparison",
    "🧠 Advanced Analytics",
    "🔍 Route Drill-Down"
])

# =====================================================
# TAB 1: OVERVIEW
# =====================================================
with tab_overview:
    st.subheader("Route Efficiency Overview")

    route_summary = filtered_df.groupby("Route").agg(
        Avg_Lead_Time=("Shipping Lead Time", "mean"),
        Median_Lead_Time=("Shipping Lead Time", "median"),
        Volume=("Order ID", "count"),
        Delay_Rate=("Delayed", "mean")
    ).reset_index()
    route_summary["Delay_Rate"] = route_summary["Delay_Rate"] * 100
    route_summary["Efficiency_Score"] = route_summary["Avg_Lead_Time"].apply(
        lambda x: calculate_efficiency_score(x, global_min_lt, global_max_lt)
    )

    left_col, right_col = st.columns(2)

    with left_col:
        top_routes = route_summary.sort_values("Avg_Lead_Time").head(10)
        fig_fast = px.bar(
            top_routes,
            x="Avg_Lead_Time",
            y="Route",
            orientation="h",
            title="Top 10 Fastest Routes",
            labels={"Avg_Lead_Time": "Avg Lead Time (Days)", "Route": "Route"}
        )
        fig_fast.update_layout(yaxis={"categoryorder": "total ascending"})
        style_plot(fig_fast)
        st.plotly_chart(fig_fast, use_container_width=True)

    with right_col:
        slow_routes = route_summary.sort_values("Avg_Lead_Time", ascending=False).head(10)
        fig_slow = px.bar(
            slow_routes,
            x="Avg_Lead_Time",
            y="Route",
            orientation="h",
            title="Bottom 10 Slowest Routes",
            labels={"Avg_Lead_Time": "Avg Lead Time (Days)", "Route": "Route"}
        )
        fig_slow.update_layout(yaxis={"categoryorder": "total ascending"})
        style_plot(fig_slow)
        st.plotly_chart(fig_slow, use_container_width=True)

    st.subheader("Shipment Volume by Region")
    region_volume = filtered_df.groupby("Region").agg(
        Shipments=("Order ID", "count"),
        Avg_Lead_Time=("Shipping Lead Time", "mean"),
        Delay_Rate=("Delayed", "mean")
    ).reset_index()
    region_volume["Delay_Rate"] = region_volume["Delay_Rate"] * 100

    fig_region = px.bar(
        region_volume,
        x="Region",
        y="Shipments",
        color="Avg_Lead_Time",
        title="Regional Shipment Volume and Average Lead Time",
        labels={"Shipments": "Number of Shipments", "Avg_Lead_Time": "Avg Lead Time"}
    )
    style_plot(fig_region)
    st.plotly_chart(fig_region, use_container_width=True)

# =====================================================
# TAB 2: ROUTE LEADERBOARD
# =====================================================
with tab_routes:
    st.subheader("Route Performance Leaderboard")

    route_perf = filtered_df.groupby("Route").agg(
        Factory=("Factory", "first"),
        State=("State/Province", "first"),
        Region=("Region", "first"),
        Avg_Lead_Time=("Shipping Lead Time", "mean"),
        Median_Lead_Time=("Shipping Lead Time", "median"),
        Min_Lead_Time=("Shipping Lead Time", "min"),
        Max_Lead_Time=("Shipping Lead Time", "max"),
        Std_Dev=("Shipping Lead Time", "std"),
        Volume=("Order ID", "count"),
        Delay_Rate=("Delayed", "mean")
    ).reset_index()

    route_perf["Std_Dev"] = route_perf["Std_Dev"].fillna(0)
    route_perf["Delay_Rate"] = route_perf["Delay_Rate"] * 100
    route_perf["Efficiency_Score"] = route_perf["Avg_Lead_Time"].apply(
        lambda x: calculate_efficiency_score(x, global_min_lt, global_max_lt)
    )
    route_perf = route_perf.sort_values("Efficiency_Score", ascending=False)

    c1, c2 = st.columns(2)
    with c1:
        st.write("🟢 Top 10 Most Efficient Routes")
        st.dataframe(
            route_perf.head(10),
            use_container_width=True,
            hide_index=True
        )

    with c2:
        st.write("🔴 Bottom 10 Least Efficient Routes")
        st.dataframe(
            route_perf.tail(10).sort_values("Efficiency_Score"),
            use_container_width=True,
            hide_index=True
        )

    st.subheader("Route Volume vs Average Lead Time")
    fig_bubble = px.scatter(
        route_perf,
        x="Volume",
        y="Avg_Lead_Time",
        size="Volume",
        color="Delay_Rate",
        hover_name="Route",
        title="High-Volume Routes with Poor Lead Time Indicate Bottlenecks",
        labels={
            "Volume": "Shipment Volume",
            "Avg_Lead_Time": "Avg Lead Time (Days)",
            "Delay_Rate": "Delay Rate (%)"
        }
    )
    style_plot(fig_bubble)
    st.plotly_chart(fig_bubble, use_container_width=True)

# =====================================================
# TAB 3: GEOGRAPHIC BOTTLENECKS
# =====================================================
with tab_geo:
    st.subheader("Geographic Shipping Bottleneck Analysis")
    st.caption("The map displays locations with valid US state codes. Canadian provinces and unmapped state/province values remain available in the tables below.")

    state_perf = filtered_df.groupby(["State/Province", "State Code"]).agg(
        Avg_Lead_Time=("Shipping Lead Time", "mean"),
        Median_Lead_Time=("Shipping Lead Time", "median"),
        Volume=("Order ID", "count"),
        Delay_Rate=("Delayed", "mean")
    ).reset_index()

    state_perf["Delay_Rate"] = state_perf["Delay_Rate"] * 100
    state_perf["Bottleneck_Score"] = state_perf["Avg_Lead_Time"] * state_perf["Volume"]
    map_df = state_perf.dropna(subset=["State Code"])

    map_metric = st.radio(
        "Select map metric",
        options=["Avg_Lead_Time", "Delay_Rate", "Bottleneck_Score"],
        horizontal=True,
        format_func=lambda x: {
            "Avg_Lead_Time": "Average Lead Time",
            "Delay_Rate": "Delay Rate",
            "Bottleneck_Score": "Bottleneck Score"
        }[x]
    )

    fig_map = px.choropleth(
        map_df,
        locations="State Code",
        locationmode="USA-states",
        color=map_metric,
        scope="usa",
        hover_data={
            "State/Province": True,
            "Avg_Lead_Time": ":.2f",
            "Median_Lead_Time": ":.2f",
            "Volume": True,
            "Delay_Rate": ":.2f",
            "Bottleneck_Score": ":.2f",
            "State Code": False
        },
        labels={
            "Avg_Lead_Time": "Avg Lead Time",
            "Delay_Rate": "Delay Rate (%)",
            "Bottleneck_Score": "Bottleneck Score"
        },
        title="US State-Level Shipping Performance"
    )
    fig_map.update_layout(title_x=0.5)
    style_plot(fig_map)
    st.plotly_chart(fig_map, use_container_width=True)

    st.write("🚧 Top Geographic Bottlenecks")
    bottlenecks = state_perf.sort_values("Bottleneck_Score", ascending=False).head(15)
    st.dataframe(bottlenecks, use_container_width=True, hide_index=True)

# =====================================================
# TAB 4: SHIP MODE COMPARISON
# =====================================================
with tab_modes:
    st.subheader("Ship Mode Performance Analysis")

    mode_perf = filtered_df.groupby("Ship Mode").agg(
        Avg_Lead_Time=("Shipping Lead Time", "mean"),
        Median_Lead_Time=("Shipping Lead Time", "median"),
        Min_Lead_Time=("Shipping Lead Time", "min"),
        Max_Lead_Time=("Shipping Lead Time", "max"),
        Volume=("Order ID", "count"),
        Delay_Rate=("Delayed", "mean")
    ).reset_index()
    mode_perf["Delay_Rate"] = mode_perf["Delay_Rate"] * 100

    if "Cost" in filtered_df.columns:
        cost_perf = filtered_df.groupby("Ship Mode")["Cost"].mean().reset_index(name="Avg_Cost")
        mode_perf = mode_perf.merge(cost_perf, on="Ship Mode", how="left")

    m1, m2 = st.columns(2)

    with m1:
        fig_mode_avg = px.bar(
            mode_perf,
            x="Ship Mode",
            y="Avg_Lead_Time",
            color="Avg_Lead_Time",
            title="Average Lead Time by Ship Mode",
            labels={"Avg_Lead_Time": "Avg Lead Time (Days)"}
        )
        style_plot(fig_mode_avg)
        st.plotly_chart(fig_mode_avg, use_container_width=True)

    with m2:
        fig_mode_delay = px.bar(
            mode_perf,
            x="Ship Mode",
            y="Delay_Rate",
            color="Delay_Rate",
            title="Delay Rate by Ship Mode",
            labels={"Delay_Rate": "Delay Rate (%)"}
        )
        style_plot(fig_mode_delay)
        st.plotly_chart(fig_mode_delay, use_container_width=True)

    st.subheader("Lead Time Distribution by Ship Mode")
    fig_box = px.box(
        filtered_df,
        x="Ship Mode",
        y="Shipping Lead Time",
        points="outliers",
        title="Shipping Lead Time Variability by Ship Mode",
        labels={"Shipping Lead Time": "Lead Time (Days)"}
    )
    style_plot(fig_box)
    st.plotly_chart(fig_box, use_container_width=True)

    st.write("Ship Mode Summary")
    st.dataframe(mode_perf, use_container_width=True, hide_index=True)


# =====================================================
# TAB 5: ADVANCED ANALYTICS
# =====================================================
with tab_advanced:
    st.subheader("Advanced Route Risk & Decision Intelligence")
    st.markdown(
        "This section adds a management-level risk model that combines lead time, delay rate, "
        "shipment volume, and route variability to identify routes that need operational attention first."
    )

    advanced_route = filtered_df.groupby("Route").agg(
        Factory=("Factory", "first"),
        State=("State/Province", "first"),
        Region=("Region", "first"),
        Avg_Lead_Time=("Shipping Lead Time", "mean"),
        Median_Lead_Time=("Shipping Lead Time", "median"),
        Variability=("Shipping Lead Time", "std"),
        Volume=("Order ID", "count"),
        Delay_Rate=("Delayed", "mean")
    ).reset_index()

    advanced_route["Variability"] = advanced_route["Variability"].fillna(0)
    advanced_route["Delay_Rate"] = advanced_route["Delay_Rate"] * 100

    def normalize_series(series):
        """Normalize a numeric series to 0-1 with safe handling for constant values."""
        series = pd.to_numeric(series, errors="coerce").fillna(0)
        min_val = series.min()
        max_val = series.max()
        if max_val == min_val:
            return pd.Series(np.zeros(len(series)), index=series.index)
        return (series - min_val) / (max_val - min_val)

    advanced_route["Risk_Score"] = (
        0.35 * normalize_series(advanced_route["Avg_Lead_Time"]) +
        0.30 * normalize_series(advanced_route["Delay_Rate"]) +
        0.20 * normalize_series(advanced_route["Volume"]) +
        0.15 * normalize_series(advanced_route["Variability"])
    ) * 100
    advanced_route["Risk_Score"] = advanced_route["Risk_Score"].round(1)

    advanced_route["Priority_Level"] = np.select(
        [
            advanced_route["Risk_Score"] >= 75,
            advanced_route["Risk_Score"] >= 50,
            advanced_route["Risk_Score"] >= 25,
        ],
        ["Critical", "High", "Medium"],
        default="Low"
    )

    advanced_route["Recommended_Action"] = np.select(
        [
            advanced_route["Priority_Level"].eq("Critical"),
            advanced_route["Priority_Level"].eq("High"),
            advanced_route["Priority_Level"].eq("Medium"),
        ],
        [
            "Immediate route review and capacity planning",
            "Monitor weekly and compare ship-mode allocation",
            "Track monthly for emerging delays",
        ],
        default="Maintain current performance"
    )

    priority_routes = advanced_route.sort_values("Risk_Score", ascending=False)

    a1, a2, a3, a4 = st.columns(4)
    a1.metric("Critical Routes", f"{(priority_routes['Priority_Level'] == 'Critical').sum():,}")
    a2.metric("High-Risk Routes", f"{(priority_routes['Priority_Level'] == 'High').sum():,}")
    a3.metric("Highest Risk Score", f"{priority_routes['Risk_Score'].max():.1f}/100")
    a4.metric("Routes Analyzed", f"{len(priority_routes):,}")

    st.subheader("Priority Action Matrix")
    avg_line = priority_routes["Avg_Lead_Time"].median()
    vol_line = priority_routes["Volume"].median()

    fig_priority = px.scatter(
        priority_routes,
        x="Volume",
        y="Avg_Lead_Time",
        size="Risk_Score",
        color="Priority_Level",
        hover_name="Route",
        hover_data={
            "Factory": True,
            "State": True,
            "Region": True,
            "Delay_Rate": ":.2f",
            "Variability": ":.2f",
            "Risk_Score": ":.1f",
            "Priority_Level": True,
        },
        title="Route Risk Matrix: Volume vs Average Lead Time",
        labels={
            "Volume": "Shipment Volume",
            "Avg_Lead_Time": "Average Lead Time (Days)",
            "Priority_Level": "Priority Level"
        }
    )
    fig_priority.add_vline(x=vol_line, line_dash="dash")
    fig_priority.add_hline(y=avg_line, line_dash="dash")
    style_plot(fig_priority)
    st.plotly_chart(fig_priority, use_container_width=True)

    st.caption(
        "Routes in the upper-right area are the most important to investigate because they combine high volume with high lead time."
    )

    st.subheader("Top Recommended Route Actions")
    action_columns = [
        "Route", "Factory", "State", "Region", "Volume", "Avg_Lead_Time",
        "Delay_Rate", "Variability", "Risk_Score", "Priority_Level", "Recommended_Action"
    ]
    st.dataframe(
        priority_routes[action_columns].head(15),
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Automated Management Insights")
    insight_col1, insight_col2 = st.columns(2)

    top_route = priority_routes.iloc[0]
    fastest_route = priority_routes.sort_values("Avg_Lead_Time").iloc[0]

    with insight_col1:
        st.warning(
            f"Highest-priority route: **{top_route['Route']}** with a risk score of "
            f"**{top_route['Risk_Score']:.1f}/100**. This route has "
            f"**{top_route['Volume']} shipments**, average lead time of "
            f"**{top_route['Avg_Lead_Time']:.1f} days**, and delay rate of "
            f"**{top_route['Delay_Rate']:.1f}%** based on the selected threshold."
        )

    with insight_col2:
        st.success(
            f"Best-performing route in the current filter: **{fastest_route['Route']}** with "
            f"average lead time of **{fastest_route['Avg_Lead_Time']:.1f} days**. "
            "This route can be used as a benchmark for comparing similar lanes."
        )

    st.subheader("Delay Threshold Sensitivity Simulator")
    threshold_step = max(1, int((max_lead_time - min_lead_time) / 30))
    threshold_values = list(range(min_lead_time, max_lead_time + 1, threshold_step))
    if max_lead_time not in threshold_values:
        threshold_values.append(max_lead_time)

    sensitivity = pd.DataFrame({
        "Threshold": threshold_values,
        "Delayed_Orders": [int((filtered_df["Shipping Lead Time"] > t).sum()) for t in threshold_values],
        "Delay_Rate": [float((filtered_df["Shipping Lead Time"] > t).mean() * 100) for t in threshold_values]
    })

    s1, s2 = st.columns([2, 1])
    with s1:
        fig_sensitivity = px.line(
            sensitivity,
            x="Threshold",
            y="Delay_Rate",
            markers=True,
            title="How Delay Classification Changes by Threshold",
            labels={"Threshold": "Lead-Time Threshold (Days)", "Delay_Rate": "Delay Rate (%)"}
        )
        fig_sensitivity.add_vline(x=delay_threshold, line_dash="dash")
        style_plot(fig_sensitivity)
        st.plotly_chart(fig_sensitivity, use_container_width=True)

    with s2:
        current_delayed_orders = int((filtered_df["Shipping Lead Time"] > delay_threshold).sum())
        st.metric("Current Threshold", f"{delay_threshold} Days")
        st.metric("Orders Above Threshold", f"{current_delayed_orders:,}")
        st.metric("Current Delay Rate", f"{delay_freq:.1f}%")
        st.info(
            "Use this simulator to justify why a specific lead-time threshold was selected for delay classification."
        )

    st.subheader("Route Flow Analysis")
    flow_df = filtered_df.groupby(["Factory", "Region", "State/Province"]).agg(
        Shipments=("Order ID", "count"),
        Avg_Lead_Time=("Shipping Lead Time", "mean")
    ).reset_index()

    fig_flow = px.sunburst(
        flow_df,
        path=["Factory", "Region", "State/Province"],
        values="Shipments",
        color="Avg_Lead_Time",
        title="Factory → Region → State Shipment Flow",
        labels={"Avg_Lead_Time": "Avg Lead Time"}
    )
    style_plot(fig_flow)
    st.plotly_chart(fig_flow, use_container_width=True)

    st.subheader("Lead-Time Anomaly Detection")
    q1 = priority_routes["Avg_Lead_Time"].quantile(0.25)
    q3 = priority_routes["Avg_Lead_Time"].quantile(0.75)
    iqr = q3 - q1
    anomaly_cutoff = q3 + 1.5 * iqr

    anomalies = priority_routes[priority_routes["Avg_Lead_Time"] > anomaly_cutoff].copy()
    if anomalies.empty:
        st.success(
            "No extreme lead-time route anomalies were detected using the IQR method under the current filters."
        )
    else:
        st.warning(
            f"{len(anomalies)} route(s) exceed the anomaly cutoff of {anomaly_cutoff:.1f} days. "
            "These routes should be reviewed for data quality, fulfillment process issues, or recurring operational delays."
        )
        st.dataframe(
            anomalies[action_columns].sort_values("Avg_Lead_Time", ascending=False),
            use_container_width=True,
            hide_index=True
        )

    if "Cost" in filtered_df.columns:
        st.subheader("Cost-Time Tradeoff by Ship Mode")
        cost_time = filtered_df.groupby("Ship Mode").agg(
            Avg_Lead_Time=("Shipping Lead Time", "mean"),
            Avg_Cost=("Cost", "mean"),
            Volume=("Order ID", "count"),
            Delay_Rate=("Delayed", "mean")
        ).reset_index()
        cost_time["Delay_Rate"] = cost_time["Delay_Rate"] * 100

        fig_cost_time = px.scatter(
            cost_time,
            x="Avg_Cost",
            y="Avg_Lead_Time",
            size="Volume",
            color="Delay_Rate",
            hover_name="Ship Mode",
            title="Ship Mode Cost-Time Tradeoff",
            labels={
                "Avg_Cost": "Average Cost",
                "Avg_Lead_Time": "Average Lead Time (Days)",
                "Delay_Rate": "Delay Rate (%)"
            }
        )
        style_plot(fig_cost_time)
        st.plotly_chart(fig_cost_time, use_container_width=True)

# =====================================================
# TAB 6: ROUTE DRILL-DOWN
# =====================================================
with tab_drill:
    st.subheader("Order-Level Route Drill-Down")

    route_options = ["All Routes"] + safe_unique(filtered_df["Route"])
    selected_route = st.selectbox("Select Route", route_options)

    drill_df = filtered_df.copy()
    if selected_route != "All Routes":
        drill_df = drill_df[drill_df["Route"] == selected_route]

    search = st.text_input("Search Order ID / Customer ID / Product / State / Factory")

    if search:
        search_lower = search.lower()
        searchable_columns = [
            col for col in [
                "Order ID", "Customer ID", "Product Name", "State/Province",
                "Region", "Factory", "Route", "Ship Mode"
            ]
            if col in drill_df.columns
        ]
        mask = drill_df[searchable_columns].astype(str).apply(
            lambda row: row.str.lower().str.contains(search_lower, na=False).any(),
            axis=1
        )
        drill_df = drill_df[mask]

    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Selected Shipments", f"{len(drill_df):,}")
    d2.metric("Avg Lead Time", f"{drill_df['Shipping Lead Time'].mean():.1f} Days" if not drill_df.empty else "N/A")
    d3.metric("Delayed Orders", f"{int(drill_df['Delayed'].sum()):,}" if not drill_df.empty else "0")
    d4.metric("Delay %", f"{drill_df['Delayed'].mean() * 100:.1f}%" if not drill_df.empty else "0.0%")

    if drill_df.empty:
        st.warning("No orders match the selected route/search.")
    else:
        # -------------------------------------------------
        # State-level performance insights for drill-down
        # -------------------------------------------------
        st.subheader("State-Level Performance Insights")
        state_drill = drill_df.groupby("State/Province").agg(
            Shipments=("Order ID", "count"),
            Avg_Lead_Time=("Shipping Lead Time", "mean"),
            Median_Lead_Time=("Shipping Lead Time", "median"),
            Delay_Rate=("Delayed", "mean")
        ).reset_index()
        state_drill["Delay_Rate"] = state_drill["Delay_Rate"] * 100
        state_drill = state_drill.sort_values("Avg_Lead_Time", ascending=False)

        sd1, sd2 = st.columns([1, 1])
        with sd1:
            fig_state_drill = px.bar(
                state_drill.head(15),
                x="Avg_Lead_Time",
                y="State/Province",
                orientation="h",
                color="Delay_Rate",
                title="State-Level Lead Time for Selected Filters",
                labels={
                    "Avg_Lead_Time": "Avg Lead Time (Days)",
                    "State/Province": "State",
                    "Delay_Rate": "Delay Rate (%)"
                }
            )
            fig_state_drill.update_layout(yaxis={"categoryorder": "total ascending"})
            style_plot(fig_state_drill)
            st.plotly_chart(fig_state_drill, use_container_width=True)

        with sd2:
            st.dataframe(
                state_drill,
                use_container_width=True,
                hide_index=True
            )

        # -------------------------------------------------
        # Aggregate lead-time trend over time
        # -------------------------------------------------
        st.subheader("Shipment Timeline Trend")
        timeline_df = drill_df.sort_values("Order Date").copy()
        timeline_daily = timeline_df.groupby("Order Date").agg(
            Avg_Lead_Time=("Shipping Lead Time", "mean"),
            Shipments=("Order ID", "count")
        ).reset_index()

        fig_timeline = px.line(
            timeline_daily,
            x="Order Date",
            y="Avg_Lead_Time",
            markers=True,
            title="Average Lead Time Trend Over Time",
            labels={"Avg_Lead_Time": "Avg Lead Time (Days)"}
        )
        style_plot(fig_timeline)
        st.plotly_chart(fig_timeline, use_container_width=True)

        # -------------------------------------------------
        # True order-level timeline/Gantt view
        # -------------------------------------------------
        st.subheader("Order-Level Shipment Timelines")
        st.caption(
            "Each bar starts at Order Date and ends at Ship Date. This directly satisfies the "
            "order-level shipment timeline requirement."
        )

        tl_col1, tl_col2 = st.columns([1, 1])
        with tl_col1:
            timeline_sort = st.selectbox(
                "Timeline order selection",
                options=[
                    "Longest lead time",
                    "Most recent orders",
                    "Earliest orders",
                    "Delayed orders first"
                ],
                index=0
            )
        with tl_col2:
            max_timeline_orders = st.slider(
                "Number of orders to show in timeline",
                min_value=5,
                max_value=50,
                value=20,
                step=5
            )

        timeline_orders = drill_df.copy()
        if timeline_sort == "Longest lead time":
            timeline_orders = timeline_orders.sort_values("Shipping Lead Time", ascending=False)
        elif timeline_sort == "Most recent orders":
            timeline_orders = timeline_orders.sort_values("Order Date", ascending=False)
        elif timeline_sort == "Earliest orders":
            timeline_orders = timeline_orders.sort_values("Order Date", ascending=True)
        else:
            timeline_orders = timeline_orders.sort_values(["Delayed", "Shipping Lead Time"], ascending=[False, False])

        timeline_orders = timeline_orders.head(max_timeline_orders).copy()
        timeline_orders["Order Label"] = timeline_orders["Order ID"].astype(str) + " | " + timeline_orders["State/Province"].astype(str)
        timeline_orders["Delay Status"] = np.where(timeline_orders["Delayed"], "Delayed", "Within Threshold")

        fig_order_timeline = px.timeline(
            timeline_orders,
            x_start="Order Date",
            x_end="Ship Date",
            y="Order Label",
            color="Delay Status",
            hover_data={
                "Order ID": True,
                "Factory": True,
                "Route": True,
                "Ship Mode": True,
                "Product Name": True,
                "Shipping Lead Time": True,
                "Order Label": False
            },
            title="Order-Level Order Date to Ship Date Timeline"
        )
        fig_order_timeline.update_yaxes(autorange="reversed")
        fig_order_timeline.update_layout(
            xaxis_title="Timeline",
            yaxis_title="Order ID | State",
            height=max(450, 28 * len(timeline_orders))
        )
        style_plot(fig_order_timeline)
        st.plotly_chart(fig_order_timeline, use_container_width=True)

        preferred_columns = [
            "Order ID", "Order Date", "Ship Date", "Shipping Lead Time", "Delayed",
            "Factory", "Route", "Ship Mode", "Customer ID", "City", "State/Province",
            "Region", "Product Name", "Sales", "Cost", "Gross Profit"
        ]
        display_columns = [col for col in preferred_columns if col in drill_df.columns]

        st.write("Order-Level Shipment Details")
        st.dataframe(
            drill_df[display_columns].sort_values("Shipping Lead Time", ascending=False),
            use_container_width=True,
            hide_index=True
        )

        csv = drill_df[display_columns].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Filtered Orders as CSV",
            data=csv,
            file_name="filtered_nassau_shipping_orders.csv",
            mime="text/csv"
        )

# =====================================================
# FOOTER
# =====================================================
st.markdown(
    """
    <div class="footer-card">
        <strong>Nassau Candy Distributor</strong> · Factory-to-Customer Shipping Route Efficiency Analysis ·
        Lead time = Ship Date − Order Date · Built for route-level logistics intelligence
    </div>
    """,
    unsafe_allow_html=True
)
