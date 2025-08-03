import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")

def main(repo_name: str, private: bool = True, description: str = "Repo created by Claude GitOps Assistant"):
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": repo_name,
        "private": private,
        "auto_init": True,
        "description": description
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 201:
            return {
                "status": "success",
                "repo_url": response.json()["html_url"]
            }
        else:
            return {
                "status": "error",
                "message": f"Failed to create repo: {response.status_code}",
                "details": response.json()
            }
    except Exception as e:
        return {
            "status": "error",
            "message": "Exception occurred",
            "details": str(e)
        }
