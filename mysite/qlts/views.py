from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import TaiSan, DanhMuc, NhaSanXuat, NhaCungCap, NhanVien
from django.views.decorators.csrf import csrf_exempt
import json

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
            du_lieu = {
                "ma_tai_san": asset.ma_tai_san,
                "ten_tai_san": asset.ten_tai_san,
                "so_serial": asset.so_serial,
                "gia_mua": float(asset.gia_mua),
                "danh_muc": {
                    "ten_danh_muc": asset.danh_muc.danh_muc if asset.danh_muc else None
                },
                "nhan_vien": {
                    "ma_nhan_vien": asset.ma_nhan_vien.ma_nhan_vien if asset.ma_nhan_vien else None
                },
                "nha_san_xuat": {
                    "ten_nha_san_xuat": asset.nha_san_xuat.nha_san_xuat if asset.nha_san_xuat else None
                },
                "nha_cung_cap": {
                    "ten_nha_cung_cap": asset.nha_cung_cap.nha_cung_cap if asset.nha_cung_cap else None
                }
            }
            return JsonResponse({
                "thanh_cong": True,
                "thong_bao": "Lấy chi tiết tài sản thành công",
                "du_lieu": du_lieu
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
            "message": "Chỉ hỗ trợ phương thức GET."
        }, status=405)

#API PUT: Cập nhật thông tin tài sản theo ID
@csrf_exempt
def cap_nhat_tai_san(request, id):
    if request.method == 'PUT':
        try:
            asset = TaiSan.objects.get(pk=id)
        except TaiSan.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "Không tìm thấy tài sản.",
                "errors": {"ma_tai_san": f"Tài sản với mã {id} không tồn tại"}
            }, status=404)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                "success": False,
                "message": "Dữ liệu gửi lên không hợp lệ.",
                "errors": {"json": "JSON không đúng định dạng"}
            }, status=400)

        # Cập nhật từng trường, nếu có trong data
        if 'ten_tai_san' in data:
            asset.ten_tai_san = data['ten_tai_san']
        if 'so_serial' in data:
            asset.so_serial = data['so_serial']
        if 'gia_mua' in data:
            asset.gia_mua = data['gia_mua']

        # Với FK, lấy object tương ứng
        if 'danh_muc' in data:
            try:
                asset.danh_muc = DanhMuc.objects.get(pk=data['danh_muc'])
            except DanhMuc.DoesNotExist:
                return JsonResponse({
                    "success": False,
                    "message": "Không tìm thấy danh mục.",
                    "errors": {"danh_muc": f"Danh mục với mã {data['danh_muc']} không tồn tại"}
                }, status=400)
        if 'ma_nhan_vien' in data:
            try:
                asset.ma_nhan_vien = NhanVien.objects.get(pk=data['ma_nhan_vien'])
            except NhanVien.DoesNotExist:
                return JsonResponse({
                    "success": False,
                    "message": "Không tìm thấy nhân viên.",
                    "errors": {"ma_nhan_vien": f"Nhân viên với mã {data['ma_nhan_vien']} không tồn tại"}
                }, status=400)
        if 'nha_san_xuat' in data:
            try:
                asset.nha_san_xuat = NhaSanXuat.objects.get(pk=data['nha_san_xuat'])
            except NhaSanXuat.DoesNotExist:
                return JsonResponse({
                    "success": False,
                    "message": "Không tìm thấy nhà sản xuất.",
                    "errors": {"nha_san_xuat": f"Nhà sản xuất với mã {data['nha_san_xuat']} không tồn tại"}
                }, status=400)
        if 'nha_cung_cap' in data:
            try:
                asset.nha_cung_cap = NhaCungCap.objects.get(pk=data['nha_cung_cap'])
            except NhaCungCap.DoesNotExist:
                return JsonResponse({
                    "success": False,
                    "message": "Không tìm thấy nhà cung cấp.",
                    "errors": {"nha_cung_cap": f"Nhà cung cấp với mã {data['nha_cung_cap']} không tồn tại"}
                }, status=400)

        asset.save()

        # Trả về dữ liệu
        return JsonResponse({
            "thanh_cong": True,
            "thong_bao": "Cập nhật tài sản thành công",
            "du_lieu": {
                "ma_tai_san": asset.ma_tai_san,
                "ten_tai_san": asset.ten_tai_san,
                "so_serial": asset.so_serial,
                "gia_mua": float(asset.gia_mua),
                "danh_muc": {
                    "ten_danh_muc": asset.danh_muc.danh_muc if asset.danh_muc else None
                },
                "nhan_vien": {
                    "ma_nhan_vien": asset.ma_nhan_vien.ma_nhan_vien if asset.ma_nhan_vien else None
                },
                "nha_san_xuat": {
                    "ten_nha_san_xuat": asset.nha_san_xuat.nha_san_xuat if asset.nha_san_xuat else None
                },
                "nha_cung_cap": {
                    "ten_nha_cung_cap": asset.nha_cung_cap.nha_cung_cap if asset.nha_cung_cap else None
                }
            }
        })
    else:
        return JsonResponse({
            "success": False,
            "message": "Chỉ hỗ trợ phương thức PUT"
        }, status=405)