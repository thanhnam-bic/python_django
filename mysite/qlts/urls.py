from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/xoa_tai_san/<str:id>/', views.xoa_tai_san, name='xoa_tai_san'),
    path('api/cap_nhat_tai_san/<str:id>/', views.cap_nhat_tai_san, name='cap_nhat_tai_san'),
    path('api/chi_tiet_tai_san/<str:id>/', views.chi_tiet_tai_san, name='chi_tiet_tai_san'),
    path('api/lay_tat_ca_tai_san/', views.lay_tat_ca_tai_san, name='lay_tat_ca_tai_san'),
    path('api/tao_tai_san/',views.tao_tai_san,name='tao_tai_san'),
    path('api/tinh_tai_san_nhan_vien/', views.tinh_tai_san_nhan_vien, name='tinh_tai_san_nhan_vien'),

]
