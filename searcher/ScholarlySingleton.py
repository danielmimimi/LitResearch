from scholarly import scholarly, ProxyGenerator


class ScholarlySingleton:
    __instance = None
    pg = ProxyGenerator()
    success = pg.ScraperAPI("3c87b51ef4cb02275a35dd24f893088b")
    if success is False:
        raise Exception("Set up Scholarly NOOOT Sucessfull")
    print("Set up Scholarly Sucessfull")
    scholarly.use_proxy(pg)

    @staticmethod
    def getInstance():
        """Static access method."""
        if ScholarlySingleton.__instance == None:
            ScholarlySingleton()
        return ScholarlySingleton.__instance

    def __init__(self):
        """Virtually private constructor."""
        if ScholarlySingleton.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            ScholarlySingleton.__instance = self

    def query_with_year(self, search_text: str, year_low: int):
        pub_summary = scholarly.search_pubs(search_text, year_low=year_low)
        return pub_summary

    def query(self, search_text: str):
        pub_summary = scholarly.search_pubs(search_text)
        return pub_summary

    def query_single_literature_title(self, search_text: str):
        pub_summary = scholarly.search_pubs(
            '"' + search_text + '"'
        )  # otherwise total shitshow
        return pub_summary
