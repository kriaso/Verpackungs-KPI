import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import os

st.set_page_config(page_title='Logistik KPI-Dashboard', layout='wide')
st.title('Logistik KPI-Dashboard')

# Linke Seitenleiste mit Standortauswahl
standort = st.sidebar.selectbox('Standort auswählen', ['Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo'])

# Dateipfad für die CSV-Datei zum Speichern der Daten
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
st.subheader(f'Manuelle Dateneingabe - {standort}')

current_week = datetime.now().isocalendar()[1]
kalenderwoche = int(st.number_input('Kalenderwoche', min_value=1, max_value=53, value=current_week))

with st.form('daten_input'):
    durchlaufzeit = st.number_input('Durchlaufzeit', min_value=0.0, step=0.1)
    auslastung = st.number_input('Auslastung (%)', min_value=0.0, max_value=100.0, step=0.1)
    schäden = st.number_input('Schäden', min_value=0, step=1)
    reklamationen = st.number_input('Reklamationen', min_value=0, step=1)
    fehlerquote = st.number_input('Fehlerquote (%)', min_value=0.0, max_value=100.0, step=0.1)
    marge = st.number_input('Marge (%)', min_value=0.0, max_value=100.0, step=0.1)
    submitted = st.form_submit_button('Daten hinzufügen')

if submitted:
    new_data = pd.DataFrame({
        'Kalenderwoche': [kalenderwoche],
        'Durchlaufzeit': [durchlaufzeit],
        'Auslastung': [auslastung],
        'Schäden': [schäden],
        'Reklamationen': [reklamationen],
        'Fehlerquote': [fehlerquote],
        'Marge': [marge]
    })
    data = pd.concat([data, new_data], ignore_index=True)
    save_data(data)
    st.success(f'Daten für {standort} - KW {kalenderwoche} erfolgreich hinzugefügt!')

st.subheader(f'Gespeicherte Daten - {standort}')
st.dataframe(data)
