from dataclasses import dataclass

@dataclass
class Article:
    title: str
    content: str 
    photo: str | None = None

