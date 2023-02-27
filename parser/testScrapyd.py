from uuid import uuid4
from urllib.parse import urlparse
from scrapyd_api import ScrapydAPI

scrapyd = ScrapydAPI('http://localhost:6800')

url = "https://aliexpress.ru/item/32953548253.html?spm=a2g2w.detail.seller_rcmd.5.28ab7b15RdwxCG&_evo_buckets=165609,165598,194275&sku_id=12000020937798804&gps-id=pcDetailBottomMoreThisSeller&scm=1007.34525.325667.0&scm_id=1007.34525.325667.0&scm-url=1007.34525.325667.0&pvid=d05244fc-6c9c-4a78-bb24-a4f8e7d84a1b&_t=gps-id:pcDetailBottomMoreThisSeller,scm-url:1007.34525.325667.0,pvid:d05244fc-6c9c-4a78-bb24-a4f8e7d84a1b,tpp_buckets:24525%230%23325667%234_21387%230%23233228%2310_21387%239507%23434558%233_21387%2314793%23456925%235&ru_algo_pv_id=d05244fc-6c9c-4a78-bb24-a4f8e7d84a1b&scenario=pcDetailBottomMoreThisSeller&tpp_rcmd_bucket_id=325667&traffic_source=recommendation"
domain = urlparse(url).netloc # parse the url and extract the domain
unique_id = str(uuid4())
settings = {
    'unique_id': unique_id,  # unique ID for each record for DB
    'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
}
print(domain)
task = scrapyd.schedule('default', 'Ali',
                        settings=settings, url=url, domain=domain)

print(task)
