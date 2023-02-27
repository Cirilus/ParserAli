from urllib.parse import urlparse
from uuid import uuid4

from django.http import JsonResponse
from rest_framework.views import APIView
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from scrapyd_api import ScrapydAPI

scrapyd = ScrapydAPI('http://localhost:6800')


def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url)
    except ValidationError:
        return False
    return True


class ParseProduct(APIView):
    def post(self, request):
        url = request.data['url']
        if not url:
            return JsonResponse({"error": "Missing url"})

        if not is_valid_url(url):
            return JsonResponse({'error': "Url is invalid"})

        domain = urlparse(url).netloc
        unique_id = str(uuid4())

        if domain != "aliexpress.ru":
            return JsonResponse({'error': "Domain is invalid"})

        settings = {
            'unique_id': unique_id,
            'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        }

        task = scrapyd.schedule('default', 'Ali',
                                settings=settings,
                                url=url, domain=domain)

        return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started'})
