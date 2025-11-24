from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
class Hit(models.Model):
    path = models.CharField(max_length=500, db_index=True)
    content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")
    hits = models.PositiveBigIntegerField(default=0)
    last_hit = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = (("path", "content_type", "object_id"),)
        indexes = [models.Index(fields=["path"])]
    def __str__(self):
        if self.content_object:
            return f"Hits for {self.content_object} ({self.hits})"
        return f"Hits for {self.path} ({self.hits})"
