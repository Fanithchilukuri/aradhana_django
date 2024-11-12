from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalesRecordViewSet, InventoryViewSet, DataViewSet, PredictionAPIView  # Import DataViewSet

# Initialize the router for the viewsets
router = DefaultRouter()
router.register(r'sales_records', SalesRecordViewSet, basename='sales-record')
router.register(r'inventory', InventoryViewSet, basename='inventory')
router.register(r'data', DataViewSet, basename='data')  # Registering the new DataViewSet

urlpatterns = [
    path('', include(router.urls)),  # Include router URLs for viewsets
    path('predict/', PredictionAPIView.as_view(), name='predict'),  # Use as_view() for APIView
]
