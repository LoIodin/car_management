from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('', views.CarListView.as_view(), name='car_list'),
    path('cars/<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('cars/add/', views.CarCreateView.as_view(), name='car_add'),
    path('cars/<int:pk>/edit', views.CarUpdateView.as_view(), name='car_edit'),
    path('cars/<int:pk>/delete', views.CarDeleteView.as_view(), name='car_delete'),
    path('register/', views.RegisterView.as_view(), name='register'),
    # API маршруты
    path('api/cars/', views.CarListCreateAPIView.as_view(), name='api_car_list'),
    path('api/cars/<int:pk>/', views.CarDetailAPIView.as_view(), name='api_car_detail'),
    path('api/cars/<int:pk>/comments/', views.CarCommentAPIView.as_view(), name='api_car_comment'),
    path('api/token/', obtain_auth_token, name='api_token'),
    path('api/info/', views.api_info_view, name='api_info'),
]
