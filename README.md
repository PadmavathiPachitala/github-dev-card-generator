# GitHub Dev Card Generator

<img width="1025" height="904" alt="Screenshot (284)" src="https://github.com/user-attachments/assets/46f85d57-d51a-4292-8dcb-b855e3746535" />


Generate beautiful, shareable developer profile cards from any GitHub username — instantly.

![GitHub Dev Cards](https://img.shields.io/badge/Built%20with-FastAPI%20%7C%20Google%20ADK%20%7C%20MCP-blue)

##🌐 Live Deployment

🔗 Frontend Web App : https://github-card-frontend-498970929990.us-central1.run.app

⚙️ Backend API Service : https://github-card-backend-498970929990.us-central1.run.app

## Overview

A full-stack web app that fetches a GitHub user's public profile data and renders it as a styled HTML developer card. Cards are served via a FastAPI backend, displayed in the browser via an iframe, and can be shared via a direct link or QR code.

## Features

- Enter any GitHub username and generate a profile card in seconds
- Displays avatar, name, bio, location, follower count, and public repo count
- Skeleton loading animation while the card is being generated
- Share via direct link or scannable QR code
- Cards are saved as static HTML files and served at `/card/{username}`
- MCP server with tools for scraping, analyzing, and generating cards programmatically
- Google ADK agent integration for AI-powered profile analysis

## Tech Stack

| Layer    | Technology                        |
|----------|-----------------------------------|
| Frontend | HTML, CSS, Vanilla JS, Nginx      |
| Backend  | Python, FastAPI, Uvicorn          |
| AI/Agent | Google ADK, Gemini 1.5 Flash      |
| MCP      | MCP SDK (`mcp[fastmcp]`)          |
| HTTP     | httpx, requests                   |
| Infra    | Docker, Docker Compose            |

## Project Structure

```
github-card-generator/
├── backend/
│   ├── main.py          # FastAPI app — /generate and /card/{username} endpoints
│   ├── agent.py         # Google ADK agent definition
│   ├── mcp_server.py    # MCP server with scrape/analyze/generate/save tools
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html       # Single-page UI
│   └── Dockerfile       # Nginx-based static server
├── docker-compose.yml
├── .env.example
└── preview.html         # Standalone preview page
```

## Getting Started

### Prerequisites

- Docker & Docker Compose
- A GitHub personal access token (optional, increases API rate limits)
- A Google API key (for ADK/Gemini features)

### Setup

1. Clone the repo and navigate into it:
   ```bash
   git clone <repo-url>
   cd github-card-generator
   ```

2. Copy the example env file and fill in your keys:
   ```bash
   cp .env.example .env
   ```

   ```env
   GITHUB_TOKEN=<your_github_token>
   GOOGLE_API_KEY=<your_google_api_key>
   GEMINI_MODEL=gemini-2.5-flash
   ```

3. Start the services:
   ```bash
   docker compose up --build
   ```

4. Open your browser at `http://localhost` and enter a GitHub username.

### Running the Backend Locally (without Docker)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8080
```

## API Endpoints

| Method | Endpoint            | Description                        |
|--------|---------------------|------------------------------------|
| GET    | `/`                 | Health check                       |
| POST   | `/generate`         | Generate a card for a username     |
| GET    | `/card/{username}`  | Serve the saved card HTML          |

### POST `/generate`

Request:
```json
{ "username": "torvalds" }
```

Response:
```json
{
  "status": "success",
  "card_url": "/card/torvalds",
  "card_html": "...",
  "profile_url": "https://github.com/torvalds"
}
```

## MCP Server Tools

The MCP server (`mcp_server.py`) exposes four tools for agent-driven workflows:

| Tool               | Description                                      |
|--------------------|--------------------------------------------------|
| `scrape_github`    | Fetch profile + top repos + language stats       |
| `analyze_profile`  | Generate developer vibe, skills, and card theme  |
| `generate_card_html` | Render a themed HTML card string               |
| `save_card`        | Save the HTML card to `static/cards/`            |

## Environment Variables

| Variable        | Description                          |
|-----------------|--------------------------------------|
| `GITHUB_TOKEN`  | GitHub PAT for higher API rate limits |
| `GOOGLE_API_KEY`| Google API key for Gemini/ADK        |
| `GEMINI_MODEL`  | Gemini model name (default: `gemini-2.5-flash`) |
| `BACKEND_URL`   | Backend URL injected into the frontend at runtime |
