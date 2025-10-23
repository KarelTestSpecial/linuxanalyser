# Linux Analyser

Dit script analyseert een Debian-gebaseerd Linux-systeem en genereert een rapport met onderhoudsaanbevelingen.

## Gebruik

Om het script uit te voeren, volg je de onderstaande stappen:

1.  **Zorg ervoor dat het script uitvoerbaar is:**

    ```bash
    chmod +x analyser.py
    ```

2.  **Voer het script uit:**

    ```bash
    ./analyser.py
    ```

    Het script zal de analyse uitvoeren en het rapport direct in de terminal weergeven.

3.  **Sla het rapport op (optioneel):**

    Nadat het rapport in de terminal is weergegeven, krijg je de vraag of je het wilt opslaan in een bestand.

    ```
    Do you want to save this report to a file? (y/n):
    ```

    Toets `y` en druk op Enter om het rapport op te slaan als `linux_analysis_report.md` in de huidige map.

## Vereisten

-   Dit script is ontworpen voor Debian-gebaseerde systemen (zoals Debian, Ubuntu, etc.).
-   Python 3 moet geïnstalleerd zijn.
