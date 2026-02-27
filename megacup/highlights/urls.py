from rest_framework.routers import DefaultRouter
from .views import HighlightsViewSet

router = DefaultRouter()
router.register(r"highlights", HighlightsViewSet)              

urlpatterns = router.urls               