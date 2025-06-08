from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('xoa_tai_san/<str:id>/', views.xoa_tai_san, name='xoa_tai_san'),
    path('api/cap_nhat_tai_san/<str:id>', views.cap_nhat_tai_san, name='cap_nhat_tai_san'),  # PUT
]
