from django.db import models
from users.models import User, Institution


class Notice(models.Model):
    PRIORITY = [('low','Low'), ('medium','Medium'), ('high','High'), ('urgent','Urgent')]
    TARGET   = [('all','All'), ('students','Students'), ('teachers','Teachers'), ('parents','Parents')]

    institution  = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='notices')
    title        = models.CharField(max_length=255)
    content      = models.TextField()
    priority     = models.CharField(max_length=10, choices=PRIORITY, default='medium')
    target_audience = models.CharField(max_length=10, choices=TARGET, default='all')
    attachment   = models.FileField(upload_to='notices/', null=True, blank=True)
    published_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='published_notices')
    is_published = models.BooleanField(default=False)
    publish_at   = models.DateTimeField(null=True, blank=True)
    expires_at   = models.DateTimeField(null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
