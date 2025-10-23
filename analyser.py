#!/usr/bin/env python3

import subprocess
import os
from datetime import datetime, timedelta

def analyze_installed_packages():
    """
    Analyzes installed Debian packages to find their size and name.
    """
    try:
        command = "dpkg-query -Wf '${Installed-Size}\\t${Package}\\n' | sort -n"
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)

        packages = []
        for line in result.stdout.strip().splitlines():
            if line:
                parts = line.split('\t')
                if len(parts) == 2:
                    size_kb, name = parts
                    packages.append({"name": name, "size_kb": int(size_kb)})

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

def generate_markdown_report(packages, node_modules):
    """
    Generates a Markdown report from the collected data.
    """
    report_lines = [
        "# Linux Partition Analysis Report",
        "",
        "## Installed Software Packages",
        "",
        "| Package Name | Size (MB) |",
        "|--------------|-----------|",
    ]

    for pkg in packages[:20]: # Show top 20 largest
        size_mb = pkg['size_kb'] / 1024
        report_lines.append(f"| {pkg['name']} | {size_mb:.2f} |")

    report_lines.extend([
        "",
        "## `node_modules` Directories",
        "",
        "| Path | Size (MB) | Last Modified |",
        "|------|-----------|---------------|",
    ])

    total_size_mb = 0
    for nm in node_modules:
        size_mb = nm['size_kb'] / 1024
        total_size_mb += size_mb
        report_lines.append(f"| {nm['path']} | {size_mb:.2f} | {nm['last_modified'].strftime('%Y-%m-%d')} |")

    report_lines.append(f"\n**Total size of all 'node_modules' folders:** {total_size_mb:.2f} MB")

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

def main():
    print("Starting Linux analysis...")
    packages = analyze_installed_packages()
    node_modules = find_node_modules()

    report = generate_markdown_report(packages, node_modules)

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
