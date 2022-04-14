import time
from scholarly import scholarly, ProxyGenerator
from model.BaseLiterature import BaseLiterature
from model.ScholarLiterature import ScholarLiterature
from searcher.ScholarlySingleton import ScholarlySingleton


class Completer(object):
    def __init__(self, configuration):
        self.configuration = configuration
        self.search_engine = ScholarlySingleton.getInstance()

    def complete(self, paper_title: str) -> BaseLiterature:
        try:
            pub_summary = self.search_engine.query_single_literature_title(paper_title)
            full_list_of_elements = list(pub_summary)
            if len(list(full_list_of_elements)) != 1:
                return BaseLiterature(paper_title)
            else:
                for pub in full_list_of_elements:
                    print("Completed : " + pub["bib"]["title"])
                    print("Citations : " + str(pub["num_citations"]))
                    typed_paper = ScholarLiterature(pub["bib"]["title"])
                    typed_paper.set_summary(pub["bib"]["abstract"])
                    typed_paper.set_citations(pub["num_citations"])
                    typed_paper.set_download_link(pub["pub_url"])
                    return typed_paper
        except Exception as err:
            print(err)
            return BaseLiterature(paper_title)
