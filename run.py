from scrapy.crawler import CrawlerProcess
from Sybot import settings
from scrapy.settings import Settings
from Sybot.spiders.webtekno import WebteknoSpider
import configparser


def run():
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    config = configparser.ConfigParser()
    config.read('scrapy.cfg')
    # print(config.sections())
    # print(config['settings']['default'])

    # Run only one page from sources
    kwargs = dict()
    kwargs['sampleMode'] = kwargs['samplePage'] = False
    kwargs['samplePrint'] = False

    process = CrawlerProcess(crawler_settings)
    process.crawl(WebteknoSpider, **kwargs)
    process.start()


if __name__ == "__main__":
    run()
