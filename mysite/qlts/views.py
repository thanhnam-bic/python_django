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
# tạo phương thức get lấy danh sách và in dánh sách khi test trên postman lúc truy cập đường link http://127.0.0.1:8000/qlts/api/taisan 
    # API GET - Lấy danh sách tất cả tài sản
@require_http_methods(["GET"])
def get_all_taisan(request):
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
            'success': True,
            'message': 'Lấy danh sách tài sản thành công',
            'danh_sach_display': danh_sach_display,
            'count': len(data),
            'data': data
        }, status=200)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Lỗi khi lấy danh sách tài sản: {str(e)}',
            'data': []
        }, status=500)
