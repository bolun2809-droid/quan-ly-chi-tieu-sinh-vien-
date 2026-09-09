"""
=====================================================================
ỨNG DỤNG QUẢN LÝ & PHÂN TÍCH CHI TIÊU SINH VIÊN
Module: GIAO DIỆN NGƯỜI DÙNG (UI) - Thành viên 5
=====================================================================
Mô tả:
    Đây là phần GIAO DIỆN (UI) của ứng dụng, xây dựng bằng Streamlit.
    App cho phép người dùng:
        1. Upload file CSV dữ liệu chi tiêu sinh viên
        2. Xem tổng quan dữ liệu (đã làm sạch)
        3. Xem thống kê chi tiêu (số liệu tổng hợp)
        4. Xem các biểu đồ trực quan hóa
        5. Lọc/tìm kiếm dữ liệu theo giới tính, năm học, chuyên ngành
        6. Tải xuống dữ liệu đã xử lý

GHI CHÚ CHO NHÓM:
    - Các hàm clean_data(), analyze_data(), plot_*() bên dưới là bản
      DEMO đơn giản để UI chạy được ngay. Khi Thành viên 2 (Data
      Cleaning), Thành viên 3 (Data Analysis), Thành viên 4 (Data
      Visualization) hoàn thiện module riêng, chỉ cần import hàm của
      các bạn vào và thay thế các hàm tương ứng bên dưới - phần giao
      diện (layout, widget) KHÔNG cần sửa gì thêm.
    - Cấu trúc thư mục đề xuất cho cả nhóm:

        student_app/
        ├── app.py                  <- File này (UI - Thành viên 5)
        ├── modules/
        │   ├── data_cleaning.py    <- Thành viên 2
        │   ├── data_analysis.py    <- Thành viên 3
        │   └── data_viz.py         <- Thành viên 4
        ├── requirements.txt
        └── README.md

Cách chạy:
   python -m pip install -r requirements.txt
   python -m streamlit run app.py
=====================================================================
"""

import io

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# ---------------------------------------------------------------
# CẤU HÌNH TRANG
# ---------------------------------------------------------------
st.set_page_config(
    page_title="Quản lý chi tiêu sinh viên",
    page_icon="🎓",
    layout="wide",
)

# Các cột bắt buộc phải có trong file CSV đầu vào.
# (khớp với bộ dữ liệu "Student Spending Habits" đã dùng để phân tích)
REQUIRED_COLUMNS = [
    "age", "gender", "year_in_school", "major",
    "monthly_income", "financial_aid",
    "tuition", "housing", "food", "transportation",
    "books_supplies", "entertainment", "personal_care",
    "technology", "health_wellness", "miscellaneous",
    "preferred_payment_method",
]

SPENDING_COLUMNS = [
    "housing", "food", "transportation", "books_supplies",
    "entertainment", "personal_care", "technology",
    "health_wellness", "miscellaneous",
]


# =================================================================
# 1. XỬ LÝ DỮ LIỆU ĐẦU VÀO (đọc + kiểm tra lỗi cơ bản)
# =================================================================
def load_data(uploaded_file):
    """
    Đọc file CSV người dùng upload và kiểm tra tính hợp lệ.

    Trả về:
        (DataFrame, list các cảnh báo) nếu đọc thành công
        (None, thông báo lỗi) nếu thất bại
    """
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        return None, [f"❌ Không đọc được file CSV: {e}"]

    warnings = []

    # Chuẩn hóa tên cột: chữ thường, bỏ khoảng trắng thừa
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Kiểm tra thiếu cột bắt buộc
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        warnings.append(
            "⚠️ File thiếu các cột: " + ", ".join(missing_cols) +
            " — một số chức năng có thể không hoạt động đầy đủ."
        )

    if df.empty:
        return None, ["❌ File CSV không có dữ liệu."]

    return df, warnings


# =================================================================
# 2. LÀM SẠCH DỮ LIỆU
#    (bản demo - sẽ được thay bằng module của Thành viên 2)
# =================================================================
def clean_data(df: pd.DataFrame):
    """
    Làm sạch dữ liệu cơ bản:
      - Ép kiểu số cho các cột chi tiêu/thu nhập, giá trị lỗi -> NaN
      - Điền giá trị thiếu bằng trung vị (median) cho cột số
      - Xóa dòng trùng lặp hoàn toàn
    Trả về: (df đã sạch, số dòng trùng đã xóa, số ô dữ liệu đã điền)
    """
    df = df.copy()

    numeric_cols = [
        c for c in ["age", "monthly_income", "financial_aid", "tuition"]
        + SPENDING_COLUMNS
        if c in df.columns
    ]

    filled_count = 0
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        n_missing = df[col].isna().sum()
        if n_missing > 0:
            df[col] = df[col].fillna(df[col].median())
            filled_count += int(n_missing)

    before = len(df)
    df = df.drop_duplicates()
    duplicates_removed = before - len(df)

    # Chuẩn hóa cột phân loại (bỏ khoảng trắng thừa, viết hoa chữ đầu)
    for col in ["gender", "year_in_school", "major", "preferred_payment_method"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    return df, duplicates_removed, filled_count


# =================================================================
# 3. PHÂN TÍCH DỮ LIỆU
#    (bản demo - sẽ được thay bằng module của Thành viên 3)
# =================================================================
def analyze_data(df: pd.DataFrame):
    """Tính các số liệu thống kê tổng hợp."""
    stats = {}
    available_spending = [c for c in SPENDING_COLUMNS if c in df.columns]

    if available_spending:
        df["total_spending"] = df[available_spending].sum(axis=1)
        stats["avg_total_spending"] = df["total_spending"].mean()
        stats["max_total_spending"] = df["total_spending"].max()
        stats["min_total_spending"] = df["total_spending"].min()

    if "monthly_income" in df.columns:
        stats["avg_income"] = df["monthly_income"].mean()

    if "financial_aid" in df.columns:
        stats["avg_financial_aid"] = df["financial_aid"].mean()

    stats["so_sinh_vien"] = len(df)
    return df, stats


# =================================================================
# 4. TRỰC QUAN HÓA DỮ LIỆU
#    (bản demo - sẽ được thay bằng module của Thành viên 4)
# =================================================================
def plot_spending_breakdown(df: pd.DataFrame):
    """Biểu đồ tròn: tỷ trọng chi tiêu trung bình theo hạng mục."""
    available = [c for c in SPENDING_COLUMNS if c in df.columns]
    if not available:
        return None
    means = df[available].mean().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(means, labels=means.index, autopct="%1.1f%%", startangle=90)
    ax.set_title("Tỷ trọng chi tiêu trung bình theo hạng mục")
    return fig


def plot_spending_by_group(df: pd.DataFrame, group_col: str):
    """Biểu đồ cột: tổng chi tiêu trung bình theo nhóm (giới tính/năm học/ngành)."""
    if group_col not in df.columns or "total_spending" not in df.columns:
        return None
    grouped = df.groupby(group_col)["total_spending"].mean().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=grouped.index, y=grouped.values, ax=ax)
    ax.set_ylabel("Chi tiêu trung bình (Housing+Food+...)")
    ax.set_xlabel(group_col)
    ax.set_title(f"Chi tiêu trung bình theo {group_col}")
    plt.xticks(rotation=20)
    return fig


def plot_income_distribution(df: pd.DataFrame):
    """Biểu đồ histogram phân bố thu nhập hàng tháng."""
    if "monthly_income" not in df.columns:
        return None
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(df["monthly_income"], bins=20, kde=True, ax=ax)
    ax.set_title("Phân bố thu nhập hàng tháng của sinh viên")
    ax.set_xlabel("Thu nhập hàng tháng ($)")
    return fig


# =================================================================
# 5. GIAO DIỆN CHÍNH (UI) - Thành viên 5 chịu trách nhiệm chính
# =================================================================
def main():
    st.title("🎓 Ứng dụng Quản lý & Phân tích Chi tiêu Sinh viên")
    st.caption(
        "Bài tập lớn học phần Ngôn ngữ lập trình Python — "
        "Module giao diện (UI) do Thành viên 5 phụ trách."
    )

    # ---------------- SIDEBAR: upload + hướng dẫn ----------------
    with st.sidebar:
        st.header("📂 Nhập dữ liệu")
        uploaded_file = st.file_uploader(
            "Tải lên file CSV dữ liệu sinh viên", type=["csv"]
        )
        st.markdown("---")
        st.markdown(
            "**Hướng dẫn:**\n"
            "1. Chuẩn bị file CSV chứa dữ liệu chi tiêu sinh viên.\n"
            "2. Upload file ở trên.\n"
            "3. Dùng bộ lọc để xem theo nhóm.\n"
            "4. Xem kết quả ở các tab bên phải."
        )

    if uploaded_file is None:
        st.info("👈 Vui lòng upload file CSV để bắt đầu.")
        st.markdown(
            "Các cột dữ liệu mong đợi:\n\n`" + ", ".join(REQUIRED_COLUMNS) + "`"
        )
        return

    # ---------------- Xử lý dữ liệu (đọc -> lỗi cơ bản) ----------------
    df_raw, messages = load_data(uploaded_file)
    for m in messages:
        if m.startswith("❌"):
            st.error(m)
        else:
            st.warning(m)

    if df_raw is None:
        st.stop()  # Dừng chương trình nếu dữ liệu không hợp lệ

    df_clean, dup_removed, filled_cells = clean_data(df_raw)
    df_analyzed, stats = analyze_data(df_clean)

    st.success(
        f"✅ Đã xử lý {len(df_analyzed)} dòng dữ liệu "
        f"(loại {dup_removed} dòng trùng, điền {filled_cells} ô thiếu dữ liệu)."
    )

    # ---------------- Bộ lọc trong sidebar ----------------
    with st.sidebar:
        st.markdown("---")
        st.header("🔍 Bộ lọc")
        filtered_df = df_analyzed.copy()

        if "gender" in filtered_df.columns:
            genders = st.multiselect(
                "Giới tính", options=sorted(filtered_df["gender"].dropna().unique())
            )
            if genders:
                filtered_df = filtered_df[filtered_df["gender"].isin(genders)]

        if "year_in_school" in filtered_df.columns:
            years = st.multiselect(
                "Năm học",
                options=sorted(filtered_df["year_in_school"].dropna().unique()),
            )
            if years:
                filtered_df = filtered_df[filtered_df["year_in_school"].isin(years)]

        if "major" in filtered_df.columns:
            majors = st.multiselect(
                "Chuyên ngành", options=sorted(filtered_df["major"].dropna().unique())
            )
            if majors:
                filtered_df = filtered_df[filtered_df["major"].isin(majors)]

    # ---------------- Các tab hiển thị kết quả ----------------
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📋 Tổng quan", "📊 Thống kê", "📈 Biểu đồ", "⬇️ Xuất dữ liệu"]
    )

    with tab1:
        st.subheader("Dữ liệu sau khi làm sạch")
        st.dataframe(filtered_df, use_container_width=True)
        st.caption(f"Đang hiển thị {len(filtered_df)} / {len(df_analyzed)} sinh viên.")

    with tab2:
        st.subheader("Thống kê tổng hợp")
        col1, col2, col3 = st.columns(3)
        col1.metric("Số sinh viên", f"{stats.get('so_sinh_vien', 0):,}")
        col2.metric(
            "Thu nhập TB / tháng",
            f"${stats.get('avg_income', 0):,.2f}" if "avg_income" in stats else "N/A",
        )
        col3.metric(
            "Hỗ trợ tài chính TB",
            f"${stats.get('avg_financial_aid', 0):,.2f}"
            if "avg_financial_aid" in stats
            else "N/A",
        )
        if "avg_total_spending" in stats:
            st.metric(
                "Chi tiêu sinh hoạt TB (không gồm học phí)",
                f"${stats['avg_total_spending']:,.2f}",
            )
        st.markdown("**Thống kê mô tả chi tiết (describe):**")
        numeric_cols = filtered_df.select_dtypes(include="number").columns
        st.dataframe(filtered_df[numeric_cols].describe(), use_container_width=True)

    with tab3:
        st.subheader("Biểu đồ trực quan hóa")
        c1, c2 = st.columns(2)
        with c1:
            fig1 = plot_spending_breakdown(filtered_df)
            if fig1:
                st.pyplot(fig1)
        with c2:
            fig2 = plot_income_distribution(filtered_df)
            if fig2:
                st.pyplot(fig2)

        group_choice = st.selectbox(
            "Xem chi tiêu trung bình theo nhóm:",
            options=[c for c in ["gender", "year_in_school", "major"] if c in filtered_df.columns],
        )
        fig3 = plot_spending_by_group(filtered_df, group_choice)
        if fig3:
            st.pyplot(fig3)

    with tab4:
        st.subheader("Xuất dữ liệu đã xử lý")
        csv_buffer = io.StringIO()
        filtered_df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="⬇️ Tải file CSV đã làm sạch",
            data=csv_buffer.getvalue(),
            file_name="student_spending_cleaned.csv",
            mime="text/csv",
        )


if __name__ == "__main__":
    # ------------------------------------------------------------
    # Cho phép chạy trực tiếp bằng nút Run / Ctrl+F5 trong VS Code
    # (thay vì bắt buộc phải gõ lệnh "streamlit run app.py" trong
    # terminal). Nếu file được chạy bằng "python app.py" (hoặc
    # Ctrl+F5), đoạn code dưới đây sẽ tự động khởi động lại chính nó
    # thông qua streamlit CLI để giao diện web hoạt động bình thường.
    # ------------------------------------------------------------
    import sys

    from streamlit import runtime
    from streamlit.web import cli as stcli

    if runtime.exists():
        # Trường hợp đã chạy đúng cách qua "streamlit run app.py"
        main()
    else:
        # Trường hợp chạy bằng "python app.py" / Ctrl+F5 trong VS Code
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
