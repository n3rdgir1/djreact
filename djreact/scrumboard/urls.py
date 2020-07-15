from rest_framework.routers import DefaultRouter

from .api import ListViewSet, CardViewSet

router = DefaultRouter()
router.register('lists', ListViewSet)
router.register('cards', CardViewSet)

urlpatterns = router.urls
