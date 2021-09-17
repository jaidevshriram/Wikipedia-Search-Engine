from os import link
import re

class Page:
    def __init__(self, body="", title="", infobox="", links=[], references=[]):
        self.body = body
        self.pageText = ""
        self.title = title
        self.infobox = infobox
        self.categories = []
        self.links = links
        self.references = references

        self.parseSection = {
            'title': self.parseTitle,
            'revision': self.parseRevision,
        }

    def initPageFromElement(self, elements):

        for element in elements:
            for key in self.parseSection.keys():
                if key in str(element):
                    self.parseSection[key](element)

        # print("Title", self.title)

    def parseTitle(self, element):
        self.title = element.text

    def parseRevision(self, element):
    
        bodyRoot = None
        for childelement in list(element):
            if 'text' in str(childelement):
                bodyRoot = childelement

        if bodyRoot is not None:
            self.pageText = bodyRoot.text            

            if self.pageText is not None:            
                self.body = bodyRoot.text

                self.parseInfobox()
                self.parseCategories()
                self.parseLinks()
                self.parseReferences()
        # print(self.infobox)

    def parseInfobox(self):
        infobox = []
        minStart = None
        maxEnd = None
        match = list(re.finditer(r"{{Infobox", self.body, flags=re.DOTALL))

        if match == []:
            return

        match = match[-1]

        start, end = match.start(), match.end()
        infobox = self.body[:end]

        content_block = self.body[end:end+1000].split('\n')
        newEnd = end
        for content_line in content_block:
            content_line = content_line.strip()
            
            if content_line[:2] == '}}':
                break
            infobox += " " + content_line
            newEnd += len(content_line)

        self.infobox = infobox
        self.body = self.body[newEnd:]

    def parseCategories(self):
        self.categories = re.findall(r"\[\[्रेणी:(.*?)\]\]", self.body, flags=re.DOTALL)
        self.body = re.sub(r"\[\[्रेणी:(.*?)\]\]", "", self.body, flags=re.DOTALL)

    def parseLinks(self):
        linkText = self.body.split("बाहरी कड़ियाँ")
        
        if len(linkText) > 1:

            links = linkText[1].split("\n")
            
            for i, link in enumerate(links):
                link = re.sub(r'(https?://[^\s]+)', "", link)
                links[i] = re.sub('[^A-Za-z0-9\ \n\t]+', '', link)

            self.links = links
            self.body = linkText[0]

    def parseReferences(self):
        self.references = re.findall(r"<ref[^/]*?>(.*?)</ref>", self.body, flags=re.DOTALL)
        self.body = re.sub(r"<ref[^/]*?>(.*?)</ref>", "", self.body, flags=re.DOTALL)
