import logging
from io import BytesIO

import networkx as nx
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import (
    Article,
    Citation,
    SearchQuery,
    UserSubscription,
    Alert,
    KnowledgeMap,
)
from .serializers import (
    ArticleSerializer,
    CitationSerializer,
    SearchQuerySerializer,
    UserSubscriptionSerializer,
    AlertSerializer,
    KnowledgeMapSerializer,
)

logger = logging.getLogger(__name__)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class CitationViewSet(viewsets.ModelViewSet):
    queryset = Citation.objects.all()
    serializer_class = CitationSerializer


class SearchQueryViewSet(viewsets.ModelViewSet):
    queryset = SearchQuery.objects.all()
    serializer_class = SearchQuerySerializer


class UserSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer


class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer


class KnowledgeMapViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeMap.objects.all()
    serializer_class = KnowledgeMapSerializer


@api_view(['POST'])
def semantic_search(request):
    query = (request.data.get('query') or '').strip()
    if not query:
        return Response({'detail': 'query is required'}, status=400)
    logger.info("Semantic search requested: %s", query)
    return Response({'query': query, 'results': []})


@api_view(['GET'])
def map_tree(request, pk):
    km = get_object_or_404(KnowledgeMap, pk=pk)
    serializer = KnowledgeMapSerializer(km)
    return Response({'id': pk, 'map': serializer.data})


@api_view(['GET'])
def map_export(request, pk):
    fmt = request.GET.get('fmt', 'mermaid')
    km = get_object_or_404(KnowledgeMap, pk=pk)

    state = km.state_json or {}
    nodes = state.get('nodes', [])
    edges = state.get('edges', [])

    if fmt == 'gexf':
        graph = nx.DiGraph()
        for node in nodes:
            graph.add_node(node['id'], **{k: v for k, v in node.items() if k != 'id'})
        for edge in edges:
            graph.add_edge(
                edge['source'],
                edge['target'],
                **{k: v for k, v in edge.items() if k not in {'source', 'target'}},
            )
        bio = BytesIO()
        nx.write_gexf(graph, bio)
        resp = HttpResponse(bio.getvalue(), content_type='application/gexf+xml')
        resp['Content-Disposition'] = f'attachment; filename="map-{pk}.gexf"'
        return resp
    elif fmt == 'mermaid':
        lines = ["graph TD"]
        for node in nodes:
            label = node.get('title', node['id'])
            lines.append(f"    {node['id']}[{label}]")
        for edge in edges:
            lines.append(f"    {edge['source']} --> {edge['target']}")
        content = "\n".join(lines)
        resp = HttpResponse(content, content_type='text/plain')
        resp['Content-Disposition'] = f'attachment; filename="map-{pk}.mmd"'
        return resp
    else:
        return Response({'detail': f'Unsupported format: {fmt}'}, status=400)
