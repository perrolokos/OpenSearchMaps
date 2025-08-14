from django.contrib import admin
from .models import Article, Citation, SearchQuery, UserSubscription, Alert, KnowledgeMap

admin.site.register(Article)
admin.site.register(Citation)
admin.site.register(SearchQuery)
admin.site.register(UserSubscription)
admin.site.register(Alert)
admin.site.register(KnowledgeMap)
