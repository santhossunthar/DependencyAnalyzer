from api.github_api import GitHubAPI
from utils.csv_writer import CSVWriter
from services.repository_service import RepositoryService
from dotenv import load_dotenv
import sys
import os

load_dotenv()

if __name__ == "__main__":
    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", None)
    github_api = GitHubAPI(token=GITHUB_TOKEN)
    arguments = sys.argv

    if len(arguments) >= 3 or len(arguments) == 1:
        print("""\nPlease select the following options:
              \n-r -> Repository Search\n-d -> Dependency Search
              """)
    elif len(arguments) == 2 and arguments[1] == "-r":    
        github_repo_url = input("Enter the GitHub repository URL: ").strip()
        repository_metadata_csv = "repository_metadata.csv"
        headers=[
            "owner",
            "name", 
            "description", 
            "stars", 
            "forks", 
            "collaborators", 
            "url"
        ]
        csv_writer = CSVWriter(repository_metadata_csv, headers)
        repository_service = RepositoryService(github_api, csv_writer)

        try:
            repository_service.process(github_repo_url)
            print(f"Repository information successfully written to {repository_metadata_csv}")
        except Exception as e:
            print(f"Error: {e}")