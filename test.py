def _crawl(spider_name=None):
    if spider_name:
        os.system('scrapy crawl %s' % spider_name)
    return None

def run_crawler():

    spider_names = ['bao']

    pool = Pool(processes=len(spider_names))
    pool.map(_crawl, spider_names)