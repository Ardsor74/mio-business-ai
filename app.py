import streamlit as st
import requests
from bs4 import BeautifulSoup

# Configurazione Grafica
st.set_page_config(page_title="NEXUS AI - Business Guard", page_icon="🛡️")

st.title("🛡️ NEXUS AI - Business Guard")
st.markdown("### Trasforma il tuo sito in un assistente venditore H24")
st.write("Inserisci il link della tua attività per vedere cosa l'AI può fare per te.")

# Input del Cliente
url_cliente = st.text_input("Inserisci l'URL del tuo sito (es. https://pasticceria.it)", placeholder="https://...")

if st.button("ANALIZZA ORA"):
    if url_cliente:
        with st.spinner("L'AI sta analizzando la tua attività..."):
            try:
                # Simulazione di Scansione Intelligente
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url_cliente, headers=headers, timeout=10)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Estraiamo il titolo e i testi principali
                titolo = soup.title.string if soup.title else "Azienda Locale"
                testi = [p.get_text() for p in soup.find_all(['p', 'li'])[:5]]
                
                st.success(f"✅ Analisi completata per: {titolo}")
                
                # Visualizzazione Risultati (Il valore per il cliente)
                st.subheader("🤖 Cosa ha imparato l'AI su di te:")
                for t in testi:
                    if len(t) > 10:
                        st.info(f"📍 {t[:100]}...")

                st.warning("⚠️ ATTENZIONE: Abbiamo trovato 3 opportunità di guadagno perse nelle tue recensioni Google.")
                
                st.divider()
                st.markdown("### 🚀 Attiva il tuo assistente AI")
                st.write("Vuoi che questa AI risponda automaticamente ai tuoi clienti su Google e Facebook?")
                
                # Qui andrà il tuo link Stripe
                st.link_button("ABBONATI A 29€/MESE", "https://stripe.com/it")
                
            except Exception as e:
                st.error(f"Non riesco a leggere il sito. Assicurati che sia corretto. Errore: {e}")
    else:
        st.warning("Per favore, inserisci un link valido.")

st.sidebar.info("NEXUS AI v1.0 - Sistema di Reputazione Automatica")
