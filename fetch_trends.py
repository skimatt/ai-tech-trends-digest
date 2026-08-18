#!/usr/bin/env python3
"""
AI & Tech Trends Automated Digest Generator
Maintained by @skimatt (Rahmat Mulia)
Fetches trending AI repositories, Hugging Face models, and engineering releases.
"""

import os
import json
import datetime
import requests

GITHUB_API = "https://api.github.com"
HUGGINGFACE_API = "https://huggingface.co/api/models"

def get_headers():
    token = os.environ.get("GITHUB_TOKEN")
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "AI-Tech-Trends-Digest/1.0"
    }
    if token:
        headers["Authorization"] = f"token {token}"
    return headers

def fetch_trending_ai_repos():
    """Fetch top trending AI / LLM repositories on GitHub."""
    print("Fetching trending GitHub AI repositories...")
    today = datetime.date.today()
    pushed_recent = today - datetime.timedelta(days=14)
    query = f"ai OR llm OR 'artificial intelligence' stars:>500 pushed:>{pushed_recent.isoformat()}"
    url = f"{GITHUB_API}/search/repositories?q={query}&sort=stars&order=desc&per_page=6"
    
    try:
        res = requests.get(url, headers=get_headers(), timeout=15)
        if res.status_code == 200:
            items = res.json().get("items", [])
            repos = []
            for item in items:
                repos.append({
                    "name": item.get("full_name"),
                    "url": item.get("html_url"),
                    "description": item.get("description") or "No description provided.",
                    "stars": item.get("stargazers_count", 0),
                    "forks": item.get("forks_count", 0),
                    "language": item.get("language") or "General",
                    "topics": item.get("topics", [])[:4]
                })
            return repos
        else:
            print(f"GitHub API returned {res.status_code}: {res.text}")
    except Exception as e:
        print(f"Error fetching GitHub repos: {e}")
    
    # Fallback to general top AI repos if search rate-limited
    return [
        {
            "name": "huggingface/transformers",
            "url": "https://github.com/huggingface/transformers",
            "description": "State-of-the-art Machine Learning for Pytorch, TensorFlow, and JAX.",
            "stars": 135000,
            "forks": 26000,
            "language": "Python",
            "topics": ["ai", "transformers", "nlp", "llm"]
        },
        {
            "name": "vllm-project/vllm",
            "url": "https://github.com/vllm-project/vllm",
            "description": "A high-throughput and memory-efficient inference and serving engine for LLMs.",
            "stars": 38000,
            "forks": 5400,
            "language": "Python",
            "topics": ["llm", "inference", "gpu", "ai"]
        }
    ]

def fetch_trending_hf_models():
    """Fetch top trending AI models from Hugging Face."""
    print("Fetching trending Hugging Face models...")
    params = {
        "sort": "trendingScore",
        "direction": "-1",
        "limit": 6
    }
    try:
        res = requests.get(HUGGINGFACE_API, params=params, timeout=15)
        if res.status_code == 200:
            items = res.json()
            models = []
            for item in items:
                model_id = item.get("id") or item.get("modelId")
                models.append({
                    "id": model_id,
                    "url": f"https://huggingface.co/{model_id}",
                    "downloads": item.get("downloads", 0),
                    "likes": item.get("likes", 0),
                    "pipeline_tag": item.get("pipeline_tag") or "text-generation"
                })
            return models
    except Exception as e:
        print(f"Error fetching HF models: {e}")
        
    return [
        {"id": "meta-llama/Llama-3.3-70B-Instruct", "url": "https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct", "downloads": 500000, "likes": 4200, "pipeline_tag": "text-generation"},
        {"id": "deepseek-ai/DeepSeek-V3", "url": "https://huggingface.co/deepseek-ai/DeepSeek-V3", "downloads": 320000, "likes": 6100, "pipeline_tag": "text-generation"}
    ]

def generate_markdown(repos, models, now_str):
    """Generate Markdown content for README and Digest."""
    date_display = datetime.datetime.utcnow().strftime("%d %B %Y, %H:%M UTC")
    
    md = f"""# 🤖 AI & Tech Trends Automated Digest

[![Auto-Update Digest](https://github.com/skimatt/ai-tech-trends-digest/actions/workflows/digest-cron.yml/badge.svg)](https://github.com/skimatt/ai-tech-trends-digest/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Maintained by](https://img.shields.io/badge/Maintained%20by-@skimatt-00C2FF?style=flat-square&logo=github)](https://github.com/skimatt)
[![Update Cadence](https://img.shields.io/badge/Cadence-Every%202%20Days-38ef7d?style=flat-square&logo=clock)](https://github.com/skimatt/ai-tech-trends-digest)

> 🚀 **An automated intelligence radar tracking high-growth AI repositories, state-of-the-art Hugging Face models, and modern full-stack development trends.**
> 
> *Generated automatically via GitHub Actions every 2 days.*

---

## 📅 Latest Snapshot: `{date_display}`

### 🔥 Top Trending Open-Source AI Repositories
Repositories gaining high momentum across the open-source developer ecosystem:

| Repository | Stars | Language | Key Focus & Topics |
| :--- | :---: | :---: | :--- |
"""
    for r in repos:
        topics_badges = " ".join([f"`{t}`" for t in r["topics"]]) if r["topics"] else "`ai`"
        md += f"| **[{r['name']}]({r['url']})**<br>*{r['description'][:95]}...* | ⭐ {r['stars']:,} | `{r['language']}` | {topics_badges} |\n"

    md += """
---

### 🧠 Trending Hugging Face Models
State-of-the-art architectures and checkpoints trending on Hugging Face:

| Model Identifier | Primary Task | Community Likes | Direct Link |
| :--- | :---: | :---: | :---: |
"""
    for m in models:
        md += f"| **`{m['id']}`** | `{m['pipeline_tag']}` | ❤️ {m['likes']:,} | [Inspect Model →]({m['url']}) |\n"

    md += f"""
---

### 🛠️ Ecosystem Watch: Core Frameworks & Tooling

| Ecosystem | Focus Area | Latest Tracked Highlight |
| :--- | :--- | :--- |
| **Next.js / React** | Full-Stack & SSR | React 19 Server Actions, Turbopack optimizations, Partial Prerendering (PPR) |
| **Python & AI Agents** | Agentic Workflows | Multi-agent orchestration, LangGraph, vLLM acceleration, Ollama local runners |
| **PHP / Laravel** | Web Services & APIs | Modern Laravel 11 architectures, Octane concurrency, dynamic RBAC integrations |
| **TypeScript / Node** | Cloud Infrastructure | Bun & Node.js 22 LTS runtime performance, typed OpenAPI generation |

---

## 📂 Historical Archives

All bi-daily snapshots are automatically versioned and archived inside the [`/digests`](./digests) directory.

---

### 👤 Curator
Curated and automated with precision by **[Rahmat Mulia (skimatt)](https://github.com/skimatt)**  
*Full-Stack Developer · AI Systems & Automation Architect*  
Portfolio: [rm.freedev.app](https://rm.freedev.app/) · GitHub: [@skimatt](https://github.com/skimatt)
"""
    return md

def main():
    now = datetime.datetime.utcnow()
    date_str = now.strftime("%Y-%m-%d")
    now_str = now.strftime("%Y-%m-%d %H:%M:%S UTC")
    
    print(f"Starting AI & Tech Trends Digest for {date_str}...")
    
    repos = fetch_trending_ai_repos()
    models = fetch_trending_hf_models()
    
    markdown_content = generate_markdown(repos, models, now_str)
    
    # 1. Update root README.md
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(markdown_content)
    print("Updated root README.md successfully.")
    
    # 2. Save historical archive
    os.makedirs("digests", exist_ok=True)
    archive_path = os.path.join("digests", f"digest-{date_str}.md")
    with open(archive_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    print(f"Saved archive digest to {archive_path}.")

if __name__ == "__main__":
    main()
