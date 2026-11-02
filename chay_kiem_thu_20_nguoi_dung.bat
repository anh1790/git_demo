@echo off
chcp 65001 >nul
title Kiểm Thử Tải Đồng Thời 20 Người Dùng - AirSense AI
echo ======================================================================
echo   AIRSENSE AI - CHƯƠNG TRÌNH KIỂM THỬ TẢI ĐỒNG THỜI 20 NGƯỜI DÙNG
echo ======================================================================
echo.
python scripts\test_20_users_load.py
echo.
pause
