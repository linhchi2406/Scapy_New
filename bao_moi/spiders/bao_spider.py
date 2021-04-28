
import scrapy
import datetime

class QuoteSpider(scrapy.Spider):
    
    name="bao"
    start_urls = [
         'https://ncov.moh.gov.vn/web/guest/dong-thoi-gian?p_p_id=com_liferay_asset_publisher_web_portlet_AssetPublisherPortlet_INSTANCE_nf7Qy5mlPXqs&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_com_liferay_asset_publisher_web_portlet_AssetPublisherPortlet_INSTANCE_nf7Qy5mlPXqs_delta=10&p_r_p_resetCur=false&_com_liferay_asset_publisher_web_portlet_AssetPublisherPortlet_INSTANCE_nf7Qy5mlPXqs_cur=2',
         'http://www.baochinhphu.vn/Search.aspx?keyword=covid+&type=0',   
    ]
  
    def parse(self, response):
        if (response.url.split("=")[0] == 'https://ncov.moh.gov.vn/web/guest/dong-thoi-gian?p_p_id'):
            for quote in response.xpath('//div[@class="timeline-detail"]'):
                format_date = '%d/%m/%Y'
                datetime_obj = datetime.datetime.strptime(quote.xpath('.//div[@class="timeline-head"]/h3/text()').extract_first().split(" ")[-1], format_date)
                yield {
                    'time' : quote.xpath('.//div[@class="timeline-head"]/h3/text()').extract_first().split(" ")[0],
                    'date' : datetime_obj.date(),
                    'content' : quote.xpath('.//div[@class="timeline-content"]/p/text()').extract()
                }
            next_page_url = response.xpath('//li[@class=""]/a/@href').extract()[1]
            if next_page_url is not None:
                yield scrapy.Request(next_page_url)
        else:
            finalPage = "http://www.baochinhphu.vn" + response.xpath('//div[@class="paging"]/span[@id="ctl00_leftContent_ctl00_pager"]/a/@href')[-1].extract()
            # finalPage = "http://www.baochinhphu.vn/Search.aspx?keyword=covid+&type=0&trang=5"
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

