from django.urls import path
from . import views


urlpatterns = [
    path('', views.CarListView.as_view(), name='car_list'),
    path('cars/<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('cars/add/', views.CarCreateView.as_view(), name='car_add'),
    path('cars/<int:pk>/edit', views.CarUpdateView.as_view(), name='car_edit'),
    path('cars/<int:pk>/delete', views.CarDeleteView.as_view(), name='car_delete'),
    path('register/', views.RegisterView.as_view(), name='register'),
]
