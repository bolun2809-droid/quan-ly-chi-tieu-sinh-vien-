import pandas as pd

def load_data(filepath_or_records):
    """
    Tạo DataFrame từ file CSV hoặc list các dict.
    Cột kỳ vọng: 'ngay', 'danh_muc', 'so_tien', 'mo_ta' (tuỳ chỉnh theo dữ liệu thực tế)
    """
    if isinstance(filepath_or_records, str):
        df = pd.read_csv(filepath_or_records)
    else:
        df = pd.DataFrame(filepath_or_records)
    return df


def tinh_tong_tien(df, cot_so_tien="so_tien"):
    """Tính tổng chi tiêu."""
    return df[cot_so_tien].sum()


def tinh_trung_binh_chi_tieu(df, cot_so_tien="so_tien"):
    """Tính trung bình chi tiêu mỗi giao dịch."""
    return df[cot_so_tien].mean()


def gom_nhom_theo_danh_muc(df, cot_danh_muc="danh_muc", cot_so_tien="so_tien"):
    """
    Gom nhóm dữ liệu theo danh mục (học tập, ăn uống, giải trí...),
    trả về tổng và trung bình chi tiêu của từng danh mục.
    """
    ket_qua = df.groupby(cot_danh_muc)[cot_so_tien].agg(
        tong_tien="sum",
        trung_binh="mean",
        so_giao_dich="count"
    ).reset_index()
    return ket_qua


def tong_hop_thong_ke(df, cot_danh_muc="danh_muc", cot_so_tien="so_tien"):
    """Trả về bộ thống kê tổng hợp: tổng tiền, trung bình, gom nhóm."""
    return {
        "tong_tien": tinh_tong_tien(df, cot_so_tien),
        "trung_binh_chi_tieu": tinh_trung_binh_chi_tieu(df, cot_so_tien),
        "theo_danh_muc": gom_nhom_theo_danh_muc(df, cot_danh_muc, cot_so_tien)
    }


# --- Ví dụ sử dụng ---
if __name__ == "__main__":
    du_lieu_mau = [
        {"danh_muc": "hoc_tap", "so_tien": 200000},
        {"danh_muc": "an_uong", "so_tien": 50000},
        {"danh_muc": "an_uong", "so_tien": 75000},
        {"danh_muc": "giai_tri", "so_tien": 150000},
        {"danh_muc": "hoc_tap", "so_tien": 300000},
    ]

    df = load_data(du_lieu_mau)
    thong_ke = tong_hop_thong_ke(df)