from abc import abstractmethod
import os
from typing import List
import dominate
from dominate.tags import link, body, div, li, a, h1, br, p, h2, h3, hr
from DominateHelper import DominateHelper
from HtmlTableElement import HtmlTableElement

from model.BaseLiterature import BaseLiterature


class BaseSearcher(object):
    def __init__(self, configuration):
        """initialize searcher"""
        self.configuration = configuration
        self.path_to_summary = ""
        self.search_string = ""

    @abstractmethod
    def search(self, search_config) -> List[BaseLiterature]:
        raise NotImplementedError("Subclass should inherit method")

    @abstractmethod
    def create_search_summary(self, path: str, search_name: str):
        raise NotImplementedError("Subclass should inherit method")

    def get_search_string(self) -> str:
        return self.search_string

    def get_summary_path(self) -> str:
        return self.path_to_summary

    @abstractmethod
    def get_searcher_name(self) -> str:
        raise NotImplementedError("Subclass should inherit method")

    @abstractmethod
    def get_amount_found(self) -> int:
        raise NotImplementedError("Subclass should inherit method")

    def create_search_summary(self, path: str, search_name: str) -> str:
        doc = dominate.document(title="Literature Research " + search_name)

        with doc.head:
            link(rel="stylesheet", href="style.css")

        with doc.add(body()).add(div(id="content")):
            a(id=search_name)
            helper = DominateHelper(doc)

            backgroundColorTc = "#c6f2b3"
            headerList = [
                HtmlTableElement(text="Index", bgColor=backgroundColorTc),
                HtmlTableElement(text="Title", bgColor=backgroundColorTc),
                HtmlTableElement(text="#Citations", bgColor=backgroundColorTc),
                HtmlTableElement(text="Summary", bgColor=backgroundColorTc),
                HtmlTableElement(text="Download", bgColor=backgroundColorTc),
            ]
            entryList = []
            index = 0
            for literature in self.foundLiteratures:
                entryList.append(HtmlTableElement(text=str(index)))
                entryList.append(HtmlTableElement(text=literature.get_title()))
                entryList.append(HtmlTableElement(text=str(literature.get_citations())))
                entryList.append(HtmlTableElement(text=literature.get_summary()))
                if literature.get_download_link() is not "":
                    entryList.append(
                        HtmlTableElement(
                            text="Download", href=literature.get_download_link()
                        )
                    )
                else:
                    entryList.append(HtmlTableElement(text="Download"))
                index = index + 1
            helper.createHtmlTable(headerList, entryList)

        final_path = path + "_" + search_name + ".html"
        final_path = final_path.replace(" ", "_")
        file = open(final_path, "w+", encoding="utf-8")
        file.write(doc.__str__())
        file.close()
        self.path_to_summary = os.path.basename(final_path)
