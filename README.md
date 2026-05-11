# 📊 GitHub Stats Pro

A high-performance, customizable GitHub statistics generator with a focus on dark, matte aesthetics. Built with FastAPI and powered by GitHub GraphQL API.

<hr style="border: none; border-top: 1px solid #444;">


## 🚀 Features
* **Customizable UI:** Change colors, fonts, and sizes via a live dashboard.
* **Dynamic Stats:** Toggle Account Age, Top Repo, Primary Stack, and more.
* **Local-First:** Optimized for privacy and speed.
* **Vercel Ready:** One-click deployment.

<hr style="border: none; border-top: 1px solid #444;">

## 🛠️ Setup
1. Clone the repo.
2. Install dependencies: `pip install -r requirements.txt`
3. Add your `GITHUB_TOKENS` to a `.env` file.
4. Run locally: `uvicorn api.index:app --reload --port 8001`

<hr style="border: none; border-top: 1px solid #444;">

## 🎨 Usage
Simply use the generated Markdown link in your profile:
`![Stats](https://your-app.vercel.app/api?username=AJ-016&theme=matte)`

Created with ❤️ by ALWIN K J