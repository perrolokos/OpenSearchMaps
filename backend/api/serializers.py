from rest_framework import serializers
from .models import (
    Article,
    Citation,
    SearchQuery,
    UserSubscription,
    Alert,
    KnowledgeMap,
)


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'doi', 'title', 'abstract', 'authors', 'publication_date', 'metadata_json']


class KnowledgeMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeMap
        fields = ['id', 'name', 'state_json']


class CitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Citation
        fields = ['id', 'source_article', 'target_article']


class SearchQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchQuery
        fields = ['id', 'user', 'query_text', 'is_semantic', 'created_at']


class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = ['id', 'user', 'query']


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['id', 'user', 'article', 'reason', 'created_at']
