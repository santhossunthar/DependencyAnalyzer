import os
import requests
import json
import csv
from dotenv import load_dotenv

load_dotenv()

# Function to fetch known vulnerabilities from the GitHub Advisory Database
def fetch_vulnerabilities(repo, ecosystem, dependency_name):
    token = os.getenv("GITHUB_TOKEN")
    url = f"https://api.github.com/graphql"
    query = """
    query ($package: String!, $ecosystem: SecurityAdvisoryEcosystem!) {
        securityVulnerabilities(first: 10, ecosystem: $ecosystem, package: $package) {
            edges {
                node {
                    advisory {
                        description
                    }
                    severity
                    vulnerableVersionRange
                }
            }
        }
    }
    """
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        url, 
        json={"query": query, "variables": {"package": dependency_name, "ecosystem": ecosystem}}, 
        headers=headers
    )

    if response.status_code == 200:
        data = response.json()
        vulnerabilities = data.get('data', {}).get('securityVulnerabilities', {}).get('edges', [])
        
        if vulnerabilities:
            output_dir = f"projects/vulns/{repo}/{ecosystem}"
            os.makedirs(output_dir, exist_ok=True)
            file_path = os.path.join(output_dir, f"{dependency_name.replace('/', '_')}_vulns.json")

            vulns_data = []
            for vuln in vulnerabilities:
                vuln_data = vuln['node']
                vulns_data.append({
                    "description": vuln_data['advisory']['description'],
                    "severity": vuln_data['severity'],
                    "vulnerableVersionRange": vuln_data['vulnerableVersionRange']
                })
            
            with open(file_path, 'w') as json_file:
                json.dump(vulns_data, json_file, indent=4)
            
            print(f"Vulnerabilities for {dependency_name} saved to {file_path}")
        else:
            print(f"No vulnerabilities found for {dependency_name}")
    else:
        print(f"Error querying the API: {response.status_code}")

repo = "repo/name".replace("/", "_")

with open(f'projects/deps/{repo}/{repo}_deps.csv', newline='') as csvfile:
    dependencies = csv.reader(csvfile)
    for row in dependencies:
        ecosystem = row[0]
        dependency_name = row[1]
        version_in_use = row[2]
        vulnerabilities = fetch_vulnerabilities(repo, ecosystem, dependency_name)
