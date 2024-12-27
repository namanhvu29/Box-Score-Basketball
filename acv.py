import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
import pandas as pd

# Load ảnh gốc
image_path = "/home/namanh/Vu_Nam_Anh/Box Score Basketball Code/Image/e37b1750b2a80ff656b9.jpg"  # Thay bằng đường dẫn tới ảnh của bạn
image = cv2.imread(image_path)

# Resize ảnh (tùy chọn để dễ làm việc)
scale_percent = 50  # Resize xuống 50% kích thước gốc
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)
resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

# Chuyển ảnh sang grayscale
gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

# Tách ngưỡng nhị phân (thresholding)
_, binary_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY_INV)

# Lọc đường kẻ ngang và dọc
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))

# Tìm đường kẻ ngang
horizontal_lines = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, horizontal_kernel)

# Tìm đường kẻ dọc
vertical_lines = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, vertical_kernel)

# Kết hợp cả hai
table_structure = cv2.add(horizontal_lines, vertical_lines)

# Hiển thị ảnh
plt.figure(figsize=(12, 8))
plt.imshow(table_structure, cmap='gray')
plt.title("Detected Table Structure")
plt.axis("off")
plt.show()

# --------------
# Tìm các đường viền (contours) trong bảng
contours, _ = cv2.findContours(table_structure, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Lặp qua các contours để cắt từng ô
cells = []
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    if w > 20 and h > 20:  # Chỉ lấy các ô đủ lớn
        cell = resized_image[y:y+h, x:x+w]
        cells.append(cell)

        # Hiển thị từng ô
        plt.imshow(cell, cmap='gray')
        plt.show()

# ------------------------------
for cell in cells:
    # Chuyển sang ảnh đen trắng
    cell_gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
    _, cell_binary = cv2.threshold(cell_gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Tìm các đường nét (gạch)
    lines = cv2.HoughLinesP(cell_binary, 1, np.pi / 180, 50, minLineLength=10, maxLineGap=5)

    # Đếm số gạch
    count = len(lines) if lines is not None else 0
    print("Số gạch trong ô:", count)

# -------------------------------
