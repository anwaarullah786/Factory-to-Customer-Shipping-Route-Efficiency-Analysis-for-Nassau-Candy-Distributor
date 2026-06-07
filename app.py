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
st.sidebar.title("🚚 Nassau Candy")
st.sidebar.caption("Factory-to-Customer Shipping Route Efficiency")

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
st.title("🚚 Nassau Candy Logistics Intelligence Dashboard")
st.markdown(
    "Analyze factory-to-customer shipping efficiency, regional bottlenecks, "
    "route performance, and ship mode behavior."
)
st.info(
    "Data note: Shipping Lead Time is calculated as Ship Date minus Order Date using the dates in the dataset. "
    "Because final customer delivery dates and carrier scan events are not available, the dashboard measures recorded order-to-shipment lead time rather than confirmed end-customer delivery time."
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

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("Avg Lead Time", f"{avg_lt:.1f} Days")
kpi2.metric("Median Lead Time", f"{median_lt:.1f} Days")
kpi3.metric("Total Shipments", f"{total_shipments:,}")
kpi4.metric("Efficiency Score", f"{eff_score}%")
kpi5.metric("Delay %", f"{delay_freq:.1f}%")

kpi6, kpi7, kpi8 = st.columns(3)
kpi6.metric("Slowest Ship Mode", slowest_mode)
if not pd.isna(total_sales):
    kpi7.metric("Total Sales", f"${total_sales:,.0f}")
else:
    kpi7.metric("Total Sales", "N/A")

if not pd.isna(total_profit):
    kpi8.metric("Total Gross Profit", f"${total_profit:,.0f}")
else:
    kpi8.metric("Total Gross Profit", "N/A")

st.divider()

# =====================================================
# TABS
# =====================================================
tab_overview, tab_routes, tab_geo, tab_modes, tab_drill = st.tabs([
    "📊 Overview",
    "🏆 Route Leaderboard",
    "🗺 Geographic Bottlenecks",
    "📦 Ship Mode Comparison",
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
    st.plotly_chart(fig_box, use_container_width=True)

    st.write("Ship Mode Summary")
    st.dataframe(mode_perf, use_container_width=True, hide_index=True)

# =====================================================
# TAB 5: ROUTE DRILL-DOWN
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
st.divider()
st.caption(
    "Nassau Candy Distributor | Factory-to-Customer Shipping Route Efficiency Analysis | Lead time = Ship Date - Order Date"
)
