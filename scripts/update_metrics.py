import os
import re
import datetime
import urllib.request
import json

def update_svg(file_path, year, repos_count, contribs_text):
    if not os.path.exists(file_path):
        return
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Update year label: CONTRIBUIÇÕES EM <YEAR>
    content = re.sub(r'CONTRIBUIÇÕES EM \d{4}', f'CONTRIBUIÇÕES EM {year}', content)
    
    # Update repos count if provided
    if repos_count:
        content = re.sub(
            r'(<text class="font-hud"[^>]*>)\d+(</text>\s*<text class="font-hud"[^>]*>Soluções de IA)',
            rf'\g<1>{repos_count}\g<2>',
            content
        )

    # Update contribs text if provided
    if contribs_text:
        content = re.sub(
            r'(<text class="font-hud"[^>]*>)\d+\+?(</text>\s*<text class="font-hud"[^>]*>Commits contínuos)',
            rf'\g<1>{contribs_text}\g<2>',
            content
        )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated {file_path}")

def main():
    now = datetime.datetime.now(datetime.timezone.utc)
    current_year = now.year
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")

    repos_count = None
    contribs_text = None

    try:
        headers = {"User-Agent": "Metrics-Bot"}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        req = urllib.request.Request("https://api.github.com/users/nicolaspn09", headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            public_repos = data.get("public_repos")
            if public_repos:
                repos_count = str(public_repos)
    except Exception as e:
        print(f"Error fetching user repos: {e}")

    for svg_file in ["assets/stats-dark.svg", "assets/stats-light.svg"]:
        update_svg(svg_file, current_year, repos_count, contribs_text)

if __name__ == "__main__":
    main()
