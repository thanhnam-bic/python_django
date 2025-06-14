from django.test import TestCase
import json
from rest_framework.test import APIClient
from qlts.models import TaiSan, DanhMuc, NhanVien, NhaSanXuat, NhaCungCap
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class TaiSanAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="admin", password="12345678", is_staff=True, is_superuser=True)
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.danh_muc = DanhMuc.objects.create(danh_muc="DanhMuc01", loai="TaiSan", so_luong=1, tao_luc="2023-01-01T00:00:00Z", cap_nhat_luc="2023-01-01T00:00:00Z")
        self.nhan_vien = NhanVien.objects.create(ma_nhan_vien="NV001", ten="test", ho="nguyen", ten_dang_nhap="user", email="nhanvien@gmail.com")
        self.nsx = NhaSanXuat.objects.create(nha_san_xuat="NSX01", tai_san=1, tao_luc="2023-01-01T00:00:00Z", cap_nhat_luc="2023-01-01T00:00:00Z")
        self.ncc = NhaCungCap.objects.create(nha_cung_cap="NCC01", ten_lien_he="Lien He", duong_dan="Duong Dan", tai_san=1, tao_luc="2023-01-01T00:00:00Z", cap_nhat_luc="2023-01-01T00:00:00Z")

        self.taisan = TaiSan.objects.create(
            ma_tai_san="TS001",
            ten_tai_san="Tài sản 01",
            so_serial="123456",
            gia_mua=1000000,
            danh_muc=self.danh_muc,
            ma_nhan_vien=self.nhan_vien,
            nha_san_xuat=self.nsx,
            nha_cung_cap=self.ncc
        )
    def test_lay_tat_ca_tai_san(self):
            res = self.client.get("/qlts/api/lay_tat_ca_tai_san/")
            self.assertEqual(res.status_code, 200)
            self.assertTrue(res.json()["thanh_cong"])

    def test_chi_tiet_tai_san(self):
        res = self.client.get(f"/qlts/api/chi_tiet_tai_san/{self.taisan.ma_tai_san}/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["du_lieu"]["ma_tai_san"], "TS001")

    def test_cap_nhat_tai_san(self):
        payload = {
            "ten_tai_san": "Updated",
            "gia_mua": 2000000
        }
        res = self.client.put(
            f"/qlts/api/cap_nhat_tai_san/{self.taisan.ma_tai_san}/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["du_lieu"]["ten_tai_san"], "Updated")


    def test_xoa_tai_san(self):
        res = self.client.delete(f"/qlts/api/xoa_tai_san/{self.taisan.ma_tai_san}/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["du_lieu"]["ma_tai_san"], "TS001")

    def test_thong_ke_tai_san_nhan_vien(self):
        res = self.client.get(f"/qlts/api/tinh_tai_san_nhan_vien/")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["thong_bao"], "Thống kê thành công")

    def test_tao_tai_san(self):
        payload = {
            "ma_tai_san": "TS006",
            "ten_tai_san": "Tài sản 01",
            "so_serial": "98765",
            "gia_mua": 1500000,
            "danh_muc": self.danh_muc.danh_muc,
            "ma_nhan_vien": self.nhan_vien.ma_nhan_vien,
            "nha_san_xuat": self.nsx.nha_san_xuat,
            "nha_cung_cap": self.ncc.nha_cung_cap
        }
        res = self.client.post("/qlts/api/tao_tai_san/", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json()["du_lieu"]["ma_tai_san"], "TS006")
        
    def test_user_khong_co_quyen(self):
        # Tạo user không phải staff
        user1 = User.objects.create_user(username="user1", password="12345678", is_staff=False)
        token1 = str(RefreshToken.for_user(user1).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token1}")

        # Thử xóa tài sản và kiểm tra quyền truy cập
        res = self.client.delete(f"/qlts/api/xoa_tai_san/{self.taisan.ma_tai_san}/")
        self.assertEqual(res.status_code, 403)