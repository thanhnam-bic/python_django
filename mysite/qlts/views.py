from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import TaiSan, DanhMuc, NhanVien, NhaSanXuat, NhaCungCap
import json
import logging
from django.http import Http404
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import Kiem_Tra_Phan_Quyen_User
from .qlts_thong_ke_tai_san_nhan_vien.qlts_thong_ke_tai_san_nhan_vien import TinhTaiSanNhanVien

# View index - Trang chủ của ứng dụng
def index(request):
    return HttpResponse("Xin chào. Bạn đã đến app quản lý Tài sản. Đây là trang chủ của ứng dụng")

#1 API DELETE - Xóa tài sản theo ID
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([Kiem_Tra_Phan_Quyen_User])
def xoa_tai_san(request, id):
        try:
            asset = TaiSan.objects.get(pk=id)
            asset.delete()
            return JsonResponse({
                "thanh_cong": True,
                "thong_bao": "Xóa tài sản thành công",
                "du_lieu": {
                    "ma_tai_san": id
                }
            })

        except TaiSan.DoesNotExist:
            return JsonResponse({
                "thanh_cong": False,
                "thong_bao": "Không tìm thấy tài nguyên",
                "loi": {
                    "id": "Không tồn tại ID này"
                }
            }, status=404)
        except Exception as e:
            return JsonResponse({
                "thanh_cong": False,
                "thong_bao": "Đã xảy ra lỗi không mong muốn trên máy chủ. Vui lòng thử lại sau"
            }, status=500)

#2 API PUT - Cập nhật tài sản theo ID
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([Kiem_Tra_Phan_Quyen_User])
def cap_nhat_tai_san(request, id):
    try:
        try:
            asset = TaiSan.objects.get(pk=id)
        except TaiSan.DoesNotExist:
            return JsonResponse({
                "thanh_cong": False,
                "thong_bao": "Không tìm thấy tài sản",
                "loi": {"ma_tai_san": f"Tài sản với mã {id} không tồn tại"}
            }, status=404)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                "thanh_cong": False,
                "thong_bao": "Dữ liệu gửi lên không hợp lệ",
                "loi": {"json": "JSON không đúng định dạng"}
            }, status=400)

        # Cập nhật các trường thông thường
        if 'ten_tai_san' in data:
            asset.ten_tai_san = data['ten_tai_san']
        if 'so_serial' in data:
            asset.so_serial = data['so_serial']
        if 'gia_mua' in data:
            asset.gia_mua = data['gia_mua']

        # Cập nhật các khóa ngoại nếu có
        if 'danh_muc' in data:
            try:
                asset.danh_muc = DanhMuc.objects.get(pk=data['danh_muc'])
            except DanhMuc.DoesNotExist:
                return JsonResponse({
                    "thanh_cong": False,
                    "thong_bao": "Không tìm thấy danh mục.",
                    "loi": {"danh_muc": f"Danh mục với mã {data['danh_muc']} không tồn tại"}
                }, status=400)

        if 'ma_nhan_vien' in data:
            try:
                asset.ma_nhan_vien = NhanVien.objects.get(pk=data['ma_nhan_vien'])
            except NhanVien.DoesNotExist:
                return JsonResponse({
                    "thanh_cong": False,
                    "thong_bao": "Không tìm thấy nhân viên.",
                    "loi": {"ma_nhan_vien": f"Nhân viên với mã {data['ma_nhan_vien']} không tồn tại"}
                }, status=400)

        if 'nha_san_xuat' in data:
            try:
                asset.nha_san_xuat = NhaSanXuat.objects.get(pk=data['nha_san_xuat'])
            except NhaSanXuat.DoesNotExist:
                return JsonResponse({
                    "thanh_cong": False,
                    "thong_bao": "Không tìm thấy nhà sản xuất",
                    "loi": {"nha_san_xuat": f"Nhà sản xuất với mã {data['nha_san_xuat']} không tồn tại"}
                }, status=400)

        if 'nha_cung_cap' in data:
            try:
                asset.nha_cung_cap = NhaCungCap.objects.get(pk=data['nha_cung_cap'])
            except NhaCungCap.DoesNotExist:
                return JsonResponse({
                    "thanh_cong": False,
                    "thong_bao": "Không tìm thấy nhà cung cấp",
                    "loi": {"nha_cung_cap": f"Nhà cung cấp với mã {data['nha_cung_cap']} không tồn tại"}
                }, status=400)

        asset.save()
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

    except Exception as e:
        return JsonResponse({
            "thanh_cong": False,
            "thong_bao": "Đã xảy ra lỗi không mong muốn trên máy chủ. Vui lòng thử lại sau"
        }, status=500)

#3 API GET - Lấy chi tiết tài sản theo ID
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([Kiem_Tra_Phan_Quyen_User])
def chi_tiet_tai_san(request, id):
    try:
        asset = TaiSan.objects.get(pk=id)
        du_lieu = {
            "ma_tai_san": asset.ma_tai_san,
            "ten_tai_san": asset.ten_tai_san,
            "so_serial": asset.so_serial,
            "gia_mua": f"{asset.gia_mua:,.0f} VND",
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
            "thanh_cong": False,
            "thong_bao": "Không tìm thấy tài nguyên",
            "ma_loi": {
                "id": "Không tồn tại ID này"
            }
        }, status=404)

    except Exception:
        return JsonResponse({
            "thanh_cong": False,
            "thong_bao": "Đã xảy ra lỗi không mong muốn trên máy chủ. Vui lòng thử lại sau"
        }, status=500) 

#4 API GET - Lấy danh sách tất cả tài sản
# Thiết lập logging
logger = logging.getLogger(__name__)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([Kiem_Tra_Phan_Quyen_User])
def lay_tat_ca_tai_san(request):
    try:
        # Lấy tất cả tài sản từ database
        taisan_list = TaiSan.objects.all()

        # Chuyển đổi dữ liệu thành dictionary để trả về chi tiết
        data = []
        for taisan in taisan_list:
            try:
                taisan_data = {
                    'ma_tai_san': taisan.ma_tai_san,
                    'ten_tai_san': taisan.ten_tai_san,
                    'so_serial': taisan.so_serial,
                    'gia_mua': f"{taisan.gia_mua:,.0f} VND",
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
        

    except Exception as e:
        # Xử lý lỗi 500 - Internal Server Error
        logger.error(f"Lỗi server khi lấy danh sách tài sản: {str(e)}")
        return JsonResponse({
            "thanh_cong": False,
            "thong_bao": "Đã xảy ra lỗi không mong muốn trên máy chủ. Vui lòng thử lại sau",
        }, status=500)

#5 API GET - Thống kê tài sản theo nhân viên
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([Kiem_Tra_Phan_Quyen_User])
def tinh_tai_san_moi_nhan_vien(request):
    try:
        # Lấy tất cả nhân viên
        try:
            nhanvien_list = NhanVien.objects.all()
        except Exception as db_error:
            logger.error(f"Lỗi khi truy vấn danh sách nhân viên: {str(db_error)}")
            return JsonResponse({
                "thanh_cong": False,
                "thong_bao": "Lỗi máy chủ nội bộ.",
                "ma_loi": {
                    "database": f'Không thể truy vấn danh sách nhân viên: {str(db_error)}'
                }
            }, status=500)
        
        # Tạo danh sách hiển thị thống kê
        thong_ke_display = []
        thong_ke_display.append("THỐNG KÊ SỐ TÀI SẢN THEO NHÂN VIÊN")
        
        # Tính tổng số nhân viên và tài sản
        try:
            tong_nhan_vien = nhanvien_list.count()
            tong_tai_san = TaiSan.objects.count()
            tai_san_chua_phan = TaiSan.objects.filter(ma_nhan_vien__isnull=True).count()
        except Exception as count_error:
            logger.error(f"Lỗi khi đếm số lượng: {str(count_error)}")
            return JsonResponse({
                "thanh_cong": False,
                "thong_bao": "Đã xảy ra lỗi không mong muốn trên máy chủ. Vui lòng thử lại sau",
                "ma_loi": {
                    "database": f'lỗi khi đếm số lượng: {str(count_error)}'
                }
            }, status=500)
        
        thong_ke_display.append(f"Tổng số nhân viên: {tong_nhan_vien}")
        thong_ke_display.append(f"Tổng số tài sản: {tong_tai_san}")
        thong_ke_display.append(f"Tài sản chưa phân công: {tai_san_chua_phan}")
        
        # Dữ liệu chi tiết cho API
        data = []
        
        try:
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
                
                # Thêm vào data để trả về
                tai_san_data = []
                for taisan in tai_san_list:
                    try:
                        taisan_data = {
                            'ma_tai_san': taisan.ma_tai_san,
                            'ten_tai_san': taisan.ten_tai_san,
                            'so_serial': taisan.so_serial,
                            'gia_mua': f"{taisan.gia_mua:,.0f} VND",
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
                        tai_san_data.append(taisan_data)
                    except AttributeError as attr_error:
                        logger.warning(f"Lỗi thuộc tính với tài sản {taisan.ma_tai_san}: {str(attr_error)}")
                        # Trả về dữ liệu cơ bản nếu có lỗi thuộc tính
                        taisan_data = {
                            'ma_tai_san': taisan.ma_tai_san,
                            'ten_tai_san': taisan.ten_tai_san,
                            'so_serial': taisan.so_serial,
                            'gia_mua': f"{taisan.gia_mua:,.0f} VND",
                        }
                        tai_san_data.append(taisan_data)
                
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
        except Exception as loop_error:
            logger.error(f"Lỗi khi xử lý dữ liệu nhân viên: {str(loop_error)}")
            return JsonResponse({
                "thanh_cong": False,
                "thong_bao": "Đã xảy ra lỗi không mong muốn trên máy chủ. Vui lòng thử lại sau.",
                "ma_loi": {
                    "database": f'lỗi khi xử lý dữ liệu nhân viên: {str(loop_error)}'
                }
            }, status=500)
        
        # Thêm thông tin tài sản chưa phân công
        try:
            if tai_san_chua_phan > 0:
                thong_ke_display.append(f"TÀI SẢN CHƯA PHÂN CÔNG ({tai_san_chua_phan} tài sản):")
                tai_san_chua_phan_list = TaiSan.objects.filter(ma_nhan_vien__isnull=True)
                for j, taisan in enumerate(tai_san_chua_phan_list, 1):
                    thong_ke_display.append(f"  {j}. {taisan.ma_tai_san} - {taisan.ten_tai_san}")
                
                # Thêm tài sản chưa phân công vào data
                tai_san_chua_phan_data = []
                for taisan in tai_san_chua_phan_list:
                    try:
                        taisan_data = {
                            'ma_tai_san': taisan.ma_tai_san,
                            'ten_tai_san': taisan.ten_tai_san,
                            'so_serial': taisan.so_serial,
                            'gia_mua': f"{taisan.gia_mua:,.0f} VND",
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
                        tai_san_chua_phan_data.append(taisan_data)
                    except AttributeError as attr_error:
                        logger.warning(f"Lỗi thuộc tính với tài sản chưa phân công {taisan.ma_tai_san}: {str(attr_error)}")
                        # Trả về dữ liệu cơ bản nếu có lỗi thuộc tính
                        taisan_data = {
                            'ma_tai_san': taisan.ma_tai_san,
                            'ten_tai_san': taisan.ten_tai_san,
                            'so_serial': taisan.so_serial,
                            'gia_mua': f"{taisan.gia_mua:,.0f} VND",
                        }
                        tai_san_chua_phan_data.append(taisan_data)
            else:
                tai_san_chua_phan_data = []
        except Exception as unassigned_error:
            logger.error(f"Lỗi khi xử lý tài sản chưa phân công: {str(unassigned_error)}")
            return JsonResponse({
                "thanh_cong": False,
                "thong_bao": "Đã xảy ra lỗi không mong muốn trên máy chủ. Vui lòng thử lại sau.",
                "ma_loi": {
                    "database": f'Lỗi khi xử lý tài sản chưa phân công: {str(unassigned_error)}'
                }
            }, status=500)
        
        return JsonResponse({
            'thanh_cong': True,
            'thong_bao': 'Lấy thống kê tài sản theo nhân viên thành công',
            'du_lieu': {
                'thong_ke': thong_ke_display,
                'du_lieu_chi_tiet': data,
                'tai_san_chua_phan_cong': tai_san_chua_phan_data,
                'tong_so_nhan_vien': len(data),
                'tong_so_tai_san_chua_phan_cong': len(tai_san_chua_phan_data)
            }
        }, status=200)

    
    except Http404:
        # Xử lý lỗi 404 - Not Found
        return JsonResponse({
            "thanh_cong": False,
            "thong_bao": "Không tìm thấy tài nguyên",
            "ma_loi": {
                "id": "Tài nguyên yêu cầu không tồn tại"
            }
        }, status=404)
    
    except Exception as e:
        # Xử lý lỗi 500 - Internal Server Error
        logger.error(f"Lỗi server khi lấy thống kê tài sản: {str(e)}")
        return JsonResponse({
            "thanh_cong": False,
            "thong_bao": "Đã xảy ra lỗi không mong muốn trên máy chủ. Vui lòng thử lại sau",
        }, status=500)

#6. API POST - tạo tài sản (api/tao_tai_san/)
# Thiết lập logging
logger = logging.getLogger(__name__)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([Kiem_Tra_Phan_Quyen_User])
def tao_tai_san(request):
    try:
        # Parse JSON data từ request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                'thanh_cong': False,
                'thong_bao': 'Dữ liệu JSON không hợp lệ',
                'ma_loi': {
                    'json': 'Định dạng JSON không đúng cú pháp'
                }
            }, status=400)

        # Kiểm tra các field bắt buộc
        required_fields = ['ma_tai_san', 'ten_tai_san', 'so_serial', 'gia_mua']
        missing_fields = {}
        
        for field in required_fields:
            if field not in data or not data[field]:
                missing_fields[field] = f'Trường {field} là bắt buộc và không được để trống'
        
        if missing_fields:
            return JsonResponse({
                'thanh_cong': False,
                'thong_bao': 'Thiếu thông tin bắt buộc',
                'ma_loi': missing_fields
            }, status=400)

        # Kiểm tra mã tài sản đã tồn tại chưa
        if TaiSan.objects.filter(ma_tai_san=data['ma_tai_san']).exists():
            return JsonResponse({
                'thanh_cong': False,
                'thong_bao': 'Mã tài sản đã tồn tại',
                'ma_loi': {
                    'ma_tai_san': f'Mã tài sản "{data["ma_tai_san"]}" đã được sử dụng'
                }
            }, status=400)

        # Xử lý foreign key relationships với xử lý 404
        danh_muc = None
        if 'danh_muc' in data and data['danh_muc']:
            try:
                danh_muc = DanhMuc.objects.get(danh_muc=data['danh_muc'])
            except DanhMuc.DoesNotExist:
                return JsonResponse({
                    "thanh_cong": False,
                    "thong_bao": "Không tìm thấy tài nguyên",
                    "ma_loi": {
                        "danh_muc": f'Danh mục "{data["danh_muc"]}" không tồn tại trong hệ thống'
                    }
                }, status=400)

        ma_nhan_vien = None
        if 'ma_nhan_vien' in data and data['ma_nhan_vien']:
            try:
                ma_nhan_vien = NhanVien.objects.get(ma_nhan_vien=data['ma_nhan_vien'])
            except NhanVien.DoesNotExist:
                return JsonResponse({
                    "thanh_cong": False,
                    "thong_bao": "Không tìm thấy tài nguyên",
                    "ma_loi": {
                        "ma_nhan_vien": f'Nhân viên "{data["ma_nhan_vien"]}" không tồn tại trong hệ thống'
                    }
                }, status=400)

        nha_san_xuat = None
        if 'nha_san_xuat' in data and data['nha_san_xuat']:
            try:
                nha_san_xuat = NhaSanXuat.objects.get(nha_san_xuat=data['nha_san_xuat'])
            except NhaSanXuat.DoesNotExist:
                return JsonResponse({
                    "thanh_cong": False,
                    "thong_bao": "Không tìm thấy tài nguyên",
                    "ma_loi": {
                        "nha_san_xuat": f'Nhà sản xuất "{data["nha_san_xuat"]}" không tồn tại trong hệ thống'
                    }
                }, status=400)

        nha_cung_cap = None
        if 'nha_cung_cap' in data and data['nha_cung_cap']:
            try:
                nha_cung_cap = NhaCungCap.objects.get(nha_cung_cap=data['nha_cung_cap'])
            except NhaCungCap.DoesNotExist:
                return JsonResponse({
                    "thanh_cong": False,
                    "thong_bao": "Không tìm thấy tài nguyên",
                    "ma_loi": {
                        "nha_cung_cap": f'Nhà cung cấp "{data["nha_cung_cap"]}" không tồn tại trong hệ thống'
                    }
                }, status=400)

        # Tạo tài sản mới
        try:
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
        except Exception as create_error:
            logger.error(f"Lỗi khi tạo tài sản: {str(create_error)}")
            return JsonResponse({
                "thanh_cong": False,
                "thong_bao": "Đã xảy ra lỗi không mong muốn trên máy chủ. Vui lòng thử lại sau",
            }, status=500)

        # Trả về thông tin tài sản vừa tạo
        try:
            response_data = {
                'ma_tai_san': taisan.ma_tai_san,
                'ten_tai_san': taisan.ten_tai_san,
                'so_serial': taisan.so_serial,
                'gia_mua': f"{taisan.gia_mua:,.0f} VND",
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
        except AttributeError as attr_error:
            logger.warning(f"Lỗi thuộc tính với tài sản {taisan.ma_tai_san}: {str(attr_error)}")
            # Trả về dữ liệu cơ bản nếu có lỗi thuộc tính
            response_data = {
                'ma_tai_san': taisan.ma_tai_san,
                'ten_tai_san': taisan.ten_tai_san,
                'so_serial': taisan.so_serial,
                'gia_mua': f"{taisan.gia_mua:,.0f} VND",
            }

        return JsonResponse({
            'thanh_cong': True,
            'thong_bao': 'Tạo tài sản thành công',
            'du_lieu': response_data
        }, status=201)

    
    except Exception as e:
        # Xử lý lỗi 500 - Internal Server Error
        logger.error(f"Lỗi server khi tạo tài sản: {str(e)}")
        return JsonResponse({
            "thanh_cong": False,
            "thong_bao": "Đã xảy ra lỗi không mong muốn trên máy chủ. Vui lòng thử lại sau",
        }, status=500)
        


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([Kiem_Tra_Phan_Quyen_User])
def tinh_tai_san_nhan_vien(request):
    try:
        thong_ke = TinhTaiSanNhanVien()
        result = thong_ke.get(request)
        return JsonResponse(result, status=result.get("status_code", 200))
    except Exception as e:
        logger.error(f"Lỗi server khi lấy thống kê tài sản: {str(e)}")
        return JsonResponse({
            "thanh_cong": False,
            "thong_bao": "Đã xảy ra lỗi không mong muốn trên máy chủ. Vui lòng thử lại sau",
        }, status=500)