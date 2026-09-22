#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BSS 代金券分析：即将到期识别 + 使用率统计
用法：
  hcloud BSS ListPartnerCouponsRecord --cli-region=cn-north-1 --output json | python3 analyze_coupons.py --expiring-days 30 --usage
"""
import argparse, json, sys, datetime

def parse_coupons(raw):
    # 兼容 list 或 {records:[]} 结构
    if isinstance(raw, list): return raw
    for k in ("records", "coupons", "data", "items"):
        if isinstance(raw, dict) and isinstance(raw.get(k), list):
            return raw[k]
    return []

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--expiring-days", type=int, default=30, help="即将到期阈值(天)")
    ap.add_argument("--usage", action="store_true", help="输出使用率统计")
    args = ap.parse_args()
    try:
        raw = json.load(sys.stdin)
    except Exception as e:
        print(json.dumps({"error": "INPUT_PARSE_ERROR", "msg": str(e)}, ensure_ascii=False)); return
    coupons = parse_coupons(raw)
    if not coupons:
        # 处理权限/错误响应
        if isinstance(raw, dict) and raw.get("error_msg"):
            print(json.dumps({"error_code": "PERMISSION_DENIED", "error_msg": raw["error_msg"],
                              "hint": "账号需开通 BSS 代金券查询权限，参见 iam-policies.md"}, ensure_ascii=False))
        else:
            print(json.dumps({"error_code": "EMPTY", "count": 0}, ensure_ascii=False))
        return
    today = datetime.date.today()
    expiring = []
    used_amount = face_value = 0
    for c in coupons:
        face = float(c.get("face_value") or c.get("faceAmount") or 0)
        used = float(c.get("used_amount") or c.get("usedAmount") or 0)
        face_value += face; used_amount += used
        status = c.get("status") or c.get("coupon_status") or ""
        expire = (c.get("expire_time") or c.get("expireTime") or "")[:10]
        try:
            days_left = (datetime.date.fromisoformat(expire) - today).days
        except Exception:
            days_left = None
        if status in ("unused", "1", "") and days_left is not None and 0 <= days_left <= args.expiring_days:
            expiring.append({"coupon_id": c.get("coupon_id") or c.get("couponId"),
                             "expire_time": expire, "days_left": days_left, "face_value": face})
    expiring.sort(key=lambda x: x["days_left"])
    out = {
        "total_coupons": len(coupons),
        "expiring_soon": expiring,
        "expiring_count": len(expiring),
        "expiring_threshold_days": args.expiring_days,
    }
    if args.usage:
        out["usage"] = {
            "total_face_value": round(face_value, 2),
            "total_used_amount": round(used_amount, 2),
            "total_remaining": round(face_value - used_amount, 2),
            "usage_rate": round(used_amount / face_value, 4) if face_value else 0,
        }
    print(json.dumps(out, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()