try:
                # 1. Scraping POTENZIATO (Simula un browser umano per non farsi bloccare)
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                res = requests.get(url_input, headers=headers, timeout=15)
                soup = BeautifulSoup(res.text, 'html.parser')
                
                # Cerchiamo di prendere tutto il testo utile (titoli, paragrafi, grassetti)
                for script in soup(["script", "style"]): script.decompose() # puliamo il codice inutile
                testo = soup.get_text(separator=' ', strip=True)[:2000] # prendiamo i primi 2000 caratteri

                # 2. CHIAMATA AL MODELLO (Gemini 2.5 Flash)
                api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
                
                prompt_serio = f"""
                Analizza queste informazioni tratte dal sito {url_input}:
                {testo}
                
                Compito:
                1. Descrivi l'offerta del business (cosa vendono).
                2. Proponi 2 consigli concreti per aumentare le vendite, formulati in modo professionale e strategico.
                Rispondi in italiano.
                """

                payload = {
                    "contents": [{"parts": [{"text": prompt_serio}]}]
                }

                response = requests.post(api_url, json=payload)
                data = response.json()
