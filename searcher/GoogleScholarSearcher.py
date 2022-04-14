import os
import time
import dominate
from dominate.tags import link, body, div, li, a, h1, br, p, h2, h3, hr
from DominateHelper import DominateHelper
from HtmlTableElement import HtmlTableElement

from model.ArxivLiterature import ArxivLiterature
from model.BaseLiterature import BaseLiterature
from model.ScholarLiterature import ScholarLiterature
from searcher.BaseSearcher import BaseSearcher
from searcher.ScholarlySingleton import ScholarlySingleton


class GoogleScholarSearcher(BaseSearcher):
    def __init__(self, configuration):
        super().__init__(configuration)
        self.foundLiteratures = []
        self.searcher_source = "Google Scholar"
        self.search_engine = ScholarlySingleton.getInstance()

    def get_searcher_name(self) -> str:
        return self.searcher_source

    def search(self, search_config):
        self.search_string = self.__prepareSearch(search_config["Keywords"])
        try:
            pub_summary = self.search_engine.query_with_year(
                self.search_string, search_config["Filter"]["Year"]
            )
        except Exception as err:
            print(err)
            return self.foundLiteratures
        full_list_of_elements = list(pub_summary)
        if len(full_list_of_elements) == 0:
            return self.foundLiteratures
        try:
            for pub in full_list_of_elements:
                print("Evaluated : " + pub["bib"]["title"])
                print("Citations : " + str(pub["num_citations"]))
                if pub["num_citations"] >= search_config["Filter"]["Citations"]:
                    typed_paper = ScholarLiterature(pub["bib"]["title"])
                    typed_paper.set_summary(pub["bib"]["abstract"])
                    typed_paper.set_citations(pub["num_citations"])
                    typed_paper.set_download_link(pub["pub_url"])
                    self.foundLiteratures.append(typed_paper)
        except Exception:
            print("Max Tries")

        return self.foundLiteratures

    def get_amount_found(self) -> int:
        return len(self.foundLiteratures)

    def __prepareSearch(self, listOfWords):
        groupedWords = []
        # Add " ond word groups
        for word in listOfWords:
            if " " in word:
                groupedWords.append('"' + word + '"')
            else:
                if "AND" in word:
                    groupedWords.append(" AND ")
                elif "NOT" in word:
                    groupedWords.append(" -")
                elif "OR" in word:
                    groupedWords.append(" OR ")
                else:
                    groupedWords.append(word)
        collocated = "".join(groupedWords)

        return collocated
