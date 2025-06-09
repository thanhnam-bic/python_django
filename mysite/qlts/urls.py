from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/xoa_tai_san/<str:id>/', views.xoa_tai_san, name='xoa_tai_san'),
    path('api/taisan/', views.get_tat_ca_taisan, name='get_all_taisan'),
    path('api/taisan/nhanvien/', views.tinh_tai_san_moi_nhan_vien, name='tinh_tai_san_moi_nhan_vien'),
]
