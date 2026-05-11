import os
import random
import httpx
from datetime import datetime
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

BASE_DIR = Path(__file__).resolve().parent.parent
TOKENS = os.getenv("GITHUB_TOKENS", "").split(",")

def get_random_token():
    return random.choice(TOKENS) if TOKENS and TOKENS[0] else None

@app.get("/")
async def home(): return FileResponse(BASE_DIR / "index.html")

@app.get("/api")
async def get_stats(
    username: str,
    bg: str = "050505",
    title_clr: str = "ffffff",
    text_clr: str = "888888",
    border_clr: str = "1a1a1a",
    font_size: int = 14,
    font_family: str = "Segoe UI",
    radius: int = 12,
    show_age: bool = True,
    show_repo: bool = True,
    show_lang: bool = True,
    show_commits: bool = True
):
    token = get_random_token()
    query = """
    query($login:String!){
      user(login:$login){
        createdAt
        repositories(first: 100, orderBy: {field: STARGAZERS, direction: DESC}) {
          nodes { name stargazerCount primaryLanguage { name } }
        }
        contributionsCollection { totalCommitContributions }
      }
    }
    """
    async with httpx.AsyncClient() as client:
        res = await client.post("https://api.github.com/graphql", 
                                json={'query': query, 'variables': {'login': username}}, 
                                headers={"Authorization": f"Bearer {token}"})
        data = res.json().get('data', {}).get('user')

    if not data: return {"error": "User not found"}

    # Process Stats
    stats = []
    if show_age:
        years = datetime.now().year - datetime.strptime(data['createdAt'], "%Y-%m-%dT%H:%M:%SZ").year
        stats.append(("Account Age", f"{years} Years"))
    if show_repo and data['repositories']['nodes']:
        stats.append(("Top Repo", data['repositories']['nodes'][0]['name']))
    if show_lang:
        langs = [r['primaryLanguage']['name'] for r in data['repositories']['nodes'][:5] if r['primaryLanguage']]
        top_lang = max(set(langs), key=langs.count) if langs else "None"
        stats.append(("Primary Stack", top_lang))
    if show_commits:
        stats.append(("Total Commits", data['contributionsCollection']['totalCommitContributions']))

    # Render SVG
    height = 80 + (len(stats) * 25)
    stat_elements = ""
    for i, (label, value) in enumerate(stats):
        y = 75 + (i * 25)
        stat_elements += f'<text x="25" y="{y}" class="label">{label}:</text>'
        stat_elements += f'<text x="185" y="{y}" class="value">{value}</text>'

    svg = f"""
    <svg width="450" height="{height}" viewBox="0 0 450 {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
        <style>
            .header {{ font: 700 {font_size + 4}px '{font_family}', sans-serif; fill: #{title_clr}; }}
            .label {{ font: 400 {font_size}px '{font_family}', sans-serif; fill: #{text_clr}; }}
            .value {{ font: 600 {font_size}px '{font_family}', sans-serif; fill: #{title_clr}; }}
        </style>
        <rect width="449" height="{height-1}" x="0.5" y="0.5" rx="{radius}" fill="#{bg}" stroke="#{border_clr}"/>
        <text x="25" y="40" class="header">{username}</text>
        {stat_elements}
    </svg>
    """
    return Response(content=svg, media_type="image/svg+xml")