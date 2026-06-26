import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data_loader import (
    load_covid_data,
    get_country_list,
    get_latest_stats,
    filter_by_country,
    get_top_countries,
)
from src.charts import (
    line_chart_cases,
    line_chart_deaths,
    bar_chart_top_countries,
    area_chart_vaccinations,
    choropleth_map,
)


# ── Page config ────────────────────────────────────────────────
st.set_page_config(
    page_title="COVID-19 Dashboard",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────
st.markdown("""

""", unsafe_allow_html=True)

# ── Load data ──────────────────────────────────────────────────
with st.spinner("Loading COVID-19 data from Our World in Data..."):
    df = load_covid_data()

if df.empty:
    st.error("Could not load data. Please check your internet connection.")
    st.stop()

# ── Sidebar ────────────────────────────────────────────────────
st.sidebar.title("🦠 COVID-19 Dashboard")
st.sidebar.markdown("**Project 05/100** — Built with Streamlit + Plotly")
st.sidebar.markdown("---")

country_list = get_country_list(df)
default_idx = country_list.index("India") if "India" in country_list else 0
selected_country = st.sidebar.selectbox(
    "Select Country",
    country_list,
    index=default_idx,
)

st.sidebar.markdown("---")
show_map = st.sidebar.checkbox("Show World Map", value=True)
map_metric = st.sidebar.selectbox(
    "Map Metric",
    ["total_cases", "total_deaths", "total_vaccinations"],
    format_func=lambda x: x.replace("_", " ").title(),
)

# ── Main header ────────────────────────────────────────────────
st.title(f"🦠 COVID-19 Dashboard — {selected_country}")
st.caption("Data source: Our World in Data (OWID) · Updated daily")
st.markdown("---")

# ── KPI metrics row ────────────────────────────────────────────
latest = get_latest_stats(df, selected_country)

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_cases = latest.get("total_cases", 0)
    st.metric("Total Cases", f"{total_cases:,.0f}")

with col2:
    total_deaths = latest.get("total_deaths", 0)
    st.metric("Total Deaths", f"{total_deaths:,.0f}")

with col3:
    total_vax = latest.get("total_vaccinations", 0)
    st.metric("Total Vaccinations", f"{total_vax:,.0f}")

with col4:
    pop = latest.get("population", 1)
    case_rate = (total_cases / pop * 100) if pop > 0 else 0
    st.metric("Case Rate", f"{case_rate:.2f}%")

st.markdown("---")

# ── Country time series charts ─────────────────────────────────
country_df = filter_by_country(df, selected_country)

col_left, col_right = st.columns(2)

with col_left:
    st.plotly_chart(
        line_chart_cases(country_df, selected_country),
        use_container_width=True,
    )

with col_right:
    st.plotly_chart(
        line_chart_deaths(country_df, selected_country),
        use_container_width=True,
    )

# ── Vaccination chart ──────────────────────────────────────────
vax_fig = area_chart_vaccinations(country_df, selected_country)
if vax_fig:
    st.plotly_chart(vax_fig, use_container_width=True)
else: 
    st.info(f"No vaccination data available for {selected_country}.")

# ── Top 10 countries ───────────────────────────────────────────
st.markdown("---")
st.subheader("Global Rankings — Top 10 Countries")

top_col1, top_col2 = st.columns(2)

with top_col1:
    top_cases = get_top_countries(df, "total_cases", 10)
    st.plotly_chart(
        bar_chart_top_countries(top_cases, "total_cases", "Total Cases"),
        use_container_width=True,
    )

with top_col2:
    top_deaths = get_top_countries(df, "total_deaths", 10)
    st.plotly_chart(
        bar_chart_top_countries(top_deaths, "total_deaths", "Total Deaths"),
        use_container_width=True,
    )

# ── World Map ──────────────────────────────────────────────────
if show_map:
    st.markdown("---")
    st.subheader("World Map")
    metric_labels = {
        "total_cases": "Total Cases",
        "total_deaths": "Total Deaths",
        "total_vaccinations": "Total Vaccinations",
    }
    map_fig = choropleth_map(
    df,
    map_metric,
    metric_label=metric_labels[map_metric],
    title=f"World {metric_labels[map_metric]} Map",
)
    st.plotly_chart(map_fig, use_container_width=True)

# ── Footer ─────────────────────────────────────────────────────
st.markdown("---")
st.caption(
    "Built by Khushi · Part of 100 Projects Challenge · "
    "Data: Our World in Data (ourworldindata.org)"
)