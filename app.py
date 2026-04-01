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

# Recupero API Key dai Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

# --- STILE PERSONALIZZATO ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #2e7d32; color: white; }
    .reportview-container .main .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR DI NAVIGAZIONE ---
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
    st.link_button("💳 Gestisci Abbonamento", "https://billing.stripe.com/p/session/test")

# --- FUNZIONE LOGICA AI (GEMINI 2.5 FLASH) ---
def call_nexus_ai(prompt):
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(api_url, json=payload, timeout=20)
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "Errore nella generazione. Riprova tra un istante."

# --- LOGICA DELLE PAGINE ---

# 1. ANALISI STRATEGICA
if menu == "🕵️ Analisi Strategica":
    st.header("🕵️ Analisi Strategica del Business")
    url_input = st.text_input("Inserisci l'URL del cliente per scansionare il sito:")
    
    if st.button("AVVIA SCANSIONE"):
        with st.spinner("Analisi dei dati in corso..."):
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                res = requests.get(url_input, headers=headers, timeout=15)
                soup = BeautifulSoup(res.text, 'html.parser')
                for s in soup(["script", "style"]): s.decompose()
                testo_sito = soup.get_text(separator=' ', strip=True)[:3000]
                
                st.session_state['testo_sito'] = testo_sito
                
                prompt = f"Analizza questo business: {testo_sito}. Crea un report professionale con: 1. Punti di Forza, 2. Errori Gravi nel sito, 3. Potenziale di guadagno inespresso. Rispondi in Italiano."
                risultato = call_nexus_ai(prompt)
                
                st.success("✅ Analisi Completata")
                st.markdown(risultato)
                st.download_button("📥 Scarica Report PDF (Simulato)", risultato, file_name="analisi_business.txt")
            except:
                st.error("Impossibile leggere il sito. Verifica l'URL.")

# 2. PIANO SOCIAL 30 GIORNI (Il valore aggiunto)
elif menu == "📱 Piano Social 30gg":
    st.header("📱 Piano Editoriale Social Automatico")
    if 'testo_sito' not in st.session_state:
        st.warning("Per favore, effettua prima un'Analisi Sito per caricare i dati del business.")
    else:
        st.write("Generiamo 12 post pronti per Instagram e Facebook basati sul tuo business.")
        if st.button("GENERA CALENDARIO POST"):
            with st.spinner("L'AI sta scrivendo i tuoi contenuti..."):
                prompt = f"Basandoti su questo business: {st.session_state['testo_sito']}, genera un calendario editoriale di 12 post. Per ogni post scrivi: Giorno, Tema, Testo del post (Caption) e Hashtag. Sii creativo e professionale."
                piano = call_nexus_ai(prompt)
                st.markdown(piano)

# 3. CUSTOMER CARE AI
elif menu == "💬 Customer Care AI":
    st.header("💬 Reputation Manager")
    st.write("Rispondi alle recensioni negative o positive in modo diplomatico.")
    recensione = st.text_area("Incolla qui la recensione del cliente:")
    if st.button("GENERA RISPOSTA"):
        with st.spinner("Scrittura risposta..."):
            info = st.session_state.get('testo_sito', 'un business locale')
            prompt = f"Scrivi una risposta professionale a questa recensione: '{recensione}'. Info business: {info}. Sii gentile e invita a tornare."
            risposta = call_nexus_ai(prompt)
            st.info("📌 Risposta suggerita:")
            st.write(risposta)

# 4. ACCOUNT
elif menu == "⚙️ Account":
    st.header("⚙️ Impostazioni Account")
    st.write("Qui puoi gestire la tua licenza e i dati di fatturazione.")
    st.metric("Analisi Rimanenti", "42", "+2 oggi")
    st.button("Aggiorna a Piano Enterprise")
