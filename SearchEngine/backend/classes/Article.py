from SearchEngine.backend.classes.Text import Text

class Article:
    """
    Text with some metadata
    """
    def __init__(self, title: str, text: str, id: int = None):
        self.title = title
        self.text = Text(text)
        self.id = id
        # self.link = link  # absolute path to the full article in txt form

    def __repr__(self):
        return f"title: {self.title}"  # link:{self.link}