# 📊 GitHub Traffic Tracker API

A FastAPI-powered backend that fetches, stores, and serves traffic data for your GitHub repositories using the GitHub REST API. Useful for monitoring total views, unique visitors, and historical traffic over time.

---

## 🚀 Features

- ✅ Fetches traffic data (views + uniques) for GitHub repos
- 📦 Stores data in a SQLite database
- 📈 Aggregates total views and uniques per repo
- 🔁 Skips duplicate dates (avoids redundant storage)
- 🔌 RESTful API endpoints to access traffic data

---

## 🧱 Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) – modern Python web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) – ORM for database interaction
- [SQLite](https://www.sqlite.org/index.html) – lightweight local database
- [Render](https://render.com/) – deployment platform

---

## 📦 Installation

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/Github-Traffic-API.git
cd Github-Traffic-API
```

2. **Create a virtual environment:**

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Set up your environment variables:**

```bash
GITHUB_USERNAME="YOUR-USERNAME"
GITHUB_TOKEN="YOUR-PERSONAL-ACCESS-TOKEN"
PROJECT_KEY="YOUR-PROJECT-KEY" # Your personal password you create to prevent others from abusing your api
```

5. **Running Locally:**

```bash
uvicorn app.main:app --reload
```

---

## 📤 Endpoints

### `GET /traffic/{repo_name}`
Returns total views, unique visitors, and the last updated timestamp for a given repo.

**Query Parameters:**
- `repo_name`: GitHub repository name (e.g., `PortFlow`)
- `github_traffic_api_key`: Your personal password you create to prevent others from abusing your api (e.g., `12345`)

**Returns:**
```json
{
  "repo": "PortFlow",
  "total_views": 273,
  "total_uniques": 31,
  "last_updated": "2025-06-04T01:49:34.023034"
}
```
