import base64
import urllib.request
import urllib.error

HTTP_URL = "http://127.0.0.1:8080/"
HTTP_USER = "admin"
HTTP_PASS = "wed892000"

def test_http_basic_auth():
    # Création du header Basic Auth : base64("user:pass")
    credentials = f"{HTTP_USER}:{HTTP_PASS}".encode("utf-8")
    token = base64.b64encode(credentials).decode("ascii")

    req = urllib.request.Request(HTTP_URL)
    req.add_header("Authorization", f"Basic {token}")

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            print("✅ HTTP OK")
            print("Status :", response.status)
            return True

    except urllib.error.HTTPError as e:
        # 401 = Unauthorized (mauvais user/pass)
        print("❌ HTTP Error")
        print("Status :", e.code)
        return False

    except Exception as e:
        print("❌ Erreur réseau / connexion")
        print("Détail :", e)
        return False

if __name__ == "__main__":
    test_http_basic_auth()
