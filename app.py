import streamlit as st
import requests
from bs4 import BeautifulSoup

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="NEXUS AI - Business Guard", page_icon="🛡️")

# --- RECUPERO CHIAVE ---
api_key = st.secrets.get("GOOGLE_API_KEY")

st.title("🛡️ NEXUS AI - Business Guard")

url_input = st.text_input("Inserisci l'URL del sito da analizzare")

if st.button("AVVIA ANALISI"):
    if url_input and api_key:
        with st.spinner("L'AI sta analizzando..."):
            try:
                # 1. Scraping del sito
                res = requests.get(url_input, timeout=10)
                soup = BeautifulSoup(res.text, 'html.parser')
                testo_sito = " ".join([p.get_text() for p in soup.find_all('p')[:10]])

                # 2. CHIAMATA DIRETTA API (Senza librerie intermedie che danno errore)
                # Usiamo la versione 'v1' invece di 'v1beta'
                api_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
                
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": f"Analizza questo business: {testo_sito}. Dimmi in 3 punti cosa vendono e un consiglio marketing. Rispondi in italiano."
                        }]
                    }]
                }

                response = requests.post(api_url, json=payload)
                data = response.json()

                # 3. Estrazione risposta
                if "candidates" in data:
                    testo_ai = data["candidates"][0]["content"]["parts"][0]["text"]
                    st.success("✅ Analisi completata!")
                    st.markdown(testo_ai)
                else:
                    st.error(f"Errore API: {data.get('error', {}).get('message', 'Errore sconosciuto')}")

                st.divider()
                st.link_button("🚀 ABBONATI A 29€", "https://stripe.com")

            except Exception as e:
                st.error(f"Errore tecnico: {e}")
    elif not api_key:
        st.error("Chiave API non configurata nei Secrets!")
