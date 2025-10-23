# Spec: Linux Partitie Analyse en Rapportage Applicatie

## 1. Doel van de Applicatie

De applicatie moet een analyse uitvoeren op de Chrostini Linux-partitie (Debian 12) van de gebruiker. Op basis van deze analyse wordt een gedetailleerd rapport gegenereerd over de geïnstalleerde software, het schijfgebruik van `node_modules` mappen en aanbevelingen voor het onderhoud van de partitie.

## 2. Functionele Vereisten

De applicatie moet de volgende drie hoofdfuncties hebben:

### 2.1. Analyse van Geïnstalleerde Softwarepakketten

De applicatie moet een lijst kunnen genereren van alle geïnstalleerde softwarepakketten. Voor elk pakket moet de volgende informatie worden weergegeven:

*   **Pakketnaam:** De naam van het softwarepakket.
*   **Versie:** De geïnstalleerde versie van het pakket.
*   **Installatiemap(pen):** De mappen waarin de bestanden van het pakket zijn geïnstalleerd.
*   **Schijfruimte:** De totale schijfruimte die door het pakket in beslag wordt genomen.

**Commando's voor implementatie:**

*   Om een lijst van geïnstalleerde pakketten met hun grootte te krijgen, kan het volgende commando worden gebruikt:
    ```bash
    dpkg-query -Wf '${Installed-Size}\t${Package}\n' | sort -n
    ```
*   Om de installatiemappen van een specifiek pakket te vinden:
    ```bash
    dpkg -L <pakketnaam>
    ```

### 2.2. Analyse van `node_modules` Mappen

De applicatie moet het hele bestandssysteem van de Linux-partitie doorzoeken naar mappen met de naam `node_modules`. Voor elke gevonden map moet de volgende informatie worden weergegeven:

*   **Locatie:** Het volledige pad naar de `node_modules` map.
*   **Schijfruimte:** De totale schijfruimte die door de map en de inhoud ervan in beslag wordt genomen.
*   **Totaal:** Een overzicht van de totale schijfruimte die door alle `node_modules` mappen samen wordt ingenomen.

**Commando voor implementatie:**

*   Een robuust commando om alle `node_modules` mappen te vinden, hun grootte te berekenen en rekening te houden met spaties in paden:
    ```bash
    find . -type d -iname node_modules -prune | sed 's/^/"/g' | sed 's/$/"/g' | tr '\n' ' ' | xargs du -chs
    ```

### 2.3. Aanbevelingen voor Onderhoud

Op basis van de verzamelde gegevens moet de applicatie een lijst met suggesties genereren om de Linux-partitie "gezond" te houden. Deze aanbevelingen moeten gericht zijn op een ontwikkelomgeving en kunnen het volgende omvatten:

*   **Pakketbeheer:**
    *   Identificeer en suggereer het verwijderen van ongebruikte of verouderde pakketten.
    *   Adviseer om `sudo apt autoremove` en `sudo apt clean` regelmatig uit te voeren om onnodige afhankelijkheden en de pakketcache te verwijderen.
*   **`node_modules` Beheer:**
    *   Markeer grote `node_modules` mappen van oudere projecten als kandidaten voor verwijdering.
    *   Suggereer het gebruik van tools zoals `npkill` om interactief `node_modules` mappen te beheren en op te ruimen.
*   **Algemeen Systeemonderhoud:**
    *   Adviseer het gebruik van versiebeheer (Git) voor projecten en configuratiebestanden.
    *   Suggereer het gebruik van `virtual environments` voor Python-projecten om afhankelijkheden te isoleren.
    *   Herinner de gebruiker aan het belang van regelmatige back-ups.

## 3. Niet-functionele Vereisten

*   **Gebruikersinterface:** De applicatie moet een command-line interface (CLI) hebben. De output moet duidelijk en gestructureerd zijn, bijvoorbeeld in de vorm van tabellen of lijsten.
*   **Platform:** De applicatie moet draaien op een Debian 12 (bookworm) omgeving.
*   **Technologie:** De applicatie kan worden ontwikkeld in een scripttaal die geschikt is voor dit doel, zoals Bash, Python of Node.js.

## 4. Oplevering

Het eindproduct is een uitvoerbaar script dat, wanneer het wordt uitgevoerd in de Linux-partitie, een analyse uitvoert en het rapport direct in de terminal weergeeft. Optioneel kan het rapport ook naar een tekstbestand worden geschreven.
