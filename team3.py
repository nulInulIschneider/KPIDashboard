import pandas as pd
import plotly.express as px
from datetime import datetime


APP_COLORS = ("#F03C14", "#FABE14", "#D7D700", "#50C8AA", "#0ABEC8", "#9696D7")


def processed_data(df, data_type):
    max_date = pd.to_datetime(datetime.today().strftime('%Y-%m-%d'))
    df['datum'] = pd.to_datetime(df['datum'])
    df = df[df['datum'] < max_date]
    
    if data_type == 'waiting_time':
        df['Wartezeit in Wochen'] = df['diff'] / 7
        df['Monat'] = df['datum'].dt.month
        df['Quartal'] = df['datum'].dt.quarter
        df['Jahr'] = df['datum'].dt.year
        return df
    elif data_type == 'consultation':
        df['Monat'] = df['datum'].dt.strftime('%Y-%m')
        # Aggregieren der Daten zur Anzahl der Beratungen pro Monat und Beratungsart
        df_grouped = df.groupby(['Monat', 'Beratungsart']).size().reset_index(name='Anzahl')
        return df_grouped

def create_figure_violin(df_processed):
    # Erstellen eines Violin-Plots für Wartezeiten pro Quartal und Jahr
    fig = px.violin(
        df_processed,
        x="Quartal",
        y="Wartezeit in Wochen",
        color="Jahr",
        labels={"Quartal": "Quartal", "Wartezeit in Wochen": "Wartezeit in Wochen", "Jahr": "Jahr"},
        #title="Wartezeiten pro Quartal und Jahr",
        box=True,
        points="all",
    )
    fig.update_traces(quartilemethod="inclusive",
                      spanmode="hard",
                      selector=dict(type='violin')) # oder 'exclusive' je nach Bedarf
    fig.update_layout(
        height=700,
        plot_bgcolor="#D9D5CD"
    )
    return fig

def create_figure_line(df_processed):
    # Erstellen des Liniendiagramms
    fig = px.line(
        df_processed,
        x="Monat",
        y="Anzahl",
        color="Beratungsart",
        labels={"Monat": "Monat/Jahr", "Anzahl": "Anzahl der Beratungen", "Beratungsart": "Beratungsart"},
        title="Anzahl der Beratungen pro Monat"
    )
    fig.update_layout(
        height=700,
        plot_bgcolor="#D9D5CD"
    )
    return fig

def create_figure_bar(df_processed):
    # Erstellen eines Balkendiagramms für die Anzahl der Beratungen pro Quartal
    fig = px.bar(
        df_processed,
        x="Monat",
        y="Anzahl",
        color="Beratungsart",
        labels={"Monat": "Monat/Jahr", "Anzahl": "Anzahl der Beratungen", "Beratungsart": "Beratungsart"},
        title="Anzahl der Beratungen pro Monat (gestapelt)"
    )
    fig.update_layout(
        height=700,
        plot_bgcolor="#D9D5CD"
    )
    return fig
