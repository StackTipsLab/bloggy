from bloggy.models import Vote


class Bookmark(Vote):
    class Meta:
        verbose_name = "Bookmark"
        verbose_name_plural = "Bookmarks"
