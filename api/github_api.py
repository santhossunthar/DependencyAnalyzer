import requests
import base64
from packaging import version

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
    
    def check_vulnerabilities(
            self,
            ecosystem,
            dependency_name, 
            dependency_version
        ):
        dependency_name = "@react/react-dom"
        dependency_version = "^16.8.0"
        """Check dependencies against a vulnerability database."""
        github_graphql_api = "https://api.github.com/graphql"
        query = """
        query ($name: String!, $ecosystem: SecurityAdvisoryEcosystem!) {
          securityVulnerabilities(packageName: $name, ecosystem: $ecosystem, first: 10) {
            edges {
              node {
                vulnerableVersionRange
                severity
                advisory {
                  description
                  permalink
                }
              }
            }
          }
        }
        """
        variables = {"name": dependency_name, "ecosystem": ecosystem}
        response = requests.post(
            github_graphql_api,
            headers=self.headers,
            json={"query": query, "variables": variables},
        )
        
        if response.status_code == 200:
            vulnerabilities = response.json()["data"]["securityVulnerabilities"]["edges"]
            return self.filter_vulnerabilities(vulnerabilities, dependency_version)
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return []
        
    def filter_vulnerabilities(self, vulnerabilities, dependency_version):
        """
        Filters vulnerabilities to check if the given version is affected.
        """
        vulnerable_entries = []
        for vuln in vulnerabilities:
            vuln_range = vuln["node"]["vulnerableVersionRange"]
            if self.is_version_vulnerable(dependency_version, vuln_range):
                vulnerable_entries.append(
                    {
                        "vulnerable_version_range": vuln_range,
                        "severity": vuln["node"]["severity"],
                        "advisory_link": vuln["node"]["advisory"]["permalink"],
                        "description": vuln["node"]["advisory"]["description"],
                    }
                )
        return vulnerable_entries

    def is_version_vulnerable(self, dependency_version, vulnerable_range):
        """
        Checks if a specific version falls within the vulnerable version range.
        """
        # Example: "^4.1.0" means >= 4.1.0 and < 5.0.0
        # Use `packaging.version` for precise version handling
        try:
            if " " in vulnerable_range:  # Handle ranges like ">1.0.0 <2.0.0"
                conditions = vulnerable_range.split(" ")
                for condition in conditions:
                    if not self.satisfies_condition(dependency_version, condition):
                        return False
                return True
            else:
                return self.satisfies_condition(dependency_version, vulnerable_range)
        except Exception as e:
            print(f"Error parsing range {vulnerable_range}: {e}")
            return False

    def satisfies_condition(self, dependency_version, condition):
        """
        Parses and checks individual conditions.
        """
        operator, ref_version = condition[:2], condition[2:]
        if operator not in (">=", "<=", ">", "<", "==", "^", "~"):
            operator, ref_version = condition[0], condition[1:]
        if operator == "^":
            # Handle caret (^) as a special case
            major_version = version.parse(ref_version).major
            upper_bound = f"{major_version + 1}.0.0"
            return version.parse(ref_version) <= version.parse(dependency_version) < version.parse(upper_bound)
        elif operator == "~":
            # Handle tilde (~) as a special case
            ref_version_parts = ref_version.split(".")
            upper_bound = f"{ref_version_parts[0]}.{int(ref_version_parts[1]) + 1}.0"
            return version.parse(ref_version) <= version.parse(dependency_version) < version.parse(upper_bound)
        else:
            # Other operators
            return eval(f"version.parse(dependency_version) {operator} version.parse(ref_version)")

