from flask import Blueprint, render_template, Response, send_file, session
from config import Config
from .database import db_data
from .decorators import login_required, team1_required, team2_required, team3_required, team4_required
from website import team1 as eg, queries, team3 as ag, family as af, team2 as pg
import plotly.io as pio
import codecs
import pandas as pd


views = Blueprint('views', __name__) # name of blueprint should be the same as var


@views.route('/')
def home():
    return render_template('home.html')


@views.route('/team1')
@team1_required
def team1_page():
    df_analysis = db_data(queries.team1_analysis, Config.DATABASE_CON)
    df_processed = eg.processed_data(df_analysis)
    fig = eg.create_figure(df_processed)
    fig_html = pio.to_html(fig, full_html=False)
    fig_trend = eg.create_figure_trend(df_processed)
    fig_trend_html = pio.to_html(fig_trend, full_html=False)
    df_results = db_data(queries.team1_results, Config.DATABASE_CON)
    df_results_processed = eg.processed_data(df_results)
    fig_results = eg.create_figure_results(df_results_processed)
    fig_results_html = pio.to_html(fig_results, full_html=False)
    df_orders = db_data(queries.team1_orders, Config.DATABASE_CON)
    df_orders_processed = eg.processed_data(df_orders)
    fig_orders = eg.create_figure_orders(df_orders_processed)
    fig_orders_html = pio.to_html(fig_orders, full_html=False)

    return render_template('team1.html', fig_html=fig_html, fig_trend_html=fig_trend_html, fig_results_html=fig_results_html, fig_orders_html=fig_orders_html)


@views.route('/team2')
@team2_required
def team2_page():
    df_analysis = db_data(queries.team2, Config.DATABASE_CON)
    df_sender_processed = pg.processed_data(df_analysis, 'sender')
    fig_sender = pg.create_figure(df_sender_processed)
    fig_sender_html = pio.to_html(fig_sender, full_html=False)
    df_indication_processed = pg.processed_data(df_analysis, 'indication')
    fig_indication = pg.create_figure_indication(df_indication_processed)
    fig_indication_html = pio.to_html(fig_indication, full_html=False)
    return render_template('team2.html', fig_sender_html=fig_sender_html, fig_indication_html=fig_indication_html)


@views.route('/team3')
@team3_required
def team3_page():
    df_waiting_time = db_data(queries.team3_waiting_time, Config.DATABASE_CON)
    df_processed = ag.processed_data(df_waiting_time, 'waiting_time')
    fig = ag.create_figure_violin(df_processed)
    fig_waiting_time_html = pio.to_html(fig, full_html=False)
    df_consultations = db_data(queries.team3_consultation, Config.DATABASE_CON)
    df_processed_cons = ag.processed_data(df_consultations, 'consultation')
    fig = ag.create_figure_line(df_processed_cons)
    fig_consultations_monthly_html = pio.to_html(fig, full_html=False)
    fig_bar = ag.create_figure_bar(df_processed_cons)
    fig_consultations_year_html = pio.to_html(fig_bar, full_html=False)
    df_fam = db_data(queries.team3_family_coun, Config.DATABASE_CON)
    df_sum_per_family, df_timediff = af.process_data(df_fam)
    fig_fam_histo = af.create_histogram(df_sum_per_family)
    fig_fam_histo_html = pio.to_html(fig_fam_histo, full_html=False)
    fig_fam_violin = af.create_violin_plot(df_timediff)
    fig_fam_violin_html = pio.to_html(fig_fam_violin, full_html=False)
    df_all = pd.concat([df_sum_per_family, df_timediff], axis=1)
    fig_fam_scatter = af.create_scatter_plot(df_all)
    fig_fam_scatter_html = pio.to_html(fig_fam_scatter, full_html=False)
    return render_template('team3.html', fig_waiting_time_html=fig_waiting_time_html, fig_consultations_monthly_html=fig_consultations_monthly_html, \
                           fig_consultations_year_html=fig_consultations_year_html, fig_fam_histo_html=fig_fam_histo_html, fig_fam_violin_html=fig_fam_violin_html, \
                            fig_fam_scatter_html=fig_fam_scatter_html)


@views.route('/download/<string:report_type>')
@login_required
def download_data(report_type):
    if report_type == "analysis":
        df = db_data(queries.team1_analysis, Config.DATABASE_CON)
        df_processed = eg.processed_data(df)
        df_grouped = eg.grouped_data(df_processed)
    elif report_type == "results":
        df = db_data(queries.team1_results, Config.DATABASE_CON)
        df_processed = eg.processed_data(df)
        df_grouped = eg.grouped_data_results(df_processed)
    elif report_type == "orders":
        df = db_data(queries.team1_orders, Config.DATABASE_CON)
        df_processed = eg.processed_data(df)
        df_grouped = eg.grouped_data_orders(df_processed)
    elif report_type == "waiting_time":
        df = db_data(queries.team3_waiting_time, Config.DATABASE_CON)
        df_grouped = ag.processed_data(df, 'waiting_time')
    elif report_type == 'consultation':
        df = db_data(queries.team3_consultation, Config.DATABASE_CON)
        df_grouped = ag.processed_data(df, 'consultation')
    elif report_type == 'family':
        df = db_data(queries.team3_family_coun, Config.DATABASE_CON)
        df_sum_per_family, df_timediff  = af.process_data(df)
        df_grouped = df_sum_per_family.merge(df_timediff, left_index=True, right_index=True, how='outer')
        df_grouped.fillna(value={'Abstand in Jahren': 0}, inplace=True)
    elif report_type == 'sender':
        df =  db_data(queries.team2, Config.DATABASE_CON)
        df_grouped = pg.processed_data(df)
    elif report_type == 'test':
        df_grouped = db_data(queries.test, Config.DATABASE_CON)
    else:
        return "Ungültiger Berichtstyp", 400
    
    # CSV in einen String umwandeln
    csv_string = df_grouped.to_csv(index=False)
    csv_string_bom = codecs.BOM_UTF8.decode('utf-8') + csv_string
    
    # Die CSV-Datei als Download zurückgeben
    return Response(
        csv_string_bom,
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename=report_{report_type}.csv"}
    )


@views.route('/test')
@login_required
def test():
    df_structure = db_data(queries.test, Config.DATABASE_CON)
    return render_template('test.html', test=df_structure)
