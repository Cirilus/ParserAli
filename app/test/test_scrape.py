import time

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from ..models import Product


class ProductApiCase(APITestCase):

    def test_scrape(self):
        url = reverse("scrape_data")
        ali_url = "https://aliexpress.ru/item/1005005165332999.html?spm=a2g2w.home.10009201.9.75dfa63dnLRiai&_evo_buckets=165609,165598,194275&sku_id=12000031940277382&gps-id=appJustForYouNew&scm=1007.34525.325667.0&scm_id=1007.34525.325667.0&scm-url=1007.34525.325667.0&pvid=d805e0a7-f3d6-4c53-8509-a592275caf10&_t=gps-id:appJustForYouNew,scm-url:1007.34525.325667.0,pvid:d805e0a7-f3d6-4c53-8509-a592275caf10,tpp_buckets:24525%230%23325667%2348_21387%230%23330480%232_21387%239507%23434561%236_21387%2314793%23456925%239_22079%230%23204795%2330_22079%235270%2324216%23135_22079%234871%2324466%2311_22079%235116%2323470%231&ru_algo_pv_id=d805e0a7-f3d6-4c53-8509-a592275caf10&scenario=appJustForYouNew&tpp_rcmd_bucket_id=325667&traffic_source=recommendation"
        response = self.client.post(url, {"url": ali_url})
        self.assert_(response.json()['task_id'])
