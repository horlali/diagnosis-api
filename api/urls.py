from django.urls import path
from api.views import (
    UploadCSV,
    CategoryListAPIView,
    CategoryDetailView,
    DiagnosisListView,
    DiagnosisDetailView,
)


urlpatterns = [
    path("upload", UploadCSV.as_view(), name="upload-csv"),
    path("category", CategoryListAPIView.as_view(), name="category-list"),
    path("category/<int:id>", CategoryDetailView.as_view(), name="category-detail"),
    path("diagnosis", DiagnosisListView.as_view(), name="diagnosis-list"),
    path("diagnosis/<int:id>", DiagnosisDetailView.as_view(), name="diagnosis-detail"),
]
