from utils.url_parser import URLParser
from api.github_api import GitHubAPI
from utils.csv_writer import CSVWriter

class RepositoryService:
    def __init__(self, github_api: GitHubAPI, csv_writer: CSVWriter):
        self.github_api = github_api
        self.csv_writer = csv_writer

    def process(self, repo_url):
        """Main process to extract and save repository data."""
        owner, repo = repo_url.rstrip("/").split("/")[-2:]
        print(f"Fetching README for {repo_url}...")
        readme_content = self.github_api.fetch_readme(owner, repo)

        print("Extracting repository URLs...")
        repo_urls = URLParser.extract_github_urls(readme_content)
        print(f"Found {len(repo_urls)} repositories.")

        for url in repo_urls:
            owner, repo = url.rstrip("/").split("/")[-2:]
            try:
                metadata = self.github_api.fetch_repo_metadata(owner, repo)
                self.csv_writer.append_row(metadata)
                print(f"Appended data for repository: {metadata['name']}")
            except Exception as e:
                print(f"Error fetching metadata for {url}: {e}")