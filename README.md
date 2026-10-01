# Linux Analyzer

Een intelligente tool om je Linux-systeem te analyseren en te optimaliseren met behulp van Google Gemini AI. Deze tool is volledig voorbereid op de Gemini 3.0 (Januari 2026) standaarden, inclusief ondersteuning voor thought signatures.

## Features
- Scant handmatig geïnstalleerde pakketten en hun grootte.
- Analyseert `node_modules` en de `pnpm` store.
- Gebruikt Gemini AI voor categorisatie en uitleg van cryptische pakketten.
- Genereert een uitgebreid Markdown rapport met onderhoudstips.
- Slaat rapporten op met een timestamp in de map `../rapporten/`.
- Interactieve frontend voor het bekijken van de verzamelde data.

## Installatie

1. **Clone de repository**
2. **Setup de virtuele omgeving:**
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate
   pip install -r requirements.txt
   ```
3. **Configureer de API Key:**
   Maak een `.env` bestand aan in de hoofdmap:
   ```bash
   GEMINI_API_KEY=jouw_api_sleutel_hier
   ```
   *Noot: De `.env` is toegevoegd aan `.gitignore` voor jouw veiligheid.*

## Gebruik

### Analyse uitvoeren:
```bash
./myenv/bin/python3 analyser.py
```
Na de analyse kun je ervoor kiezen om het rapport op te slaan. Dit wordt geplaatst in de map `rapporten/` met een timestamp.

### Frontend bekijken:
1. Zorg dat je de analyse hebt uitgevoerd (dit genereert `frontend/public/data.json`).
2. Navigeer naar de `frontend` map.
3. Start de dev server:
   ```bash
   pnpm install
   pnpm dev
   ```

## Systeemvereisten
- Geoptimaliseerd voor systemen met beperkt RAM (zoals Chromebooks met 4GB RAM).
- Python 3.11+
- Node.js & pnpm (voor de frontend)
