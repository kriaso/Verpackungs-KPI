
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import os
import io

st.set_page_config(page_title='Logistik KPI-Dashboard', layout='wide')
st.title('KPI-Dashboard')

# Linke Seitenleiste mit Standortauswahl
standort = st.sidebar.selectbox('Standort auswählen', ['Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo'])
data_file = f'kpi_dashboard_data_{standort.lower()}.csv'

# Funktion zum Laden vorhandener Daten
def load_data():
    if os.path.exists(data_file):
        try:
            data = pd.read_csv(data_file)
            if 'Kalenderwoche' not in data.columns:
                raise ValueError("Spalte 'Kalenderwoche' nicht gefunden")
            data['Kalenderwoche'] = pd.to_numeric(data['Kalenderwoche'], errors='coerce').fillna(0).astype(int)
            return data
        except Exception:
            return pd.DataFrame()
    else:
        return pd.DataFrame()

# Funktion zum Speichern der Daten
def save_data(data):
    data.to_csv(data_file, index=False)

# Bestehende Daten laden
data = load_data()

# Manuelle Dateneingabe
st.subheader('Manuelle Dateneingabe')

current_week = datetime.now().isocalendar()[1]
kalenderwoche = st.number_input('Kalenderwoche', min_value=1, max_value=53, value=current_week, step=1)

with st.form('daten_input'):
    # Operative Kennzahlen
    st.subheader('Operative Kennzahlen')
    durchlaufzeit = st.number_input('Durchlaufzeit', min_value=0.0, step=0.1)
    auslastung = st.number_input('Auslastung (%)', min_value=0.0, max_value=100.0, step=0.1)

    # Qualität
    st.subheader('Qualität')
    schäden = st.number_input('Schäden', min_value=0, step=1)
    reklamationen = st.number_input('Reklamationen', min_value=0, step=1)
    fehlerquote = st.number_input('Fehlerquote (%)', min_value=0.0, max_value=100.0, step=0.1)

    # Zahlen
    st.subheader('Zahlen')
    marge = st.number_input('Marge (%)', min_value=0.0, max_value=100.0, step=0.1)
    personalaufwand = st.number_input('Personalaufwand', min_value=0.0, step=1.0)
    materialaufwand = st.number_input('Materialaufwand', min_value=0.0, step=1.0)
    umsatz = st.number_input('Umsatz', min_value=0.0, step=1.0)

    # Effizienz
    st.subheader('Effizienz')
    geplante_stunden = st.number_input('Geplante Stunden', min_value=0.0, step=0.25)
    tatsächliche_stunden = st.number_input('Tatsächliche Stunden', min_value=0.0, step=0.25)

    submitted = st.form_submit_button('Daten hinzufügen')

# Daten speichern und aktualisieren
if submitted:
    new_data = pd.DataFrame({'Kalenderwoche': [kalenderwoche], 'Durchlaufzeit': [durchlaufzeit], 'Auslastung': [auslastung], 'Schäden': [schäden], 'Reklamationen': [reklamationen], 'Fehlerquote': [fehlerquote], 'Marge': [marge], 'Personalaufwand': [personalaufwand], 'Materialaufwand': [materialaufwand], 'Umsatz': [umsatz], 'Geplante Stunden': [geplante_stunden], 'Tatsächliche Stunden': [tatsächliche_stunden]})
    data = pd.concat([data, new_data], ignore_index=True)
    save_data(data)
    st.success(f'Daten für KW {kalenderwoche} erfolgreich hinzugefügt!')

# Anzeige der aktuellen Daten
st.subheader('Gespeicherte Daten')
st.dataframe(data)

# Download Buttons
st.subheader('Daten herunterladen')
if not data.empty:
    csv_data = data.to_csv(index=False).encode('utf-8')
    st.download_button('CSV herunterladen', data=csv_data, file_name='kpi_dashboard_data.csv', mime='text/csv')
