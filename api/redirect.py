from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
import os
app = FastAPI()

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/{short_url}")
def redirect_url(short_url: str):
    # Retrieve long URL from Supabase
    response = supabase.table("urls").select("long_url").eq("short_url", short_url).execute()

    if not response.data:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return {"long_url": response.data[0]["long_url"]}