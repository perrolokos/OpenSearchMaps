from celery import shared_task

from .models import Article, UserSubscription, Alert


@shared_task
def check_new_articles():
    """Create alerts for subscriptions matching existing articles."""
    created = 0
    for sub in UserSubscription.objects.select_related('query', 'user'):
        matches = Article.objects.filter(title__icontains=sub.query.query_text)
        for article in matches:
            alert, was_created = Alert.objects.get_or_create(
                user=sub.user,
                article=article,
                reason=f"Match for {sub.query.query_text}"
            )
            if was_created:
                created += 1
    return created
