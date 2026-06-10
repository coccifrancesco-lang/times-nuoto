import streamlit as st
import pandas as pd
import os

# Configurazione Pagina
st.set_page_config(page_title="Records Certaldo Nuoto", page_icon="🏊‍♂️", layout="wide")

# CSS Personalizzato per i colori della squadra (Giallo e Blu o quello che preferisci)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stDataFrame { border-radius: 10px; overflow: hidden; }
    h1 { color: #003366; }
    h2 { color: #00509d; border-bottom: 2px solid #ffcc00; padding-bottom: 10px; }
    </style>
    """, unsafe_allow_info=True)

# --- CARICAMENTO DATI ---
file_database = "Storico_Tempi.csv"

if os.path.exists(file_database):
    df = pd.read_csv(file_database, sep=';', dtype={'Tempo': str})
    df['Atleta'] = df['Atleta'].str.strip()
    
    # --- SIDEBAR (Barra Laterale) ---
    st.sidebar.image("https://via.placeholder.com/150?text=LOGO+CERTALDO", width=150) # Sostituisci con link vero logo
    st.sidebar.title("Menu")
    atleti = sorted(df['Atleta'].unique())
    atleta_selezionato = st.sidebar.selectbox("🔍 Cerca Atleta:", atleti)
    
    st.sidebar.info("Questo portale mostra i Record Personali (PB) e gli ultimi tempi registrati ufficialmente.")

    # --- CORPO PRINCIPALE ---
    st.title("🏊‍♂️ Certaldo Nuoto - Archivio Record")
    
    if atleta_selezionato:
        st.header(f"Scheda Atleta: {atleta_selezionato}")
        
        # Logica dei tempi (stessa di prima)
        gare_target = ["50 SL", "100 SL", "200 SL", "400 SL", "800 SL", "1500 SL", 
                       "50 FA", "100 FA", "200 FA", "50 DO", "100 DO", "200 DO", 
                       "50 RA", "100 RA", "200 RA", "100 MX", "200 MX", "400 MX"]
        
        df_atleta = df[df['Atleta'] == atleta_selezionato]
        
        res = []
        for g in gare_target:
            d_g = df_atleta[df_atleta['Gara'] == g]
            d25 = d_g[d_g['Vasca'] == '25m']
            d50 = d_g[d_g['Vasca'] == '50m']
            
            res.append({
                "Gara": g,
                "🏆 PB (25m)": d25['Tempo'].min() if not d25.empty else "-",
                "⏱️ Ultimo (25m)": d25.iloc[-1]['Tempo'] if not d25.empty else "-",
                "🏆 PB (50m)": d50['Tempo'].min() if not d50.empty else "-",
                "⏱️ Ultimo (50m)": d50.iloc[-1]['Tempo'] if not d50.empty else "-"
            })
        
        final_df = pd.DataFrame(res)

        # Visualizzazione a due colonne
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Vasca Corta (25m)")
            st.table(final_df[["Gara", "🏆 PB (25m)", "⏱️ Ultimo (25m)"]].set_index("Gara"))
        with c2:
            st.subheader("Vasca Lunga (50m)")
            st.table(final_df[["Gara", "🏆 PB (50m)", "⏱️ Ultimo (50m)"]].set_index("Gara"))

else:
    st.warning("Carica il file Storico_Tempi.csv su GitHub per vedere i dati.")
