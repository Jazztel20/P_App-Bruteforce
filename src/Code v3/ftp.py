import time
import hashlib

# -------------------------
# CONFIGURATION
# -------------------------

USERNAME = "admin"              # Utilisateur simulé (FTP)
PLAINTEXT_PASSWORD = "wed892000"  # Mot de passe réel (pour générer le hash UNE FOIS)
WORDLIST_PATH = "wordlist.txt"  # Fichier contenant une liste de mots de passe


def generer_hash_mdp(mot_de_passe: str) -> str:
    """
    Génère le hash SHA-256 d'un mot de passe en clair.
    Cette fonction simule ce que ferait un serveur FTP sécurisé :
    il ne stocke que le hash, pas le mot de passe en clair.
    """
    return hashlib.sha256(mot_de_passe.encode("utf-8")).hexdigest()


# On simule ce que le serveur connaît : uniquement le hash du mot de passe
HASH_PASSWORD = generer_hash_mdp(PLAINTEXT_PASSWORD)


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


def tester_login_ftp_simule(password_a_tester: str) -> bool:
    """
    Fonction de test qui SIMULE une authentification FTP locale.

    Dans un vrai serveur FTP sécurisé, le mot de passe saisi par l'utilisateur est hashé,
    puis comparé au hash stocké en base de données.

    Ici, on reproduit exactement ce principe :
    - on hash le mot de passe à tester
    - on compare au hash du mot de passe réel (HASH_PASSWORD)
    """
    hash_teste = generer_hash_mdp(password_a_tester)
    return hash_teste == HASH_PASSWORD


def bruteforce():
    """
    Effectue un bruteforce par dictionnaire sur la SIMULATION d'un compte FTP :
    - lit tous les mots de passe de la wordlist
    - les teste un par un (hash + comparaison)
    - s'arrête dès que le bon mot de passe est trouvé
    - mesure le temps total
    """
    print("=== Outil de bruteforce pédagogique (FTP simulé, avec hash) ===")
    print(f"Utilisateur ciblé : {USERNAME}")
    print(f"Wordlist utilisée : {WORDLIST_PATH}")
    print("----------------------------------------------")

    mots_de_passe = charger_mots_de_passe(WORDLIST_PATH)
    print(f"Nombre de mots de passe dans la wordlist : {len(mots_de_passe)}")
    print()

    tentative = 0
    start = time.time()

    for mot in mots_de_passe:
        tentative += 1

        if tester_login_ftp_simule(mot):
            end = time.time()
            duree = end - start

            print()
            print("✅ Mot de passe trouvé !")
            print(f"   Utilisateur : {USERNAME}")
            print(f"   Mot de passe (en clair) : {mot}")
            print(f"   Tentatives   : {tentative}")
            print(f"   Temps écoulé : {duree:.4f} secondes")
            return

    end = time.time()
    duree = end - start

    print()
    print("❌ Aucun mot de passe de la wordlist ne correspond.")
    print(f"   Tentatives   : {tentative}")
    print(f"   Temps écoulé : {duree:.4f} secondes")


if __name__ == "__main__":
    bruteforce()
