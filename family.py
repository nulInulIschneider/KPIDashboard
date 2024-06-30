import pandas as pd
import plotly.express as px
from datetime import datetime


APP_COLORS = ["#F03C14", "#FABE14", "#D7D700", "#50C8AA", "#0ABEC8", "#9696D7"]


def process_data(df):
    df_grouped = df.groupby("ID Famile")
    
    df_sum_per_family = pd.DataFrame({"Familiengröße": df_grouped["Anzahl"].sum().astype(int)})
    
    df["Älteste Beratung"] = pd.to_datetime(df["Älteste Beratung"], errors='coerce')
    df["Neuste Beratung"] = pd.to_datetime(df["Neuste Beratung"], errors='coerce')

    today = pd.Timestamp(datetime.now())
    df.loc[df["Älteste Beratung"] > today, "Älteste Beratung"] = pd.NaT
    df.loc[df["Neuste Beratung"] > today, "Neuste Beratung"] = pd.NaT

    df_timediff = pd.DataFrame({
        "Ältester Kontakt": df_grouped["Älteste Beratung"].min(),
        "Neuste Beratung": df_grouped["Neuste Beratung"].max(),
    })

    df_timediff["Abstand in Jahren"] = (df_timediff["Neuste Beratung"] - df_timediff["Ältester Kontakt"]).dt.days / 365.25
    df_timediff.drop(columns=["Ältester Kontakt", "Neuste Beratung"], inplace=True)
    df_timediff.drop(df_timediff[df_timediff["Abstand in Jahren"] == 0].index, inplace=True)
    
    return df_sum_per_family, df_timediff  


def create_histogram(df_sum_per_family):
    fig = px.histogram(
        df_sum_per_family, 
        x="Familiengröße",
        nbins=int(df_sum_per_family["Familiengröße"].max()), 
        title="Anzahl nach Familiengröße"
    )
    fig.update_layout(
        bargap=0.2,
        height=700,
        plot_bgcolor="#D9D5CD"
        )
    return fig


def create_violin_plot(df_timediff):
    fig = px.violin(
        df_timediff, 
        y="Abstand in Jahren", 
        box=True, 
        points="all", 
        title="Abstand zwischen erster und letzter Beratung"
    )
    fig.update_traces(marker_color=APP_COLORS[0],
                      spanmode="hard",
                      selector=dict(type='violin'))
    fig.update_layout(
        height=700,
        plot_bgcolor="#D9D5CD"
    )
    return fig


def create_scatter_plot(df_all):
    fig = px.scatter(
        df_all, 
        x="Abstand in Jahren", 
        y="Familiengröße", 
        title="Beratungsabstand zu Familiengröße"
    )
    fig.update_layout(
        height=700,
        plot_bgcolor="#D9D5CD"
    )
    return fig
