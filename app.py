import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# Configurazione Pagina
st.set_page_config(page_title="NEXUS AI - Business Guard", page_icon="🛡️")

# --- CONNESSIONE AI (VERSIONE FORZATA) ---
if "GOOGLE_API_KEY" in st.secrets:
    # Questa riga è il segreto: forza la connessione stabile
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"], transport='rest')
else:
    st.error("⚠️ Inserisci la chiave nei Secrets!")

st.title("🛡️ NEXUS AI - Business Guard")

url_input = st.text_input("Inserisci l'URL del sito da analizzare")

if st.button("AVVIA ANALISI"):
    if url_input:
        with st.spinner("Analisi in corso..."):
            try:
                # 1. Leggiamo il sito
                res = requests.get(url_input, timeout=10)
                soup = BeautifulSoup(res.text, 'html.parser')
                testo = " ".join([p.get_text() for p in soup.find_all('p')[:10]])

                # 2. Usiamo il modello Flash (il più compatibile)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Generiamo il contenuto
                response = model.generate_content(
                    f"Analizza brevemente questo business: {testo}. Dimmi cosa vendono e un consiglio marketing."
                )
                
                st.success("✅ Analisi completata!")
                st.markdown(response.text)
                st.divider()
                st.link_button("🚀 ABBONATI A 29€", "https://stripe.com")

            except Exception as e:
                # Se dà ancora errore, stampiamo un messaggio più pulito
                st.error(f"Errore tecnico: {e}")
