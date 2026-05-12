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
    bg: str = "050505", border_clr: str = "1a1a1a",
    user_clr: str = "3b82f6", title_clr: str = "ffffff", text_clr: str = "888888",
    font_size: int = 14, radius: int = 12,
    transparent: bool = False,  # New Parameter
    s_age: bool = True, s_repo: bool = True, s_lang: bool = True,
    s_commits: bool = True, s_stars: bool = True, s_prs: bool = True,
    s_issues: bool = True, s_reviews: bool = True, s_forks: bool = True,
    l_age: str = "Account Age", l_repo: str = "Top Repo", l_lang: str = "Stack",
    l_commits: str = "Commits", l_stars: str = "Stars", l_prs: str = "PRs",
    l_issues: str = "Issues", l_reviews: str = "Reviews", l_forks: str = "Forks"
):
    token = get_random_token()
    query = """query($login:String!){user(login:$login){createdAt pullRequests(first:1){totalCount}issues(states:CLOSED){totalCount}contributionsCollection{totalCommitContributions totalPullRequestReviewContributions}repositories(first:100,orderBy:{field:STARGAZERS,direction:DESC}){nodes{name stargazerCount forkCount primaryLanguage{name}}}}}"""
    
    async with httpx.AsyncClient() as client:
        res = await client.post("https://api.github.com/graphql", json={'query': query, 'variables': {'login': username}}, headers={"Authorization": f"Bearer {token}"})
        data = res.json().get('data', {}).get('user')

    if not data: return {"error": "User not found"}

    stats = []
    if s_age:
        yrs = datetime.now().year - datetime.strptime(data['createdAt'], "%Y-%m-%dT%H:%M:%SZ").year
        stats.append((l_age, f"{yrs} Years"))
    if s_repo and data['repositories']['nodes']:
        stats.append((l_repo, data['repositories']['nodes'][0]['name']))
    if s_lang:
        langs = list(set([r['primaryLanguage']['name'] for r in data['repositories']['nodes'] if r['primaryLanguage']]))[:2]
        stats.append((l_lang, ", ".join(langs)))
    if s_commits: stats.append((l_commits, data['contributionsCollection']['totalCommitContributions']))
    if s_stars: stats.append((l_stars, sum(r['stargazerCount'] for r in data['repositories']['nodes'])))
    if s_prs: stats.append((l_prs, data['pullRequests']['totalCount']))
    if s_issues: stats.append((l_issues, data['issues']['totalCount']))
    if s_reviews: stats.append((l_reviews, data['contributionsCollection']['totalPullRequestReviewContributions']))
    if s_forks: stats.append((l_forks, sum(r['forkCount'] for r in data['repositories']['nodes'])))

    max_label_w = max([len(str(x[0])) for x in stats]) * (font_size * 0.6) if stats else 100
    width = max(460, max_label_w + 250)
    height = 95 + (len(stats) * 30)

    # Transparency Logic
    bg_fill = "none" if transparent else f"#{bg}"
    
    rows = "".join([f'<text x="30" y="{90 + (i * 30)}" class="label">{l}:</text><text x="{max_label_w + 60}" y="{90 + (i * 30)}" class="val">{v}</text>' for i, (l, v) in enumerate(stats)])

    return Response(content=f"""
    <svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
        <style>
            .user {{ font: 900 {font_size + 8}px 'Segoe UI', sans-serif; fill: #{user_clr}; }}
            .label {{ font: 400 {font_size}px 'Segoe UI', sans-serif; fill: #{text_clr}; }}
            .val {{ font: 600 {font_size}px 'Segoe UI', sans-serif; fill: #{title_clr}; }}
        </style>
        <rect width="{width-1}" height="{height-1}" x="0.5" y="0.5" rx="{radius}" fill="{bg_fill}" stroke="#{border_clr}"/>
        <text x="30" y="50" class="user">{username.upper()}</text>
        {rows}
    </svg>
    """, media_type="image/svg+xml")