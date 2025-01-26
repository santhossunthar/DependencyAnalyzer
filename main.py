from api.github_api import GitHubAPI
from utils.csv_writer import CSVWriter
from services.repository_service import RepositoryService
from services.dependency_service import DependencyService
from services.vulnerability_service import VulnerabilityService
from dotenv import load_dotenv
import csv
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

    elif len(arguments) == 2 and arguments[1] == "-d":
        repository_metadata_csv = "repository_metadata.csv"
        dependency_csv = "dependencies.csv"
        headers = [
            "repo", 
            "url",
            "source_file",
            "ecosystem",
            "name",
            "operator", 
            "version", 
        ]
        csv_writer = CSVWriter(dependency_csv, headers)
        dependency_service = DependencyService(github_api, csv_writer)

        # Read repository list from input CSV
        try:
            with open(repository_metadata_csv, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    owner, repo = row.get("owner"), row.get("name")  
                    url = row.get("url")

                    if owner and repo:
                        dependency_service.analyze_dependencies(owner, repo, url)
            print(f"Dependency information successfully written to {dependency_csv}")
        except Exception as e:
            print(f"Error: {e}")

    elif len(arguments) == 2 and arguments[1] == "-v":
        dependencies_csv = "dependencies.csv"
        vulnerabilities_csv = "vulnerabilities.csv"
        headers = [
            "repo", 
            "ecosystem", 
            "source_file", 
            "name", 
            "version", 
            "severity", 
            "advisory", 
            "url"
        ]
        csv_writer = CSVWriter(vulnerabilities_csv, headers)
        vulnerability_service = VulnerabilityService(github_api, csv_writer)
        
        try:
            with open(dependencies_csv, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    repo, ecosystem, source_file, name, version = row.get("repo"), \
                        row.get("ecosystem"), row.get("source_file"), \
                        row.get("name"), row.get("version")
                    vulnerability_service.process(repo, ecosystem, source_file, name, version)
                    break
            print(f"Vulnerability information successfully written to {vulnerabilities_csv}")
        except Exception as e:
            print(f"Error: {e}")