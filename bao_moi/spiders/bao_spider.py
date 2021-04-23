
import scrapy
import datetime

# class QuoteSpider(scrapy.Spider):
#     name="bao"
#     start_urls= [
#         'https://anninhthudo.vn/phap-luat/80.antd'
#     ]

#     def parse(self, response):
#         for linkbao in response.xpath('//article[@class="article media"]/figure[@class="media-left"]/a/@href').extract():
#             yield scrapy.Request(linkbao, callback=self.saveFile)
#         next_page_url = response.xpath('//ul[@class="pagination-list"]/a/@href').extract_first()
#         if next_page_url is not None:
#             yield scrapy.Request(response.urljoin(next_page_url))


#     def saveFile(self, response):
#         yield {
#             'title': response.xpath('//header[@class="header"]/h1[@class="title cms-title"]/text()').extract_first(),
#             }
      




class QuoteSpider(scrapy.Spider):
    
    name="bao"
    start_urls = [
        'http://www.baochinhphu.vn/Search.aspx?keyword=covid+&type=0'
    ]

    def parse(self, response):
        finalPage = "http://www.baochinhphu.vn" + response.xpath('//div[@class="paging"]/span[@id="ctl00_leftContent_ctl00_pager"]/a/@href')[-1].extract()
        # finalPage = "http://www.baochinhphu.vn/Search.aspx?keyword=covid+&type=0&trang=1"
        totalPage = int(finalPage.split("=")[-1])
        for page in range(totalPage):
            link = finalPage.replace(str(totalPage), str(page + 1))
            yield scrapy.Request(link, callback=self.crawlContent)

    def crawlContent(self, response):
        for linkbao in response.xpath('//div[@class="story"]/p/a/@href').extract():
            linkbao = "http://www.baochinhphu.vn" + linkbao
            yield scrapy.Request(linkbao, callback=self.saveFile)

    def saveFile(self, response):
        format_date = '%d/%m/%Y'
        datetime_obj = datetime.datetime.strptime(response.xpath('//div[@class="article-header"]/p[@class="meta"]/text()').extract_first().split(", ")[-1], format_date)
        content = ""
        
        for page in response.xpath('//div[@class="article-body cmscontents"]/p/text()').extract():
            content = content + page
        yield {
            'title': response.xpath('//div[@class="article-header"]/h1/text()').extract_first(),
            'time' : response.xpath('//div[@class="article-header"]/p[@class="meta"]/text()').extract_first().split(",")[0],
            'date' : datetime_obj.date(),
            'content' : content
            }
            