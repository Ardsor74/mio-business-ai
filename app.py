import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="NEXUS AI - Business Guard", page_icon="🛡️", layout="centered")

# --- CONNESSIONE AI (GOOGLE GEMINI) ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Errore: Chiave API non trovata nei Secrets di Streamlit!")

# --- INTERFACCIA UTENTE ---
st.title("🛡️ NEXUS AI - Business Guard")
st.subheader("Trasforma i visitatori in clienti con l'Intelligenza Artificiale")
st.write("Analizza il tuo sito web per scoprire come migliorare la tua presenza online.")

url_input = st.text_input("Inserisci l'URL del sito (es. https://pasticceria.it)", placeholder="https://...")

if st.button("AVVIA ANALISI INTELLIGENTE"):
    if url_input:
        with st.spinner("🤖 L'AI sta studiando il sito..."):
            try:
                # 1. Recupero dati dal sito
                headers = {'User-Agent': 'Mozilla/5.0'}
                res = requests.get(url_input, headers=headers, timeout=10)
                soup = BeautifulSoup(res.text, 'html.parser')
                
                # Pulizia testo per l'AI
                titolo = soup.title.string if soup.title else "Sito Web"
                testi = [p.get_text() for p in soup.find_all(['p', 'li'])[:15]]
                contesto = " ".join(testi)

                # 2. Generazione Analisi con Gemini
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                Analizza questo contenuto web: "{contesto}"
                Sei un esperto di marketing digitale. Scrivi un'analisi breve per il proprietario del sito:
                1. Cosa fa l'azienda (in una frase).
                2. Un punto di forza che salta all'occhio.
                3. Una grave mancanza che sta facendo perdere soldi (es. mancanza di chatbot, recensioni non gestite, call to action debole).
                Sii molto convincente e professionale. Lingua: Italiano.
                """
                
                response = model.generate_content(prompt)

                # 3. Risultati a schermo
                st.success(f"✅ Analisi completata per: {titolo}")
                st.markdown("---")
                st.markdown(response.text)
                st.markdown("---")
                
                # Sezione Vendita
                st.info("💡 **Consiglio dell'esperto:** Questo business potrebbe raddoppiare le conversioni integrando un assistente AI attivo 24/7.")
                st.link_button("🎁 ATTIVA IL TUO ASSISTENTE A 29€", "https://stripe.com/it")

            except Exception as e:
                st.error(f"Impossibile analizzare il sito. Verifica il link. Errore: {e}")
    else:
        st.warning("Inserisci un link prima di cliccare.")

# --- SIDEBAR ---
st.sidebar.markdown("### NEXUS AI v2.0")
st.sidebar.write("Sistema di monitoraggio reputazione e vendite automatiche.")
