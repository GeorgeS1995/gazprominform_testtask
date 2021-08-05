import re
from abc import ABC


class HTMLParser(ABC):
    """ Inherit this class and change regex attr. Parse method parse the given html and result a list of matches. """
    regexp = None

    def __init__(self, html: str):
        self._html = html

    def parse(self) -> set:
        """
        :returns: Returns list of matches.
        """
        return set(self.regexp.findall(self._html))


class EmailHTMLParser(HTMLParser):
    regexp = re.compile(r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)")
