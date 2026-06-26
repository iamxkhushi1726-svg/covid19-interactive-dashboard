# 🦠 COVID-19 Interactive Dashboard

> Project 05/100 — Building a strong GitHub portfolio from scratch.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://iamxkhushi1726-svg-covid19-interactive-dashboard-app-qxbl02.streamlit.app/)

An interactive COVID-19 analytics dashboard built with Streamlit and Plotly.
Select any country, explore time series trends, compare top nations globally,
and visualise worldwide spread on an interactive choropleth map.

## Live Demo

👉 [Open Dashboard](https://iamxkhushi1726-svg-covid19-interactive-dashboard-app-qxbl02.streamlit.app/)

## Features

- Real-time data from Our World in Data (updated daily, 200+ countries)
- KPI cards: total cases, deaths, vaccinations, case rate
- Interactive line charts: daily cases and deaths over time
- Area chart: vaccination rollout progress
- Horizontal bar chart: top 10 countries by cases and deaths
- Interactive choropleth world map with metric selector
- Country dropdown with sidebar controls
- Data cached with @st.cache_data for fast performance

## Tech Stack

- Python 3.x
- Streamlit (web app framework)
- Plotly Express + Graph Objects (interactive charts)
- pandas (data loading and processing)
- Our World in Data COVID-19 dataset

## Run Locally

```bash
git clone https://github.com/iamxkhushi1726-svg/covid19-interactive-dashboard.git
cd covid19-interactive-dashboard
pip install -r requirements.txt
streamlit run app.py
```

## Project Structure

```
covid19-interactive-dashboard/
├── src/
│   ├── data_loader.py   # OWID data fetch, caching, filtering
│   └── charts.py        # All Plotly chart functions
├── app.py               # Streamlit dashboard entry point
├── requirements.txt
├── .gitignore
└── README.md
```

## What I Learned

- How to build and deploy a multi-page Streamlit dashboard
- How to use @st.cache_data to cache large CSV files efficiently
- How to create interactive choropleth maps with Plotly Express
- How to structure a Streamlit app with separate data and chart modules
- How to deploy a Python web app to Streamlit Cloud for free

## Part of 100 Projects Challenge

Project 05 of my 100-project challenge to secure AI/ML and SWE internships.

Follow my progress: [GitHub Profile](https://github.com/iamxkhushi1726-svg)