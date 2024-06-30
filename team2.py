import pandas as pd
import plotly.express as px


def processed_data(df, data_type):
    # Konvertiere 'datum' zu Datetime, falls noch nicht geschehen
    df['datum'] = pd.to_datetime(df['datum'])

    df['name_ort'] = df['name_einrichtung'] + ", " + df['ort']
    
    if data_type == 'sender':
        df_processed = df.groupby([pd.Grouper(key='datum', freq='ME'), 'name_ort']).size().reset_index(name='anzahl_einsendungen')
        df_processed = df_processed[df_processed.groupby('name_ort')['anzahl_einsendungen'].transform('min') >= 3]
        
        return df_processed
    
    if data_type == 'indication':
        df_processed = df.groupby([pd.Grouper(key='datum', freq='ME'), 'indication']).size().reset_index(name='anzahl_einsendungen')
        df_processed = df_processed[df_processed.groupby('indication')['anzahl_einsendungen'].transform('min') >= 2]
        
        return df_processed


def create_figure(df_processed):
    # Erstelle das gestapelte Balkendiagramm
    fig = px.bar(df_processed, x='datum', y='anzahl_einsendungen', color='name_ort', text='anzahl_einsendungen')
    
    # Anpassen des Layouts
    fig.update_layout(
        title='Anzahl pro Einsender (mind. 3 Einsendungen pro Monat)',
        xaxis_title='Monat',
        yaxis_title='Anzahl der Einsendungen',
        legend_title='Einrichtung, Ort',
        barmode='stack',
        height=900,
        plot_bgcolor="#D9D5CD",
        legend=dict(
            orientation="h",  # Horizontale Orientierung der Legende
            yanchor="top", # Verankern am unteren Rand des Layouts
            y=-0.1,           # Negative Y-Position, um es unter das Diagramm zu setzen
            xanchor="center", # Zentrieren auf der X-Achse
            x=0.5             # X-Position in der Mitte des Layouts
        )
    )
    
    return fig


def create_figure_indication(df_processed):
    # Erstelle das gestapelte Balkendiagramm
    fig = px.bar(df_processed, x='datum', y='anzahl_einsendungen', color='indication', text='anzahl_einsendungen')
    
    # Anpassen des Layouts
    fig.update_layout(
        title='Anzahl pro Indikation (mind. 2 Vorkommen pro Monat)',
        xaxis_title='Monat',
        yaxis_title='Anzahl der Einsendungen',
        legend_title='Indikation',
        barmode='stack',
        height=900,
        plot_bgcolor="#D9D5CD",
        legend=dict(
            orientation="h",  # Horizontale Orientierung der Legende
            yanchor="top", # Verankern am unteren Rand des Layouts
            y=-0.1,           # Negative Y-Position, um es unter das Diagramm zu setzen
            xanchor="center", # Zentrieren auf der X-Achse
            x=0.5             # X-Position in der Mitte des Layouts
        )
    )

    return fig
