import re
import json
import yaml
import tomli
import xml.etree.ElementTree as ET
from typing import List, Dict

class DependencyExtractor:
    @staticmethod
    def parse_requirements_txt(content: str) -> List[Dict]:
        """Parses a requirements.txt file content."""
        dependencies = []
        for line in content.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):  # Ignore comments
                match = re.match(r"([a-zA-Z0-9\-_.]+)([<>=!~]*)(.*)", line)
                if match:
                    name, operator, version = match.groups()
                    dependencies.append({
                        "name": name,
                        "operator": operator or "",
                        "version": version or "",
                    })
        return dependencies

    @staticmethod
    def parse_pyproject_toml(content: str) -> List[Dict]:
        """Parses a pyproject.toml file content."""
        dependencies = []
        try:
            data = tomli.loads(content)
            deps = data.get("tool", {}).get("poetry", {}).get("dependencies", {})
            for dep, version in deps.items():
                if isinstance(version, str):
                    dependencies.append({"name": dep, "operator": "==", "version": version})
                elif isinstance(version, dict):
                    dependencies.append({"name": dep, "operator": ">=", "version": version.get("min", "")})
        except tomli.TomlDecodeError:
            pass
        return dependencies

    @staticmethod
    def parse_pipfile(content: str) -> List[Dict]:
        """Parses a Pipfile content."""
        dependencies = []
        try:
            data = tomli.loads(content)
            for dep, version in data.get("packages", {}).items():
                dependencies.append({"name": dep, "operator": "==", "version": version})
        except tomli.TomlDecodeError:
            pass
        return dependencies
    
    @staticmethod
    def parse_pipfile_toml(content: str) -> List[Dict]:
        """Parses a Pipfile.toml file content."""
        dependencies = []
        try:
            data = tomli.loads(content)
            for dep, version in data.get("packages", {}).items():
                dependencies.append({"name": dep, "operator": "==", "version": version})
        except tomli.TomlDecodeError:
            pass
        return dependencies
    
    @staticmethod
    def parse_pipfile_lock(content: str) -> List[Dict]:
        """Parses a Pipfile.lock file content."""
        dependencies = []
        try:
            data = json.loads(content)
            for dep, info in data.get("_meta", {}).get("requires", {}).items():
                dependencies.append({"name": dep, "operator": "==", "version": info.get("version", "")})
        except json.JSONDecodeError:
            pass
        return dependencies
    
    @staticmethod
    def parse_setup_py(content: str) -> List[Dict]:
        """Parses a setup.py file content."""
        dependencies = []
        for match in re.finditer(r"install_requires=\[(.*?)\]", content):
            for dep in match.group(1).split(","):
                dep = dep.strip().strip("'").strip('"')
                dependencies.append({"name": dep, "operator": "", "version": ""})
        return dependencies
    
    @staticmethod
    def parse_setup_cfg(content: str) -> List[Dict]:
        """Parses a setup.cfg file content."""
        dependencies = []
        for match in re.finditer(r"install_requires = (.*?)\n", content):
            for dep in match.group(1).split(","):
                dep = dep.strip().strip("'").strip('"')
                dependencies.append({"name": dep, "operator": "", "version": ""})
        return dependencies
    
    @staticmethod
    def parse_environment_yml(content: str) -> List[Dict]:
        """Parses a environment.yml file content."""
        dependencies = []
        try:
            data = yaml.safe_load(content)
            deps = data.get("dependencies", [])
            for dep in deps:
                if isinstance(dep, str):
                    dependencies.append({"name": dep, "operator": "", "version": ""})
                elif isinstance(dep, dict):
                    for name, version in dep.items():
                        dependencies.append({"name": name, "operator": "", "version": version})
        except yaml.YAMLError:
            pass
        return dependencies
    
    @staticmethod
    def parse_pyproject_toml(content: str) -> List[Dict]:
        """Parses a pyproject.toml file content."""
        dependencies = []
        try:
            data = tomli.loads(content)
            deps = data.get("tool", {}).get("poetry", {}).get("dependencies", {})
            for dep, version in deps.items():
                dependencies.append({"name": dep, "operator": "==", "version": version})
        except tomli.TomlDecodeError:
            pass
        return dependencies

    @staticmethod
    def parse_package_json(content: str) -> List[Dict]:
        """Parses a package.json file content."""
        dependencies = []
        try:
            data = json.loads(content)
            deps = data.get("dependencies", {})
            for dep, version in deps.items():
                dependencies.append({"name": dep, "operator": "", "version": version})
        except json.JSONDecodeError:
            pass
        return dependencies
    
    @staticmethod
    def parse_package_lock_json(content: str) -> List[Dict]:
        """Parses a package-lock.json file content."""
        dependencies = []
        try:
            data = json.loads(content)
            deps = data.get("dependencies", {})
            for dep, info in deps.items():
                dependencies.append({"name": dep, "operator": "", "version": info.get("version", "")})
        except json.JSONDecodeError:
            pass
        return dependencies
    
    @staticmethod
    def parse_yarn_lock(content: str) -> List[Dict]:
        """Parses a yarn.lock file content."""
        dependencies = []
        for line in content.splitlines():
            parts = line.split("@")
            if len(parts) >= 2:
                name, version = parts[0], parts[1]
                dependencies.append({"name": name, "operator": "", "version": version})
        return dependencies
    
    @staticmethod
    def parse_webpack_config_js(content: str) -> List[Dict]:
        """Parses a webpack.config.js file content."""
        dependencies = []
        for match in re.finditer(r"require\(['\"](.+?)['\"]\)", content):
            name = match.group(1)
            dependencies.append({"name": name, "operator": "", "version": ""})
        return dependencies
    
    @staticmethod
    def parse_pnpm_lock_yaml(content: str) -> List[Dict]:
        """Parses a pnpm-lock.yaml file content."""
        dependencies = []
        try:
            data = yaml.safe_load(content)
            for dep, info in data.get("packages", {}).items():
                dependencies.append({"name": dep, "operator": "", "version": info.get("version", "")})
        except yaml.YAMLError:
            pass
        return dependencies
    
    @staticmethod
    def parse_bower_json(content: str) -> List[Dict]:
        """Parses a bower.json file content."""
        dependencies = []
        try:
            data = json.loads(content)
            deps = data.get("dependencies", {})
            for dep, version in deps.items():
                dependencies.append({"name": dep, "operator": "", "version": version})
        except json.JSONDecodeError:
            pass
        return dependencies

    @staticmethod
    def parse_gemfile(content: str) -> List[Dict]:
        """Parses a Gemfile content."""
        dependencies = []
        for line in content.splitlines():
            line = line.strip()
            match = re.match(r"gem ['\"](.+?)['\"],\s*['\"](.+?)['\"]", line)
            if match:
                name, version = match.groups()
                dependencies.append({"name": name, "operator": "==", "version": version})
        return dependencies
    
    @staticmethod
    def parse_gemfile_lock(content: str) -> List[Dict]:
        """Parses a Gemfile.lock content."""
        dependencies = []
        for match in re.finditer(r"    (.+?) \((.+?)\)", content):
            name, version = match.groups()
            dependencies.append({"name": name, "operator": "==", "version": version})
        return dependencies
    
    @staticmethod
    def parse_composer_json(content: str) -> List[Dict]:
        """Parses a composer.json file content."""
        dependencies = []
        try:
            data = json.loads(content)
            deps = data.get("require", {})
            for dep, version in deps.items():
                dependencies.append({"name": dep, "operator": "==", "version": version})
        except json.JSONDecodeError:
            pass
        return dependencies

    @staticmethod
    def parse_composer_lock(content: str) -> List[Dict]:
        """Parses a composer.lock file content."""
        dependencies = []
        try:
            data = json.loads(content)
            packages = data.get("packages", [])
            for package in packages:
                name = package.get("name", "")
                version = package.get("version", "")
                dependencies.append({"name": name, "operator": "==", "version": version})
        except json.JSONDecodeError:
            pass
        return dependencies

    @staticmethod
    def parse_pom_xml(content: str) -> List[Dict]:
        """Parses a pom.xml file content."""
        dependencies = []
        root = ET.fromstring(content)
        for dep in root.findall(".//dependency"):
            name = dep.findtext("artifactId")
            version = dep.findtext("version")
            dependencies.append({"name": name, "operator": "==", "version": version})
        return dependencies

    @staticmethod
    def parse_gradle_properties(content: str) -> List[Dict]:
        """Parses a gradle.properties file content."""
        dependencies = []
        for match in re.finditer(r"^(.+)=(.+)$", content, re.MULTILINE):
            name, version = match.groups()
            dependencies.append({"name": name, "operator": "", "version": version})
        return dependencies
    
    @staticmethod
    def parse_gradle_lockfile(content: str) -> List[Dict]:
        """Parses a gradle.lockfile content."""
        dependencies = []
        try:
            data = json.loads(content)
            for dep, info in data.get("dependencies", {}).items():
                dependencies.append({"name": dep, "operator": "", "version": info.get("version", "")})
        except json.JSONDecodeError:
            pass
        return dependencies

    @staticmethod
    def build_gradle(content: str) -> List[Dict]:
        """Parses a build.gradle file content."""
        dependencies = []
        for match in re.finditer(r"implementation ['\"](.*?):(.*?)['\"]", content):
            group, name = match.groups()
            dependencies.append({"name": f"{group}:{name}", "operator": "", "version": ""})
        return dependencies

    @staticmethod
    def parse_build_xml(content: str) -> List[Dict]:
        """Parses a build.xml file content."""
        dependencies = []
        for match in re.finditer(r"ivy-module name=['\"](.*?)['\"]", content):
            name = match.group(1)
            dependencies.append({"name": name, "operator": "", "version": ""})
        return dependencies
    
    @staticmethod
    def build_gradle_kts(content: str) -> List[Dict]:
        """Parses a build.gradle.kts file content."""
        dependencies = []
        for match in re.finditer(r"implementation[(]['\"](.*?):(.*?)['\"]", content):
            group, name = match.groups()
            dependencies.append({"name": f"{group}:{name}", "operator": "", "version": ""})
        return dependencies

    @staticmethod
    def settings_gradle(content: str) -> List[Dict]:
        """Parses a settings.gradle file content."""
        dependencies = []
        for match in re.finditer(r"include ['\"](.*?)['\"]", content):
            name = match.group(1)
            dependencies.append({"name": name, "operator": "", "version": ""})
        return dependencies

    @staticmethod
    def parse_cargo_toml(content: str) -> List[Dict]:
        """Parses a Cargo.toml file content."""
        dependencies = []
        try:
            data = tomli.loads(content)
            deps = data.get("dependencies", {})
            for dep, version in deps.items():
                dependencies.append({"name": dep, "operator": "==", "version": version})
        except tomli.TomlDecodeError:
            pass
        return dependencies
    
    @staticmethod
    def parse_cargo_lock(content: str) -> List[Dict]:
        """Parses a Cargo.lock file content."""
        dependencies = []
        try:
            data = tomli.loads(content)
            for package in data.get("package", []):
                name = package.get("name", "")
                version = package.get("version", "")
                dependencies.append({"name": name, "operator": "==", "version": version})
        except tomli.TomlDecodeError:
            pass
        return dependencies

    @staticmethod
    def parse_packages_config_json(content: str) -> List[Dict]:
        """Parses a Packages.config file content."""
        dependencies = []
        root = ET.fromstring(content)
        for dep in root.findall(".//package"):
            name = dep.get("id")
            version = dep.get("version")
            dependencies.append({"name": name, "operator": "==", "version": version})
        return dependencies
    
    @staticmethod
    def parse_project_json(content: str) -> List[Dict]:
        """Parses a project.json file content."""
        dependencies = []
        try:
            data = json.loads(content)
            deps = data.get("dependencies", {})
            for dep, version in deps.items():
                dependencies.append({"name": dep, "operator": "==", "version": version})
        except json.JSONDecodeError:
            pass
        return dependencies

    @staticmethod
    def parse_csproj(content: str) -> List[Dict]:
        """Parses a .csproj file content."""
        dependencies = []
        for match in re.finditer(r'<PackageReference Include="(.+?)" Version="(.+?)"', content):
            name, version = match.groups()
            dependencies.append({"name": name, "operator": "==", "version": version})
        return dependencies

    @staticmethod
    def parse_nuspec(content: str) -> List[Dict]:
        """Parses a .nuspec file content."""
        dependencies = []
        root = ET.fromstring(content)
        for dep in root.findall(".//dependency"):
            name = dep.get("id")
            version = dep.get("version")
            dependencies.append({"name": name, "operator": "==", "version": version})
        return dependencies

    @staticmethod
    def parse_project_assets_json(content: str) -> List[Dict]:
        """Parses a project.assets.json file content."""
        dependencies = []
        try:
            data = json.loads(content)
            targets = data.get("targets", {})
            for target in targets.values():
                libs = target.get("libraries", {})
                for lib, info in libs.items():
                    dependencies.append({"name": lib, "operator": "==", "version": info.get("version", "")})
        except json.JSONDecodeError:
            pass
        return dependencies

    @staticmethod
    def parse_packages_lock_json(content: str) -> List[Dict]:
        """Parses a packages.lock.json file content."""
        dependencies = []
        try:
            data = json.loads(content)
            for dep, info in data.get("dependencies", {}).items():
                dependencies.append({"name": dep, "operator": "==", "version": info.get("version", "")})
        except json.JSONDecodeError:
            pass
        return dependencies

    @staticmethod
    def parse_paket(content: str) -> List[Dict]:
        """Parses a .paket file content."""
        dependencies = []
        for match in re.finditer(r"nuget\s+(.*?)\s+(.*?)\s+", content):
            name, version = match.groups()
            dependencies.append({"name": name, "operator": "==", "version": version})
        return dependencies
    
    @staticmethod
    def parse_paket_dependencies(content: str) -> List[Dict]:
        """Parses a paket.dependencies file content."""
        dependencies = []
        for match in re.finditer(r"nuget\s+(.*?)\s+(.*?)\s+", content):
            name, version = match.groups()
            dependencies.append({"name": name, "operator": "==", "version": version})
        return dependencies
    
    @staticmethod
    def parse_paket_lock(content: str) -> List[Dict]:
        """Parses a paket.lock file content."""
        dependencies = []
        for match in re.finditer(r"    (.*?)\s+(.*?)\s+", content):
            name, version = match.groups()
            dependencies.append({"name": name, "operator": "==", "version": version})
        return dependencies

    @staticmethod
    def parse_go_mod(content: str) -> List[Dict]:
        """Parses a go.mod file content."""
        dependencies = []
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("require ("):
                continue
            if line.startswith("require "):
                parts = line.split(" ")
                if len(parts) == 3:
                    name, version = parts[1], parts[2]
                    dependencies.append({"name": name, "operator": "==", "version": version})
        return dependencies

    @staticmethod
    def parse_go_sum(content: str) -> List[Dict]:
        """Parses a go.sum file content."""
        dependencies = []
        for line in content.splitlines():
            parts = line.split(" ")
            if len(parts) >= 3:
                name, version = parts[0], parts[1]
                dependencies.append({"name": name, "operator": "==", "version": version})
        return dependencies
    
    @staticmethod
    def parse_glide_lock(content: str) -> List[Dict]:
        """Parses a glide.lock file content."""
        dependencies = []
        for match in re.finditer(r"([a-zA-Z0-9/\-_]+)\s+([a-f0-9]+)", content):
            name, version = match.groups()
            dependencies.append({"name": name, "operator": "==", "version": version})
        return dependencies
    
    @staticmethod
    def parse_glide_yaml(content: str) -> List[Dict]:
        """Parses a glide.yaml file content."""
        dependencies = []
        try:
            data = yaml.safe_load(content)
            for dep, version in data.get("import", {}).items():
                dependencies.append({"name": dep, "operator": "==", "version": version})
        except yaml.YAMLError:
            pass
        return dependencies
    
    @staticmethod
    def parse_gogradle_lock(content: str) -> List[Dict]:
        """Parses a gogradle.lock file content."""
        dependencies = []
        try:
            data = json.loads(content)
            for dep, info in data.get("dependencies", {}).items():
                dependencies.append({"name": dep, "operator": "==", "version": info.get("version", "")})
        except json.JSONDecodeError:
            pass
        return dependencies
    
    @staticmethod
    def parse_gopkg_lock(content: str) -> List[Dict]:
        """Parses a Gopkg.lock file content."""
        dependencies = []
        for match in re.finditer(r"([a-zA-Z0-9/\-_]+)\s+([a-f0-9]+)", content):
            name, version = match.groups()
            dependencies.append({"name": name, "operator": "==", "version": version})
        return dependencies
    
    @staticmethod
    def parse_godeps_lock(content: str) -> List[Dict]:
        """Parses a Godeps.lock file content."""
        dependencies = []
        for match in re.finditer(r"([a-zA-Z0-9/\-_]+)\s+([a-f0-9]+)", content):
            name, version = match.groups()
            dependencies.append({"name": name, "operator": "==", "version": version})
        return dependencies
    
    @staticmethod
    def parse_vendor_conf(content: str) -> List[Dict]:
        """Parses a vendor.conf file content."""
        dependencies = []
        for match in re.finditer(r"([a-zA-Z0-9/\-_]+)\s+([a-f0-9]+)", content):
            name, version = match.groups()
            dependencies.append({"name": name, "operator": "==", "version": version})
        return dependencies

    @staticmethod
    def parse_cmakelists_txt(content: str) -> List[Dict]:
        """Parses a CMakeLists.txt file content."""
        dependencies = []
        for match in re.finditer(r"find_package\((.*?)\)", content):
            name = match.group(1)
            dependencies.append({"name": name, "operator": "", "version": ""})
        return dependencies
    
    @staticmethod
    def parse_makefile(content: str) -> List[Dict]:
        """Parses a Makefile content."""
        dependencies = []
        for match in re.finditer(r"([a-zA-Z0-9_-]+)\s*:", content):
            name = match.group(1)
            dependencies.append({"name": name, "operator": "", "version": ""})
        return dependencies
    
    @staticmethod   
    def parse_pubsec_yaml(content: str) -> List[Dict]:
        """Parses a pubspec.yaml file content."""
        dependencies = []
        try:
            data = yaml.safe_load(content)
            deps = data.get("dependencies", {})
            for dep, version in deps.items():
                dependencies.append({"name": dep, "operator": "", "version": version})
        except yaml.YAMLError:
            pass
        return dependencies
    
    @staticmethod
    def parse_podfile(content: str) -> List[Dict]:
        """Parses a Podfile content."""
        dependencies = []
        for match in re.finditer(r"pod ['\"](.+?)['\"],\s*['\"](.+?)['\"]", content):
            name, version = match.groups()
            dependencies.append({"name": name, "operator": "==", "version": version})
        return dependencies
    
    @staticmethod
    def parse_podfile_lock(content: str) -> List[Dict]:
        """Parses a Podfile.lock content."""
        dependencies = []
        for match in re.finditer(r"    - (.+?) \((.+?)\)", content):
            name, version = match.groups()
            dependencies.append({"name": name, "operator": "==", "version": version})
        return dependencies
    
    @staticmethod
    def parse_packages_swift(content: str) -> List[Dict]:
        """Parses a packages.swift file content."""
        dependencies = []
        for match in re.finditer(r"(.+?)\s*:\s*['\"](.+?)['\"]", content):
            name, version = match.groups()
            dependencies.append({"name": name, "operator": "==", "version": version})
        return dependencies
    
    @staticmethod
    def parse_cartfile(content: str) -> List[Dict]:
        """Parses a Cartfile content."""
        dependencies = []
        for match in re.finditer(r"binary ['\"](.+?)['\"]\s*['\"](.+?)['\"]", content):
            name, version = match.groups()
            dependencies.append({"name": name, "operator": "==", "version": version})
        return dependencies