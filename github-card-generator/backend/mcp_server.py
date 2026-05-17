import os
import json
import httpx
import asyncio
from typing import Dict, List, Optional
from mcp.server import Server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from dotenv import load_dotenv

load_dotenv()

# Initialize standard MCP server
app = Server("GitHubDevCard")

GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

async def get_client():
    headers = {"User-Agent": "GitHubDevCard-Agent"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    return httpx.AsyncClient(headers=headers)

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="scrape_github",
            description="Fetch GitHub profile and repository data",
            inputSchema={
                "type": "object",
                "properties": {"username": {"type": "string"}},
                "required": ["username"]
            }
        ),
        Tool(
            name="analyze_profile",
            description="Analyze GitHub profile for developer insights",
            inputSchema={
                "type": "object",
                "properties": {"github_data": {"type": "object"}},
                "required": ["github_data"]
            }
        ),
        Tool(
            name="generate_card_html",
            description="Generate a beautiful HTML card string",
            inputSchema={
                "type": "object",
                "properties": {
                    "username": {"type": "string"},
                    "github_data": {"type": "object"},
                    "analysis": {"type": "object"}
                },
                "required": ["username", "github_data", "analysis"]
            }
        ),
        Tool(
            name="save_card",
            description="Save the HTML card to a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "username": {"type": "string"},
                    "html": {"type": "string"}
                },
                "required": ["username", "html"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "scrape_github":
        username = arguments["username"]
        async with await get_client() as client:
            user_resp = await client.get(f"{GITHUB_API_URL}/users/{username}")
            if user_resp.status_code != 200:
                return [TextContent(type="text", text=json.dumps({"error": f"User {username} not found"}))]
            
            user_data = user_resp.json()
            repos_resp = await client.get(f"{GITHUB_API_URL}/users/{username}/repos", params={"sort": "stars", "per_page": 100})
            repos = repos_resp.json() if repos_resp.status_code == 200 else []
            
            top_repos = []
            languages = {}
            for r in sorted(repos, key=lambda x: x.get("stargazers_count", 0), reverse=True)[:6]:
                top_repos.append({
                    "name": r.get("name"),
                    "stars": r.get("stargazers_count"),
                    "language": r.get("language"),
                    "description": r.get("description")
                })
            for r in repos:
                lang = r.get("language")
                if lang: languages[lang] = languages.get(lang, 0) + 1
            
            sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)
            
            res = {
                "name": user_data.get("name") or username,
                "avatar_url": user_data.get("avatar_url"),
                "bio": user_data.get("bio"),
                "location": user_data.get("location"),
                "public_repos": user_data.get("public_repos"),
                "followers": user_data.get("followers"),
                "top_repos": top_repos,
                "most_used_languages": [l[0] for l in sorted_langs[:5]]
            }
            return [TextContent(type="text", text=json.dumps(res))]

    elif name == "analyze_profile":
        github_data = arguments["github_data"]
        # Simulated analysis for Gemini 2.5 Flash
        res = {
            "developer_vibe": f"A high-impact {github_data['most_used_languages'][0] if github_data['most_used_languages'] else 'developer'} shaping the future.",
            "top_skills": github_data['most_used_languages'][:3],
            "fun_fact": f"Architected systems with {sum(r['stars'] for r in github_data['top_repos'])} stars in top repos.",
            "card_theme": "hacker"
        }
        return [TextContent(type="text", text=json.dumps(res))]

    elif name == "generate_card_html":
        username = arguments["username"]
        github_data = arguments["github_data"]
        analysis = arguments["analysis"]
        
        theme_colors = {
            "hacker": {"bg": "#0d1117", "text": "#c9d1d9", "accent": "#238636"},
            "builder": {"bg": "#ffffff", "text": "#24292f", "accent": "#0969da"}
        }
        theme = theme_colors.get(analysis.get("card_theme"), theme_colors["builder"])
        
        html = f"<html><body style='background:{theme['bg']}; color:{theme['text']};'><h1>{github_data['name']}</h1><p>{analysis['developer_vibe']}</p></body></html>"
        return [TextContent(type="text", text=html)]

    elif name == "save_card":
        username = arguments["username"]
        html = arguments["html"]
        os.makedirs("static/cards", exist_ok=True)
        file_path = f"static/cards/{username}.html"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)
        return [TextContent(type="text", text=f"/static/cards/{username}.html")]

if __name__ == "__main__":
    from mcp.server.stdio import stdio_server
    async def main():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(read_stream, write_stream, app.create_initialization_options())
    asyncio.run(main())
