from dataclasses import dataclass

@dataclass
class User:
    name: str
    email:str

@dataclass
class Article:
    author: User
    title: str
    content: str
    image: str | None = None
    id: int | None = None
    
