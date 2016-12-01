class Movie:
    def __init__(self, title):
        self.title = title
        self.likes = 0

    def like_added(self):
        self.likes += 1

    def like_removed(self):
        if self.likes > 0:
            self.likes -= 1
