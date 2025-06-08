from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
<<<<<<< HEAD
    path('api/xoa_tai_san/<str:id>/', views.xoa_tai_san, name='xoa_tai_san'),
    path('api/chi_tiet_tai_san/<str:id>/', views.chi_tiet_tai_san, name='chi_tiet_tai_san'),
=======
    path('xoa_tai_san/<str:id>/', views.xoa_tai_san, name='xoa_tai_san'),
    path('api/taisan/', views.get_tat_ca_taisan, name='get_all_taisan'),
    path('api/taisan/nhanvien/', views.tinh_taisan_moi_nhanvien, name='tinh_taisan_moi_nhanvien'),
>>>>>>> 451ac883a4c968da4f1c5dafd32fec2f74a73186
]
