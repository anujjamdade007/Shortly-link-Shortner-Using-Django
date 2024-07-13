from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class urls(models.Model):
    name = models.CharField(max_length=300)
    link = models.TextField()
    short_url = models.CharField(max_length=200)
    visits = models.IntegerField(default=0)
    created_by = models.ForeignKey(User , on_delete= models.CASCADE , )
    id = models.UUIDField(default=uuid.uuid4 , unique=True , primary_key= True , editable=False)
    unique_code = models.CharField(max_length = 10 , blank=True, null=True)
    def __str__(self):
        return self.name


