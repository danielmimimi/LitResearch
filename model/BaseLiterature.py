import datetime


class BaseLiterature(object):
    def __init__(self, title: str):
        """initialize helper"""
        self.title = title
        self.summary = ""
        self.link = ""
        self.citations = 0

    def set_download_link(self, link: str):
        self.link = link

    def get_download_link(self) -> str:
        return self.link

    def set_summary(self, summary: str):
        self.summary = summary

    def get_summary(self) -> str:
        return self.summary

    def set_data(self, date: datetime):
        self.date = date

    def get_data(self):
        return self.date

    def set_title(self, title: str):
        self.title = title

    def get_title(self) -> str:
        return self.title

    def set_citations(self, citations: int):
        self.citations = citations

    def get_citations(self) -> int:
        return self.citations
