from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.urls import reverse

from django.db import IntegrityError

from .models import Article, KnowledgeMap, SearchQuery, UserSubscription, Alert, Citation
from .tasks import check_new_articles


class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_semantic_search_endpoint(self):
        response = self.client.post('/api/search/semantic', {'query': 'test'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'query': 'test', 'results': []})

    def test_semantic_search_requires_query(self):
        response = self.client.post('/api/search/semantic', {}, format='json')
        self.assertEqual(response.status_code, 400)

    def test_map_tree_endpoint_not_found(self):
        response = self.client.get('/api/map/1/tree/')
        self.assertEqual(response.status_code, 404)

    def test_map_tree_endpoint(self):
        user = get_user_model().objects.create_user(username='u', password='p')
        km = KnowledgeMap.objects.create(owner=user, name='Map', state_json={})
        response = self.client.get(f'/api/map/{km.id}/tree/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], km.id)

    def test_article_crud_and_alert_task(self):
        User = get_user_model()
        user = User.objects.create_user(username='user', password='pass')

        article_resp = self.client.post(
            reverse('article-list'),
            {
                'doi': '10.1/xyz',
                'title': 'Sample Article',
                'abstract': '',
                'authors': 'A. Author',
                'publication_date': '2024-01-01',
                'metadata_json': {},
            },
            format='json',
        )
        self.assertEqual(article_resp.status_code, 201)
        article_id = article_resp.json()['id']

        query = SearchQuery.objects.create(user=user, query_text='Sample', is_semantic=False)
        UserSubscription.objects.create(user=user, query=query)

        created = check_new_articles()
        self.assertEqual(created, 1)
        self.assertEqual(Alert.objects.filter(user=user, article_id=article_id).count(), 1)

    def test_map_export(self):
        user = get_user_model().objects.create_user(username='exp', password='p')
        state = {
            "nodes": [{"id": "a", "title": "A"}, {"id": "b", "title": "B"}],
            "edges": [{"source": "a", "target": "b"}],
        }
        km = KnowledgeMap.objects.create(owner=user, name="M", state_json=state)
        self.assertEqual(KnowledgeMap.objects.count(), 1)

        mermaid_resp = self.client.get(f"/api/map/{km.id}/export/")
        self.assertEqual(mermaid_resp.status_code, 200)
        self.assertIn("a --> b", mermaid_resp.content.decode())
        self.assertEqual(KnowledgeMap.objects.count(), 1)

        gexf_resp = self.client.get(f"/api/map/{km.id}/export/", {"fmt": "gexf"})
        self.assertEqual(gexf_resp.status_code, 200)
        self.assertIn("<gexf", gexf_resp.content.decode())

        bad_resp = self.client.get(f"/api/map/{km.id}/export/", {"fmt": "bad"})
        self.assertEqual(bad_resp.status_code, 400)

    def test_citation_unique(self):
        a1 = Article.objects.create(doi='d1', title='A1', abstract='', authors='A', publication_date='2024-01-01', metadata_json={})
        a2 = Article.objects.create(doi='d2', title='A2', abstract='', authors='B', publication_date='2024-01-02', metadata_json={})
        Citation.objects.create(source_article=a1, target_article=a2)
        with self.assertRaises(IntegrityError):
            Citation.objects.create(source_article=a1, target_article=a2)
