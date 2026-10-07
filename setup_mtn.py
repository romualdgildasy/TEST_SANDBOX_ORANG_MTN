import asyncio
import base64
import uuid
import httpx


SUBSCRIPTION_KEY = "1623d2b036c04d708dbb4f5d241869c8"

BASE_URL = "https://sandbox.momodeveloper.mtn.com"


async def setup_mtn_momo():
    # Étape A : Générer un UUID v4 unique pour ton utilisateur Sandbox
    api_user_id = str(uuid.uuid4())
    print(f"1. Identifiant utilisateur généré (UUID) : {api_user_id}")

    headers_common = {
        "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        # Étape B : Créer l'utilisateur sur le sandbox MTN
        print("2. Création de l'utilisateur sur le Sandbox MTN...")
        create_user_url = f"{BASE_URL}/v1_0/apiuser"
        create_user_headers = {
            **headers_common,
            "X-Reference-Id": api_user_id,
            "Content-Type": "application/json",
        }
        create_user_body = {
            "providerCallbackHost": "webhook.site"  # Hôte factice requis en sandbox
        }

        resp_user = await client.post(
            create_user_url, 
            headers=create_user_headers, 
            json=create_user_body
        )

        if resp_user.status_code != 201:
            print(f" Échec création utilisateur : {resp_user.status_code}")
            print(resp_user.text)
            return

        print(" Utilisateur créé avec succès sur MTN (Code 201) !")

        # Étape C : Générer la clé API (API Key) pour cet utilisateur
        print("3. Demande de l'API Key à MTN...")
        create_key_url = f"{BASE_URL}/v1_0/apiuser/{api_user_id}/apikey"
        resp_key = await client.post(create_key_url, headers=headers_common)

        if resp_key.status_code != 201:
            print(f" Échec génération API Key : {resp_key.status_code}")
            print(resp_key.text)
            return

        api_key = resp_key.json().get("apiKey")
        print(f" API Key obtenue : {api_key}")

        # Étape D : Récupérer le premier token OAuth pour valider
        print("4. Test d'obtention du token Bearer...")
        # MTN demande une authentification HTTP Basic avec "api_user_id:api_key" encodé en base64
        credentials = f"{api_user_id}:{api_key}"
        encoded_auth = base64.b64encode(credentials.encode()).decode()

        token_url = f"{BASE_URL}/collection/token/"
        token_headers = {
            "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
            "Authorization": f"Basic {encoded_auth}",
        }

        resp_token = await client.post(token_url, headers=token_headers)

        if resp_token.status_code == 200:
            token_data = resp_token.json()
            print("\n==========================================")
            print(" SUCCÈS TOTAL MTN SANDBOX !")
            print("==========================================")
            print(f"MTN_API_USER       : {api_user_id}")
            print(f"MTN_API_KEY        : {api_key}")
            print(f"MTN_SUB_KEY        : {SUBSCRIPTION_KEY}")
            print(f"Access Token reçu  : {token_data.get('access_token')[:25]}... (tronqué)")
            print(f"Expire dans        : {token_data.get('expires_in')} secondes")
            print("==========================================")
            print(" Conserve précieusement ces identifiants dans ton fichier .env !")
        else:
            print(f" Échec obtention token : {resp_token.status_code}")
            print(resp_token.text)


if __name__ == "__main__":
    asyncio.run(setup_mtn_momo())