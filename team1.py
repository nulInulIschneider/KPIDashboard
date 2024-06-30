import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

COLORS = ["#786E64", "#B1AA9E", "#C5BFB6", "#D9D5CD", "#EDEAE6"]


def processed_data(df):
    max_date = pd.to_datetime(datetime.today().strftime('%Y-%m-%d'))
    datum_cols = [col for col in df.columns if "_datum" in col]
    df[datum_cols] = df[datum_cols].apply(pd.to_datetime)
    df_processed = df[(df[datum_cols] < max_date).all(axis=1)]

    return df_processed


def grouped_data(df_processed):
    df_processed = (
        df_processed
        .set_index("analyse_datum")
        .groupby([pd.Grouper(freq="ME"), "analyse_bezeichnung"])["analyse_id"]
        .nunique()
        .unstack()
        .reset_index()
    )

    # Reorder columns based on their sum
    df_processed = df_processed[['analyse_datum'] + df_processed.drop(columns=['analyse_datum']).sum().sort_values(ascending=False).index.tolist()]

    df_processed = df_processed.drop(
        columns=[
            col
            for col in df_processed.columns
            if col.startswith("HGE_") and not (df_processed[col] > 20).any()
        ]
    ).fillna(0)

    return df_processed


def create_figure(df_processed):
    global COLORS
    df_processed = grouped_data(df_processed)
    fig_analysen = px.bar(
        df_processed,
        x="analyse_datum",
        y=df_processed.columns[1:],
        labels={"analyse_datum": "Monat", "value": "Anzahl"},
    )

    # Update the legend position and orientation
    fig_analysen.update_layout(
        height=700,
        plot_bgcolor="#D9D5CD",
        colorway=COLORS,
        legend=dict(
            title=None, orientation="h", yanchor="bottom", y=1, xanchor="right", x=1
        ),
    )

    return fig_analysen


def create_figure_trend(df_processed):
    df_processed = grouped_data(df_processed)
    fig_analyse_trendlines = px.scatter(
    df_processed,
    x="analyse_datum",
    y=df_processed.columns[1:],
    labels={"analyse_datum": "Monat", "value": "Anzahl"},
    trendline="rolling",
    trendline_options=dict(window=3, min_periods=1),
    title="3 Monate rollender Durchschnitt",
    )
    fig_analyse_trendlines.data = [
        t for t in fig_analyse_trendlines.data if t.mode == "lines"
    ]
    fig_analyse_trendlines.update_traces(showlegend=True)
    fig_analyse_trendlines.update_layout(
        height=700,
        plot_bgcolor="#D9D5CD",
        legend=dict(
            title=None, orientation="h", yanchor="bottom", y=1, xanchor="right", x=1
        ),
    )

    return fig_analyse_trendlines


def grouped_data_results(df_processed):
    df_processed = (
        df_processed
        .set_index("ergebnis_datum")
        .groupby([pd.Grouper(freq="ME"), "ergebnis_bewertet"])["ergebnis_id"]
        .nunique()
        .unstack()
        .reset_index()
    )

    # Reorder columns based on their sum
    df_processed = df_processed[['ergebnis_datum'] + df_processed.drop(columns=['ergebnis_datum']).sum().sort_values(ascending=False).index.tolist()]

    return df_processed


def create_figure_results(df_processed):
    df_processed = grouped_data_results(df_processed)
    fig_ergebnisse = px.bar(
        df_processed,
        x="ergebnis_datum",
        y=df_processed.columns[1:],
        labels={"ergebnis_datum": "Monat", "value": "Anzahl"},
    )

    # Update the legend position and orientation
    fig_ergebnisse.update_layout(
        height=700,
        plot_bgcolor="#D9D5CD",
        legend=dict(
            title=None, orientation="h", yanchor="bottom", y=1, xanchor="right", x=1
        ),
    )

    return fig_ergebnisse


def grouped_data_orders(df_processed):
    df_processed.loc[df_processed['auftrag_status'].str.startswith("abgeschlossen"), 'auftrag_status'] = 'abgeschlossen'

    # Resample to monthly frequency and count distinct 'auftrag_id's
    df_processed = (
        df_processed
        .set_index("auftrag_datum")
        .groupby([pd.Grouper(freq="ME"), "auftrag_status"])["auftrag_id"]
        .nunique()
        .unstack()
        .reset_index()
    )

    # Reorder the DataFrame columns
    df_processed = df_processed[['auftrag_datum'] + df_processed.drop(columns=['auftrag_datum']).sum().sort_values(ascending=False).index.tolist()]

    return df_processed


def create_figure_orders(df_processed):

    df_processed = grouped_data_orders(df_processed)
    fig_auftraege = px.bar(
        df_processed,
        x="auftrag_datum",
        y=df_processed.columns[1:],
        labels={"auftrag_datum": "Monat", "value": "Anzahl"},
    )

    # Update the legend position and orientation
    fig_auftraege.update_layout(
        height=700,
        plot_bgcolor="#D9D5CD",
        legend=dict(
            title=None, orientation="h", yanchor="bottom", y=1, xanchor="right", x=1
        ),
    )

    return fig_auftraege