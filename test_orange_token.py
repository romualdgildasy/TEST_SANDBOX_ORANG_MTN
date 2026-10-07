import asyncio
import httpx

# Remplace par ta vraie valeur (ex: "Basic OGRLc...")
ORANGE_BASIC_AUTH = "Basic VTZrZWRPSU1xYlJVaEVtNDB1RVF6TG02cXBJeXpIVEo6WnpwVmI1enFrb2VieTFZVFc2ckQ1UkFqOTZkOUVKMGFwdHRZYkNhQUJVTGc="

# URL exacte fournie par ton dashboard sandbox
OAUTH_URL = "https://api.orange.com/openidconnect/playground/v1.0/token"

async def test_connexion_orange():
    headers = {
        "Authorization": ORANGE_BASIC_AUTH,
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }
    data = {
        "grant_type": "client_credentials"
    }

    print("Envoi de la requête au Sandbox Orange...")
    
    # follow_redirects=True correspond au flag --location de curl
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        try:
            response = await client.post(OAUTH_URL, headers=headers, data=data)
            
            print(f"Code HTTP reçu : {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(" Authentification réussie !")
                print(f"Type de jeton  : {result.get('token_type')}")
                print(f"Expire dans    : {result.get('expires_in')} secondes")
                print(f"Access Token   : {result.get('access_token')[:25]}... (tronqué)")
            else:
                print(" Erreur renvoyée par Orange :")
                print(response.text)
                
        except httpx.ConnectTimeout:
            print(" Délai d'attente dépassé (Timeout de connexion). Vérifie ta connexion internet ou le pare-feu.")
        except Exception as e:
            print(f" Erreur inattendue : {e}")

if __name__ == "__main__":
    asyncio.run(test_connexion_orange())