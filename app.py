import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# Configurazione API Google dai Secret
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("Configura la chiave API nei Secrets di Streamlit!")

st.set_page_config(page_title="NEXUS AI - Business Guard", page_icon="🛡️")
st.title("🛡️ NEXUS AI - Business Guard")

url_cliente = st.text_input("Inserisci l'URL del sito da analizzare")

if st.button("ANALIZZA CON AI"):
    if url_cliente:
        with st.spinner("L'Intelligenza Artificiale sta studiando il sito..."):
            try:
                # 1. Leggiamo il sito
                res = requests.get(url_cliente, timeout=10)
                soup = BeautifulSoup(res.text, 'html.parser')
                testo = " ".join([p.get_text() for p in soup.find_all('p')[:10]])

                # 2. Chiediamo a Gemini di analizzare
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = f"Analizza questo testo di un sito web: {testo}. Dimmi in 3 punti elenco quali sono i punti di forza e una criticità evidente per le vendite."
                response = model.generate_content(prompt)
                
                st.success("✅ Analisi Intelligente Generata!")
                st.markdown(response.text)
                
                st.divider()
                st.info("💡 Consiglio Pro: Questa azienda ha bisogno di un assistente che risponda alle recensioni.")
                st.link_button("ATTIVA ASSISTENTE A 29€", "https://stripe.com")
                
            except Exception as e:
                st.error(f"Errore: {e}")

# Ricordati di aggiungere 'google-generativeai' nel file requirements.txt!
