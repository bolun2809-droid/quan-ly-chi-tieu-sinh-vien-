import matplotlib.pyplot as plt


def ve_bieu_do_tron(theo_danh_muc):
    labels = list(theo_danh_muc.keys())
    values = list(theo_danh_muc.values())

    plt.figure(figsize=(7, 7))

    plt.pie(
        values,
        labels=labels,
        autopct='%1.1f%%',
        startangle=90
    )

    plt.title("Tỷ lệ chi tiêu theo danh mục")
    plt.show()


def ve_bieu_do_cot(theo_danh_muc):
    labels = list(theo_danh_muc.keys())
    values = list(theo_danh_muc.values())

    plt.figure(figsize=(8, 5))

    plt.bar(labels, values)

    plt.title("So sánh chi tiêu theo danh mục")
    plt.xlabel("Danh mục")
    plt.ylabel("Số tiền (VNĐ)")

    plt.xticks(rotation=20)

    plt.show()
