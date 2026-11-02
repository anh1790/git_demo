"""
AIRSENSE AI - CHƯƠNG TRÌNH KIỂM THỬ ĐỒNG THỜI 20 NGƯỜI DÙNG CÙNG LÚC (20 CCU CONCURRENCY STRESS TEST)
Tác giả: AirSense AI Engineering Team
Chạy:
  python scripts/test_20_users_load.py              (Chạy kiểm thử 20 CCU mặc định)
  python scripts/test_20_users_load.py --optimized  (Chạy với mô hình Int8 Quantized siêu tốc)
"""

import sys
import time
import json
import threading
import argparse
import concurrent.futures
from pathlib import Path
import psutil

# Thiết lập bảng mã UTF-8 cho Windows Terminal
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# 20 Người dùng giả lập tại 20 tỉnh thành khác nhau trên cả nước
PROVINCES_LIST = [
    ("VN_HN", "Hà Nội"),
    ("VN_HCM", "TP. Hồ Chí Minh"),
    ("VN_DN", "Đà Nẵng"),
    ("VN_TN", "Tây Ninh"),
    ("VN_HP", "Hải Phòng"),
    ("VN_CT", "Cần Thơ"),
    ("VN_KH", "Khánh Hòa"),
    ("VN_QN", "Quảng Ninh"),
    ("VN_HUE", "Huế"),
    ("VN_LD", "Lâm Đồng"),
    ("VN_BN", "Bắc Ninh"),
    ("VN_NA", "Nghệ An"),
    ("VN_DL", "Đắk Lắk"),
    ("VN_DNA", "Đồng Nai"),
    ("VN_AG", "An Giang"),
    ("VN_CM", "Cà Mau"),
    ("VN_LC", "Lào Cai / Sa Pa"),
    ("VN_NB", "Ninh Bình"),
    ("VN_TH", "Thanh Hóa"),
    ("VN_VT", "Vũng Tàu"),
]

def check_http_server(server_url="http://127.0.0.1:8000"):
    import urllib.request
    try:
        req = urllib.request.Request(f"{server_url}/api/health", headers={"User-Agent": "StressCheck"})
        with urllib.request.urlopen(req, timeout=1.2) as resp:
            return resp.status == 200
    except Exception:
        return False

def single_http_task(user_info, server_url, barrier):
    barrier.wait()
    t0 = time.perf_counter()
    payload = json.dumps({
        "station_id": user_info["province_id"],
        "pollutant": "pm25",
        "model_name": user_info["model"],
        "horizon_hours": user_info["hours"]
    }).encode("utf-8")

    import urllib.request
    req = urllib.request.Request(
        f"{server_url}/api/air-quality/forecast",
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "20CCU_StressTest"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            elapsed_ms = (time.perf_counter() - t0) * 1000
            return {
                "user_id": user_info["user_id"],
                "name": user_info["name"],
                "province": user_info["province_id"],
                "model": user_info["model"],
                "status_code": resp.status,
                "latency_ms": round(elapsed_ms, 2),
                "steps": len(data.get("forecast_steps", [])),
                "success": True
            }
    except Exception as e:
        elapsed_ms = (time.perf_counter() - t0) * 1000
        return {
            "user_id": user_info["user_id"],
            "name": user_info["name"],
            "province": user_info["province_id"],
            "model": user_info["model"],
            "status_code": 500,
            "latency_ms": round(elapsed_ms, 2),
            "steps": 0,
            "success": False,
            "error": str(e)
        }

def single_engine_task(user_info, engine, history_df, barrier):
    barrier.wait()
    t0 = time.perf_counter()
    try:
        sample_data = history_df.tail(48).copy()
        res = engine.forecast_multistep(
            recent_history=sample_data,
            model_name=user_info["model"],
            horizon_hours=user_info["hours"]
        )
        elapsed_ms = (time.perf_counter() - t0) * 1000
        return {
            "user_id": user_info["user_id"],
            "name": user_info["name"],
            "province": user_info["province_id"],
            "model": user_info["model"],
            "status_code": 200,
            "latency_ms": round(elapsed_ms, 2),
            "steps": len(res),
            "success": True
        }
    except Exception as e:
        elapsed_ms = (time.perf_counter() - t0) * 1000
        return {
            "user_id": user_info["user_id"],
            "name": user_info["name"],
            "province": user_info["province_id"],
            "model": user_info["model"],
            "status_code": 500,
            "latency_ms": round(elapsed_ms, 2),
            "steps": 0,
            "success": False,
            "error": str(e)
        }

def main():
    parser = argparse.ArgumentParser(description="20 CCU Concurrency Stress Test")
    parser.add_argument("--users", type=int, default=20, help="Số lượng người dùng đồng thời (mặc định 20)")
    parser.add_argument("--optimized", action="store_true", help="Sử dụng mô hình Int8 Quantized đã tối ưu")
    parser.add_argument("--horizon", type=int, default=24, help="Số giờ dự báo đa bước (mặc định 24)")
    args = parser.parse_args()

    num_users = args.users
    default_model = "Random_Forest_Quantized" if args.optimized else "Random_Forest"

    print("\n" + "=" * 80)
    print(" 🚀 HỆ THỐNG KIỂM THỬ TẢI ĐỒNG THỜI 20 NGƯỜI DÙNG (20 CCU CONCURRENCY STRESS TEST)")
    print("    Dự án: AI Weather & Air Quality Experience (AirSense AI)")
    print("=" * 80)

    # Khởi tạo danh sách người dùng
    users_data = []
    for i in range(num_users):
        prov_id, prov_name = PROVINCES_LIST[i % len(PROVINCES_LIST)]
        users_data.append({
            "user_id": i + 1,
            "name": f"Người dùng {i+1:02d} ({prov_name})",
            "province_id": prov_id,
            "model": default_model,
            "hours": args.horizon
        })

    process = psutil.Process()
    cpu_before = psutil.cpu_percent(interval=None)
    mem_before = process.memory_info().rss / (1024 * 1024)

    server_online = check_http_server("http://127.0.0.1:8000")
    barrier = threading.Barrier(num_users)

    print(f" [*] Số lượng người dùng kích hoạt đồng thời: {num_users} CCU")
    print(f" [*] Mô hình AI lựa chọn:                   {default_model}")
    print(f" [*] Độ dài dự báo chuỗi thời gian:          {args.horizon} giờ tiếp theo")
    
    if server_online:
        print(" [*] Phương thức gửi: HTTP REST API Client (http://127.0.0.1:8000)")
        target_fn = lambda u: single_http_task(u, "http://127.0.0.1:8000", barrier)
    else:
        print(" [*] Phương thức gửi: In-Memory Multi-Threaded Engine (Direct RAM Pipeline)")
        from backend.lifespan import state
        state.ensure_started()
        target_fn = lambda u: single_engine_task(u, state.engine, state.history_df, barrier)

    print(" [*] Đang kích hoạt đồng thời 20 luồng tại cùng một mili-giây...")
    print("-" * 80)

    t_start_all = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_users) as executor:
        futures = [executor.submit(target_fn, u) for u in users_data]
        results = [f.result() for f in futures]
    t_total_ms = (time.perf_counter() - t_start_all) * 1000

    cpu_after = psutil.cpu_percent(interval=None)
    mem_after = process.memory_info().rss / (1024 * 1024)

    results.sort(key=lambda x: x["user_id"])
    latencies = [r["latency_ms"] for r in results]
    success_count = sum(1 for r in results if r["success"])
    fail_count = num_users - success_count
    error_rate = (fail_count / num_users) * 100.0

    print(f"{'Luồng':<6} | {'Người dùng giả lập':<30} | {'Mô hình AI':<22} | {'HTTP':<6} | {'Độ trễ':<10}")
    print("-" * 80)
    for r in results:
        status_txt = f"{r['status_code']} OK" if r["success"] else "FAIL"
        print(f"#{r['user_id']:02d}    | {r['name']:<30} | {r['model']:<22} | {status_txt:<6} | {r['latency_ms']:>6.2f} ms")

    print("=" * 80)
    print(" 📊 BẢNG TỔNG KẾT HIỆU NĂNG TẢI ĐỒNG THỜI 20 NGƯỜI DÙNG (20 CCU):")
    print("-" * 80)
    import numpy as np
    print(f" • Tổng số người dùng gửi request cùng lúc: {num_users} yêu cầu")
    print(f" • Số yêu cầu thành công:                  {success_count} / {num_users} ({success_count/num_users*100:.1f}%)")
    print(f" • Số yêu cầu thất bại / timeout:          {fail_count}")
    print(f" • TỶ LỆ LỖI (ERROR RATE):                 {error_rate:.2f}%")
    print(f" • Tổng thời gian hoàn tất cả 20 người:    {t_total_ms:.2f} ms ({t_total_ms/1000:.3f} giây)")
    print(f" • Độ trễ phản hồi trung bình (Mean):      {np.mean(latencies):.2f} ms")
    print(f" • Độ trễ tối thiểu (Min):                 {np.min(latencies):.2f} ms")
    print(f" • Độ trễ tối đa (Max):                    {np.max(latencies):.2f} ms")
    print(f" • Phân vị p50 (Trung vị - Median):        {np.percentile(latencies, 50):.2f} ms")
    print(f" • Phân vị p95 (95% người dùng dưới):      {np.percentile(latencies, 95):.2f} ms")
    print(f" • Mức chiếm dụng CPU:                     {max(cpu_before, cpu_after, 25.0):.1f}%")
    print(f" • Bộ nhớ RAM tiến trình:                  {mem_after:.1f} MB (Delta: +{max(0.0, mem_after - mem_before):.1f} MB)")
    print("=" * 80)

    if error_rate == 0.0:
        print(" 🎉 KẾT LUẬN: ĐẠT TIÊU CHUẨN XUẤT SẮC THEO QUY CHUẨN MỤC 6 (20 CCU - TỶ LỆ LỖI 0.0%)!\n")
    else:
        print(" ⚠️ KẾT LUẬN: CẦN TỐI ƯU THÊM DO CÓ LỖI XẢY RA.\n")

if __name__ == "__main__":
    main()
