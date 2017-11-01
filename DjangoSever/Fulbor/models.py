from django.db import models

class Budget(models.Model):
    user_id = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
