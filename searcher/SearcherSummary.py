from typing import List
import dominate
from dominate.tags import link, body, div, li, a, h1, br, p, h2, h3, hr

from DominateHelper import DominateHelper
from HtmlTableElement import HtmlTableElement


class SearcherSummary(object):
    def __init__(self, search_name: str) -> None:
        self.search_name = search_name
        pass

    def store_searcher(self, name: str):
        self.searcher_name = name

    def store_number_of_found_elements(self, number: int):
        self.found_elements = number

    def store_keywords(self, keywords: str):
        self.keywords = keywords

    def store_filters(self, filters: List[str]):
        self.filters = filters

    def create_searcher_summary(self, path: str):
        doc = dominate.document(title="Literature Research " + self.search_name)

        with doc.head:
            link(rel="stylesheet", href="utils/style.css")
        with doc.add(body()).add(div(id="content")):
            a(id=self.searcher_name)
            helper = DominateHelper(doc)

            backgroundColorTc = "#c6f2b3"
            headerList = [
                HtmlTableElement(text="Number of Results", bgColor=backgroundColorTc),
                HtmlTableElement(text="Keywords", bgColor=backgroundColorTc),
            ]
            entryList = []
            entryList.append(HtmlTableElement(text=str(self.found_elements)))
            entryList.append(HtmlTableElement(text=self.keywords))
            helper.createHtmlTable(headerList, entryList)

        file = open(self.htmlFilePath, "w+")
        file.write(doc.__str__())
        file.close()
