from SearchEngine.backend.classes.Text import Text

class Article:
    """
    Represantation of Text with some metadata for Search Structure
    """
    def __init__(self, title: str, text: str, id: int = None):
        self.title = title
        self.text = Text(text)
        self.id = id

    def __repr__(self):
        return f"title: {self.title}"  # link:{self.link}
