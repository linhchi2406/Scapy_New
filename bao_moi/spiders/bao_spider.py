
import scrapy
import datetime

class QuoteSpider(scrapy.Spider):
    
    name="bao1"
    start_urls = [
         'https://www.phunuonline.com.vn/tim-kiem/covid-19.html',
            # 'https://ncov.moh.gov.vn/web/guest/dong-thoi-gian',
    ]
  
    def parse(self, response):
        for linkbao in response.xpath('//div[@id="listcate"]/ul[@class="cate-content-list-item"]/li[@class="item post"]/div[@class="news-img-left box-content"]/a/@href').extract():
            yield scrapy.Request(linkbao, callback=self.saveFile)
        next_page_url = response.xpath('//div[@class="fright"]/ul/li/a/@href').extract()[6]
        if next_page_url is not None:
            yield scrapy.Request(next_page_url)

    def saveFile(self, response):
        format_date = ' %d/%m/%Y '
        datetime_obj = datetime.datetime.strptime(response.xpath('//div[@class="detail-date-share mobi-none-hr"]/div[@class="pubdate fleft"]/text()').extract()[1].split("-")[0], format_date)
        content = ""
        for page in response.xpath('//div[@class="content-fck-font-size"]/p/text()').extract():
            content = content + page
        yield {
            'title': response.xpath('//div[@class="detail-title"]/h1/text()').extract_first(),
            'time' : response.xpath('//div[@class="detail-date-share mobi-none-hr"]/div[@class="pubdate fleft"]/text()').extract()[1].split("-")[-1],
            'date' : datetime_obj.date(),
            'content' : content
            }
   