from dataclasses import dataclass

@dataclass
class User:
    name: str
    email:str

@dataclass
class Article:
    author_name: str
    author_email: str
    title: str
    content: str
    image: str | None = None
    id: int | None = None
    
