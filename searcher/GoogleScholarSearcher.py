import os
from typing import List
from scholarly import scholarly, ProxyGenerator
import dominate
from dominate.tags import link, body, div, li, a, h1, br, p, h2, h3, hr
from DominateHelper import DominateHelper
from HtmlTableElement import HtmlTableElement

from model.ArxivLiterature import ArxivLiterature
from model.BaseLiterature import BaseLiterature
from model.ScholarLiterature import ScholarLiterature
from searcher.BaseSearcher import BaseSearcher


class GoogleScholarSearcher(BaseSearcher):
    def __init__(self, configuration):
        super().__init__(configuration)
        self.foundLiteratures = []
        self.searcher_source = "Google Scholar"

    def get_searcher_name(self) -> str:
        return self.searcher_source

    def search(self):
        self.search_string = self.__prepareSearch(self.configuration["Keywords"])
        pg = ProxyGenerator()
        success = pg.Tor_Internal(tor_cmd="tor")
        scholarly.use_proxy(pg)
        pub_summary = scholarly.search_pubs(
            self.search_string, year_low=self.configuration["Filter"]["Year"]
        )

        pub_summary._get_total_results()
        for pub in pub_summary:
            if pub["num_citations"] > self.configuration["Filter"]["Citations"]:
                typed_paper = ScholarLiterature(pub["bib"]["title"])
                typed_paper.set_summary(pub["bib"]["abstract"])
                typed_paper.set_citations(pub["num_citations"])
                typed_paper.set_download_link(pub["pub_url"])
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
        changedList = ['"' + s + '"' for s in listOfWords]
        keyword_list = " ".join(changedList)
        keyword_list = keyword_list.replace('"AND"', "+")
        keyword_list = keyword_list.replace('"NOT"', "-")
        return keyword_list
