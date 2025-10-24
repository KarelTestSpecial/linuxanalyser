# Linux Partitie Analyser

Dit script analyseert de Crostini Linux-omgeving op een Chromebook. Het inventariseert handmatig geïnstalleerde Debian-pakketten, `node_modules`-mappen en de home-directory. Vervolgens wordt de Google Gemini API gebruikt om intelligente inzichten, samenvattingen en gepersonaliseerde onderhoudstips te genereren.

## Vereisten

Voordat je begint, zorg ervoor dat je de volgende zaken hebt:

*   Een werkende Linux-omgeving (getest op Crostini voor ChromeOS).
*   Python 3 en `pip` geïnstalleerd.
*   Git geïnstalleerd.
*   Een Google Gemini API-sleutel. Je kunt er een aanmaken via [Google AI Studio](https://aistudio.google.com/).

## Installatie & Configuratie

Volg deze stappen om het project op te zetten:

1.  **Kloon de repository** (als je dat nog niet hebt gedaan):
    ```bash
    git clone <url-van-jouw-repository>
    cd <naam-van-de-repository>
    ```

2.  **Maak een Python virtual environment aan:**
    Dit zorgt ervoor dat de benodigde packages geïsoleerd blijven van je systeem.
    ```bash
    python3 -m venv venv
    ```

3.  **Activeer de virtual environment:**
    Je moet dit elke keer doen als je in een nieuwe terminal aan het project werkt.
    ```bash
    source venv/bin/activate
    ```
    *(Je terminalprompt zou nu `(venv)` moeten tonen.)*

4.  **Installeer de benodigde Python-bibliotheken:**
    ```bash
    python3 -m pip install google-generativeai
    ```

## Gebruik

Voer de volgende stappen uit om het script te draaien:

1.  **Zorg ervoor dat je virtual environment actief is:**
    ```bash
    source venv/bin/activate
    ```

2.  **Stel je API-sleutel in als een environment variable.**
    Het script leest de sleutel veilig uit je omgeving. Deze stap moet je voor elke nieuwe terminalsessie herhalen.
    ```bash
    # Vervang "JOUW_API_SLEUTEL_HIER" door je daadwerkelijke sleutel
    export GEMINI_API_KEY="JOUW_API_SLEUTEL_HIER"
    ```
    **Belangrijk:** Zet je API-sleutel nooit direct in het script of deel deze publiekelijk!

3.  **Voer het analyser-script uit:**
    ```bash
    python3 analyser.py
    ```

## Wat je kunt verwachten

Het script zal de analyse uitvoeren en de verschillende AI-prompts versturen. Dit kan even duren.

Na afloop wordt een volledig rapport in Markdown-formaat direct in de terminal geprint. Vervolgens krijg je de vraag of je dit rapport wilt opslaan in een bestand met de naam `AI_linux_report.md`.