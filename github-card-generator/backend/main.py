from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

import os

# ---------------------------------------------------
# APP
# ---------------------------------------------------

app = FastAPI()

# ---------------------------------------------------
# CORS
# ---------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------
# PATHS
# ---------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATIC_DIR = os.path.join(BASE_DIR, "static")

CARDS_DIR = os.path.join(STATIC_DIR, "cards")

os.makedirs(CARDS_DIR, exist_ok=True)

# ---------------------------------------------------
# MODEL
# ---------------------------------------------------

class CardRequest(BaseModel):
    username: str

# ---------------------------------------------------
# ROOT
# ---------------------------------------------------

@app.get("/")
async def root():

    return {
        "message": "Backend running"
    }

# ---------------------------------------------------
# GENERATE CARD
# ---------------------------------------------------

@app.post("/generate")
async def generate_card(request: CardRequest):

    import requests

    username = request.username.replace("@", "").strip()

    # ---------------------------------------------------
    # FETCH USER
    # ---------------------------------------------------

    github_url = f"https://api.github.com/users/{username}"

    response = requests.get(github_url)

    if response.status_code != 200:

        return {
            "error": "GitHub user not found"
        }

    data = response.json()

    # ---------------------------------------------------
    # USER DATA
    # ---------------------------------------------------

    name = data.get("name") or username

    bio = data.get("bio") or "Passionate developer building cool things."

    avatar = data.get("avatar_url")

    followers = data.get("followers", 0)

    public_repos = data.get("public_repos", 0)

    location = data.get("location") or "Unknown"

    profile_url = data.get("html_url")

    # ---------------------------------------------------
    # HTML CARD
    # ---------------------------------------------------

    html = f"""
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>{username} Dev Card</title>

    <style>

        * {{
            box-sizing: border-box;
        }}

        body {{

            margin: 0;

            min-height: 100vh;

            display: flex;

            align-items: center;

            justify-content: center;

            background:
                linear-gradient(
                    135deg,
                    #020617,
                    #0f172a
                );

            font-family: Arial, sans-serif;

            color: white;
        }}

        .card {{

            width: 440px;

            background: #111827;

            border:
                2px solid rgba(96,165,250,0.45);

            border-radius: 28px;

            padding: 24px;

            box-shadow:
                0 0 40px rgba(59,130,246,0.18);
        }}

        .top {{

            display: flex;

            align-items: center;

            gap: 18px;

            margin-bottom: 24px;
        }}

        .avatar {{

            width: 90px;

            height: 90px;

            border-radius: 50%;

            object-fit: cover;

            border:
                3px solid rgba(96,165,250,0.6);
        }}

        .name {{

            font-size: 26px;

            font-weight: bold;

            margin-bottom: 6px;
        }}

        .username {{

            color: #94a3b8;

            font-size: 15px;
        }}

        .bio {{

            margin-top: 18px;

            color: #d1d5db;

            line-height: 1.8;

            font-size: 16px;

            font-style: italic;
        }}

        .location {{

            margin-top: 14px;

            color: #60a5fa;

            font-size: 14px;
        }}

        .tags {{

            display: flex;

            flex-wrap: wrap;

            gap: 10px;

            margin-top: 24px;
        }}

        .tag {{

            background: #1e293b;

            border:
                1px solid rgba(255,255,255,0.08);

            padding: 8px 14px;

            border-radius: 999px;

            font-size: 13px;

            color: #cbd5e1;
        }}

        .stats {{

            margin-top: 28px;

            display: grid;

            grid-template-columns: repeat(2,1fr);

            gap: 16px;
        }}

        .stat {{

            background: #0f172a;

            border:
                1px solid rgba(255,255,255,0.05);

            padding: 18px;

            border-radius: 18px;

            text-align: center;
        }}

        .stat-number {{

            font-size: 30px;

            font-weight: bold;

            color: #60a5fa;
        }}

        .stat-label {{

            margin-top: 6px;

            color: #94a3b8;

            font-size: 14px;
        }}

        .section-title {{

            margin-top: 32px;

            margin-bottom: 16px;

            font-size: 18px;

            font-weight: bold;

            color: #e2e8f0;
        }}

        .projects {{

            display: flex;

            flex-direction: column;

            gap: 12px;
        }}

        .project {{

            background: #0f172a;

            padding: 14px;

            border-radius: 14px;

            border:
                1px solid rgba(255,255,255,0.05);
        }}

        .project-name {{

            font-weight: bold;

            color: #f8fafc;
        }}

        .project-tech {{

            margin-top: 4px;

            color: #94a3b8;

            font-size: 13px;
        }}

        .button {{

            display: block;

            margin-top: 30px;

            text-align: center;

            padding: 14px;

            border-radius: 16px;

            text-decoration: none;

            background:
                linear-gradient(
                    90deg,
                    #3b82f6,
                    #8b5cf6
                );

            color: white;

            font-weight: bold;
        }}

        .footer {{

            margin-top: 30px;

            padding-top: 18px;

            border-top:
                1px solid rgba(255,255,255,0.08);

            color: #64748b;

            font-size: 13px;

            line-height: 1.6;
        }}

    </style>

</head>

<body>

    <div class="card">

        <div class="top">

            <img
                class="avatar"
                src="{avatar}"
            />

            <div>

                <div class="name">
                    {name}
                </div>

                <div class="username">
                    @{username}
                </div>

            </div>

        </div>

        <div class="bio">
            "{bio}"
        </div>

        <div class="location">
            📍 {location}
        </div>

        <div class="tags">

            <div class="tag">Python</div>

            <div class="tag">AI</div>

            <div class="tag">Web Dev</div>

            <div class="tag">Open Source</div>

        </div>

        <div class="stats">

            <div class="stat">

                <div class="stat-number">
                    {public_repos}
                </div>

                <div class="stat-label">
                    Repositories
                </div>

            </div>

            <div class="stat">

                <div class="stat-number">
                    {followers}
                </div>

                <div class="stat-label">
                    Followers
                </div>

            </div>

        </div>

        <div class="section-title">
            Top Projects
        </div>

        <div class="projects">

            <div class="project">

                <div class="project-name">
                    AI Portfolio
                </div>

                <div class="project-tech">
                    React • FastAPI • AI
                </div>

            </div>

            <div class="project">

                <div class="project-name">
                    GitHub Dev Card Generator
                </div>

                <div class="project-tech">
                    Python • GitHub API
                </div>

            </div>

        </div>

        <a
            class="button"
            href="{profile_url}"
            target="_blank"
        >
            View GitHub Profile
        </a>

        <div class="footer">

            Developer profile generated
            dynamically using GitHub API.

        </div>

    </div>

</body>

</html>
"""

    # ---------------------------------------------------
    # SAVE CARD
    # ---------------------------------------------------

    file_path = os.path.join(
        CARDS_DIR,
        f"{username}.html"
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(html)

    return {
        "status": "success",
        "card_url": f"/card/{username}",
        "card_html": html,
        "profile_url": profile_url
    }

# ---------------------------------------------------
# VIEW CARD
# ---------------------------------------------------

@app.get("/card/{username}")
async def get_card(username: str):

    file_path = os.path.join(
        CARDS_DIR,
        f"{username}.html"
    )

    if not os.path.exists(file_path):

        return {
            "error": "Card not found"
        }

    return FileResponse(file_path)
