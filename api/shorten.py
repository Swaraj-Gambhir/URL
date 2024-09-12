from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
from pydantic import BaseModel
import os
import random
import string

app = FastAPI()

# Load environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
class Url(BaseModel):
    long_url: str
def generate_short_url(length: int = 6) -> str:
    """Generate a random string of fixed length with only letters."""
    return ''.join(random.choices(string.ascii_letters, k=length))

@app.post("/api/shorten")
def shorten_url(url: Url):
    long_url = url.long_url

    # Ensure a unique short URL
    while True:
        short_url = generate_short_url()
        response = supabase.table("urls").select("short_url").eq("short_url", short_url).execute()
        if not response.data:  # If no existing entry with the same short URL
            break

    # Insert into Supabase
    response = supabase.table("urls").insert({"long_url": long_url, "short_url": short_url}).execute()

    if response.status_code != 201:
        raise HTTPException(status_code=500, detail="Failed to create short URL")

    return {"short_url": f"https://gen.innov/{short_url}"}