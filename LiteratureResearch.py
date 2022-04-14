import datetime
from distutils.dir_util import copy_tree
import os
import shutil
import webbrowser
import arxiv
import dominate
from dominate.tags import link, body, div, li, a, h1, br, p, h2, h3, hr
from tqdm import tqdm

from ConfigHandler import ConfigHandler
from DominateHelper import DominateHelper
from HtmlTableElement import HtmlTableElement
from searcher.SearcherFactory import SearcherFactory

import logging

logging.basicConfig(level=logging.INFO)

config_file_path = "configurations/iteration_1.json"
# READ CONFIG

configuation = ConfigHandler(config_file_path)
config = configuation.read_config_file()

search_dict = {}

shutil.rmtree(config["ResultPath"], ignore_errors=True)
os.mkdir(config["ResultPath"])

for search in tqdm(config["Search"]):
    print("Search " + search["Name"] + " Started")

    searcherFactory = SearcherFactory(config)
    searchers = searcherFactory.assemble_searcher()

    # SEARCH
    results = []
    for searcher in tqdm(searchers):
        print("Search with : " + searcher.get_searcher_name())
        results += searcher.search(search)

        searcher.create_search_summary(
            os.path.join(config["ResultPath"], search["Name"]),
            str(searcher.get_searcher_name()),
        )
    search_dict[search["Name"]] = {
        "Searchers": searchers,
        "Reason": search["Description"],
        "SearchName": search["Name"],
    }

# DISPLAY
doc = dominate.document(title="Literature Research")
with doc.head:
    link(rel="stylesheet", href="style.css")

with doc.add(body()).add(div(id="content")):
    h1(config["Title"])

    helper = DominateHelper(doc)

    for key_search_name in search_dict:
        h2(search_dict[key_search_name]["Reason"])
        h3(search_dict[key_search_name]["SearchName"])
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

path_to_file = os.path.join(config["ResultPath"], "LiteratureResearch.html")
file = open(path_to_file, "w+", encoding="utf-8")
file.write(doc.__str__())
file.close()

dateTimeStringFileName = (
    config["SearchName"] + "_" + datetime.datetime.now().strftime("%Y_%m_%d_%H")
)

print("> Copy Utils Folder ...")
copy_tree("utils", config["ResultPath"])
shutil.copy(config_file_path, config["ResultPath"])

print("> Start compressing ...")
shutil.make_archive(
    config["ResultPath"] + dateTimeStringFileName, "zip", config["ResultPath"]
)
print("> Compressing finished")

webbrowser.open(path_to_file)
