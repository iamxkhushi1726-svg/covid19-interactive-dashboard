import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

CHART_THEME = "plotly_dark"

def line_chart_cases(df, country):
    """Line chart: daily new cases over time for a country."""
    fig = px.line(
        df, 
        x="date",
        y="new_cases",
        title=f"Daily New COVID-19 Cases - {country}",
        labels={"date": "Date", "new_cases": "New Cases"},
        template=CHART_THEME,
        color_discrete_sequence=["#e74c3c"],
    )
    fig.update_traces(line_width=1.5)
    fig.update_layout(
        hovermode="x unified",
        title_font_size=16,
        margin=dict(t=50, b=30),
    )
    return fig

def line_chart_deaths(df, country):
    """Line chart: daily new deaths over time for a country."""
    fig = px.line(
        df,
        x="date",
        y="new_deaths",
        title=f"Daily New Deaths - {country}",
        labels={"date": "Date", "new_deaths": "New Deaths"},
        template=CHART_THEME,
        color_discrete_sequence=["#fafa47"],
    )
    fig.update_traces(line_width=1.5)
    fig.update_layout(
        hovermode="x unified",
        title_font_size=16,
        margin=dict(t=50, b=30)
    )
    return fig

def bar_chart_top_countries(top_df, metric, metric_label):
    """Horizontal bar chart: top 10 countries by a metric."""
    top_df = top_df.sort_values(metric, ascending=True)
    fig=px.bar(
        top_df,
        x=metric,
        y="location",
        orientation="h",
        title=f"Top 10 Countries by {metric_label}",
        labels={metric: metric_label, "location": "Country"},
        template=CHART_THEME,
        color=metric,
        color_continuous_scale="Reds",
    )
    fig.update_layout(
        title_font_size=16,
        showlegend=False,
        margin=dict(t=50, b=30),
        coloraxis_showscale=False,
    )
    return fig

def area_chart_vaccinations(df, country):
    """Area chart: vaccinations progress over time for a country."""
    vax_df = df[df["total_vaccinations"] > 0].copy()
    if vax_df.empty:
        return None
    
    fig = px.area(
        vax_df,
        x="date",
        y="total_vaccinations",
        title=f"Total Vaccinations - {country}",
        labels={"date": "Date", "total_vaccinations": "Total Vaccinations"},
        template=CHART_THEME,
        color_discrete_sequence=["#2ecc71"],
    )
    fig.update_layout(
        title_font_size=16,
        hovermode="x unified",
        margin=dict(t=50, b=30)
    )
    return fig

def choropleth_map(df, metric, metric_label, title):
    """World choropleth map coloured by a chosen metric."""
    latest = df.sort_values("date").groupby("location").last().reset_index()
    latest = latest[latest[metric] > 0]

    fig = px.choropleth(
        latest,
        locations="location",
        locationmode="country names",
        color=metric,
        hover_name="location",
        color_continuous_scale="Reds",
        title=title,
        labels={metric: metric_label},
        template=CHART_THEME,
    )
    fig.update_layout(
        title_font_size=16,
        geo=dict(showframe=False, showcoastlines=True),
        margin=dict(t=60, b=0, l=0, r=0),
        coloraxis_colorbar=dict(title=metric_label),
    )
    return fig