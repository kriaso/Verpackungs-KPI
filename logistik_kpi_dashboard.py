
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title='Logistik KPI-Dashboard', layout='wide')
st.title('Logistik KPI-Dashboard')

# Manuelle Dateneingabe
st.subheader('Manuelle Dateneingabe')

with st.form('daten_input'):
    woche = st.date_input('Woche')
    durchlaufzeit = st.number_input('Durchlaufzeit', min_value=0.0, step=0.1)
    auslastung = st.number_input('Auslastung (%)', min_value=0.0, max_value=100.0, step=0.1)
    schäden = st.number_input('Schäden', min_value=0, step=1)
    reklamationen = st.number_input('Reklamationen', min_value=0, step=1)
    fehlerquote = st.number_input('Fehlerquote (%)', min_value=0.0, max_value=100.0, step=0.1)
    marge = st.number_input('Marge (%)', min_value=0.0, max_value=100.0, step=0.1)
    personalaufwand = st.number_input('Personalaufwand', min_value=0.0, step=0.1)
    materialaufwand = st.number_input('Materialaufwand', min_value=0.0, step=0.1)
    umsatz = st.number_input('Umsatz', min_value=0.0, step=0.1)
    geplante_stunden = st.number_input('Geplante Stunden', min_value=0.0, step=0.1)
    tatsächliche_stunden = st.number_input('Tatsächliche Stunden', min_value=0.0, step=0.1)
    pünktlichkeit = st.number_input('Pünktlichkeit (%)', min_value=0.0, max_value=100.0, step=0.1)
    kundenzufriedenheit = st.number_input('Kundenzufriedenheit (%)', min_value=0.0, max_value=100.0, step=0.1)
    nps = st.number_input('Net Promoter Score', min_value=-100.0, max_value=100.0, step=0.1)
    materialeinsparung = st.number_input('Materialeinsparung (%)', min_value=0.0, max_value=100.0, step=0.1)
    recyclingquote = st.number_input('Recyclingquote (%)', min_value=0.0, max_value=100.0, step=0.1)
    co2 = st.number_input('CO2 Fußabdruck', min_value=0.0, step=0.1)
    unfälle = st.number_input('Unfälle', min_value=0, step=1)
    beinaheunfälle = st.number_input('Beinaheunfälle', min_value=0, step=1)
    krankheitsquote = st.number_input('Krankheitsquote (%)', min_value=0.0, max_value=100.0, step=0.1)
    weiterempfehlungsquote = st.number_input('Weiterempfehlungsquote (%)', min_value=0.0, max_value=100.0, step=0.1)
    submitted = st.form_submit_button('Daten hinzufügen')

# Daten speichern
if submitted:
    new_data = pd.DataFrame({
        'Woche': [woche],
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
    st.success('Daten erfolgreich hinzugefügt!')
    st.write(new_data)
