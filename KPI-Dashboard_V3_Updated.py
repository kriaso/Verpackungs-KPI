import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import os

st.set_page_config(page_title='Logistik KPI-Dashboard', layout='wide')
st.title('KPI-Dashboard')

# Linke Seitenleiste mit Standortauswahl
standort = st.sidebar.selectbox('Standort auswählen', ['Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo'])

# Dateipfad für die CSV-Datei zum Speichern der Daten
data_file = f'kpi_dashboard_data_{standort.lower()}.csv'


# Dateipfad für die CSV-Datei zum Speichern der Daten
data_file = 'kpi_dashboard_data.csv'

# Funktion zum Laden vorhandener Daten
def load_data():
    if os.path.exists(data_file):
        try:
            data = pd.read_csv(data_file)
            if 'Kalenderwoche' not in data.columns:
                raise ValueError("Spalte 'Kalenderwoche' nicht gefunden")
            # Sicherstellen, dass Kalenderwoche als Integer interpretiert wird
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

# Kalenderwoche auswählen
current_week = datetime.now().isocalendar()[1]
kalenderwoche = int(st.number_input('Kalenderwoche', min_value=1, max_value=53, value=current_week))

with st.form('daten_input'):
     # Operative Kennzahlen
    st.subheader('Operative Kennzahlen')
    durchlaufzeit = st.number_input('Durchlaufzeit', min_value=0.0, step=0.1)
    auslastung = st.number_input('Auslastung (%)', min_value=0.0, max_value=100.0, step=1)

    # Qualität
    st.subheader('Qualität')
    schäden = st.number_input('Schäden', min_value=0, step=1)
    reklamationen = st.number_input('Reklamationen', min_value=0, step=1)
    fehlerquote = st.number_input('Fehlerquote (%)', min_value=0.0, max_value=100.0, step=1.25)

    # Zahlen
    st.subheader('Zahlen')
    marge = st.number_input('Marge (%)', min_value=0.0, max_value=100.0, step=0.1)
    personalaufwand = st.number_input('Personalaufwand (T€)', min_value=0.0, step=1.0)
    materialaufwand = st.number_input('Materialaufwand (T€)', min_value=0.0, step=1.0)
    umsatz = st.number_input('Umsatz (T€)', min_value=0.0, step=1.0)

    # Effizienz
    st.subheader('Effizienz')
    geplante_stunden = st.number_input('Geplante Stunden', min_value=0.0, step=0.25)
    tatsächliche_stunden = st.number_input('Tatsächliche Stunden', min_value=0.0, step=0.25)

    # Kundenzufriedenheit
    st.subheader('Kundenzufriedenheit')
    pünktlichkeit = st.number_input('Pünktlichkeit (%)', min_value=0.0, max_value=100.0, step=0.1)
    kundenzufriedenheit = st.number_input('Kundenzufriedenheit (%)', min_value=0.0, max_value=5.0, step=0.25)
    nps = st.number_input('Net Promoter Score', min_value=0.0, max_value=10.0, step=0.25)

    # Nachhaltigkeit
    st.subheader('Nachhaltigkeit')
    materialeinsparung = st.number_input('Materialeinsparung (%)', min_value=0.0, max_value=100.0, step=0.1)
    recyclingquote = st.number_input('Recyclingquote (%)', min_value=0.0, max_value=100.0, step=0.1)
    co2 = st.number_input('CO2 Fußabdruck', min_value=0.0, step=0.1)

    # Sicherheit
    st.subheader('Sicherheit')
    unfälle = st.number_input('Unfälle', min_value=0, step=1)
    beinaheunfälle = st.number_input('Beinaheunfälle', min_value=0, step=1)

    # Mitarbeiter
    st.subheader('Mitarbeiter')
    krankheitsquote = st.number_input('Krankheitsquote (%)', min_value=0.0, max_value=100.0, step=0.1)
    weiterempfehlungsquote = st.number_input('Weiterempfehlungsquote (%)', min_value=0.0, max_value=100.0, step=0.1)
    
    submitted = st.form_submit_button('Daten hinzufügen')
 
# Daten speichern und aktualisieren
if submitted:
    new_data = pd.DataFrame({
        'Kalenderwoche': [kalenderwoche],
        'Durchlaufzeit': [durchlaufzeit],
        'Auslastung': [auslastung],
        'Schäden': [schäden],
        'Reklamationen': [reklamationen],
        'Fehlerquote': [fehlerquote],
        'Marge': [marge],
        'Personalaufwand': [personalaufwand],
        'Materialaufwand': [materialaufwand],
        'Umsatz': [umsatz],
        'Geplante Stunden': [geplante_stunden],
        'Tatsächliche Stunden': [tatsächliche_stunden],
        'Pünktlichkeit': [pünktlichkeit],
        'Kundenzufriedenheit': [kundenzufriedenheit],
        'NPS': [nps],
        'Materialeinsparung': [materialeinsparung],
        'Recyclingquote': [recyclingquote],
        'CO2 Fußabdruck': [co2],
        'Unfälle': [unfälle],
        'Beinaheunfälle': [beinaheunfälle],
        'Krankheitsquote': [krankheitsquote],
        'Weiterempfehlungsquote': [weiterempfehlungsquote]
    })
    data = pd.concat([data, new_data], ignore_index=True)
    save_data(data)
    st.success(f'Daten für KW {kalenderwoche} erfolgreich hinzugefügt!')

# Anzeige der aktuellen Daten
st.subheader('Gespeicherte Daten')
st.dataframe(data)

# Gruppierte Darstellung der Oberbegriffe
def plot_group(title, columns):
    if not data.empty:
        fig = px.line(data, x='Kalenderwoche', y=columns, title=title, markers=True)
        st.plotly_chart(fig)

# Oberbegriffe mit zugehörigen Kennzahlen
plot_group('Operative Kennzahlen', ['Durchlaufzeit', 'Auslastung'])
plot_group('Qualität', ['Schäden', 'Reklamationen', 'Fehlerquote'])
plot_group('Zahlen', ['Marge', 'Personalaufwand', 'Materialaufwand', 'Umsatz'])
plot_group('Effizienz', ['Geplante Stunden', 'Tatsächliche Stunden'])
plot_group('Kundenzufriedenheit', ['Pünktlichkeit', 'Kundenzufriedenheit', 'NPS'])
plot_group('Nachhaltigkeit', ['Materialeinsparung', 'Recyclingquote', 'CO2 Fußabdruck'])
plot_group('Sicherheit', ['Unfälle', 'Beinaheunfälle'])
plot_group('Mitarbeiter', ['Krankheitsquote', 'Weiterempfehlungsquote'])
