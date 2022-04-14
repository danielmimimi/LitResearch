from dominate.tags import tr, table, tbody


class DominateHelper(object):
    def __init__(self, document):
        """initialize helper"""
        self.doc = document

    def createHtmlTable(self, headerTextList, scoreResultsList):
        """Creates html table with html elements"""
        columnLenght = len(headerTextList)
        assert columnLenght > 0
        assert (len(scoreResultsList) % columnLenght) == 0
        with table(style="width:1400px").add(tbody()):
            htmlList = tr()
            for header in headerTextList:
                htmlList.add(header.GetHeader())
            for entry in range(0, len(scoreResultsList), columnLenght):
                htmlList = tr()
                for i in range(entry, entry + columnLenght):
                    htmlList = scoreResultsList[i].GetElement(htmlList)
