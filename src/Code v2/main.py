import time

# -------------------------
# CONFIGURATION
# -------------------------

USERNAME = "admin"              # Juste pour l'affichage
CORRECT_PASSWORD = "wed892000"    # Mot de passe réel à trouver
WORDLIST_PATH = "wordlist.txt"  # Fichier contenant une liste de mots de passe


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


def tester_mot_de_passe(password_a_tester):
    """
    Fonction de test.
    Version pédagogique : on compare simplement avec CORRECT_PASSWORD.
    """
    return password_a_tester == CORRECT_PASSWORD


def bruteforce():
    """
    Effectue un bruteforce par dictionnaire sans affichage des tentatives.
    """
    print("=== Outil de bruteforce pédagogique (local) ===")
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

        if tester_mot_de_passe(mot):
            end = time.time()
            duree = end - start

            print()
            print("✅ Mot de passe trouvé !")
            print(f"   Utilisateur : {USERNAME}")
            print(f"   Mot de passe : {mot}")
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
