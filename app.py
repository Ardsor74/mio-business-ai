import streamlit as st
import requests
from bs4 import BeautifulSoup

# --- CONFIGURAZIONE PROFESSIONALE ---
st.set_page_config(
    page_title="NEXUS AI - Business Suite", 
    page_icon="🛡️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

api_key = st.secrets.get("GOOGLE_API_KEY")

# --- STILE PERSONALIZZATO ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #2e7d32; color: white; font-weight: bold; }
    .stExpander { border: 1px solid #2e7d32; border-radius: 10px; background-color: #161b22; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡️ NEXUS AI")
    st.subheader("Business Suite v3.0")
    st.divider()
    menu = st.radio(
        "MENU PRINCIPALE",
        ["🕵️ Analisi Strategica", "📱 Piano Social 30gg", "💬 Customer Care AI", "⚙️ Account"]
    )
    st.divider()
    st.info("Piano Attivo: **Premium Business**")
    st.link_button("💳 Gestisci Abbonamento", "https://stripe.com")

# --- FUNZIONE LOGICA AI ---
def call_nexus_ai(prompt):
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(api_url, json=payload, timeout=20)
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "Errore di connessione. Riprova."

# --- LOGICA PAGINE ---

if menu == "🕵️ Analisi Strategica":
    st.header("🕵️ Analisi Strategica del Business")
    
    # --- NUOVA GUIDA RAPIDA ---
    with st.expander("📖 COME USARE NEXUS AI (Guida Rapida)", expanded=True):
        col_g1, col_g2, col_g3 = st.columns(3)
        with col_g1:
            st.markdown("**1. Scansiona**")
            st.write("Inserisci l'URL del sito qui sotto per caricare i dati dell'azienda.")
        with col_g2:
            st.markdown("**2. Genera**")
            st.write("Sposta il menu su 'Piano Social' per creare i post di un mese.")
        with col_g3:
            st.markdown("**3. Rispondi**")
            st.write("Usa 'Customer Care' per gestire le recensioni su Google Maps.")

    st.divider()
    
    url_input = st.text_input("Inserisci l'URL del sito da analizzare:")
    
    if st.button("AVVIA SCANSIONE"):
        if url_input:
            with st.spinner("Scansione del sito in corso..."):
                try:
                    headers = {'User-Agent': 'Mozilla/5.0'}
                    res = requests.get(url_input, headers=headers, timeout=15)
                    soup = BeautifulSoup(res.text, 'html.parser')
                    for s in soup(["script", "style"]): s.decompose()
                    testo_sito = soup.get_text(separator=' ', strip=True)[:3000]
                    
                    st.session_state['testo_sito'] = testo_sito
                    
                    prompt = f"Analizza questo business: {testo_sito}. Crea un report con: Punti di Forza, Errori nel sito e Potenziale di crescita. Rispondi in Italiano."
                    risultato = call_nexus_ai(prompt)
                    
                    st.success("✅ ANALISI COMPLETATA")
                    st.markdown(risultato)
                except:
                    st.error("Errore nella lettura del sito.")
        else:
            st.warning("Inserisci un URL valido per iniziare.")

elif menu == "📱 Piano Social 30gg":
    st.header("📱 Piano Editoriale Social")
    if 'testo_sito' not in st.session_state:
        st.warning("⚠️ Torna in 'Analisi Strategica' e scansiona un sito prima di generare il piano social.")
    else:
        st.write("Genera 12 post pronti (testo + hashtag) per il tuo business.")
        if st.button("GENERA CALENDARIO"):
            with st.spinner("Creazione contenuti..."):
                prompt = f"Basandoti su: {st.session_state['testo_sito']}, crea un calendario di 12 post social. Scrivi Giorno, Titolo, Testo del post e Hashtag. In Italiano."
                piano = call_nexus_ai(prompt)
                st.markdown(piano)

elif menu == "💬 Customer Care AI":
    st.header("💬 Reputation Manager")
    recensione = st.text_area("Incolla qui la recensione del cliente:")
    if st.button("GENERA RISPOSTA"):
        with st.spinner("Scrittura..."):
            prompt = f"Scrivi una risposta professionale a: '{recensione}'. Sii gentile e invita a tornare."
            risposta = call_nexus_ai(prompt)
            st.info("📌 Risposta consigliata:")
            st.write(risposta)

elif menu == "⚙️ Account":
    st.header("⚙️ Il Mio Account")
    st.write("Gestione licenza e statistiche.")
    st.metric("Analisi effettuate", "12", "+3 questa settimana")
