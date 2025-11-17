from typing import Dict, Any, List


class UserInput:
    def __init__(self, schema, data: Dict[str, Any]):
        self.schema = schema
        self.data = data

    def validate(self):
        return self.schema().validate(self.data)


import re
import unicodedata


def generate_slug(title: str) -> str:
    # Normalize accents (e.g., café -> cafe)
    title = (
        unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("utf-8")
    )
    # Lowercase
    title = title.lower().strip()
    # Replace non-alphanumeric characters with hyphen
    title = re.sub(r"[^a-z0-9]+", "-", title)
    # Remove leading/trailing hyphens
    title = title.strip("-")
    return title


def generate_unique_slug(title: str, slugs: List[str]) -> str:
    base_slug = generate_slug(title)

    if base_slug not in slugs:
        return base_slug

    counter = 2
    unique_slug = f"{base_slug}{counter}"

    while base_slug in slugs:
        counter += 1
        unique_slug = f"{base_slug}{counter}"

    return unique_slug
