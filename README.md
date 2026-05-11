# 📊 Stats Pro: The Ultimate Profile Architect

A high-performance, matte-black GitHub stats generator with a **Live Interactive Design Studio**. Built with FastAPI and designed for developers who want pixel-perfect control over their profile's aesthetic.

## 🚀 Live Demo
**[Build your card here →](https://github-stats-pro-seven.vercel.app/)**

## ✨ Features

*   **🎨 Triple-Color Engine:** Independent color pickers for **Username**, **Value Text**, and **Muted Labels**.
*   **⚡ Live Interactive Studio:** Real-time SVG preview with a built-in "Copy Link" tool.
*   **⚙️ 10+ Toggleable Stats:** Choose what to show:
    *   *Identity:* Account Age, Top Project, Tech Stack.
    *   *Activity:* Commits, Total Stars, PRs, Issues Closed, PR Reviews, Fork Count.
*   **📏 Precision Layout:** Dynamic SVG scaling with adjustable **Font Size** and **Border Radius**.
*   **🎯 Reset & Quick-Start:** One-click reset to a professional "Identity-only" view.

## 🛠️ Technical Stack

*   **Backend:** FastAPI (Python)
*   **Frontend:** Tailwind CSS & Vanilla JS
*   **Data:** GitHub GraphQL API (v4)
*   **Architecture:** Zero-dependency SVG rendering for maximum speed.

## 📦 Local Setup

1.  **Clone the repo:**
* `git clone [https://github.com/AJ-016/github-stats-pro.git]https://github.com/AJ-016/github-stats-pro.git)`
* `cd stats-pro`
2. **Install dependencies**:
* ```pip install -r requirements.txt```

3. **Environment Variables:**
  Create a `.env` file and add your GitHub token:
 * `GITHUB_TOKENS=your_token_here`

4. **Run the Studio**:
* `uvicorn api.index:app --reload --port 8001`

## 🛡️ Privacy & Performance

This project is built with a **local-first** philosophy. 
- **No Tracking:** We don't log your GitHub data.
- **Secure:** Your GitHub tokens are never exposed to the frontend.
- **Efficient:** Optimized for low VRAM usage and high concurrency.

## 📜 License
This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

*Built with* ♥️ *by [Alwin K J](https://github.com/AJ-016)*
