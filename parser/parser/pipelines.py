import os
import sys
from asgiref.sync import sync_to_async
from Authentication.models import CustomUser
sys.path.append(os.path.dirname(os.path.abspath('.')))

class AliPipeline(object):
    @sync_to_async()
    def process_item(self, item, spider):
        item["user"] = CustomUser.objects.get(pk=item['user'])
        item.save()
        return item
