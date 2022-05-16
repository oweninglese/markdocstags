#! /usr/bin/python

class Article(object):
    """create article object.

    Args:
        object (_object_): _article string_
    """

    def __init__(self):
        """Prepare frontmatter yaml."""
        self.taglist = []
        self.content = ''

    def get(self, art=None, tags=None):
        """Get_article_."""
        if art is None and tags:
            return self.taglist
        return self.content

    def set(self, art=None, tags=None):
        """Set article contents.

        Args:
            update (str, optional): or empty. Defaults to str.
        """
        if tags is None:
            self.content = art
            return self.content
        if tags:
            self.taglist += [str(tag+",") for tag in tags]
            return self.taglist
