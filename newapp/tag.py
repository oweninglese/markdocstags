#! /usr/bin/python


class Tag(object):
    """Create Tag object.

    Args:
        object (_object_): _base_

    Returns:
        _str_: _tag_
    """

    def __init__(self):
        self.tagstr = ''

    def get(self):
        """Get str(Tag).

        Returns:
            _str_: _tag_
        """
        a = self.tagstr
        return a

    def set(self, newtag=str):
        """Update Tag w new string.

        Args:
            newtag (_str_, optional): _desc_. Defaults to str.

        Returns:
            _str_: _newtag-or-empty_
        """
        self.tagstr = newtag
        a = self
        return a.tagstr
