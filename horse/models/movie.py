class Movie:
    def __init__(self, title):
        self.title = title
        self.likes = 0

    def like_added(self):
        self.likes += 1
