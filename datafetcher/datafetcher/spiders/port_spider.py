import scrapy


class PortSpider(scrapy.Spider):
    name = "port_spider"
    start_urls = ['https://directories.lloydslist.com/port-browse-name/searchid/0/searchchar/']

    def parse(self, response):

        yield {"names": response.css("div.browseresults p b a::text").getall()}

        for page_button in response.css("div.page-buttons a"):
            if page_button.css("::text").get() == 'Next >':
                nextpageurl = page_button.css("::attr(href)").get()
                print(nextpageurl)
                yield response.follow(nextpageurl, callback=self.parse)
