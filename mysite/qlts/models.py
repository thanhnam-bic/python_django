from django.db import models

class ViTri(models.Model):
    vi_tri = models.CharField(max_length=150, primary_key=True)
    so_nguoi = models.IntegerField()
    dia_chi = models.CharField(max_length=150)
    thanh_pho = models.CharField(max_length=150)
    tao_luc = models.DateTimeField(auto_now_add=True)
    cap_nhat_luc = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vi_tri} - {self.thanh_pho}"


class NhanVien(models.Model):
    ma_nhan_vien = models.CharField(max_length=10, primary_key=True)
    ten = models.CharField(max_length=150)
    ho = models.CharField(max_length=150)
    ten_dang_nhap = models.CharField(max_length=150)
    vi_tri = models.ForeignKey(ViTri, on_delete=models.SET_NULL, null=True)
    email = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.ho} {self.ten} ({self.ma_nhan_vien})"


class DanhMuc(models.Model):
    danh_muc = models.CharField(max_length=150, primary_key=True)
    loai = models.CharField(max_length=150)
    so_luong = models.IntegerField()
    tao_luc = models.DateTimeField(auto_now_add=True)
    cap_nhat_luc = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.danh_muc} ({self.loai})"


class NhaSanXuat(models.Model):
    nha_san_xuat = models.CharField(max_length=150, primary_key=True)
    tai_san = models.IntegerField()
    tao_luc = models.DateTimeField(auto_now_add=True)
    cap_nhat_luc = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nha_san_xuat


class NhaCungCap(models.Model):
    nha_cung_cap = models.CharField(max_length=150, primary_key=True)
    ten_lien_he = models.CharField(max_length=150)
    duong_dan = models.CharField(max_length=150)
    tai_san = models.IntegerField()
    tao_luc = models.DateTimeField(auto_now_add=True)
    cap_nhat_luc = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nha_cung_cap} - {self.ten_lien_he}"


class TaiSan(models.Model):
    ma_tai_san = models.CharField(max_length=10, primary_key=True)
    ten_tai_san = models.CharField(max_length=150)
    so_serial = models.CharField(max_length=150)
    danh_muc = models.ForeignKey(DanhMuc, on_delete=models.SET_NULL, null=True)
    ma_nhan_vien = models.ForeignKey(NhanVien, on_delete=models.SET_NULL, null=True)
    nha_san_xuat = models.ForeignKey(NhaSanXuat, on_delete=models.SET_NULL, null=True)
    nha_cung_cap = models.ForeignKey(NhaCungCap, on_delete=models.SET_NULL, null=True)
    gia_mua = models.DecimalField(max_digits=150, decimal_places=2)

    def __str__(self):
        return f"{self.ten_tai_san} ({self.ma_tai_san})"
