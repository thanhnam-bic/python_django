from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/xoa_tai_san/<str:id>/', views.xoa_tai_san, name='xoa_tai_san'),
    path('api/taisan/', views.get_tat_ca_taisan, name='lay_tat_ca_tai_san'),
    path('api/taisan/nhanvien/', views.tinh_taisan_moi_nhanvien, name='tinh_taisan_moi_nhanvien'),
    path('api/taisan/add/', views.tao_tai_san, name='tao_tai_san'),
]
