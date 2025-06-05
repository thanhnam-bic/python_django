from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import TaiSan, DanhMuc, NhanVien, NhaSanXuat, NhaCungCap
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_http_methods


def index(request):
    print(">> Đã vào view index")
    return HttpResponse("Xin chào. Bạn đã đến app QLTS")

@csrf_exempt
def xoa_tai_san(request, id):
    if request.method == 'DELETE':
        try:
            asset = TaiSan.objects.get(pk=id)
            asset.delete()
            return JsonResponse({'message': 'Xóa tài sản thành công', 'ma_tai_san': id})
        except TaiSan.DoesNotExist:
            return JsonResponse({'error': 'Tài sản không tồn tại', 'ma_tai_san': id}, status=404)
    else:
        return JsonResponse({'error': 'Chỉ hỗ trợ phương thức DELETE'}, status=405)

# Create your views here.
# tạo phương thức get lấy danh sách và in dánh sách khi test trên postman khi truy cập đường link http://127.0.0.1:8000/qlts/api/taisan 
    # API GET - Lấy danh sách tất cả tài sản
@require_http_methods(["GET"])
def get_tat_ca_taisan(request):
    try:
        # Lấy tất cả tài sản từ database
        taisan_list = TaiSan.objects.all()
        
        # Tạo danh sách hiển thị đẹp
        danh_sach_display = []
        danh_sach_display.append("=" * 80)
        danh_sach_display.append("DANH SÁCH TẤT CẢ TÀI SẢN")
        danh_sach_display.append("=" * 80)
        danh_sach_display.append(f"Tổng số tài sản: {taisan_list.count()}")
        danh_sach_display.append("-" * 80)
        
        for i, taisan in enumerate(taisan_list, 1):
            danh_sach_display.append(f"{i}. Mã tài sản: {taisan.ma_tai_san}")
            danh_sach_display.append(f"   Tên tài sản: {taisan.ten_tai_san}")
            danh_sach_display.append(f"   Số serial: {taisan.so_serial}")
            danh_sach_display.append(f"   Giá mua: {taisan.gia_mua:,.0f} VND")
            danh_sach_display.append(f"   Danh mục: {taisan.danh_muc.danh_muc if taisan.danh_muc else 'Chưa có'}")
            danh_sach_display.append(f"   Nhân viên: {taisan.ma_nhan_vien.ma_nhan_vien if taisan.ma_nhan_vien else 'Chưa có'}")
            danh_sach_display.append(f"   Nhà sản xuất: {taisan.nha_san_xuat.nha_san_xuat if taisan.nha_san_xuat else 'Chưa có'}")
            danh_sach_display.append(f"   Nhà cung cấp: {taisan.nha_cung_cap.nha_cung_cap if taisan.nha_cung_cap else 'Chưa có'}")
            danh_sach_display.append("-" * 80)
        
        danh_sach_display.append("=" * 80)
        
        # Chuyển đổi dữ liệu thành dictionary để trả về chi tiết
        data = []
        for taisan in taisan_list:
            taisan_data = {
                'ma_tai_san': taisan.ma_tai_san,
                'ten_tai_san': taisan.ten_tai_san,
                'so_serial': taisan.so_serial,
                'gia_mua': float(taisan.gia_mua),
                'danh_muc': {
                    'danh_muc': taisan.danh_muc.danh_muc if taisan.danh_muc else None,
                    'loai': taisan.danh_muc.loai if taisan.danh_muc else None,
                    'so_luong': taisan.danh_muc.so_luong if taisan.danh_muc else None
                } if taisan.danh_muc else None,
                'ma_nhan_vien': {
                    'ma_nhan_vien': taisan.ma_nhan_vien.ma_nhan_vien if taisan.ma_nhan_vien else None,
                    'ten': taisan.ma_nhan_vien.ten if taisan.ma_nhan_vien else None,
                    'ho': taisan.ma_nhan_vien.ho if taisan.ma_nhan_vien else None,
                    'email': taisan.ma_nhan_vien.email if taisan.ma_nhan_vien else None
                } if taisan.ma_nhan_vien else None,
                'nha_san_xuat': {
                    'nha_san_xuat': taisan.nha_san_xuat.nha_san_xuat if taisan.nha_san_xuat else None,
                    'tai_san': taisan.nha_san_xuat.tai_san if taisan.nha_san_xuat else None
                } if taisan.nha_san_xuat else None,
                'nha_cung_cap': {
                    'nha_cung_cap': taisan.nha_cung_cap.nha_cung_cap if taisan.nha_cung_cap else None,
                    'ten_lien_he': taisan.nha_cung_cap.ten_lien_he if taisan.nha_cung_cap else None,
                    'duong_dan': taisan.nha_cung_cap.duong_dan if taisan.nha_cung_cap else None
                } if taisan.nha_cung_cap else None
            }
            data.append(taisan_data)
        
        return JsonResponse({
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
# tạo phương thức post tao tai san khi truy cập đường link http://127.0.0.1:8000/qlts/api/taisan/add
    # API POST - Tạo tài sản mới
@csrf_exempt
@require_http_methods(["POST"])
def tao_taisan(request):
    try:
        # Parse JSON data từ request body
        data = json.loads(request.body)
        
        # Kiểm tra các field bắt buộc
        required_fields = ['ma_tai_san', 'ten_tai_san', 'so_serial', 'gia_mua']
        for field in required_fields:
            if field not in data or not data[field]:
                return JsonResponse({
                    'Thông báo': f'Thiếu thông tin bắt buộc: {field}',
                    'Dữ liệu': None
                }, status=400)
        
        # Kiểm tra mã tài sản đã tồn tại chưa
        if TaiSan.objects.filter(ma_tai_san=data['ma_tai_san']).exists():
            return JsonResponse({
                'Thông báo': 'Mã tài sản đã tồn tại',
                'Dữ liệu': None
            }, status=400)
        
        # Xử lý foreign key relationships
        danh_muc = None
        if 'danh_muc' in data and data['danh_muc']:
            try:
                danh_muc = DanhMuc.objects.get(danh_muc=data['danh_muc'])
            except DanhMuc.DoesNotExist:
                return JsonResponse({
                    'Thông báo': f'Danh mục "{data["danh_muc"]}" không tồn tại',
                    'Dữ liệu': None
                }, status=400)
        
        ma_nhan_vien = None
        if 'ma_nhan_vien' in data and data['ma_nhan_vien']:
            try:
                ma_nhan_vien = NhanVien.objects.get(ma_nhan_vien=data['ma_nhan_vien'])
            except NhanVien.DoesNotExist:
                return JsonResponse({
                    'Thông báo': f'Nhân viên "{data["ma_nhan_vien"]}" không tồn tại',
                    'Dữ liệu': None
                }, status=400)
        
        nha_san_xuat = None
        if 'nha_san_xuat' in data and data['nha_san_xuat']:
            try:
                nha_san_xuat = NhaSanXuat.objects.get(nha_san_xuat=data['nha_san_xuat'])
            except NhaSanXuat.DoesNotExist:
                return JsonResponse({
                    'Thông báo': f'Nhà sản xuất "{data["nha_san_xuat"]}" không tồn tại',
                    'Dữ liệu': None
                }, status=400)
        
        nha_cung_cap = None
        if 'nha_cung_cap' in data and data['nha_cung_cap']:
            try:
                nha_cung_cap = NhaCungCap.objects.get(nha_cung_cap=data['nha_cung_cap'])
            except NhaCungCap.DoesNotExist:
                return JsonResponse({
                    'Thông báo': f'Nhà cung cấp "{data["nha_cung_cap"]}" không tồn tại',
                    'Dữ liệu': None
                }, status=400)
        
        # Tạo tài sản mới
        taisan = TaiSan.objects.create(
            ma_tai_san=data['ma_tai_san'],
            ten_tai_san=data['ten_tai_san'],
            so_serial=data['so_serial'],
            gia_mua=data['gia_mua'],
            danh_muc=danh_muc,
            ma_nhan_vien=ma_nhan_vien,
            nha_san_xuat=nha_san_xuat,
            nha_cung_cap=nha_cung_cap
        )
        
        # Trả về thông tin tài sản vừa tạo
        response_data = {
            'ma_tai_san': taisan.ma_tai_san,
            'ten_tai_san': taisan.ten_tai_san,
            'so_serial': taisan.so_serial,
            'gia_mua': float(taisan.gia_mua),
            'danh_muc': taisan.danh_muc.danh_muc if taisan.danh_muc else None,
            'ma_nhan_vien': taisan.ma_nhan_vien.ma_nhan_vien if taisan.ma_nhan_vien else None,
            'nha_san_xuat': taisan.nha_san_xuat.nha_san_xuat if taisan.nha_san_xuat else None,
            'nha_cung_cap': taisan.nha_cung_cap.nha_cung_cap if taisan.nha_cung_cap else None
        }
        
        return JsonResponse({
            'Thông báo': 'Tạo tài sản thành công',
            'Dữ liệu gồm có': response_data
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'Thông báo': 'Dữ liệu JSON không hợp lệ',
            'Dữ liệu': None
        }, status=400)
        
    except Exception as e:
        return JsonResponse({
            'Thông báo': f'Lỗi khi tạo tài sản: {str(e)}',
            'Dữ liệu': None
        }, status=500)
