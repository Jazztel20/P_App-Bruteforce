import time
import base64
import urllib.request
import urllib.error
from ftplib import FTP, error_perm
import subprocess

# -------------------------
# CONFIGURATION
# -------------------------

WORDLIST_PATH = "wordlist.txt"

# Choisis ici :
# "FTP"  -> bruteforce réel FTP via Docker
# "HTTP" -> test Basic Auth HTTP (sans requests)
# "SSH"  -> preuve SSH via logs Docker (sans client SSH)
MODE = "SSH"

# FTP
FTP_HOST = "127.0.0.1"
FTP_PORT = 21
FTP_USER = "admin"

# HTTP (Caddy recommandé) ou autre service sur 8080
HTTP_URL = "http://127.0.0.1:8080/"
HTTP_USER = "admin"
HTTP_PASS = "wed892000"

# Progression (FTP)
PROGRESS_BAR_WIDTH = 30
PROGRESS_STEP = 50


def charger_mots_de_passe(chemin_fichier):
    mots = []
    with open(chemin_fichier, "r", encoding="utf-8") as f:
        for ligne in f:
            mot = ligne.strip()
            if mot:
                mots.append(mot)
    return mots


def afficher_progression(tentative: int, total: int, start_time: float):
    if total == 0:
        return
    progress = tentative / total
    filled_length = int(PROGRESS_BAR_WIDTH * progress)
    bar = "#" * filled_length + "-" * (PROGRESS_BAR_WIDTH - filled_length)
    temps_ecoule = time.time() - start_time
    print(
        f"[PROGRESSION] [{bar}] {progress * 100:5.1f}% "
        f"- {tentative}/{total} tentatives "
        f"- Temps écoulé : {temps_ecoule:.2f} sec"
    )


# -------------------------
# FTP: bruteforce réel
# -------------------------
def tester_login_ftp(password_a_tester: str) -> bool:
    if FTP_HOST not in ("127.0.0.1", "localhost"):
        raise ValueError("Par sécurité, FTP doit rester local (127.0.0.1 / localhost).")

    try:
        with FTP() as ftp:
            ftp.connect(host=FTP_HOST, port=FTP_PORT, timeout=3)
            ftp.login(user=FTP_USER, passwd=password_a_tester)
            return True
    except error_perm:
        return False
    except OSError:
        return False


def run_ftp_bruteforce():
    print("=== Bruteforce pédagogique (FTP Docker local) ===")
    print(f"Serveur FTP       : {FTP_HOST}:{FTP_PORT}")
    print(f"Utilisateur ciblé : {FTP_USER}")
    print(f"Wordlist          : {WORDLIST_PATH}")
    print("----------------------------------------------")

    mots_de_passe = charger_mots_de_passe(WORDLIST_PATH)
    total = len(mots_de_passe)
    print(f"Nombre de mots de passe : {total}\n")

    tentative = 0
    start = time.time()

    for mot in mots_de_passe:
        tentative += 1

        if tentative % PROGRESS_STEP == 0:
            afficher_progression(tentative, total, start)

        if tester_login_ftp(mot):
            duree = time.time() - start
            afficher_progression(tentative, total, start)

            print("\n✅ Mot de passe trouvé !")
            print(f"   Mot de passe : {mot}")
            print(f"   Tentatives   : {tentative}")
            print(f"   Temps total  : {duree:.4f} secondes")
            return

    duree = time.time() - start
    afficher_progression(tentative, total, start)

    print("\n❌ Aucun mot de passe ne correspond.")
    print(f"   Tentatives   : {tentative}")
    print(f"   Temps total  : {duree:.4f} secondes")


# -------------------------
# HTTP: test Basic Auth (sans requests)
# -------------------------
def run_http_test():
    print("=== Test HTTP Basic Auth (local) ===")
    print(f"URL : {HTTP_URL}")

    credentials = f"{HTTP_USER}:{HTTP_PASS}".encode("utf-8")
    token = base64.b64encode(credentials).decode("ascii")

    req = urllib.request.Request(HTTP_URL)
    req.add_header("Authorization", f"Basic {token}")

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            print("✅ HTTP OK")
            print("Status :", response.status)
    except urllib.error.HTTPError as e:
        print("❌ HTTP Error")
        print("Status :", e.code)
    except Exception as e:
        print("❌ Erreur réseau / connexion")
        print("Détail :", e)


# -------------------------
# SSH: preuve via logs docker (sans client)
# -------------------------
def run_ssh_proof():
    print("=== Preuve SSH (Docker logs) ===")
    print("Consigne sécurité : pas d'installation de client SSH sur Windows.\n")

    try:
        result = subprocess.run(
            ["docker", "logs", "ssh-test", "--tail", "25"],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print("❌ Impossible de lire les logs du conteneur 'ssh-test'.")
            print(result.stderr.strip())
            return

        print(result.stdout.strip())
        print("SSH OK.")
    except Exception as e:
        print("❌ Erreur docker logs :", e)


if __name__ == "__main__":
    if MODE == "FTP":
        run_ftp_bruteforce()
    elif MODE == "HTTP":
        run_http_test()
    elif MODE == "SSH":
        run_ssh_proof()
    else:
        raise ValueError("MODE invalide. Choisis 'FTP', 'HTTP' ou 'SSH'.")
