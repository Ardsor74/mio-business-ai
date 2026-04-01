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
        with st.spinner("L'AI sta leggendo il sito..."):
            try:
                # 1. Scraping POTENZIATO
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                res = requests.get(url_input, headers=headers, timeout=15)
                soup = BeautifulSoup(res.text, 'html.parser')
                
                # Pulizia codice
                for script in soup(["script", "style"]): 
                    script.decompose()
                
                testo = soup.get_text(separator=' ', strip=True)[:3000]

                # 2. CHIAMATA AL MODELLO (Gemini 2.5 Flash)
                api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
                
                prompt_serio = f"Analizza questo business basandoti sul testo del sito: {testo}. Spiega cosa offrono e dai 2 consigli di marketing. Rispondi in italiano."

                payload = {
                    "contents": [{"parts": [{"text": prompt_serio}]}]
                }

                response = requests.post(api_url, json=payload)
                data = response.json()

                if "candidates" in data:
                    analisi = data["candidates"][0]["content"]["parts"][0]["text"]
                    st.success("✅ ANALISI COMPLETATA!")
                    st.markdown(analisi)
                else:
                    st.error("L'AI non ha potuto generare l'analisi. Controlla i log.")
                    st.json(data)

            except Exception as e:
                st.error(f"Errore tecnico durante la lettura del sito: {e}")
                
    elif not api_key:
        st.error("Chiave API mancante nei Secrets!")
    else:
        st.warning("Inserisci un URL valido.")

st.divider()
st.info("💡 Vuoi sbloccare tutte le funzioni? Clicca sul tasto abbonati.")
st.link_button("🚀 ABBONATI A 29€", "https://stripe.com")
