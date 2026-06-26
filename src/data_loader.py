import pandas as pd
import requests
import streamlit as st

DATA_URL = (
    "https://raw.githubusercontent.com/owid/covid-19-data/"
    "master/public/data/owid-covid-data.csv"
)

COLUMNS_NEEDED = [
    "iso_code",
    "continent",
    "location",
    "date",
    "total_cases",
    "new_cases",
    "total_deaths",
    "new_deaths",
    "total_vaccinations",
    "people_fully_vaccinated",
    "population",
]

EXCLUDE_LOCATIONS =[
    "World",
    "High income",
    "Upper middle income",
    "Lower middle income",
    "Low income",
    "European Union",
    "Asia",
    "Europe",
    "North America",
    "South America",
    "Africa",
    "Oceania"
]

@st.cache_data(ttl=3600)
def load_covid_data():
    """
    Load COVID-19 data from Our World in Data.
    Cached for 1 hour using Streamlit's cache decorator.
    Returns a cleaned DataFrame.
    """
    try:
        df = pd.read_csv(DATA_URL, usecols=COLUMNS_NEEDED, parse_dates=["date"])
    
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()
    
    df = df[~df["location"].isin(EXCLUDE_LOCATIONS)]
    df = df.dropna(subset=["continent"])
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["location", "date"]).reset_index(drop=True)

    numeric_cols = [
        "total_cases", "new_cases",
        "total_deaths", "new_deaths",
        "total_vaccinations", "people_fully_vaccinated",
    ]
   
    df[numeric_cols] = df[numeric_cols].fillna(0)
    return df

def get_country_list(df):
    """Return sorted list of all unique countries."""
    return sorted(df["location"].unique().tolist())

def get_latest_stats(df, country):
    """Return the most recent rows of data for a given country."""
    country_df = df[df["location"] == country]
    if country_df.empty:
        return {}
    
    latest = country_df.sort_values("date").iloc[-1]
    return latest.to_dict()

def filter_by_country(df, country):
    """Return all rows for a given country, sorted by date."""
    return df[df["location"] == country].sort_values("date")

def get_top_countries(df, metric="total_cases", n=10):
    """Return top N countries by a given metric (latest values)."""

    latest = df.sort_values("date").groupby("location").last().reset_index()

    if metric not in latest.columns:
        raise ValueError(f"Invalid metric: {metric}")

    return (
        latest.nlargest(n, metric)[["location", metric]]
        .reset_index(drop=True)
    )
    




