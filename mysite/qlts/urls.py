from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('xoa_tai_san/<str:id>/', views.xoa_tai_san, name='xoa_tai_san'),
    path('api/taisan/', views.get_tat_ca_taisan, name='get_all_taisan'),
    path('api/taisan/add/', views.tao_tai_san, name='tao_tai_san'),
]
