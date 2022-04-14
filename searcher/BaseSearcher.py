from abc import abstractmethod
from typing import List

from model.BaseLiterature import BaseLiterature


class BaseSearcher(object):
    def __init__(self, configuration):
        """initialize searcher"""
        self.configuration = configuration
        self.path_to_summary = ""
        self.search_string = ""

    @abstractmethod
    def search(self) -> List[BaseLiterature]:
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
