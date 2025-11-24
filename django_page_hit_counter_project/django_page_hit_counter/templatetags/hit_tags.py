from django import template
from ..models import Hit
from django.contrib.contenttypes.models import ContentType
register = template.Library()
@register.simple_tag(takes_context=True)
def get_hits_for_path(context, path=None):
    if path is None:
        path = context.get("request").path
    try:
        hit = Hit.objects.get(path=path, content_type=None, object_id=None)
        return hit.hits
    except Hit.DoesNotExist:
        return 0
@register.simple_tag
def get_hits_for_object(obj):
    ct = ContentType.objects.get_for_model(type(obj))
    try:
        hit = Hit.objects.get(path=obj.get_absolute_url() if hasattr(obj, "get_absolute_url") else "", content_type=ct, object_id=obj.pk)
        return hit.hits
    except Hit.DoesNotExist:
        return 0
@register.inclusion_tag("hit_counter/hits.html", takes_context=True)
def render_hits(context, path=None, obj=None, label="Views:"):
    if obj is not None:
        hits = get_hits_for_object(obj)
    else:
        hits = get_hits_for_path(context, path)
    return {"hits": hits, "label": label}
