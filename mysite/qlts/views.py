from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import TaiSan, DanhMuc, NhanVien, NhaSanXuat, NhaCungCap
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_http_methods
import logging
from django.core.exceptions import PermissionDenied
from django.http import Http404

# View index - Trang chủ của ứng dụng
def index(request):
    return HttpResponse("Xin chào. Bạn đã đến app QLTS")

# API DELETE - Xóa tài sản theo ID
@csrf_exempt
@require_http_methods(["DELETE"])
def xoa_tai_san(request, id):
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
                "thanh_cong": False,
                "thong_bao": "Không tìm thấy tài nguyên.",
                "loi": {
                    "id": "Không tồn tại ID này"
                }
            }, status=404)
        except Exception as e:
            return JsonResponse({
                "thanh_cong": False,
                "thong_bao": "Đã xảy ra lỗi không mong muốn trên máy chủ. Vui lòng thử lại sau"
            }, status=500)
      

# API GET - Lấy danh sách tất cả tài sản
# Thiết lập logging
logger = logging.getLogger(__name__)

@require_http_methods(["GET"])
def get_tat_ca_taisan(request):
    try:
        # Kiểm tra quyền truy cập (403)
        # Ví dụ: Chỉ cho phép user đã đăng nhập hoặc có quyền cụ thể
        '''if not request.user.is_authenticated:
            return JsonResponse({
                "thanh_cong": False,
                "thong_bao": "Không có quyền truy cập tài nguyên này.",
                "ma_loi": {
                    "authentication": "Người dùng chưa được xác thực"
                }
            }, status=403)
        '''
        # Có thể thêm kiểm tra quyền cụ thể
        # if not request.user.has_perm('mysite.view_taisan'):
        #     return JsonResponse({
        #         "thanh_cong": False,
        #         "thong_bao": "Không có quyền truy cập tài nguyên này.",
        #         "ma_loi": {
        #             "permission": "Người dùng không có quyền xem tài sản"
        #         }
        #     }, status=403)

        # Lấy tất cả tài sản từ database
        taisan_list = TaiSan.objects.all()
        
        # Kiểm tra nếu không có dữ liệu (404)
        if not taisan_list.exists():
            return JsonResponse({
                "thanh_cong": False,
                "thong_bao": "Không tìm thấy tài nguyên.",
                "ma_loi": {
                    "data": "Không có tài sản nào trong hệ thống"
                }
            }, status=404)
        
        # Chuyển đổi dữ liệu thành dictionary để trả về chi tiết
        data = []
        for taisan in taisan_list:
            try:
                taisan_data = {
                    'ma_tai_san': taisan.ma_tai_san,
                    'ten_tai_san': taisan.ten_tai_san,
                    'so_serial': taisan.so_serial,
                    'gia_mua': float(taisan.gia_mua),
                    'danh_muc': {
                        'ten_danh_muc': taisan.danh_muc.danh_muc if taisan.danh_muc else None,
                    } if taisan.danh_muc else None,
                    'ma_nhan_vien': {
                        'ma_nhan_vien': taisan.ma_nhan_vien.ma_nhan_vien if taisan.ma_nhan_vien else None,
                    } if taisan.ma_nhan_vien else None,
                    'nha_san_xuat': {
                         'ten_nha_san_xuat': taisan.nha_san_xuat.nha_san_xuat if taisan.nha_san_xuat else None,
                    } if taisan.nha_san_xuat else None,
                    'nha_cung_cap': {
                        'ten_nha_cung_cap': taisan.nha_cung_cap.nha_cung_cap if taisan.nha_cung_cap else None,
                    } if taisan.nha_cung_cap else None
                }
                data.append(taisan_data)
            except AttributeError as attr_error:
                # Xử lý lỗi thuộc tính không tồn tại
                logger.warning(f"Lỗi thuộc tính với tài sản {taisan.ma_tai_san}: {str(attr_error)}")
                continue
        
        # Trả về dữ liệu thành công
        return JsonResponse({
            'thanh_cong': True,
            'thong_bao': 'Lấy danh sách tài sản thành công',
            'du_lieu': {
                'tong_so_tai_san': len(data),
                'tai_san': data
            }
        }, status=200)
        
    except PermissionDenied:
        # Xử lý lỗi 403 - Forbidden
        return JsonResponse({
            "thanh_cong": False,
            "thong_bao": "Không có quyền truy cập tài nguyên này.",
            "ma_loi": {
                "permission": "Người dùng không có quyền thực hiện thao tác này"
            }
        }, status=403)
    
    except Http404:
        # Xử lý lỗi 404 - Not Found
        return JsonResponse({
            "thanh_cong": False,
            "thong_bao": "Không tìm thấy tài nguyên.",
            "ma_loi": {
                "resource": "Tài nguyên yêu cầu không tồn tại"
            }
        }, status=404)
    
    except Exception as e:
        # Xử lý lỗi 500 - Internal Server Error
        logger.error(f"Lỗi server khi lấy danh sách tài sản: {str(e)}")
        return JsonResponse({
            "thanh_cong": False,
            "thong_bao": "Lỗi máy chủ nội bộ.",
            "ma_loi": {
                "server": f"Lỗi hệ thống: {str(e)}"
            }
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