
from ..models import TaiSan, NhanVien
import logging
from django.db.models import Sum
from django.views import View
logger = logging.getLogger(__name__)

class TinhTaiSanNhanVien(View):
    """
    Class để thống kê tài sản theo nhân viên
    """
    def __init__(self):
        pass
    
    def get(self, request):
            # Lấy tất cả nhân viên
            try:
                nhanvien_list = NhanVien.objects.all()
            except Exception as db_error:
                logger.error(f"Lỗi khi truy vấn danh sách nhân viên: {str(db_error)}")
                return {
                    "thanh_cong": False,
                    "thong_bao": "Lỗi máy chủ nội bộ.",
                    "ma_loi": {
                        "database": f'Không thể truy vấn danh sách nhân viên: {str(db_error)}'
                    },
                    "status_code": 500
                }
            
            
            # Dữ liệu chi tiết cho API
            data = []
            
            try:
                for i, nhanvien in enumerate(nhanvien_list, 1):
                    # Đếm số tài sản của nhân viên này
                    tai_san_list = TaiSan.objects.filter(ma_nhan_vien=nhanvien)
                    so_tai_san = tai_san_list.count()
                    tong_gia_tri_tai_san = TaiSan.objects.filter(ma_nhan_vien=nhanvien).aggregate(Sum('gia_mua'))['gia_mua__sum'] or 0
                    tong_gia_tri_tai_san_vnd = f"{tong_gia_tri_tai_san:,.0f} VND"
                
                    # Thêm vào data để trả về
                    tai_san_data = []
                    for taisan in tai_san_list:
                        try:
                            taisan_data = {
                                'ma_tai_san': taisan.ma_tai_san,
                                'ten_tai_san': taisan.ten_tai_san,
                                'so_serial': taisan.so_serial,
                                'gia_mua': f"{taisan.gia_mua:,.0f} VND",
                                'ma_nhan_vien': {
                                    'ma_nhan_vien': taisan.ma_nhan_vien.ma_nhan_vien if taisan.ma_nhan_vien else None,
                                } if taisan.ma_nhan_vien else None,
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
                        'ho_ten': f"{nhanvien.ho} {nhanvien.ten}",
                        'so_tai_san_quan_ly': so_tai_san,
                        'tong_gia_tri_tai_san': tong_gia_tri_tai_san_vnd,
                        'danh_sach_cac_tai_san': tai_san_data
                    }
                    data.append(nhanvien_data)
            except Exception as loop_error:
                logger.error(f"Lỗi khi xử lý dữ liệu nhân viên: {str(loop_error)}")
                return {
                    "thanh_cong": False,
                    "thong_bao": "Đã xảy ra lỗi không mong muốn trên máy chủ. Vui lòng thử lại sau.",
                    "ma_loi": {
                        "database": f'lỗi khi xử lý dữ liệu nhân viên: {str(loop_error)}'
                    },
                    "status_code": 500
                }
            return {
                "thanh_cong": True,
                "thong_bao": "Thống kê thành công",
                "du_lieu": data
            }