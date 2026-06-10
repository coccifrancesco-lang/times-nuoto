import streamlit as st
import pandas as pd
import os

# Configurazione Pagina
st.set_page_config(page_title="Records Certaldo Nuoto", page_icon="🏊‍♂️", layout="wide")

# CSS Personalizzato per i colori della squadra e la home page
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stDataFrame { border-radius: 10px; overflow: hidden; }
    h1 { color: #003366; text-align: center; font-family: 'Arial Black', sans-serif; }
    h2 { color: #00509d; border-bottom: 2px solid #ffcc00; padding-bottom: 10px; }
    .welcome-box { 
        text-align: center; 
        padding: 40px; 
        background-color: #ffffff; 
        border-radius: 15px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border-top: 5px solid #00509d;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CARICAMENTO DATI ---
file_database = "Storico_Tempi.csv"

if os.path.exists(file_database):
    df = pd.read_csv(file_database, sep=';', dtype={'Tempo': str})
    df['Atleta'] = df['Atleta'].str.strip()
    
    # --- SIDEBAR (Barra Laterale) ---
    # NOTA: Sostituisci questo URL con il link vero del logo del Certaldo se lo hai online
    st.sidebar.image("https://via.placeholder.com/150?text=LOGO+CERTALDO", width=150)
    st.sidebar.title("Filtri di Ricerca")
    
    # 1. NUOVO FILTRO: Divisione per Sezione (Maschi/Femmine)
    sezione = st.sidebar.radio("👥 Sezione:", ["Tutti", "Femmine", "Maschi"])
    
    if sezione == "Femmine":
        df_filtrato = df[df['Sesso'] == 'Femmine']
    elif sezione == "Maschi":
        df_filtrato = df[df['Sesso'] == 'Maschi']
    else:
        df_filtrato = df
        
    elenco_atleti = sorted(df_filtrato['Atleta'].unique())
    
    # 2. TENDINA ATLETA: impostata con index=None parte completamente VUOTA
    atleta_selezionato = st.sidebar.selectbox(
        "🔍 Cerca Atleta:", 
        elenco_atleti, 
        index=None, 
        placeholder="Scegli un atleta..."
    )
    
    st.sidebar.info("Scegli il sesso per ridurre la lista, poi seleziona il nome dell'atleta per vedere i suoi record personali.")

    # --- CORPO PRINCIPALE ---
    
    # CASO A: Il sito è appena stato aperto (Nessun atleta selezionato)
    if atleta_selezionato is None:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div class='welcome-box'>
                <h1>🟡🔵 CERTALDO NUOTO 🔵🟡</h1>
                <h3 style='color: #555;'>Portate Ufficiale dei Record e Tempi di Squadra</h3>
                <p style='font-size: 1.1em; color: #777; margin-top: 15px;'>
                    Seleziona un atleta dal menu laterale a sinistra per visualizzare la sua scheda tecnica dettagliata.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #003366;'>📊 Numeri della nostra Enciclopedia:</h3>", unsafe_allow_html=True)
        
        # Generazione automatica delle statistiche generali di squadra
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric(label="🏊 Atleti Registrati", value=df['Atleta'].nunique())
        with c2:
            st.metric(label="📋 Gare Tracciate", value=df['Gara'].nunique())
        with c3:
            st.metric(label="⏱️ Tempi in Archivio", value=len(df))
            
    # CASO B: Un utente ha selezionato un atleta
    else:
        st.title("🏊‍♂️ Certaldo Nuoto - Archivio Record")
        st.header(f"Scheda Atleta: {atleta_selezionato}")
        
        # Logica dei tempi fissa
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

        # Visualizzazione a due colonne affiancate
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Vasca Corta (25m)")
            st.table(final_df[["Gara", "🏆 PB (25m)", "⏱️ Ultimo (25m)"]].set_index("Gara"))
        with c2:
            st.subheader("Vasca Lunga (50m)")
            st.table(final_df[["Gara", "🏆 PB (50m)", "⏱️ Ultimo (50m)"]].set_index("Gara"))

else:
    st.warning("Carica il file Storico_Tempi.csv su GitHub per sbloccare il tabellone dei dati.")
