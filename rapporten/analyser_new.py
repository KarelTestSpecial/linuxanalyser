#!/usr/bin/env python3

import subprocess
import os
from datetime import datetime
from google.genai import Client  # De nieuwe, toekomstbestendige library

# Configure the Gemini API met de nieuwe library
try:
    api_key = os.environ["GEMINI_API_KEY"]
    # De nieuwe Client gebruikt geen aparte model-configuratie hier, 
    # het model wordt meegegeven tijdens het aanroepen.
    client = Client(api_key=api_key) if api_key else None
except KeyError:
    print("Warning: The GEMINI_API_KEY environment variable is not set. AI features will be disabled.")
    client = None


def ask_ai(prompt):
    """
    Sends a prompt to the AI using the new google.genai SDK and returns the response.
    """
    if client is None:
        return "AI insights not available (API Key missing)."
    try:
        # De nieuwe methode is client.models.generate_content()
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp', # Of 'gemini-1.5-flash' als je een oudere stabiele versie wilt
            contents=prompt
        )
        # De response structuur is meestal hetzelfde (.text)
        return response.text
    except Exception as e:
        return f"An error occurred while communicating with the AI: {e}"


def analyze_installed_packages(manual_packages):
    """
    Analyzes installed Debian packages to find their size, name and description.
    """
    try:
        command = "dpkg-query -Wf '${Installed-Size}\t${Package}\t${Description}\n' | sort -n"
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)

        packages = []
        for line in result.stdout.strip().splitlines():
            if line:
                parts = line.split('\t')
                if len(parts) >= 3:
                    size_kb_str, name, description = parts[0], parts[1], parts[2]
                    try:
                        size_kb = int(size_kb_str)
                        is_manual = name in manual_packages
                        packages.append({"name": name, "size_kb": size_kb, "description": description, "manual": is_manual})
                    except ValueError:
                        print(f"Warning: Could not parse size for package '{name}'. Size string: '{size_kb_str}'")

        packages.sort(key=lambda x: x["size_kb"], reverse=True)
        return packages
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []

def find_node_modules():
    """
    Finds all 'node_modules' directories in the user's home folder and calculates their size.
    """
    home_dir = os.path.expanduser("~")

    try:
        command = f"find {home_dir} -type d -name 'node_modules' -prune -exec du -sk {{}} +"
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)

        node_modules_list = []
        for line in result.stdout.strip().splitlines():
            if line:
                parts = line.split('\t')
                if len(parts) == 2:
                    size_kb_str, path = parts
                    last_modified = datetime.fromtimestamp(os.path.getmtime(path))
                    node_modules_list.append({"path": path, "size_kb": int(size_kb_str), "last_modified": last_modified})

        return node_modules_list
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []


def find_pnpm_store():
    """
    Finds the pnpm content-addressable store and calculates its size.
    """
    pnpm_store_path = os.path.expanduser("~/.pnpm-store")

    if not os.path.isdir(pnpm_store_path):
        return None

    try:
        command = f"du -sk {pnpm_store_path}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)

        if result.stdout:
            parts = result.stdout.strip().split('\t')
            if len(parts) == 2:
                size_kb_str, path = parts
                return {"path": path, "size_kb": int(size_kb_str)}

        return None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def analyze_home_directory():
    home_dir = os.path.expanduser("~")
    dir_analysis = []

    # A knowledge base of common directories and their purpose
    known_dirs = {
        ".config": "Contains configuration files for many applications.",
        ".local": "Contains user-specific data, such as installed programs and libraries.",
        ".cache": "Stores cached data for applications to speed up performance.",
        ".vscode": "Configuration and data for Visual Studio Code.",
        ".npm": "Cache and configuration for the npm package manager.",
        ".nvm": "Node Version Manager, used to manage multiple versions of Node.js.",
        "snap": "Contains applications installed via the Snap package manager.",
        "Downloads": "Default directory for downloaded files.",
        "Documents": "Default directory for user documents.",
        "Pictures": "Default directory for pictures.",
        "Music": "Default directory for music.",
        "Videos": "Default directory for videos.",
        "Desktop": "Represents the user's desktop.",
        "Public": "For sharing files with other users on the network.",
        "Templates": "Contains templates for creating new documents.",
    }

    for item in os.listdir(home_dir):
        full_path = os.path.join(home_dir, item)
        if os.path.isdir(full_path):
            description = known_dirs.get(item, "Unknown purpose.")
            
            # Add more specific checks
            if os.path.exists(os.path.join(full_path, ".git")):
                description += " This directory is a Git repository."
            if os.path.exists(os.path.join(full_path, "package.json")):
                description += " This directory appears to be a Node.js project."

            dir_analysis.append({"name": item, "description": description})
            
    return dir_analysis

def get_manually_installed_packages():
    """
    Gets a set of manually installed packages.
    """
    try:
        command = "apt-mark showmanual"
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return set(result.stdout.strip().splitlines())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return set()


def get_auto_installed_packages():
    """
    Gets a set of automatically installed packages.
    """
    try:
        command = "apt-mark showauto"
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return set(result.stdout.strip().splitlines())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return set()


def generate_markdown_report(manual_packages, node_modules, pnpm_store, home_dir_analysis, ai_insights):
    """
    Generates a Markdown report from the collected data and AI insights.
    """
    report_lines = [
        f"# Intelligent Report of your Linux Partion",
        f"*Generated on: {datetime.now().strftime('%Y-%m-%d')}*",
        "",
        "## 1. Jouw Werkplaats: Zelf Geïnstalleerde Applicaties",
        "",
        "Dit is de software die jij bewust hebt toegevoegd aan het basissysteem.",
        "",
        "| Applicatie | Grootte (MB) | Beschrijving |",
        "|------------|--------------|----------------|",
    ]

    # This part will be tricky, as we have to parse the AI's output.
    # For now, we will just display the raw output. A more robust solution would be to parse the output
    # and format it nicely, but for now, this will do.
    report_lines.append(ai_insights["categorized_packages"])


    report_lines.extend([
        "",
        "---",
        "",
        "## 2. Inzichten van de AI: Hoe Werkt Je Systeem?",
        "",
        "Hieronder legt de AI uit hoe bepaalde onderdelen van je systeem samenwerken en wat hun functie is.",
        "",
    ])

    report_lines.append(ai_insights["explained_packages"])
    report_lines.append(ai_insights["explained_cryptic_packages"])

    report_lines.extend([
        "",
        "---",
        "",
        "## 3. Analyse van `node_modules`",
        "",
    ])

    total_size_mb = sum(nm['size_kb'] for nm in node_modules) / 1024
    report_lines.append(f"- **Totaal ingenomen ruimte:** {total_size_mb:.2f} MB")

    if node_modules:
        biggest_folder = max(node_modules, key=lambda x: x['size_kb'])
        report_lines.append(f"- **Grootste map:** `{biggest_folder['path']}` ({biggest_folder['size_kb'] / 1024:.2f} MB)")

    report_lines.append("- **Projectmappen:**")
    for nm in node_modules:
        report_lines.append(f"  - `{nm['path']}` ({nm['size_kb'] / 1024:.2f} MB)")

    if pnpm_store:
        report_lines.extend([
            "",
            "---",
            "",
            "## 3.1. Analyse van `pnpm`",
            "",
            "De `pnpm` package manager is gedetecteerd. In tegenstelling tot `npm` gebruikt `pnpm` een centrale opslagplaats om schijfruimte te besparen.",
            "",
            f"- **Locatie van de centrale opslagplaats:** `{pnpm_store['path']}`",
            f"- **Totaal ingenomen ruimte:** {pnpm_store['size_kb'] / 1024:.2f} MB",
        ])

    report_lines.extend([
        "",
        "---",
        "",
        "## 4. Home Directory Analysis",
        "",
        "| Directory | Purpose |",
        "|-----------|---------|",
    ])

    for dir_info in home_dir_analysis:
        report_lines.append(f"| {dir_info['name']} | {dir_info['description']} |")


    report_lines.extend([
        "",
        "---",
        "",
        "## 5. Gepersonaliseerde Onderhoudstips",
        "",
    ])

    report_lines.append(ai_insights["recommendations"])

    return "\n".join(report_lines)


def main():
    print("Starting Linux analysis...")
    manual_packages_set = get_manually_installed_packages()
    auto_packages_set = get_auto_installed_packages()
    
    # We pass all packages to the analysis function, and then filter them
    all_packages = analyze_installed_packages(manual_packages_set)
    
    manual_packages = [p for p in all_packages if p['manual']]
    auto_packages = [p for p in all_packages if not p['manual']]

    node_modules = find_node_modules()
    pnpm_store = find_pnpm_store()
    home_dir_analysis = analyze_home_directory()

    # AI Analysis
    print("Asking AI to categorize packages...")
    categorization_prompt = f"Here is a list of manually installed packages:\n\n{manual_packages}\n\nPlease categorize them into 'Core System & Essential Tools' and 'User-Installed Applications'."
    categorized_packages_str = ask_ai(categorization_prompt)

    print("Asking AI to explain package groups...")
    explanation_prompt = f"Here is a list of all installed packages:\n\n{all_packages}\n\nThe size values in the list are in Kilobytes (KB). Please convert them correctly to MB or GB in your text analysis.\n\nPlease identify functional groups of packages (e.g., docker, java) and explain their relationships."
    explained_packages_str = ask_ai(explanation_prompt)

    print("Asking AI to explain cryptic packages...")
    cryptic_packages = sorted([p for p in auto_packages if p['name'].startswith('lib')], key=lambda x: x['size_kb'], reverse=True)[:5]
    cryptic_packages_prompt = f"Please explain in simple terms what the following packages are and why they might be installed on a development machine:\n\n{cryptic_packages}"
    explained_cryptic_packages_str = ask_ai(cryptic_packages_prompt)

    print("Asking AI for personalized recommendations...")
    recommendations_prompt = f"""Based on the following analysis, please provide personalized maintenance recommendations.

Packages:
{all_packages}

node_modules:
{node_modules}

pnpm_store:
{pnpm_store}

Special Instructions:
- If you recommend Docker cleanup, advise using `docker system prune` as the safe default for removing dangling images and stopped containers.
- Clearly explain that `docker system prune -a` is a more aggressive command that will remove ALL unused images, including images that were pulled but are not currently used by a container. Warn the user that this might remove images they want to keep.
"""
    recommendations_str = ask_ai(recommendations_prompt)

    ai_insights = {
        "categorized_packages": categorized_packages_str,
        "explained_packages": explained_packages_str,
        "explained_cryptic_packages": explained_cryptic_packages_str,
        "recommendations": recommendations_str,
    }

    # Save to JSON for frontend
    import json
    
    # Convert datetime objects to strings for JSON serialization
    node_modules_serializable = []
    for nm in node_modules:
        nm_copy = nm.copy()
        if isinstance(nm_copy['last_modified'], datetime):
            nm_copy['last_modified'] = nm_copy['last_modified'].isoformat()
        node_modules_serializable.append(nm_copy)

    data_for_frontend = {
        "manual_packages": manual_packages,
        "node_modules": node_modules_serializable,
        "pnpm_store": pnpm_store,
        "home_dir_analysis": home_dir_analysis,
        "ai_insights": ai_insights,
        "generated_at": datetime.now().isoformat()
    }
    
    # Determine where to save. If frontend/public exists, save there.
    frontend_public_path = os.path.join(os.path.dirname(__file__), "frontend", "public")
    if os.path.isdir(frontend_public_path):
        json_path = os.path.join(frontend_public_path, "data.json")
    else:
        json_path = "data.json"

    with open(json_path, "w") as f:
        json.dump(data_for_frontend, f, indent=2)
    print(f"Data exported to {json_path}")

    report = generate_markdown_report(manual_packages, node_modules, pnpm_store, home_dir_analysis, ai_insights)

    print("\n--- Analysis Report ---")
    print(report)

    # Ask to save the report
    try:
        save_report = input("\nDo you want to save this report to a file? (y/n): ").lower()
        if save_report == 'y':
            filename = "AI_linux_report.md"
            with open(filename, "w") as f:
                f.write(report)
            print(f"Report saved to {filename}")
    except EOFError:
        print("\nSkipping file save in non-interactive mode.")

if __name__ == "__main__":
    main()