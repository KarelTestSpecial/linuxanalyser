Spec: Intelligente Linux Partitie Analyse Applicatie met AI
1. Doel van de Applicatie
Het doel is om een command-line applicatie (CLI) te ontwikkelen die een diepgaande en begrijpelijke analyse van de gebruiker's Linux-partitie uitvoert. De applicatie verzamelt systeeminformatie en gebruikt vervolgens een Generative AI model (Google Gemini) om deze ruwe data te vertalen naar duidelijke, gegroepeerde en bruikbare inzichten. Het eindresultaat is een rapport dat niet alleen toont wat er is geïnstalleerd, maar ook waarom en hoe het met elkaar in verband staat.
2. Functionele Vereisten
2.1. Fase 1: Lokale Dataverzameling
Het script moet eerst lokaal, zonder AI, de volgende informatie verzamelen:
Pakketlijsten:
Genereer een lijst van alle geïnstalleerde apt-pakketten met hun grootte.
Maak een apart onderscheid tussen pakketten die "handmatig" zijn geïnstalleerd en pakketten die "automatisch" als afhankelijkheid zijn geïnstalleerd.
Commando: apt-mark showmanual
Commando: apt-mark showauto
Verzamel de officiële beschrijving van elk belangrijk pakket.
Commando: apt-cache show <pakketnaam>
node_modules Analyse:
Vind alle node_modules mappen, hun locaties en hun respectievelijke groottes.
Bereken de totale ingenomen ruimte.
2.2. Fase 2: AI-Gedreven Analyse en Interpretatie
De verzamelde data uit Fase 1 wordt als context naar de Gemini API gestuurd. Het script moet de AI de volgende taken laten uitvoeren:
Categorisatie van Pakketten:
Input: De showmanual en showauto lijsten.
Taak: Vraag de AI om de showmanual-lijst te analyseren en op te splitsen in twee duidelijke categorieën:
Kernsysteem & Essentiële Tools: Pakketten die deel uitmaken van de Debian basisinstallatie (bash, coreutils, apt, etc.).
Door de Gebruiker Geïnstalleerde Applicaties: De software die de gebruiker waarschijnlijk zelf bewust heeft toegevoegd (code, docker-ce, nodejs, gh, etc.).
Resultaat: Een schone lijst van software die de gebruiker zelf heeft geïnstalleerd.
Groeperen en Uitleggen van Relaties:
Input: De volledige pakketlijst.
Taak: Vraag de AI om functionele groepen te identificeren en de relatie uit te leggen.
Voorbeelden:
"Groeper alle docker-* pakketten en leg uit waarom containerd.io ook deel uitmaakt van de Docker-ecosysteem, ook al heeft het een andere naam."
"Identificeer alle Java-gerelateerde pakketten (zoals openjdk-*) en leg hun functie uit."
Verklaren van Cryptische Pakketten:
Input: Een selectie van de grootste of meest onduidelijke bibliotheek-pakketten (bv. libllvm15, libgl1-mesa-dri, libicu72).
Taak: Vraag de AI: "Leg in eenvoudige termen uit wat de functie is van pakket X en waarom het waarschijnlijk op een ontwikkelomgeving is geïnstalleerd als afhankelijkheid."
Genereren van Gepersonaliseerde Aanbevelingen:
Input: De volledige analyse (grootste pakketten, node_modules omvang, etc.).
Taak: Vraag de AI om onderhoudstips te genereren die specifiek zijn voor de gevonden situatie.
Voorbeelden:
Indien grote node_modules mappen gevonden: "Je hebt meerdere grote node_modules mappen. Overweeg het gebruik van npkill om oude projecten op te ruimen."
Indien Docker is geïnstalleerd: "Docker images kunnen veel ruimte innemen. Gebruik docker system prune -a om ongebruikte images, containers en volumes op te ruimen."
2.3. Fase 3: Rapportage
De applicatie moet de verwerkte en door AI verrijkte informatie samenvoegen tot één duidelijk, leesbaar Markdown-bestand (AI_linux_report.md). De structuur moet intuïtief zijn voor de gebruiker. (Zie voorbeeld output hieronder).
3. Technologie & Implementatie
Programmeertaal: Python 3. Dit is ideaal voor het uitvoeren van shell-commando's en het maken van API-aanroepen.
Systeem Commando's: De applicatie zal gebruik maken van dpkg-query, find, du, apt-mark en apt-cache.
AI Integratie:
De applicatie moet de google-generativeai Python library gebruiken.
Er moet een API-sleutel voor de Gemini API worden gebruikt (de gebruiker moet deze zelf aanleveren, bijvoorbeeld via een omgevingsvariabele).
Het model gemini-pro-latest of gemini-flash-latest moet worden aangeroepen.
4. Voorbeeld van de Gewenste Output (AI_linux_report.md)
code
Markdown
# Intelligent Rapport van je Linux Partitie
*Gegenereerd op: 2025-10-23*

## 1. Jouw Werkplaats: Zelf Geïnstalleerde Applicaties

Dit is de software die jij bewust hebt toegevoegd aan het basissysteem.

| Applicatie | Grootte (MB) | Beschrijving |
|------------|--------------|----------------|
| Visual Studio Code | 437.72 | Een krachtige code editor van Microsoft. |
| Docker Engine | 291.66 | Platform voor het bouwen en draaien van applicaties in containers. |
| OpenJDK 17 | 261.90 | Ontwikkel- en runtime-omgeving voor de programmeertaal Java. |
| Node.js | 95.21 | JavaScript runtime voor server-side ontwikkeling. |
| GitHub CLI | 52.83 | Command-line tool voor interactie met GitHub. |
| ... | ... | ... |

---

## 2. Inzichten van de AI: Hoe Werkt Je Systeem?

Hieronder legt de AI uit hoe bepaalde onderdelen van je systeem samenwerken en wat hun functie is.

### De Docker Familie: Meer dan je denkt
Je hebt `docker-ce` geïnstalleerd, maar je ziet ook `containerd.io`. Dit is normaal en correct. Docker is opgesplitst in componenten: `docker-ce` is de 'motor' waarmee jij praat, en deze geeft de opdrachten door aan `containerd.io`, de onderliggende 'runtime' die het zware werk van containerbeheer doet. Ze horen dus onlosmakelijk bij elkaar.

### Wat is `libllvm15`?
Dit pakket (111.92 MB) is een 'compiler toolkit'. Zie het als een geavanceerde gereedschapskist die andere programma's (zoals je grafische drivers of Java) gebruiken om code om te zetten naar supersnelle machine-instructies. Je hebt het niet zelf geïnstalleerd, maar het is essentieel voor de prestaties van andere software.

---

## 3. Analyse van `node_modules`

- **Totaal ingenomen ruimte:** 1024.19 MB
- **Grootste map:** `/home/kareltestspecial/.config/nvm/versions/node/v22.20.0/lib/node_modules` (628.99 MB)
- **Projectmappen:**
  - `/home/kareltestspecial/_/kanbanpro/frontend/node_modules` (345.02 MB)
  - `/home/kareltestspecial/_/kanbanpro/node_modules` (47.90 MB)

---

## 4. Gepersonaliseerde Onderhoudstips

*   **Docker Onderhoud:** Je gebruikt Docker. Voer periodiek `docker system prune` uit om ongebruikte containers, netwerken en images te verwijderen en schijfruimte vrij te maken.
*   **Node.js Projecten:** Je `kanbanpro` project heeft een `node_modules` map van 345 MB. Overweeg `npm dedupe` uit te voeren in die map om dubbele pakketten te verminderen.
*   **Algemeen Systeem:** Voer maandelijks `sudo apt autoremove && sudo apt clean` uit om onnodige pakketten en de pakketcache te verwijderen.
