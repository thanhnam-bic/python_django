from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import TaiSan
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
<<<<<<< HEAD
            "success": False,
            "message": "Chỉ hỗ trợ phương thức GET."
        }, status=405)
=======
            'Thông báo': 'Lấy danh sách tài sản thành công',
            'Danh sách': danh_sach_display,
            'Tài sản có tổng cộng': len(data),
            'Dữ liệu gồm có': data
        }, status=200)
        
    except Exception as e:
        return JsonResponse({
            'Thông Báo': f'Lỗi khi lấy danh sách tài sản: {str(e)}',
            'dữ liệu': []
        }, status=500)
@require_http_methods(["GET"])
def tinh_taisan_moi_nhanvien(request):
    try:
        # Lấy tất cả nhân viên
        nhanvien_list = NhanVien.objects.all()
        
        # Tạo danh sách hiển thị thống kê
        thong_ke_display = []
        #thong_ke_display.append("=" * 80)
        thong_ke_display.append("THỐNG KÊ SỐ TÀI SẢN THEO NHÂN VIÊN")
        #thong_ke_display.append("=" * 80)
        
        # Tính tổng số nhân viên và tài sản
        tong_nhan_vien = nhanvien_list.count()
        tong_tai_san = TaiSan.objects.count()
        tai_san_chua_phan = TaiSan.objects.filter(ma_nhan_vien__isnull=True).count()
        
        thong_ke_display.append(f"Tổng số nhân viên: {tong_nhan_vien}")
        thong_ke_display.append(f"Tổng số tài sản: {tong_tai_san}")
        thong_ke_display.append(f"Tài sản chưa phân công: {tai_san_chua_phan}")
        #thong_ke_display.append("-" * 80)
        
        # Dữ liệu chi tiết cho API
        data = []
        
        for i, nhanvien in enumerate(nhanvien_list, 1):
            # Đếm số tài sản của nhân viên này
            so_tai_san = TaiSan.objects.filter(ma_nhan_vien=nhanvien).count()
            
            # Lấy danh sách tài sản của nhân viên
            tai_san_list = TaiSan.objects.filter(ma_nhan_vien=nhanvien)
            
            # Hiển thị thông tin nhân viên
            thong_ke_display.append(f"{i}. Nhân viên: {nhanvien.ho} {nhanvien.ten}")
            thong_ke_display.append(f"   Mã NV: {nhanvien.ma_nhan_vien}")
            thong_ke_display.append(f"   Email: {nhanvien.email}")
            thong_ke_display.append(f"   Vị trí: {nhanvien.vi_tri.vi_tri if nhanvien.vi_tri else 'Chưa có'}")
            thong_ke_display.append(f"   Số tài sản quản lý: {so_tai_san}")
            
            if so_tai_san > 0:
                thong_ke_display.append("   Danh sách tài sản:")
                for j, taisan in enumerate(tai_san_list, 1):
                    thong_ke_display.append(f"     {j}. {taisan.ma_tai_san} - {taisan.ten_tai_san}")
            else:
                thong_ke_display.append("   Chưa quản lý tài sản nào")
            
           # thong_ke_display.append("-" * 80)
            
            # Thêm vào data để trả về
            tai_san_data = []
            for taisan in tai_san_list:
                tai_san_data.append({
                    'ma_tai_san': taisan.ma_tai_san,
                    'ten_tai_san': taisan.ten_tai_san,
                    'so_serial': taisan.so_serial,
                    'gia_mua': float(taisan.gia_mua)
                })
            
            nhanvien_data = {
                'ma_nhan_vien': nhanvien.ma_nhan_vien,
                'ho': nhanvien.ho,
                'ten': nhanvien.ten,
                'ho_ten': f"{nhanvien.ho} {nhanvien.ten}",
                'email': nhanvien.email,
                'vi_tri': nhanvien.vi_tri.vi_tri if nhanvien.vi_tri else None,
                'so_tai_san_quan_ly': so_tai_san,
                'danh_sach_tai_san': tai_san_data
            }
            data.append(nhanvien_data)
        
        # Thêm thông tin tài sản chưa phân công
        if tai_san_chua_phan > 0:
            thong_ke_display.append(f"TÀI SẢN CHƯA PHÂN CÔNG ({tai_san_chua_phan} tài sản):")
            tai_san_chua_phan_list = TaiSan.objects.filter(ma_nhan_vien__isnull=True)
            for j, taisan in enumerate(tai_san_chua_phan_list, 1):
                thong_ke_display.append(f"  {j}. {taisan.ma_tai_san} - {taisan.ten_tai_san}")
           # thong_ke_display.append("-" * 80)
            
            # Thêm tài sản chưa phân công vào data
            tai_san_chua_phan_data = []
            for taisan in tai_san_chua_phan_list:
                tai_san_chua_phan_data.append({
                    'ma_tai_san': taisan.ma_tai_san,
                    'ten_tai_san': taisan.ten_tai_san,
                    'so_serial': taisan.so_serial,
                    'gia_mua': float(taisan.gia_mua)
                })
        else:
            tai_san_chua_phan_data = []
        
        #thong_ke_display.append("=" * 80)
        
        return JsonResponse({
            'thanh_cong': True,
            'thong_bao': 'Lấy thống kê tài sản theo nhân viên thành công',
            'thong_ke': thong_ke_display,
            #'tong_quan': {
              #  'tong_nhan_vien': tong_nhan_vien,
              #  'tong_tai_san': tong_tai_san,
            #    'tai_san_chua_phan_cong': tai_san_chua_phan
        #    },
            'du_lieu_chi_tiet': data,
            'tai_san_chua_phan_cong': tai_san_chua_phan_data
        }, status=200)
        
    except Exception as e:
        return JsonResponse({
            'that_bai': False,
            'thong_bao': f'Lỗi khi lấy thống kê: {str(e)}',
            'du_lieu': []
        }, status=500)
>>>>>>> 451ac883a4c968da4f1c5dafd32fec2f74a73186
