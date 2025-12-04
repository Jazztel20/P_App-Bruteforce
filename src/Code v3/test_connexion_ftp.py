from ftplib import FTP, error_perm

FTP_HOST = "127.0.0.1"
FTP_PORT = 21
FTP_USER = "admin"
FTP_PASS = "wed892000"  # Ton mot de passe FTP Docker

def test_ftp_connection():
    try:
        with FTP() as ftp:
            print(f"Connexion à {FTP_HOST}:{FTP_PORT} ...")
            ftp.connect(host=FTP_HOST, port=FTP_PORT, timeout=5)

            print(f"Tentative de login avec utilisateur '{FTP_USER}' ...")
            ftp.login(user=FTP_USER, passwd=FTP_PASS)

            print("✅ Connexion FTP réussie !")
            print("Répertoire courant :", ftp.pwd())

            # Optionnel : afficher la liste des fichiers
            # ftp.retrlines("LIST")

    except error_perm as e:
        print("❌ Erreur d'authentification FTP :", e)

    except OSError as e:
        print("❌ Erreur réseau / connexion impossible :", e)


if __name__ == "__main__":
    test_ftp_connection()
