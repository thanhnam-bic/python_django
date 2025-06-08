from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/xoa_tai_san/<str:id>/', views.xoa_tai_san, name='xoa_tai_san'),
    path('api/chi_tiet_tai_san/<str:id>/', views.chi_tiet_tai_san, name='chi_tiet_tai_san'),
]
