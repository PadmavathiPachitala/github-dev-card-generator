import httpx
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def debug_github():
    url = "https://api.github.com/users/google"
    token = os.getenv("GITHUB_TOKEN")
    headers = {"User-Agent": "MCP-Test"}
    if token:
        headers["Authorization"] = f"token {token}"
    
    print(f"Requesting {url}...")
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        print(f"Status: {resp.status_code}")
        print(f"Body: {resp.text[:500]}")

if __name__ == "__main__":
    asyncio.run(debug_github())
