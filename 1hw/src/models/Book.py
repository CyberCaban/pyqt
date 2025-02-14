
class Book:
    def __init__(self, name: str, author: str, page_num: int, cover_path: str):
        self.name = name
        self.author = author
        self.page_num = page_num
        self.cover_path = cover_path

    def __str__(self):
        return f"Book: (name={self.name},author={self.author},pages={self.page_num},cover={self.cover_path})"
    
