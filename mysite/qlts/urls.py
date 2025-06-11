from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/xoa_tai_san/<str:id>/', views.xoa_tai_san, name='xoa_tai_san'),
    path('api/cap_nhat_tai_san/<str:id>/', views.cap_nhat_tai_san, name='cap_nhat_tai_san'),
    path('api/chi_tiet_tai_san/<str:id>/', views.chi_tiet_tai_san, name='chi_tiet_tai_san'),
    path('api/taisan/', views.get_tat_ca_taisan, name='get_all_taisan'),
    path('api/taisan/nhanvien/', views.tinh_taisan_moi_nhanvien, name='tinh_taisan_moi_nhanvien'),
]
