from django.conf import settings
from django.db import models


class Article(models.Model):
    doi = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=1024)
    abstract = models.TextField(blank=True)
    authors = models.TextField(blank=True)
    publication_date = models.DateField(null=True, blank=True)
    metadata_json = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.title


class Citation(models.Model):
    source_article = models.ForeignKey(Article, related_name='citations_from', on_delete=models.CASCADE)
    target_article = models.ForeignKey(Article, related_name='citations_to', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('source_article', 'target_article')

    def __str__(self):
        return f"{self.source_article_id} -> {self.target_article_id}"


class SearchQuery(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    query_text = models.TextField()
    is_semantic = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.query_text} ({'semantic' if self.is_semantic else 'basic'})"


class UserSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    query = models.ForeignKey(SearchQuery, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_id} subscribes to {self.query_id}"


class Alert(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert for {self.user_id} on {self.article_id}"


class KnowledgeMap(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    state_json = models.JSONField(default=dict, blank=True)
    collaborators = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='collaborations', blank=True)

    def __str__(self):
        return self.name
