from django.db import models
from accounts.models import User

class ChecklistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=50)
    status = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'item_name')
