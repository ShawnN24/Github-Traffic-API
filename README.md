# 📊 GitHub Traffic Tracker API

A FastAPI backend service that fetches, stores, and serves traffic data for your GitHub repositories using the GitHub REST API. Useful for monitoring total views, unique visitors, and historical traffic over time.

---

## 🚀 Features

- ✅ Fetches traffic data (views + uniques) for GitHub repos
- 📦 Stores data in a SQLite database
- 📈 Aggregates total views and uniques per repo
- 🔌 RESTful API endpoints to access traffic data (lifetime views, lifetime uniques, and timeline)

---

## 🧱 Tech Stack

- [Python](https://www.python.org/) – Language
- [FastAPI](https://fastapi.tiangolo.com/) – Web Framework
- [SQLAlchemy](https://www.sqlalchemy.org/) – ORM
- [SQLite](https://www.sqlite.org/index.html) – Database
- [Render](https://render.com/) – Deployment

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

### `GET /timeline/{repo_name}`
Returns a timeline of views, unique visitors, and dates for a given repo.

**Query Parameters:**
- `repo_name`: GitHub repository name (e.g., `PortFlow`)
- `github_traffic_api_key`: Your personal password you create to prevent others from abusing your api (e.g., `12345`)

**Returns:**
```json
[
  {
    "date": "2025-05-21",
    "views": 40,
    "uniques": 2
  },
  {
    "date": "2025-05-22",
    "views": 116,
    "uniques": 8
  },
  {
    "date": "2025-05-23",
    "views": 13,
    "uniques": 3
  }
]
```
