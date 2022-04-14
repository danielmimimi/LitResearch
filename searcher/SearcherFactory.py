from typing import List
from searcher.ArxivSearcher import ArxivSearcher

from searcher.BaseSearcher import BaseSearcher
from searcher.GoogleScholarSearcher import GoogleScholarSearcher


class SearcherFactory(object):
    def __init__(self, configuration):
        self.configuration = configuration

    def assemble_searcher(self) -> List[BaseSearcher]:
        self.searchers = []
        for searcherString in self.configuration["Searcher"]:
            if "Arxiv" in searcherString:
                self.searchers.append(ArxivSearcher(self.configuration))
            if "Scholar" in searcherString:
                self.searchers.append(GoogleScholarSearcher(self.configuration))
        return self.searchers
