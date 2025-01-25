import requests
import base64

class GitHubAPI:
    """Handles GitHub API requests."""
    def __init__(self, token):
        self.headers = {"Authorization": f"token {token}"}

    def fetch_readme(self, owner, repo):
        """Fetch the README content of a repository."""
        api_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
        response = requests.get(api_url, headers=self.headers)

        if response.status_code == 200:
            content_base64 = response.json().get("content", "")
            if content_base64:
                return base64.b64decode(content_base64).decode("utf-8")
        raise Exception(f"Failed to fetch README: {response.status_code}, {response.json()}")

    def fetch_repo_metadata(self, owner, repo):
        """Fetch metadata for a GitHub repository."""
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        response = requests.get(api_url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            collaborators_url = f"{api_url}/collaborators"
            collaborators = requests.get(collaborators_url, headers=self.headers).json()
            return {
                "owner": owner,
                "name": data.get("name", ""),
                "description": data.get("description", ""),
                "stars": data.get("stargazers_count", 0),
                "forks": data.get("forks_count", 0),
                "collaborators": len(collaborators),
                "url": f"https://github.com/{owner}/{repo}"
            }
        raise Exception(f"Failed to fetch repository metadata: {response.status_code}")
    
    def fetch_file_content(self, owner: str, repo: str, file_name: str) -> str:
        """Fetches file content from a GitHub repository."""
        api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_name}"
        response = requests.get(api_url, headers=self.headers)

        if response.status_code == 200:
            print(f"Successfully fetched {file_name} from {owner}/{repo}")
            content_base64 = response.json().get("content", "")
            return base64.b64decode(content_base64).decode("utf-8")
        return ""