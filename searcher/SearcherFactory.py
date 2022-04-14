from typing import List


from searcher.BaseSearcher import BaseSearcher
from searcher.GoogleScholarSearcher import GoogleScholarSearcher
from searcher.WebOfScienceSearcher import WebOfScienceSearcher
from searcher.ArxivSearcher import ArxivSearcher


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
            if "WOS" in searcherString:
                self.searchers.append(WebOfScienceSearcher(self.configuration))

        return self.searchers
