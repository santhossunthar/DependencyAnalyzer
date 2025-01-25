import re

class URLParser:
    """Extracts GitHub repository URLs from text."""
    @staticmethod
    def extract_github_urls(content):
        """Extract repository URLs from the README content."""
        return re.findall(r"https?://github\.com/[\w-]+/[\w-]+", content)