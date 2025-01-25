import requests
import base64
from typing import List, Dict
from utils.csv_writer import CSVWriter
from utils.dependency_extractor import DependencyExtractor
from api.github_api import GitHubAPI

class DependencyService:
    def __init__(self, github_api: GitHubAPI, csv_writer: CSVWriter):
        self.github_api = github_api
        self.csv_writer = csv_writer

    def analyze_dependencies(self, owner: str, repo: str, url: str):
        """Fetches and analyzes dependencies from a GitHub repository."""
        files = [
            "requirements.txt", # Python Projects
            "pyproject.toml", 
            "Pipfile",
            "pipfile.toml",
            "pipfile.lock",
            "setup.py",
            "setup.cfg",
            "environment.yml",
            "pyproject.toml",
            "package.json", # JavaScript Projects
            "package-lock.json",
            "yarn.lock",
            "webpack.config.js",
            "pnpm-lock.yaml",
            "bower.json",
            "Gemfile",  # Ruby Projects
            "Gemfile.lock",
            "composer.json",    # PHP Projects
            "composer.lock",
            "pom.xml",  # Java Projects
            "gradle.properties",
            "gradle.lockfile",
            "build.gradle",
            "build.xml",
            "build.gradle.kts", # Java and Kotlin Projects
            "settings.gradle",
            "Cargo.toml",   # Rust Projects
            "Cargo.lock",
            "packages.config", # .NET Projects
            "project.json",
            ".csproj",
            ".nuspec",
            "project.assets.json",
            "packages.lock.json",
            ".paket",
            "paket.dependencies",
            "paket.lock",
            "go.mod", # Go Projects
            "go.sum",
            "glide.lock",
            "glide.yaml",
            "gogradle.lock",
            "Gopkg.lock",
            "Godeps.lock",
            "vendor.conf",
            "CMakeLists.txt", # C/C++ Projects
            "Makefile",
            "pubspec.yaml",
            "Podfile",  # Swift Projects
            "Podfile.lock",
            "packages.swift",
            "Cartfile"
        ]

        for file_name in files:
            try:
                print(f"Fetching {file_name} from {owner}/{repo}...")
                content = self.github_api.fetch_file_content(owner, repo, file_name)

                if not content:
                    continue

                dependencies = self.extract_dependencies(file_name, content)
                
                for dep in dependencies:
                    dep["repo"] = f"{owner}/{repo}"
                    dep["url"] = url
                    dep["source_file"] = file_name
                    self.csv_writer.append_row(dep)

                print(f"Extracted dependencies from {file_name}: {len(dependencies)}")
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

    def extract_dependencies(self, file_name: str, content: str) -> List[Dict]:
        """Extracts dependencies from a given file content."""
        if file_name == "requirements.txt":
            return DependencyExtractor.parse_requirements_txt(content)
        elif file_name == "pyproject.toml":
            return DependencyExtractor.parse_pyproject_toml(content)
        elif file_name == "Pipfile":
            return DependencyExtractor.parse_pipfile(content)
        elif file_name == "pipfile.toml":
            return DependencyExtractor.parse_pipfile_toml(content)
        elif file_name == "pipfile.lock":
            return DependencyExtractor.parse_pipfile_lock(content)
        elif file_name == "setup.py":
            return DependencyExtractor.parse_setup_py(content)
        elif file_name == "setup.cfg":
            return DependencyExtractor.parse_setup_cfg(content)
        elif file_name == "environment.yml":
            return DependencyExtractor.parse_environment_yml(content)
        elif file_name == "pyproject.toml":
            return DependencyExtractor.parse_pyproject_toml(content)
        elif file_name == "package.json":
            return DependencyExtractor.parse_package_json(content)
        elif file_name == "package-lock.json":
            return DependencyExtractor.parse_package_lock_json(content)
        elif file_name == "yarn.lock":
            return DependencyExtractor.parse_yarn_lock(content)
        elif file_name == "webpack.config.js":
            return DependencyExtractor.parse_webpack_config_js(content)
        elif file_name == "pnpm-lock.yaml":
            return DependencyExtractor.parse_pnpm_lock_yaml(content)
        elif file_name == "bower.json":
            return DependencyExtractor.parse_bower_json(content)
        elif file_name == "Gemfile":
            return DependencyExtractor.parse_gemfile(content)
        elif file_name == "Gemfile.lock":
            return DependencyExtractor.parse_gemfile_lock(content)
        elif file_name == "composer.json":
            return DependencyExtractor.parse_composer_json(content)
        elif file_name == "composer.lock":
            return DependencyExtractor.parse_composer_lock_json(content)
        elif file_name == "pom.xml":
            return DependencyExtractor.parse_pom_xml(content)
        elif file_name == "gradle.properties":
            return DependencyExtractor.parse_gradle_properties(content)
        elif file_name == "gradle.lockfile":
            return DependencyExtractor.parse_gradle_lockfile(content)
        elif file_name == "build.gradle":
            return DependencyExtractor.build_gradle(content)
        elif file_name == "build.xml":
            return DependencyExtractor.parse_build_xml(content)
        elif file_name == "build.gradle.kts":
            return DependencyExtractor.build_gradle_kts(content)
        elif file_name == "settings.gradle":
            return DependencyExtractor.settings_gradle(content)
        elif file_name == "Cargo.toml":
            return DependencyExtractor.parse_cargo_toml(content)
        elif file_name == "Cargo.lock":
            return DependencyExtractor.parse_cargo_lock(content)
        elif file_name == "packages.config":
            return DependencyExtractor.parse_packages_config_json(content)
        elif file_name == "project.json":
            return DependencyExtractor.parse_project_json(content)
        elif file_name == ".csproj":
            return DependencyExtractor.parse_csproj(content)
        elif file_name == ".nuspec":
            return DependencyExtractor.parse_nuspec(content)
        elif file_name == "project.assets.json":
            return DependencyExtractor.parse_project_assets_json(content)
        elif file_name == "packages.lock.json":
            return DependencyExtractor.parse_packages_lock_json(content)
        elif file_name == ".paket":
            return DependencyExtractor.parse_paket(content)
        elif file_name == "paket.dependencies":
            return DependencyExtractor.parse_paket_dependencies(content)
        elif file_name == "paket.lock":
            return DependencyExtractor.parse_paket_lock(content)
        elif file_name == "go.mod":
            return DependencyExtractor.parse_go_mod(content)
        elif file_name == "go.sum":
            return DependencyExtractor.parse_go_sum(content)
        elif file_name == "glide.lock":
            return DependencyExtractor.parse_glide_lock(content)
        elif file_name == "glide.yaml":
            return DependencyExtractor.parse_glide_yaml(content)
        elif file_name == "gogradle.lock":
            return DependencyExtractor.parse_gogradle_lock(content)
        elif file_name == "Gopkg.lock":
            return DependencyExtractor.parse_gopkg_lock(content)
        elif file_name == "Godeps.lock":
            return DependencyExtractor.parse_godeps_lock(content)
        elif file_name == "vendor.conf":
            return DependencyExtractor.parse_vendor_conf(content)
        elif file_name == "CMakeLists.txt":
            return DependencyExtractor.parse_cmakelists_txt(content)
        elif file_name == "Makefile":
            return DependencyExtractor.parse_makefile(content)
        elif file_name == "pubspec.yaml":
            return DependencyExtractor.parse_pubsec_yaml(content)
        elif file_name == "Podfile":
            return DependencyExtractor.parse_podfile(content)
        elif file_name == "Podfile.lock":
            return DependencyExtractor.parse_podfile_lock(content)
        elif file_name == "packages.swift":
            return DependencyExtractor.parse_packages_swift(content)
        elif file_name == "Cartfile":
            return DependencyExtractor.parse_cartfile(content)
        return []