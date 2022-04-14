import os
import time
import arxiv

import dominate
from dominate.tags import link, body, div, li, a, h1, br, p, h2, h3, hr
from DominateHelper import DominateHelper
from HtmlTableElement import HtmlTableElement

from model.ArxivLiterature import ArxivLiterature
from model.BaseLiterature import BaseLiterature
from searcher.BaseSearcher import BaseSearcher
from searcher.Completer import Completer


class ArxivSearcher(BaseSearcher):
    def __init__(self, configuration):
        super().__init__(configuration)
        self.foundLiteratures = []
        self.searcher_source = "Arxiv"
        self.completer = Completer(configuration)

    def get_searcher_name(self) -> str:
        return self.searcher_source

    def search(self, search_config):
        self.search_string = self.__prepareSearch(search_config["Keywords"])
        search = None

        time.sleep(3)
        search = arxiv.Search(
            query=self.search_string,
            max_results=100,
            sort_by=arxiv.SortCriterion.Relevance,
            sort_order=arxiv.SortOrder.Descending,
        )

        for foundLiterature in list(search.results()):
            print("Evaluated : " + foundLiterature.title)
            typed_paper = ArxivLiterature(foundLiterature.title)
            typed_paper.set_summary(foundLiterature.summary)

            baseLiterature = self.completer.complete(foundLiterature.title)
            typed_paper.set_citations(baseLiterature.get_citations())
            for link in foundLiterature.links:
                if link.title is not None:
                    if "pdf" in link.title:
                        typed_paper.set_download_link(link.href)
            # Exclustion
            if baseLiterature.get_citations() >= search_config["Filter"]["Citations"]:
                self.foundLiteratures.append(typed_paper)
        return self.foundLiteratures

    def get_amount_found(self) -> int:
        return len(self.foundLiteratures)

    def __prepareSearch(self, listOfWords):
        return " ".join(listOfWords)
