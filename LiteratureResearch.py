import os
import shutil
import webbrowser
import arxiv
import dominate
from dominate.tags import link, body, div, li, a, h1, br, p, h2, h3, hr

from ConfigHandler import ConfigHandler
from DominateHelper import DominateHelper
from HtmlTableElement import HtmlTableElement
from model.ArxivLiterature import ArxivLiterature
from searcher.SearcherFactory import SearcherFactory

# READ CONFIG
configuation = ConfigHandler(r"configurations/search.json")
config = configuation.read_config_file()

search_dict = {}

for search in config["Search"]:
    searcherFactory = SearcherFactory(search)
    searchers = searcherFactory.assemble_searcher()

    # SEARCH
    results = []
    for searcher in searchers:
        results += searcher.search()
        searcher.create_search_summary(
            os.path.join("results", search["Name"]),
            str(searcher.get_searcher_name()),
        )
    search_dict[search["Name"]] = {
        "Searchers": searchers,
        "Reason": search["Description"],
    }

# DISPLAY
doc = dominate.document(title="Literature Research")
with doc.head:
    link(rel="stylesheet", href="utils/style.css")

with doc.add(body()).add(div(id="content")):
    h1(config["Title"])

    helper = DominateHelper(doc)

    for key_search_name in search_dict:
        h3(search_dict[key_search_name]["Reason"])
        backgroundColorTc = "#c6f2b3"
        headerList = [
            HtmlTableElement(text="Source", bgColor=backgroundColorTc),
            HtmlTableElement(text="Number of Results", bgColor=backgroundColorTc),
            HtmlTableElement(text="Search String", bgColor=backgroundColorTc),
        ]
        entryList = []
        numbers = 0
        for searcher in search_dict[key_search_name]["Searchers"]:
            entryList.append(
                HtmlTableElement(
                    text=searcher.get_searcher_name(), href=searcher.get_summary_path()
                )
            )
            entryList.append(HtmlTableElement(text=str(searcher.get_amount_found())))
            entryList.append(HtmlTableElement(text=str(searcher.get_search_string())))
        helper.createHtmlTable(headerList, entryList)

path_to_file = "LiteratureResearch.html"
file = open(path_to_file, "w+")
file.write(doc.__str__())
file.close()


webbrowser.open(path_to_file)
