from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import TaiSan
import json
from django.views.decorators.csrf import csrf_exempt

# API IndexIndex
def index(request):
    return HttpResponse("Xin chào. Bạn đã đến app QLTS")

#API Delete: Xóa tài sản theo ID
@csrf_exempt
def xoa_tai_san(request, id):
    if request.method == 'DELETE':
        try:
            asset = TaiSan.objects.get(pk=id)
            asset.delete()
            return JsonResponse({
                "thanh_cong": True,
                "thong_bao": "Xóa tài sản thành công.",
                "du_lieu": {
                    "ma_tai_san": id
                }
            })
        except TaiSan.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "Không tìm thấy tài nguyên.",
                "errors": {
                    "id": "Không tồn tại ID này"
                }
            }, status=404)
    else:
        return JsonResponse({
            "success": False,
            "message": "Không hỗ trợ phương thức này.",
            "errors": {
                "method": "Chỉ hỗ trợ phương thức DELETE"
            }
        }, status=405)

#API GET: Lấy thông tin chi tiết của 1 tài sản theo ID  
@csrf_exempt
def chi_tiet_tai_san(request, id):
    if request.method == 'GET':
        try:
            asset = TaiSan.objects.get(pk=id)
            return JsonResponse({
                "thanh_cong": True,
                "thong_bao": "Lấy thông tin tài sản thành công.",
                "du_lieu": {
                    "ma_tai_san": asset.ma_tai_san,
                    "ten_tai_san": asset.ten_tai_san,
                    "so_serial": asset.so_serial,
                    "gia_mua": float(asset.gia_mua),
                    "danh_muc": {
                        "ten_danh_muc": asset.danh_muc.ten_danh_muc if asset.danh_muc else None
                    },
                    "nhan_vien": {
                        "ma_nhan_vien": asset.ma_nhan_vien.ma_nhan_vien if asset.ma_nhan_vien else None
                    },
                    "nha_san_xuat": {
                        "ten_nha_san_xuat": asset.nha_san_xuat.ten_nha_san_xuat if asset.nha_san_xuat else None
                    },
                    "nha_cung_cap": {
                        "ten_nha_cung_cap": asset.nha_cung_cap.ten_nha_cung_cap if asset.nha_cung_cap else None
                    }
                }
            })
        except TaiSan.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "Không tìm thấy tài nguyên.",
                "errors": {
                    "id": "Không tồn tại ID này"
                }
            }, status=404)
    else:
        return JsonResponse({
            "success": False,
            "message": "Không hỗ trợ phương thức này.",
            "errors": {
                "method": "Chỉ hỗ trợ phương thức GET"
            }
        }, status=405)