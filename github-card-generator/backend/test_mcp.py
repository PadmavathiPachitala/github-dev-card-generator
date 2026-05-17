import asyncio
import json
import os
import sys

# Add the current directory to sys.path so we can import mcp_server
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp_server import call_tool

async def test_workflow():
    username = "google"
    print(f"Testing workflow for {username}...")
    
    # 1. Scrape GitHub
    print("1. Scraping GitHub...")
    resp = await call_tool("scrape_github", {"username": username})
    github_data = json.loads(resp[0].text)
    if "error" in github_data:
        print(f"FAILED at scrape_github: {github_data['error']}")
        return

    # 2. Analyze Profile
    print("2. Analyzing Profile...")
    resp = await call_tool("analyze_profile", {"github_data": github_data})
    analysis = json.loads(resp[0].text)

    # 3. Generate Card HTML
    print("3. Generating Card HTML...")
    resp = await call_tool("generate_card_html", {
        "username": username,
        "github_data": github_data,
        "analysis": analysis
    })
    html = resp[0].text
    
    # 4. Save Card
    print("4. Saving Card...")
    resp = await call_tool("save_card", {"username": username, "html": html})
    save_path = resp[0].text
    
    print("\n--- TEST RESULTS ---")
    print(f"Developer Vibe: {analysis.get('developer_vibe')}")
    print(f"Card Theme: {analysis.get('card_theme')}")
    print(f"Save Path: {save_path}")
    print("--------------------")

if __name__ == "__main__":
    asyncio.run(test_workflow())
