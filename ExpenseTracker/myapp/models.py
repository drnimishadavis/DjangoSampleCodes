from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Expense(models.Model):
    title=models.CharField(max_length=200)
    amount=models.PositiveIntegerField()
    CATEGORY_CHOICES=(
        ("food","FOOD"),
        ("housing","Housing"),
        ("Travel","Travel"),
        ("Others","Others")
    )
    category=models.CharField(max_length=100,choices=CATEGORY_CHOICES,default="Others")
    created_at=models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    bill_image = models.ImageField(upload_to='bills/', null=True, blank=True)

    # Objects string representation
    def __str__(self):
        return self.title