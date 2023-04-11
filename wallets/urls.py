from rest_framework.routers import DefaultRouter

from wallets.views import WalletViewSet

router = DefaultRouter()
router.register(r"wallets", WalletViewSet, basename="wallet")
urlpatterns = router.urls
