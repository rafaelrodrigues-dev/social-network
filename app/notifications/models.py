from django.db import models
from django.contrib.auth import get_user_model
from publications.models import Publication

User = get_user_model()

class Notification(models.Model):
    recipient = models.ForeignKey(User, related_name="notifications", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE, null=True, blank=True)
    notification_type = models.CharField(max_length=50)
    text = models.TextField()
    publication = models.ForeignKey(Publication, related_name='notifications', on_delete=models.CASCADE, null=True, blank=True)
    is_read =models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Notification {self.id} from {self.sender} to {self.recipient}"
