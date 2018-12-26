class HomeSpider:
    def __init__(self, **kwargs):
        self.sourceUrls = kwargs.get('sourceUrls', [])

    def setSourceUrls(self, url):
        return self.sourceUrls.append(url)

    def getSourceUrls(self):
        return self.sourceUrls
