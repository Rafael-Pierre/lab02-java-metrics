import requests
import csv
import os
import subprocess
import time

# ==========================
# CONFIGURAÇÕES
# ==========================
GITHUB_TOKEN = ""  # Coloque seu token pessoal do GitHub
OUTPUT_CSV = "repositorios_java.csv"
CLONE_DIR = "repos_clonados"
LANGUAGE = "Java"
PER_PAGE = 100
TOTAL_REPOS = 1000

# Cabeçalho para autenticação
headers = {"Authorization": f"token {GITHUB_TOKEN}"}

# ==========================
# FUNÇÃO PARA BUSCAR REPOSITÓRIOS
# ==========================
def fetch_repositories():
    repos = []
    for page in range(1, (TOTAL_REPOS // PER_PAGE) + 1):
        print(f"🔍 Buscando página {page}...")
        url = f"https://api.github.com/search/repositories?q=language:{LANGUAGE}&sort=stars&order=desc&per_page={PER_PAGE}&page={page}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            repos.extend(data["items"])
        else:
            print(f"⚠️ Erro {response.status_code}: {response.text}")
            break

        time.sleep(2)  # evitar rate limit

    return repos[:TOTAL_REPOS]

# ==========================
# FUNÇÃO PARA CLONAR REPOSITÓRIOS
# ==========================
def clone_repository(repo_url, repo_name):
    if not os.path.exists(CLONE_DIR):
        os.makedirs(CLONE_DIR)

    repo_path = os.path.join(CLONE_DIR, repo_name)

    if not os.path.exists(repo_path):
        print(f"⬇️ Clonando {repo_name}...")
        subprocess.run(["git", "clone", "--depth", "1", repo_url, repo_path])
    else:
        print(f"✅ {repo_name} já clonado.")

# ==========================
# FUNÇÃO PARA SALVAR CSV
# ==========================
def save_to_csv(repos):
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["name", "full_name", "stars", "forks", "url", "created_at", "updated_at", "language", "clone_url"])

        for repo in repos:
            writer.writerow([
                repo["name"],
                repo["full_name"],
                repo["stargazers_count"],
                repo["forks_count"],
                repo["html_url"],
                repo["created_at"],
                repo["updated_at"],
                repo["language"],
                repo["clone_url"]
            ])
    print(f"📄 CSV gerado: {OUTPUT_CSV}")

# ==========================
# MAIN
# ==========================
if __name__ == "__main__":
    repositorios = fetch_repositories()

    # Salvar informações no CSV
    save_to_csv(repositorios)

    # Clonar só o primeiro como exemplo (Sprint 1 pede 1 CSV com 1 repositório medido)
    if repositorios:
        primeiro_repo = repositorios[0]
        clone_repository(primeiro_repo["clone_url"], primeiro_repo["name"])
