import streamlit as st
import requests
from bs4 import BeautifulSoup

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="NEXUS AI - Business Guard", page_icon="🛡️")
api_key = st.secrets.get("GOOGLE_API_KEY")

st.title("🛡️ NEXUS AI - Business Guard")
st.write("Analisi intelligente con tecnologia Gemini 2.5")

url_input = st.text_input("Inserisci l'URL del sito da analizzare")

if st.button("AVVIA ANALISI"):
    if url_input and api_key:
        with st.spinner("L'AI di nuova generazione sta analizzando..."):
            try:
                # 1. Scraping veloce del sito
                headers = {'User-Agent': 'Mozilla/5.0'}
                res = requests.get(url_input, headers=headers, timeout=10)
                soup = BeautifulSoup(res.text, 'html.parser')
                testo = " ".join([p.get_text() for p in soup.find_all('p')[:8]])

                # 2. CHIAMATA AL NUOVO MODELLO (Gemini 2.5 Flash)
                # Usiamo la versione v1beta perché è un modello preview/nuovo
                api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
                
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": f"Analizza questo business: {testo}. Dimmi cosa offrono e 2 consigli per vendere di più. Rispondi in modo professionale in italiano."
                        }]
                    }]
                }

                response = requests.post(api_url, json=payload)
                data = response.json()

                if "candidates" in data:
                    analisi = data["candidates"][0]["content"]["parts"][0]["text"]
                    st.success("✅ ANALISI COMPLETATA!")
                    st.markdown(analisi)
                else:
                    st.error("Errore di configurazione API")
                    st.json(data) # Questo ci serve se Google cambia ancora idea

                st.divider()
                st.link_button("🚀 ABBONATI A 29€", "https://stripe.com")

            except Exception as e:
                st.error(f"Errore tecnico: {e}")
    else:
        st.warning("Assicurati di aver inserito l'URL e la Chiave API nei Secrets.")
