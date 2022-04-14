import os
from typing import List
import arxiv
import dominate
from dominate.tags import link, body, div, li, a, h1, br, p, h2, h3, hr
from DominateHelper import DominateHelper
from HtmlTableElement import HtmlTableElement

from model.ArxivLiterature import ArxivLiterature
from model.BaseLiterature import BaseLiterature
from searcher.BaseSearcher import BaseSearcher


class ArxivSearcher(BaseSearcher):
    def __init__(self, configuration):
        super().__init__(configuration)
        self.foundLiteratures = []
        self.searcher_source = "Arxiv"

    def get_searcher_name(self) -> str:
        return self.searcher_source

    def search(self):
        self.search_string = self.__prepareSearch(self.configuration["Keywords"])
        search = arxiv.Search(
            query=self.search_string,
            max_results=float("inf"),
            sort_by=arxiv.SortCriterion.Relevance,
            sort_order=arxiv.SortOrder.Descending,
        )
        for foundLiterature in list(search.results()):
            typed_paper = ArxivLiterature(foundLiterature.title)
            typed_paper.set_summary(foundLiterature.summary)
            for link in foundLiterature.links:
                if link.title is not None:
                    if "pdf" in link.title:
                        typed_paper.set_download_link(link.href)

            self.foundLiteratures.append(typed_paper)
        return self.foundLiteratures

    def get_amount_found(self) -> int:
        return len(self.foundLiteratures)

    def create_search_summary(self, path: str, search_name: str) -> str:
        doc = dominate.document(title="Literature Research " + search_name)

        with doc.head:
            link(rel="stylesheet", href="../utils/style.css")

        with doc.add(body()).add(div(id="content")):
            a(id=search_name)
            helper = DominateHelper(doc)

            backgroundColorTc = "#c6f2b3"
            headerList = [
                HtmlTableElement(text="Title", bgColor=backgroundColorTc),
                HtmlTableElement(text="Summary", bgColor=backgroundColorTc),
                HtmlTableElement(text="Download", bgColor=backgroundColorTc),
            ]
            entryList = []
            for literature in self.foundLiteratures:
                entryList.append(HtmlTableElement(text=literature.get_title()))
                entryList.append(HtmlTableElement(text=literature.get_summary()))
                if literature.get_download_link() is not "":
                    entryList.append(
                        HtmlTableElement(
                            text="Download", href=literature.get_download_link()
                        )
                    )
                else:
                    entryList.append(HtmlTableElement(text="Download"))
            helper.createHtmlTable(headerList, entryList)

        final_path = path + "_" + search_name + ".html"
        file = open(final_path, "w+")
        file.write(doc.__str__())
        file.close()
        self.path_to_summary = final_path

    def __prepareSearch(self, listOfWords):
        return " ".join(listOfWords)
