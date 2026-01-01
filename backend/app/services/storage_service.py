import os
import requests

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")


def generate_signed_url(bucket: str, file_path: str, expires_in: int = 300) -> str:
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        raise RuntimeError("Supabase environment variables are not set")

    # 🔒 Correct endpoint
    url = f"{SUPABASE_URL}/storage/v1/object/sign/{bucket}"

    headers = {
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        # 🔑 SINGULAR path — THIS is the key change
        "paths": file_path.strip().lstrip("/"),
        "expiresIn": expires_in
    }

    resp = requests.post(url, headers=headers, json=payload)

    if resp.status_code != 200:
        raise RuntimeError(
            f"Supabase sign failed: {resp.status_code} {resp.text}"
        )

    # 1. Get signed path from response FIRST
    signed_path = resp.json()[0]["signedURL"]


    # 2. signed_path already starts with /object/sign/...
    # Supabase requires /storage/v1 prefix when accessing it
    # Return full URL
    return f"{SUPABASE_URL}/storage/v1{signed_path}"


    