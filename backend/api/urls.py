from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'articles', views.ArticleViewSet)
router.register(r'citations', views.CitationViewSet)
router.register(r'search-queries', views.SearchQueryViewSet)
router.register(r'subscriptions', views.UserSubscriptionViewSet)
router.register(r'alerts', views.AlertViewSet)
router.register(r'knowledge-maps', views.KnowledgeMapViewSet)

urlpatterns = [
    path('search/semantic', views.semantic_search, name='semantic_search'),
    path('map/<int:pk>/tree/', views.map_tree, name='map_tree'),
    path('map/<int:pk>/export/', views.map_export, name='map_export'),
    path('', include(router.urls)),
]
