import os
from typing import List
import dominate
import woslite_client
from woslite_client.rest import ApiException
from pprint import pprint
from dominate.tags import link, body, div, li, a, h1, br, p, h2, h3, hr
from DominateHelper import DominateHelper
from HtmlTableElement import HtmlTableElement

from model.WebOfScienceLiterature import WebOfScienceLiterature
from model.BaseLiterature import BaseLiterature
from searcher.BaseSearcher import BaseSearcher
from searcher.Completer import Completer


class WebOfScienceSearcher(BaseSearcher):
    def __init__(self, configuration):
        super().__init__(configuration)
        self.foundLiteratures = []
        self.searcher_source = "Web of Science"
        configuration = woslite_client.Configuration()
        configuration.api_key["X-ApiKey"] = "39933d8290434369dbd9ec8dc60d7b0d61c219e7"
        self.integration_api_instance = woslite_client.IntegrationApi(
            woslite_client.ApiClient(configuration)
        )
        self.search_api_instance = woslite_client.SearchApi(
            woslite_client.ApiClient(configuration)
        )

        self.completer = Completer(configuration)

    def get_searcher_name(self) -> str:
        return self.searcher_source

    def search(self, search_config):
        self.search_string = self.__prepareSearch(search_config["Keywords"])
        try:
            max_results = 99
            publish_time_span = (
                str(search_config["Filter"]["Year"]) + "-01-01+2022-12-31"
            )
            # Submits a user query and returns results
            api_response = self.search_api_instance.root_get(
                "WOS", self.search_string, max_results, 1, lang="en"
            )
            for literature in api_response.data:
                baseLiterature = self.completer.complete(literature.title.title[0])
                if (
                    baseLiterature.get_citations()
                    >= search_config["Filter"]["Citations"]
                ):
                    self.foundLiteratures.append(baseLiterature)
        except ApiException as e:
            # abort
            print("Exception when calling SearchApi->root_get: %s\n" % e)

        return self.foundLiteratures

    def get_amount_found(self) -> int:
        return len(self.foundLiteratures)

    def __prepareSearch(self, listOfWords):
        configure_words = []
        for word in listOfWords:
            if "AND" in word:
                configure_words.append("AND")
            elif "NOT" in word:
                configure_words.append("NOT")
            elif "OR" in word:
                configure_words.append("OR")
            else:
                configure_words.append("AB=(" + word + ")")

        return " ".join(configure_words)
