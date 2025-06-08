from qlts.models import ViTri, NhanVien, DanhMuc, NhaSanXuat, NhaCungCap, TaiSan

# === ViTri ===
vitris = []
for i in range(1, 6):
    v = ViTri.objects.create(
        vi_tri=f"VT{i:02}",
        so_nguoi=5 * i,
        dia_chi=f"{i*10} Đường ABC",
        thanh_pho="Hà Nội" if i % 2 == 0 else "Hồ Chí Minh"
    )
    vitris.append(v)

# === NhanVien ===
nhanviens = []
for i in range(1, 6):
    nv = NhanVien.objects.create(
        ma_nhan_vien=f"NV{i:03}",
        ten=f"Tên{i}",
        ho=f"Họ{i}",
        ten_dang_nhap=f"user{i}",
        email=f"user{i}@example.com",
        vi_tri=vitris[i % 5]
    )
    nhanviens.append(nv)

# === DanhMuc ===
danhmucs = []
for i in range(1, 6):
    dm = DanhMuc.objects.create(
        danh_muc=f"DanhMuc{i}",
        loai="Thiết bị" if i % 2 == 0 else "Nội thất",
        so_luong=10 * i
    )
    danhmucs.append(dm)

# === NhaSanXuat ===
nha_san_xuats = []
for i in range(1, 6):
    nsx = NhaSanXuat.objects.create(
        nha_san_xuat=f"NSX{i}",
        tai_san=100 + i
    )
    nha_san_xuats.append(nsx)

# === NhaCungCap ===
nha_cung_caps = []
for i in range(1, 6):
    ncc = NhaCungCap.objects.create(
        nha_cung_cap=f"NCC{i}",
        ten_lien_he=f"Liên hệ {i}",
        duong_dan=f"https://ncc{i}.vn",
        tai_san=200 + i
    )
    nha_cung_caps.append(ncc)

# === TaiSan ===
for i in range(1, 6):
    TaiSan.objects.create(
        ma_tai_san=f"TS{i:03}",
        ten_tai_san=f"Tài sản {i}",
        so_serial=f"SERIAL{i*1000}",
        danh_muc=danhmucs[i % 5],
        ma_nhan_vien=nhanviens[i % 5],
        nha_san_xuat=nha_san_xuats[i % 5],
        nha_cung_cap=nha_cung_caps[i % 5],
        gia_mua=1000000.00 * i
    )
