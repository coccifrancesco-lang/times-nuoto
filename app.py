import streamlit as st
import pandas as pd
import os

# 1. CONFIGURAZIONE DELLA PAGINA (Titolo della scheda del browser e layout)
st.set_page_config(page_title="Record Certaldo Nuoto", layout="wide")

st.title("🏊‍♂️ Tabellone Record - Certaldo Nuoto")
st.write("Seleziona un atleta per vedere la sua scheda tecnica con i Personal Best e gli ultimi tempi.")

# Elenco fisso delle gare nello stesso ordine ufficiale
gare_target = [
    "50 SL", "100 SL", "200 SL", "400 SL", "800 SL", "1500 SL",
    "50 FA", "100 FA", "200 FA", "50 DO", "100 DO", "200 DO",
    "50 RA", "100 RA", "200 RA", "100 MX", "200 MX", "400 MX"
]

# Nome del file che metteremo insieme al codice
file_database = "Storico_Tempi.csv"

# Controllo se il file esiste nella cartella del sito
if os.path.exists(file_database):
    # Carichiamo i dati forzando il tempo come testo
    df = pd.read_csv(file_database, sep=';', dtype={'Tempo': str})
    df['Atleta'] = df['Atleta'].str.strip()
    
    # 2. MENU DI SELEZIONE ATLETA
    elenco_atleti = sorted(df['Atleta'].unique())
    atleta_selezionato = st.selectbox("🎯 Scegli l'Atleta:", elenco_atleti)
    
    if atleta_selezionato:
        st.markdown(f"## Scheda Tecnica: **{atleta_selezionato}**")
        
        # Filtriamo i dati solo per l'atleta scelto
        df_atleta = df[df['Atleta'] == atleta_selezionato]
        
        # Prepariamo la griglia dei dati da mostrare sul sito
        righe_tabella = []
        for g in gare_target:
            df_g = df_atleta[df_atleta['Gara'] == g]
            
            # Dati vasca corta (25m)
            df_25 = df_g[df_g['Vasca'] == '25m']
            pb_25 = df_25['Tempo'].min() if not df_25.empty else "-"
            last_25 = df_25.iloc[-1]['Tempo'] if not df_25.empty else "-"
            
            # Dati vasca lunga (50m)
            df_50 = df_g[df_g['Vasca'] == '50m']
            pb_50 = df_50['Tempo'].min() if not df_50.empty else "-"
            last_50 = df_50.iloc[-1]['Tempo'] if not df_50.empty else "-"
            
            righe_tabella.append({
                "Gara": g,
                "PB (25m)": pb_25,
                "Ultimo Tempo (25m)": last_25,
                "PB (50m)": pb_50,
                "Ultimo Tempo (50m)": last_50
            })
            
        df_visualizzazione = pd.DataFrame(righe_tabella)
        
        # 3. CREAZIONE INTERFACCIA WEB VISIVA
        # Usiamo le colonne di Streamlit per fare una visualizzazione pazzesca su PC e responsive su smartphone
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏁 Vasca Corta (25 metri)")
            # Mostriamo solo le colonne della vasca corta
            df_corta = df_visualizzazione[["Gara", "PB (25m)", "Ultimo Tempo (25m)"]].rename(
                columns={"PB (25m)": "🏆 Miglior Tempo", "Ultimo Tempo (25m)": "⏱️ Ultimo"}
            )
            st.dataframe(df_corta, use_container_width=True, hide_index=True)
            
        with col2:
            st.subheader("🌊 Vasca Lunga (50 metri)")
            # Mostriamo solo le colonne della vasca lunga
            df_lunga = df_visualizzazione[["Gara", "PB (50m)", "Ultimo Tempo (50m)"]].rename(
                columns={"PB (50m)": "🏆 Miglior Tempo", "Ultimo Tempo (50m)": "⏱️ Ultimo"}
            )
            st.dataframe(df_lunga, use_container_width=True, hide_index=True)

else:
    st.error("❌ Errore: Archivio 'Storico_Tempi.csv' non trovato. Carica il file nella cartella del progetto.")
