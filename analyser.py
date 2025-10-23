#!/usr/bin/env python3

import subprocess
import os
from datetime import datetime, timedelta

def analyze_installed_packages(manual_packages):
    """
    Analyzes installed Debian packages to find their size and name.
    """
    try:
        command = "dpkg-query -Wf '${Installed-Size}\t${Package}\t${binary:Summary}\n' | sort -n"
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)

        packages = []
        for line in result.stdout.strip().splitlines():
            if line:
                parts = line.split('\t')
                if len(parts) >= 2:
                    size_kb_str, name = parts[0], parts[1]
                    summary = parts[2] if len(parts) > 2 else "N/A"
                    try:
                        size_kb = int(size_kb_str)
                        is_manual = name in manual_packages
                        packages.append({"name": name, "size_kb": size_kb, "summary": summary, "manual": is_manual})
                    except ValueError:
                        # This can happen if Installed-Size is not a number.
                        # In this case, we can probably ignore the package or log it.
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



def generate_markdown_report(packages, node_modules, home_dir_analysis):
    """
    Generates a Markdown report from the collected data.
    """
    report_lines = [
        "# Linux Partition Analysis Report",
        "",
        "## Installed Software Packages",
        "",
        "| Package Name | Size (MB) | Manually Installed | Summary |",
        "|--------------|-----------|--------------------|---------|",
    ]

    for pkg in packages[:20]: # Show top 20 largest
        size_mb = pkg['size_kb'] / 1024
        if "children" in pkg:
            # This is a group
            any_manual = any(child.get("manual") for child in pkg["children"])
            manual_str = "Yes" if any_manual else "No"
            report_lines.append(f"| **{pkg['name']}** | **{size_mb:.2f}** | **{manual_str}** | **{pkg.get('summary', 'N/A')}** |")
            for child_pkg in pkg["children"]:
                child_size_mb = child_pkg['size_kb'] / 1024
                child_manual_str = "Yes" if child_pkg.get("manual") else "No"
                report_lines.append(f"| &nbsp;&nbsp;&nbsp;{child_pkg['name']} | {child_size_mb:.2f} | {child_manual_str} | {child_pkg.get('summary', 'N/A')} |")
        else:
            # This is a single package
            manual_str = "Yes" if pkg.get("manual") else "No"
            report_lines.append(f"| {pkg['name']} | {size_mb:.2f} | {manual_str} | {pkg.get('summary', 'N/A')} |")

    report_lines.extend([
        "",
        "## `node_modules` Directories",
        "",
        "| Path | Size (MB) | Last Modified |",
        "|------|-----------|---------------|",
    ])

    total_size_mb = 0
    node_modules.sort(key=lambda x: x['size_kb'], reverse=True)
    for nm in node_modules:
        size_mb = nm['size_kb'] / 1024
        total_size_mb += size_mb
        report_lines.append(f"| {nm['path']} | {size_mb:.2f} | {nm['last_modified'].strftime('%Y-%m-%d')} |")

    report_lines.append(f"\n**Total size of all 'node_modules' folders:** {total_size_mb:.2f} MB")

    report_lines.extend([
        "",
        "## Home Directory Analysis",
        "",
        "| Directory | Purpose |",
        "|-----------|---------|",
    ])

    for dir_info in home_dir_analysis:
        report_lines.append(f"| {dir_info['name']} | {dir_info['description']} |")

    report_lines.extend([
        "",
        "## Maintenance Recommendations",
        "",
        "**Package Management:**",
        "- Regularly run `sudo apt autoremove` and `sudo apt clean` to remove orphaned packages and clear the package cache.",
        "- Review the list of the largest packages above. Consider removing any that you no longer use.",
        "",
        "**`node_modules` Management:**",
    ])

    six_months_ago = datetime.now() - timedelta(days=180)
    old_node_modules = [nm for nm in node_modules if nm['last_modified'] < six_months_ago]

    if old_node_modules:
        report_lines.append("- The following `node_modules` directories haven't been modified in over 6 months and might be from old projects:")
        for nm in old_node_modules:
            report_lines.append(f"  - `{nm['path']}`")

    report_lines.append("- Consider using a tool like `npkill` to easily find and remove old or large `node_modules` directories.")

    return "\n".join(report_lines)

def group_packages(packages):
    grouped = {}
    remaining_packages = []
    groups_to_find = ["docker", "openjdk", "gcc", "g++", "cpp", "node", "git", "vim"]

    for pkg in packages:
        found_group = None
        for group_name in groups_to_find:
            if pkg["name"].startswith(group_name):
                found_group = group_name
                break
        
        if found_group:
            if found_group not in grouped:
                grouped[found_group] = {"name": f"{found_group} related packages", "size_kb": 0, "summary": f"Packages related to {found_group}", "children": []}
            grouped[found_group]["size_kb"] += pkg["size_kb"]
            grouped[found_group]["children"].append(pkg)
        else:
            remaining_packages.append(pkg)
            
    # Sort children by size
    for group in grouped.values():
        group['children'].sort(key=lambda x: x['size_kb'], reverse=True)

    # Create a new list with the grouped packages and the remaining ones
    new_package_list = list(grouped.values()) + remaining_packages
    
    # Sort the final list by size
    new_package_list.sort(key=lambda x: x["size_kb"], reverse=True)
    
    return new_package_list

def main():
    print("Starting Linux analysis...")
    manual_packages = get_manually_installed_packages()
    packages = analyze_installed_packages(manual_packages)
    packages = group_packages(packages)
    node_modules = find_node_modules()
    home_dir_analysis = analyze_home_directory()

    report = generate_markdown_report(packages, node_modules, home_dir_analysis)

    print("\n--- Analysis Report ---")
    print(report)

    # Ask to save the report
    try:
        save_report = input("\nDo you want to save this report to a file? (y/n): ").lower()
        if save_report == 'y':
            filename = "linux_analysis_report.md"
            with open(filename, "w") as f:
                f.write(report)
            print(f"Report saved to {filename}")
    except EOFError:
        print("\nSkipping file save in non-interactive mode.")

if __name__ == "__main__":
    main()
