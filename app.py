import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# 1. Configurazione Iniziale
st.set_page_config(page_title="NEXUS AI - Business Guard", page_icon="🛡️")

# Caricamento sicuro della Chiave API dai Secrets di Streamlit
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Chiave API mancante! Inseriscila nei Secrets di Streamlit come GOOGLE_API_KEY")

# 2. Interfaccia Grafica
st.title("🛡️ NEXUS AI - Business Guard")
st.markdown("### Analisi Intelligente dell'Attività")
st.write("Inserisci l'URL del sito per scoprire i punti deboli e le opportunità di crescita.")

url_cliente = st.text_input("URL del sito (es. https://pasticceria.it)", placeholder="https://...")

if st.button("ANALIZZA CON AI"):
    if url_cliente:
        with st.spinner("L'AI sta scansionando il sito e generando l'analisi..."):
            try:
                # Scansione del sito
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url_cliente, headers=headers, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Estrazione testo (titolo + primi paragrafi)
                titolo_sito = soup.title.string if soup.title else "Azienda analizzata"
                paragrafi = [p.get_text() for p in soup.find_all('p')[:12]]
                testo_sito = " ".join(paragrafi)

                # Chiamata a Gemini (Modello Flash 1.5 - il più veloce)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                Analizza questo testo tratto dal sito web di {titolo_sito}:
                ---
                {testo_sito}
                ---
                Agisci come un esperto di marketing digitale. 
                1. Riassumi brevemente cosa offre questa azienda.
                2. Elenca 3 criticità o punti deboli evidenti nel sito o nella comunicazione.
                3. Spiega perché dovrebbero usare un assistente AI per rispondere alle recensioni.
                Rispondi in modo professionale e convincente in italiano.
                """
                
                risposta_ai = model.generate_content(prompt)
                
                # Visualizzazione Risultati
                st.success(f"✅ Analisi completata per: {titolo_sito}")
                st.markdown("---")
                st.markdown(risposta_ai.text)
                st.markdown("---")
                
                # Conclusione e Vendita
                st.warning("🚨 **OPPORTUNITÀ PERSA:** Questa attività non sta rispondendo a tutte le domande dei clienti su Google Maps.")
                st.write("Vuoi automatizzare la crescita di questo business?")
                st.link_button("🚀 ATTIVA ASSISTENTE AI A 29€/MESE", "https://stripe.com/it")

            except Exception as e:
                st.error(f"Si è verificato un errore durante l'analisi: {e}")
    else:
        st.warning("Inserisci un URL valido per iniziare.")

st.sidebar.info("NEXUS AI v1.2 - Powered by Gemini 1.5 Flash")
