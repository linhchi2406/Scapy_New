
# import scrapy
# import datetime

# class QuoteSpider(scrapy.Spider):
#     2
#     name="bao2"
#     start_urls = [
#          'https://ncov.moh.gov.vn/web/guest/dong-thoi-gian?p_p_id=com_liferay_asset_publisher_web_portlet_AssetPublisherPortlet_INSTANCE_nf7Qy5mlPXqs&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_com_liferay_asset_publisher_web_portlet_AssetPublisherPortlet_INSTANCE_nf7Qy5mlPXqs_delta=10&p_r_p_resetCur=false&_com_liferay_asset_publisher_web_portlet_AssetPublisherPortlet_INSTANCE_nf7Qy5mlPXqs_cur=1', 
#     ]
  
#     def parse(self, response):
#         for quote in response.xpath('//div[@class="timeline-detail"]'):
#             format_date = '%d/%m/%Y'
#             content = ""
#             for page in quote.xpath('.//div[@class="timeline-content"]/p/text()').extract():
#                 content = content + page
#             datetime_obj = datetime.datetime.strptime(quote.xpath('.//div[@class="timeline-head"]/h3/text()').extract_first().split(" ")[-1], format_date)
#             yield {
#                 'time' : quote.xpath('.//div[@class="timeline-head"]/h3/text()').extract_first().split(" ")[0],
#                 'date' : datetime_obj.date(),
#                 'content' : content
#             }
        
#         if(len(response.xpath('//ul[@class="lfr-pagination-buttons pager"]/li[@class=""]/a/@href').extract())==1):
#             next_page_url = response.xpath('//ul[@class="lfr-pagination-buttons pager"]/li[@class=""]/a/@href').extract_first()
#         else:
#             next_page_url = response.xpath('//ul[@class="lfr-pagination-buttons pager"]/li[@class=""]/a/@href').extract()[1]

#         if next_page_url is not None:
#             yield scrapy.Request(next_page_url)

       
import scrapy
import datetime
class QuotesSpider(scrapy.Spider):
    name = "bao2" #định danh cho spider
    start_urls = [
        'https://thuvienphapluat.vn/tintuc/tag?keyword=Covid-19&p=1',
        ]
    def parse(self, response):
        for linkbao in response.xpath('//ul[@class="ulTinList"]/li[@class="tt"]/a/@href').extract():
            linkbao = 'https://thuvienphapluat.vn/'+ linkbao
            yield scrapy.Request(linkbao, callback=self.saveFile)
        next_page_url = response.xpath('//nav[@class="pagi-center"]/ul[@class="pagination pagination-sm"]/li/a/@href').extract()[7]
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
    def saveFile(self, response):
        content = ""
        for a in response.xpath('//div[@class="newcontent"]/p/text()').extract():
            content = content + a
        date = response.xpath('//div[@class="divCate"]/span/text()').extract_first().split()
        format_date = '%d/%m/%Y'
        date_object= datetime.datetime.strptime(date[0],format_date)
        dateTime = str(date_object.date())+" "+date[1]
        yield {
            'title': response.xpath('//h1/text()').extract_first(),
            'content' : content,
            
        }