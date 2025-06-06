# Project Setup to Track your GitHub Traffic

This project uses two branches:
- **`main`**: Contains the core API and application code.
- **`traffic-db-storage`**: Contains the up-to-date `traffic.db` SQLite database file.

---

## 🔧 Prerequisites

Make sure you have the following installed:

- Python 3.11+
- Git
- `pip` (Python package installer)
- `venv` or virtualenv (optional but recommended)

---

## 🚀 Setup Instructions

### **Fork the repository:**

Click "Fork" on the repository in GitHub

### **Clone your fork of the repository:**

```bash
git clone https://github.com/{YOUR_USERNAME}/Github-Traffic-API.git
cd Github-Traffic-API
```

### **Create branch `traffic-db-storage` with added database**

```bash
git checkout -b traffic-db-storage
touch traffic.db
git add traffic.db
git commit -m "Add traffic.db file to root"
git push -u origin traffic-db-storage
```

### **Set up your environment variables on main:**

```bash
GITHUB_USERNAME="YOUR-USERNAME"
GITHUB_TOKEN="YOUR-PERSONAL-ACCESS-TOKEN"
PROJECT_KEY="YOUR-PROJECT-KEY" # Your personal password you create to prevent others from abusing your api
```

1. Generate your personal access token

To generate a person access token go to [Settings](https://github.com/settings/profile) -> [Developer settings](https://github.com/settings/apps) -> [Personal access tokens](https://github.com/settings/tokens) -> [Tokens classic](https://github.com/settings/tokens)

Select repo permissions

2. Enable Workflow permissions

From your repo go to Settings -> Actions -> General

Scroll down to Workflow permissions and select: Read and write permissions

---

## Deploy Locally

### **Create a virtual environment:**

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### **Install dependencies:**

```bash
pip install -r requirements.txt
```

### **Running Locally:**

```bash
uvicorn app.main:app --reload
```

---

## Deploy on Render

1. Make a Free Account
2. Create a New Web Service
3. Paste the URL of the forked Public Git Repository
4. Branch: `main`
5. Build command: `pip install -r requirements.txt`
6. Start command: `bash start.sh`
7. Paste in your environment variables
