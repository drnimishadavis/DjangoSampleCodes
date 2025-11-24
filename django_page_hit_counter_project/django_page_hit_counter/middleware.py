from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.db import models as dj_models
from .models import Hit
from django.contrib.contenttypes.models import ContentType
import re
EXCLUDE_PATHS = getattr(settings, "PAGE_HIT_COUNTER_EXCLUDE_PATHS", [r"^/admin/", r"^/static/", r"^/media/", r"^/__debug__/"])
class PageHitCounterMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.method != "GET":
            return None
        path = request.path
        for patt in EXCLUDE_PATHS:
            if re.match(patt, path):
                return None
        if getattr(settings, "PAGE_HIT_COUNTER_IGNORE_AJAX", True):
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return None
        hit_obj = getattr(request, "hit_object", None)
        if hit_obj is not None:
            ct = ContentType.objects.get_for_model(type(hit_obj))
            obj_id = getattr(hit_obj, "pk", None)
            hit, _ = Hit.objects.get_or_create(path=path, content_type=ct, object_id=obj_id)
        else:
            hit, _ = Hit.objects.get_or_create(path=path, content_type=None, object_id=None)
        Hit.objects.filter(pk=hit.pk).update(hits=dj_models.F("hits") + 1)
        return None
