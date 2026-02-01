"""
URL configuration for vocab app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WordViewSet, MyWordsViewSet, GrammarRuleViewSet, ReviewHistoryViewSet

router = DefaultRouter()
router.register(r'words', WordViewSet, basename='word')
router.register(r'my-words', MyWordsViewSet, basename='mywords')
router.register(r'grammar', GrammarRuleViewSet, basename='grammarrule')
router.register(r'history', ReviewHistoryViewSet, basename='reviewhistory')

urlpatterns = [
    path('', include(router.urls)),
]
