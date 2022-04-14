"""
************************************************************************************************************************

Dominate Table helper (for Daniel Klauser), created for specifying single columns

------------------------------------------------------------------------------------------------------------------------

 Author      Daniel Klauser

 Copyright   CC Intelligent Sensors and Networks
             Lucerne University of Applied Sciences
             and Arts T&A, Switzerland.

************************************************************************************************************************
"""

from dominate.tags import td, img, a, ul, li, p, th


class HtmlTableElement(object):
    """HTML Table Element specifier"""

    def __init__(self, *args, **kwargs):
        self.text = kwargs.get("text", None)
        self.src = kwargs.get("src", None)
        self.width = kwargs.get("width", None)
        self.href = kwargs.get("href", None)
        self.text_dict = kwargs.get("text_dict", None)
        self.color_list = kwargs.get("color_list", None)
        self.backgroundColor = kwargs.get("bgColor", None)

    def GetElement(self, htmlList):
        """Gets specific html element, properties set in constructor"""
        if self.text is not None:
            if self.href is not None:
                if self.backgroundColor is not None:
                    return htmlList.add(
                        td(
                            self.text,
                            style="background-color:{}".format(self.backgroundColor),
                        )
                    )
                else:
                    return htmlList.add(
                        td(
                            a(self.text, href=self.href),
                            style="background-color:{}".format(self.backgroundColor),
                        )
                    )
            else:
                if self.backgroundColor is not None:
                    return htmlList.add(
                        td(
                            self.text,
                            style="background-color:{}".format(self.backgroundColor),
                        )
                    )
                else:
                    return htmlList.add(td(self.text))

        if self.text_dict is not None:
            list = ul()
            if self.text_dict is not None and self.color_list is not None:
                for color, entry in zip(self.color_list, self.text_dict):
                    txt = p(str(entry) + " : " + str(self.text_dict[entry]))
                    txt.attributes["style"] = "color:" + color
                    list += li(txt)
                return htmlList.add(td(list))
            else:
                for entry in self.text_dict:
                    list += li(str(entry) + " : " + str(self.text_dict[entry]))
                return htmlList.add(td(list))
        else:
            return htmlList.add(td(img(src=self.src, width=self.width)))

    def GetHeader(self):
        """Gets hmtl header element, properties set in constructor"""
        if self.text is not None:
            if self.backgroundColor is not None:
                return th(
                    self.text, style="background-color:{}".format(self.backgroundColor)
                )
            else:
                return th(self.text)
        else:
            return th("")
