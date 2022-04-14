from typing import List
from searcher.ArxivSearcher import ArxivSearcher

from searcher.BaseSearcher import BaseSearcher


class SearcherFactory(object):
    def __init__(self, configuration):
        self.configuration = configuration

    def assemble_searcher(self) -> List[BaseSearcher]:
        self.searchers = []
        for searcherString in self.configuration["Searcher"]:
            if "Arxiv" in searcherString:
                self.searchers.append(ArxivSearcher(self.configuration))
        return self.searchers
