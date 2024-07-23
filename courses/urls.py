from django.urls import path
from .views import (
    SectionCreateAPIView,
    SectionListAPIView,
    SectionRetrieveAPIView,
    SectionUpdateAPIView,
    SectionDestroyAPIView,
    MaterialCreateAPIView,
    MaterialListAPIView,
    MaterialRetrieveAPIView,
    MaterialUpdateAPIView,
    MaterialDestroyAPIView
)

urlpatterns = [
    path('sections/', SectionListAPIView.as_view(), name='section_list'),
    path('sections/create/', SectionCreateAPIView.as_view(), name='section_create'),
    path('sections/<int:pk>/', SectionRetrieveAPIView.as_view(), name='section_detail'),
    path('sections/<int:pk>/update/', SectionUpdateAPIView.as_view(), name='section_update'),
    path('sections/<int:pk>/delete/', SectionDestroyAPIView.as_view(), name='section_delete'),
    path('materials/', MaterialListAPIView.as_view(), name='material_list'),
    path('materials/create/', MaterialCreateAPIView.as_view(), name='material_create'),
    path('materials/<int:pk>/', MaterialRetrieveAPIView.as_view(), name='material_detail'),
    path('materials/<int:pk>/update/', MaterialUpdateAPIView.as_view(), name='material_update'),
    path('materials/<int:pk>/delete/', MaterialDestroyAPIView.as_view(), name='material_delete'),
]